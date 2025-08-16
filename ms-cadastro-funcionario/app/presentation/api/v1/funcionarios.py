"""
Endpoints para operações CRUD de funcionários.

Este módulo implementa todos os endpoints REST para gerenciamento
de funcionários, incluindo validações, filtros e paginação.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.responses import JSONResponse

from app.presentation.schemas import (
    FuncionarioCreateSchema,
    FuncionarioUpdateSchema,
    FuncionarioResponseSchema,
    FuncionarioListQuerySchema,
    FuncionarioListResponseSchema,
    SuccessResponseSchema,
    ErrorResponseSchema
)
from app.presentation.api.dependencies import (
    ValidObjectId,
    PaginationParams,
    FuncionarioControllerDep
)
from app.presentation.api.controllers import FuncionarioController
from app.application.exceptions import (
    ApplicationException,
    ValidationException,
    BusinessRuleException,
    ResourceNotFoundException,
    DuplicateResourceException
)


# Router para funcionários
router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


# ==========================================
# ENDPOINTS CRUD
# ==========================================

@router.post(
    "/",
    response_model=SuccessResponseSchema[FuncionarioResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Criar Funcionário",
    description="Cadastra um novo funcionário no sistema com validações completas",
    responses={
        201: {
            "description": "Funcionário criado com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Funcionário criado com sucesso",
                        "data": {
                            "id": "507f1f77bcf86cd799439011",
                            "nome": "João",
                            "sobrenome": "Silva Santos",
                            "email": "joao.silva@empresa.com.br",
                            "telefone": "(11) 99999-9999",
                            "cpf": "12345678901",
                            "data_nascimento": "1990-05-15",
                            "data_admissao": "2020-01-15",
                            "cargo": "Desenvolvedor Pleno",
                            "departamento": "Tecnologia",
                            "salario": 8500.00,
                            "status": "ativo",
                            "ativo": False,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        },
                        "timestamp": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Dados inválidos na requisição"},
        409: {"description": "Email já existe no sistema"},
        422: {"description": "Erro de validação nos dados"}
    }
)
async def criar_funcionario(
    funcionario_data: FuncionarioCreateSchema,
    controller: FuncionarioControllerDep
) -> SuccessResponseSchema[FuncionarioResponseSchema]:
    """
    Cria um novo funcionário no sistema.
    
    **Validações aplicadas:**
    - Email único no sistema
    - CPF válido (algoritmo da Receita Federal)
    - Telefone no formato brasileiro
    - Idade mínima de 16 anos
    - Salário dentro da faixa permitida
    - Email corporativo obrigatório
    
    **Campos obrigatórios:**
    - nome, sobrenome, email, cpf
    - data_nascimento, data_admissao
    - cargo, departamento, salario
    
    Args:
        funcionario_data: Dados do funcionário para criação
        controller: Controller injetado automaticamente
        
    Returns:
        Resposta com dados do funcionário criado
        
    Raises:
        HTTPException: Em caso de validação, duplicação ou erro de negócio
    """
    try:
        return await controller.criar_funcionario(funcionario_data)
    except DuplicateResourceException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "error": "DUPLICATE_EMAIL",
                "message": str(e),
                "field": "email"
            }
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": str(e),
                "details": getattr(e, 'errors', [])
            }
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "BUSINESS_RULE_ERROR",
                "message": str(e)
            }
        )


@router.get(
    "/",
    response_model=SuccessResponseSchema[FuncionarioListResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Listar Funcionários",
    description="Lista funcionários com filtros opcionais e paginação",
    responses={
        200: {
            "description": "Lista de funcionários retornada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "25 funcionários encontrados",
                        "data": {
                            "items": [
                                {
                                    "id": "507f1f77bcf86cd799439011",
                                    "nome": "João",
                                    "sobrenome": "Silva Santos",
                                    "email": "joao.silva@empresa.com.br",
                                    "cargo": "Desenvolvedor Pleno",
                                    "departamento": "Tecnologia"
                                }
                            ],
                            "total": 25,
                            "page": 1,
                            "size": 20,
                            "pages": 2
                        }
                    }
                }
            }
        }
    }
)
async def listar_funcionarios(
    controller: FuncionarioControllerDep,
    # Paginação
    page: int = Query(
        1, 
        ge=1, 
        description="Número da página (inicia em 1)",
        example=1
    ),
    size: int = Query(
        10, 
        ge=1, 
        le=100, 
        description="Itens por página (máximo 100)",
        example=10
    ),
    # Filtros opcionais
    departamento: Optional[str] = Query(
        None,
        max_length=50,
        description="Filtro por departamento (opcional)",
        example="Tecnologia"
    ),
    cargo: Optional[str] = Query(
        None,
        max_length=50,
        description="Filtro por cargo (opcional)",
        example="Desenvolvedor Senior"
    )
) -> SuccessResponseSchema[FuncionarioListResponseSchema]:
    """
    Lista funcionários com paginação e filtros opcionais.
    
    **Paginação:**
    - page: Página atual (início em 1)
    - size: Itens por página (máximo 100)
    
    **Filtros opcionais:**
    - departamento: Filtra funcionários por departamento
    - cargo: Filtra funcionários por cargo
    
    Args:
        controller: Controller injetado
        page: Número da página
        size: Tamanho da página
        departamento: Filtro por departamento (opcional)
        cargo: Filtro por cargo (opcional)
        
    Returns:
        Lista paginada de funcionários
    """
    try:
        # Construir schema de consulta com filtros
        query_schema = FuncionarioListQuerySchema(
            page=page,
            size=size,
            departamento=departamento,
            cargo=cargo
        )
        
        return await controller.listar_funcionarios(query_schema)
        
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "INVALID_FILTERS",
                "message": str(e)
            }
        )


@router.get(
    "/{funcionario_id}",
    response_model=SuccessResponseSchema[FuncionarioResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Buscar Funcionário por ID",
    description="Retorna dados completos de um funcionário específico",
    responses={
        200: {"description": "Funcionário encontrado"},
        400: {"description": "ID inválido"},
        404: {"description": "Funcionário não encontrado"}
    }
)
async def buscar_funcionario(
    funcionario_id: ValidObjectId,
    controller: FuncionarioControllerDep
) -> SuccessResponseSchema[FuncionarioResponseSchema]:
    """
    Busca funcionário por ID.
    
    **Validações:**
    - ID deve ser um ObjectId válido (24 caracteres hexadecimais)
    - Funcionário deve existir no sistema
    
    Args:
        funcionario_id: ID único do funcionário
        controller: Controller injetado
        
    Returns:
        Dados completos do funcionário
        
    Raises:
        HTTPException: Se ID inválido ou funcionário não encontrado
    """
    try:
        return await controller.buscar_funcionario(funcionario_id)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": "FUNCIONARIO_NOT_FOUND",
                "message": str(e),
                "funcionario_id": funcionario_id
            }
        )


@router.put(
    "/{funcionario_id}",
    response_model=SuccessResponseSchema[FuncionarioResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Atualizar Funcionário",
    description="Atualiza dados de um funcionário (campos imutáveis protegidos)",
    responses={
        200: {"description": "Funcionário atualizado com sucesso"},
        400: {"description": "Dados inválidos"},
        404: {"description": "Funcionário não encontrado"},
        422: {"description": "Tentativa de alterar campos imutáveis"}
    }
)
async def atualizar_funcionario(
    funcionario_id: ValidObjectId,
    funcionario_data: FuncionarioUpdateSchema,
    controller: FuncionarioControllerDep
) -> SuccessResponseSchema[FuncionarioResponseSchema]:
    """
    Atualiza dados de um funcionário.
    
    **Campos imutáveis (não podem ser alterados):**
    - email, cpf, data_nascimento, data_admissao
    
    **Campos atualizáveis:**
    - nome, sobrenome, telefone
    - cargo, departamento, salario, status
    
    **Validações mantidas:**
    - Todos os validadores aplicados na criação
    - Verificação de campos imutáveis
    
    Args:
        funcionario_id: ID do funcionário para atualizar
        funcionario_data: Novos dados (campos opcionais)
        controller: Controller injetado
        
    Returns:
        Dados atualizados do funcionário
        
    Raises:
        HTTPException: Para vários cenários de erro
    """
    try:
        return await controller.atualizar_funcionario(funcionario_id, funcionario_data)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": "FUNCIONARIO_NOT_FOUND",
                "message": str(e),
                "funcionario_id": funcionario_id
            }
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": str(e),
                "details": getattr(e, 'errors', [])
            }
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": "BUSINESS_RULE_ERROR",
                "message": str(e)
            }
        )


@router.delete(
    "/{funcionario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir Funcionário",
    description="Remove um funcionário do sistema (com validações de negócio)",
    responses={
        204: {"description": "Funcionário excluído com sucesso"},
        400: {"description": "ID inválido"},
        404: {"description": "Funcionário não encontrado"},
        409: {"description": "Funcionário ativo em projetos - exclusão não permitida"}
    }
)
async def excluir_funcionario(
    funcionario_id: ValidObjectId,
    controller: FuncionarioControllerDep
) -> None:
    """
    Exclui um funcionário do sistema.
    
    **Regras de negócio:**
    - Funcionários ativos em projetos não podem ser excluídos
    - Exclusão é lógica inicialmente, física após período
    
    **Validações:**
    - ID deve ser válido
    - Funcionário deve existir
    - Não pode estar ativo em projetos
    
    Args:
        funcionario_id: ID do funcionário para excluir
        controller: Controller injetado
        
    Returns:
        Status 204 (No Content) em caso de sucesso
        
    Raises:
        HTTPException: Para vários cenários de erro
    """
    try:
        await controller.excluir_funcionario(funcionario_id)
        # FastAPI retorna automaticamente 204 para None
        return None
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": "FUNCIONARIO_NOT_FOUND",
                "message": str(e),
                "funcionario_id": funcionario_id
            }
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "error": "DELETION_NOT_ALLOWED",
                "message": str(e),
                "funcionario_id": funcionario_id
            }
        )


# ==========================================



# ==========================================
# ENDPOINTS DE VALIDAÇÃO
# ==========================================

@router.post(
    "/validar/email",
    status_code=status.HTTP_200_OK,
    summary="Validar Email Único",
    description="Verifica se um email está disponível para uso"
)
async def validar_email_unico(
    controller: FuncionarioControllerDep,
    email: str = Query(..., description="Email para validar")
) -> Dict[str, Any]:
    """
    Valida se um email está disponível para uso.
    
    Útil para validação em tempo real durante preenchimento de formulários.
    
    Args:
        email: Email para validar
        controller: Controller injetado
        
    Returns:
        Resultado da validação
    """
    try:
        # Tentar buscar funcionário com este email
        query = FuncionarioListQuerySchema(page=1, size=1)
        # TODO: Implementar busca por email específico
        
        return {
            "success": True,
            "email": email,
            "disponivel": True,  # TODO: Implementar lógica real
            "message": "Email disponível para uso"
        }
        
    except Exception as e:
        return {
            "success": False,
            "email": email,
            "disponivel": False,
            "message": str(e)
        }


@router.post(
    "/validar/cpf",
    status_code=status.HTTP_200_OK,
    summary="Validar CPF",
    description="Valida formato e dígitos verificadores de um CPF"
)
async def validar_cpf(
    cpf: str = Query(..., description="CPF para validar")
) -> Dict[str, Any]:
    """
    Valida CPF usando algoritmo da Receita Federal.
    
    Args:
        cpf: CPF para validar
        
    Returns:
        Resultado da validação
    """
    try:
        from app.application.validators import CPFValidator
        
        validator = CPFValidator()
        cpf_valido = validator.validate(cpf)
        
        return {
            "success": True,
            "cpf": cpf,
            "valido": cpf_valido,
            "message": "CPF válido" if cpf_valido else "CPF inválido"
        }
        
    except Exception as e:
        return {
            "success": False,
            "cpf": cpf,
            "valido": False,
            "message": str(e)
        }
