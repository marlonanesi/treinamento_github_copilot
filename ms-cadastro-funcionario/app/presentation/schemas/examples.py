"""
Exemplos de uso dos schemas Pydantic.

Este módulo contém exemplos práticos de como usar os schemas
da aplicação para validação, serialização e integração com
endpoints da API.
"""

import json
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, List
from pydantic import ValidationError

from .base import BaseSchema
from .funcionario_schemas import (
    FuncionarioCreateSchema,
    FuncionarioUpdateSchema,
    FuncionarioResponseSchema,
    FuncionarioListQuerySchema,
    FuncionarioListResponseSchema
)
from .response_schemas import (
    SuccessResponseSchema,
    ErrorResponseSchema,
    ValidationErrorSchema
)
from .health_schemas import (
    HealthCheckResponseSchema,
    ApplicationHealthSchema,
    DatabaseHealthSchema
)
from .validators import CustomValidators
from .middleware import ValidationErrorHandler, SchemaSerializer
from .config import SchemaUtils


# ==========================================
# EXEMPLOS DE CRIAÇÃO DE FUNCIONÁRIO
# ==========================================

class FuncionarioExamples:
    """
    Exemplos de uso dos schemas de funcionário.
    """
    
    @staticmethod
    def exemplo_criacao_valida() -> Dict[str, Any]:
        """
        Exemplo de criação de funcionário com dados válidos.
        
        Returns:
            Dict com dados de exemplo válidos
        """
        dados_validos = {
            "nome": "Maria",
            "sobrenome": "Silva Santos",
            "email": "maria.silva@empresa.com.br",
            "telefone": "(11) 98765-4321",
            "cpf": "12345678901",
            "data_nascimento": "1985-03-20",
            "data_admissao": "2020-06-01",
            "cargo": "Desenvolvedora Senior",
            "departamento": "Tecnologia",
            "salario": 12000.50,
            "status": "ativo"
        }
        
        try:
            # Validação usando schema
            funcionario = FuncionarioCreateSchema(**dados_validos)
            print("✅ Dados válidos - Funcionário criado com sucesso!")
            print(f"Schema validado: {funcionario.model_dump_json(indent=2)}")
            
            return funcionario.model_dump()
            
        except ValidationError as e:
            print(f"❌ Erro na validação: {e}")
            return {}
    
    @staticmethod
    def exemplo_criacao_invalida() -> Dict[str, Any]:
        """
        Exemplo de tentativa de criação com dados inválidos.
        
        Returns:
            Dict com informações do erro de validação
        """
        dados_invalidos = {
            "nome": "A",  # Muito curto
            "sobrenome": "",  # Vazio
            "email": "email-invalido",  # Formato inválido
            "telefone": "123",  # Formato inválido
            "cpf": "123",  # CPF inválido
            "data_nascimento": "2010-01-01",  # Muito jovem
            "data_admissao": "1900-01-01",  # Data muito antiga
            "cargo": "",  # Vazio
            "departamento": "",  # Vazio
            "salario": 100.00,  # Abaixo do mínimo
            "status": "invalido"  # Status inválido
        }
        
        try:
            funcionario = FuncionarioCreateSchema(**dados_invalidos)
            return funcionario.model_dump()
            
        except ValidationError as e:
            print("❌ Dados inválidos - Erros de validação encontrados:")
            
            # Formatar erros usando o handler
            formatted_error = ValidationErrorHandler.format_validation_error(e)
            
            print(f"Total de erros: {formatted_error.total_errors}")
            for error in formatted_error.details:
                print(f"  - Campo '{error['field']}': {error['message']}")
            
            return {
                "erro": "Dados inválidos",
                "detalhes": [error.model_dump() for error in formatted_error.details]
            }
    
    @staticmethod
    def exemplo_atualizacao_parcial() -> Dict[str, Any]:
        """
        Exemplo de atualização parcial de funcionário.
        
        Returns:
            Dict com dados de atualização
        """
        dados_atualizacao = {
            "cargo": "Tech Lead",
            "salario": 15000.00,
            "departamento": "Arquitetura"
        }
        
        try:
            # Validação de atualização (permite campos opcionais)
            funcionario_update = FuncionarioUpdateSchema(**dados_atualizacao)
            print("✅ Dados de atualização válidos!")
            print(f"Campos atualizados: {list(dados_atualizacao.keys())}")
            
            return funcionario_update.model_dump(exclude_unset=True)
            
        except ValidationError as e:
            print(f"❌ Erro na validação da atualização: {e}")
            return {}
    
    @staticmethod
    def exemplo_tentativa_atualizacao_campos_imutaveis() -> Dict[str, Any]:
        """
        Exemplo de tentativa de atualização de campos imutáveis.
        
        Returns:
            Dict com resultado da tentativa
        """
        dados_invalidos = {
            "cpf": "98765432100",  # Tentativa de alterar CPF (imutável)
            "data_nascimento": "1990-01-01",  # Tentativa de alterar nascimento
            "cargo": "Desenvolvedor Pleno"
        }
        
        try:
            funcionario_update = FuncionarioUpdateSchema(**dados_invalidos)
            return funcionario_update.model_dump(exclude_unset=True)
            
        except ValidationError as e:
            print("❌ Tentativa de alterar campos imutáveis bloqueada:")
            formatted_error = ValidationErrorHandler.format_validation_error(e)
            
            for error in formatted_error.details:
                print(f"  - {error['message']}")
            
            return {"erro": "Campos imutáveis não podem ser alterados"}
    
    @staticmethod
    def exemplo_consulta_com_filtros() -> Dict[str, Any]:
        """
        Exemplo de consulta com filtros e paginação.
        
        Returns:
            Dict com parâmetros de consulta
        """
        parametros_consulta = {
            "departamento": "Tecnologia",
            "status": "ativo",
            "salario_minimo": 5000.00,
            "salario_maximo": 20000.00,
            "data_admissao_inicial": "2020-01-01",
            "data_admissao_final": "2024-12-31",
            "page": 1,
            "size": 10,
            "ordenar_por": "nome",
            "ordem": "asc"
        }
        
        try:
            consulta = FuncionarioListQuerySchema(**parametros_consulta)
            print("✅ Parâmetros de consulta válidos!")
            print(f"Filtros aplicados: {consulta.get_active_filters()}")
            
            return consulta.model_dump(exclude_unset=True)
            
        except ValidationError as e:
            print(f"❌ Erro nos parâmetros de consulta: {e}")
            return {}


# ==========================================
# EXEMPLOS DE RESPOSTAS DA API
# ==========================================

class ResponseExamples:
    """
    Exemplos de respostas da API usando schemas.
    """
    
    @staticmethod
    def exemplo_resposta_sucesso_criacao() -> Dict[str, Any]:
        """
        Exemplo de resposta de sucesso para criação de funcionário.
        
        Returns:
            Dict com resposta de sucesso
        """
        # Dados do funcionário criado
        funcionario_data = SchemaUtils.criar_exemplo_funcionario()
        funcionario_data["id"] = "507f1f77bcf86cd799439011"
        funcionario_data["created_at"] = datetime.utcnow()
        funcionario_data["updated_at"] = datetime.utcnow()
        
        # Schema de resposta do funcionário
        funcionario_response = FuncionarioResponseSchema(**funcionario_data)
        
        # Schema de resposta de sucesso
        success_response = SuccessResponseSchema(
            success=True,
            message="Funcionário criado com sucesso",
            data=funcionario_response,
            timestamp=datetime.utcnow()
        )
        
        print("✅ Resposta de sucesso criada:")
        print(json.dumps(
            SchemaSerializer.serialize_model(success_response),
            indent=2,
            ensure_ascii=False
        ))
        
        return SchemaSerializer.serialize_model(success_response)
    
    @staticmethod
    def exemplo_resposta_lista_paginada() -> Dict[str, Any]:
        """
        Exemplo de resposta paginada com lista de funcionários.
        
        Returns:
            Dict com resposta paginada
        """
        # Criar alguns funcionários de exemplo
        funcionarios = []
        for i in range(3):
            func_data = SchemaUtils.criar_exemplo_funcionario()
            func_data["id"] = f"507f1f77bcf86cd79943901{i}"
            func_data["nome"] = f"Funcionario {i+1}"
            func_data["email"] = f"funcionario{i+1}@empresa.com.br"
            func_data["created_at"] = datetime.utcnow()
            func_data["updated_at"] = datetime.utcnow()
            
            funcionarios.append(FuncionarioResponseSchema(**func_data))
        
        # Resposta paginada
        lista_response = FuncionarioListResponseSchema(
            items=funcionarios,
            total=25,
            page=1,
            size=10,
            pages=3
        )
        
        print("✅ Resposta paginada criada:")
        print(f"Total de itens: {lista_response.total}")
        print(f"Página atual: {lista_response.page}")
        print(f"Itens por página: {lista_response.size}")
        
        return SchemaSerializer.serialize_model(lista_response)
    
    @staticmethod
    def exemplo_resposta_erro_validacao() -> Dict[str, Any]:
        """
        Exemplo de resposta de erro de validação.
        
        Returns:
            Dict com resposta de erro
        """
        # Simular erro de validação
        validation_errors = [
            {
                "field": "email",
                "message": "Formato de email inválido",
                "type": "value_error",
                "value": "email-invalido"
            },
            {
                "field": "cpf",
                "message": "CPF deve ter exatamente 11 dígitos",
                "type": "value_error",
                "value": "123"
            }
        ]
        
        validation_error = ValidationErrorSchema(
            type="ValidationError",
            message="Erro na validação dos dados fornecidos",
            details=validation_errors,
            total_errors=len(validation_errors)
        )
        
        error_response = ErrorResponseSchema(
            success=False,
            message="Erro na validação dos dados",
            error=validation_error,
            timestamp=datetime.utcnow()
        )
        
        print("❌ Resposta de erro de validação:")
        print(json.dumps(
            SchemaSerializer.serialize_model(error_response),
            indent=2,
            ensure_ascii=False
        ))
        
        return SchemaSerializer.serialize_model(error_response)
    
    @staticmethod
    def exemplo_resposta_erro_nao_encontrado() -> Dict[str, Any]:
        """
        Exemplo de resposta para recurso não encontrado.
        
        Returns:
            Dict com resposta de erro
        """
        error_response = ErrorResponseSchema(
            success=False,
            message="Funcionário não encontrado",
            error={
                "type": "NotFoundError",
                "message": "Funcionário com ID '507f1f77bcf86cd799439011' não foi encontrado",
                "code": "FUNCIONARIO_NAO_ENCONTRADO"
            },
            timestamp=datetime.utcnow()
        )
        
        print("❌ Resposta de erro - Não encontrado:")
        print(json.dumps(
            SchemaSerializer.serialize_model(error_response),
            indent=2,
            ensure_ascii=False
        ))
        
        return SchemaSerializer.serialize_model(error_response)


# ==========================================
# EXEMPLOS DE HEALTH CHECK
# ==========================================

class HealthExamples:
    """
    Exemplos de schemas de health check.
    """
    
    @staticmethod
    def exemplo_health_check_saudavel() -> Dict[str, Any]:
        """
        Exemplo de health check com todos os componentes saudáveis.
        
        Returns:
            Dict com status de saúde
        """
        # Status da aplicação
        app_health = ApplicationHealthSchema(
            status="healthy",
            message="Aplicação funcionando normalmente",
            version="1.0.0",
            uptime_seconds=3600.5,
            environment="production",
            memory_usage_mb=128.5
        )
        
        # Status do banco de dados
        db_health = DatabaseHealthSchema(
            status="healthy",
            message="Conexão com MongoDB funcionando normalmente",
            response_time_ms=12.3,
            connection_pool_size=10,
            active_connections=3,
            database_version="7.0.4"
        )
        
        # Health check completo
        health_response = HealthCheckResponseSchema(
            status="healthy",
            application=app_health,
            database=db_health,
            total_response_time_ms=25.8
        )
        
        print("✅ Health check saudável:")
        print(f"Status geral: {health_response.status}")
        print(f"Aplicação saudável: {health_response.is_healthy}")
        
        return SchemaSerializer.serialize_model(health_response)
    
    @staticmethod
    def exemplo_health_check_com_problemas() -> Dict[str, Any]:
        """
        Exemplo de health check com problemas no banco de dados.
        
        Returns:
            Dict com status de saúde
        """
        # Status da aplicação (saudável)
        app_health = ApplicationHealthSchema(
            status="healthy",
            message="Aplicação funcionando normalmente",
            version="1.0.0",
            uptime_seconds=3600.5,
            environment="production",
            memory_usage_mb=128.5
        )
        
        # Status do banco de dados (com problemas)
        db_health = DatabaseHealthSchema(
            status="degraded",
            message="Conexão com banco lenta - pool de conexões saturado",
            response_time_ms=2500.0,
            connection_pool_size=10,
            active_connections=10,
            database_version="7.0.4"
        )
        
        # Health check com problemas
        health_response = HealthCheckResponseSchema(
            status="degraded",
            application=app_health,
            database=db_health,
            total_response_time_ms=2525.8
        )
        
        print("⚠️ Health check com problemas:")
        print(f"Status geral: {health_response.status}")
        print(f"Aplicação saudável: {health_response.is_healthy}")
        print(f"Problema no banco: {db_health.message}")
        
        return SchemaSerializer.serialize_model(health_response)


# ==========================================
# EXEMPLOS DE VALIDADORES CUSTOMIZADOS
# ==========================================

class ValidatorExamples:
    """
    Exemplos de uso dos validadores customizados.
    """
    
    @staticmethod
    def exemplo_validacao_cpf():
        """
        Demonstra validação de CPF.
        """
        cpfs_teste = [
            "12345678901",  # Válido
            "11111111111",  # Inválido - sequência
            "123",          # Inválido - muito curto
            "12345678900"   # Inválido - dígito verificador
        ]
        
        print("🔍 Testando validação de CPF:")
        
        for cpf in cpfs_teste:
            try:
                validado = CustomValidators.validar_cpf(cpf)
                print(f"  ✅ CPF {cpf}: Válido")
            except ValueError as e:
                print(f"  ❌ CPF {cpf}: {str(e)}")
    
    @staticmethod
    def exemplo_validacao_telefone():
        """
        Demonstra validação de telefone brasileiro.
        """
        telefones_teste = [
            "(11) 99999-9999",  # Válido
            "+55 11 98888-7777", # Válido
            "11999998888",       # Válido
            "123",               # Inválido
            "(00) 1234-5678"     # Inválido - DDD inválido
        ]
        
        print("\n📱 Testando validação de telefone:")
        
        for telefone in telefones_teste:
            try:
                validado = CustomValidators.validar_telefone_brasileiro(telefone)
                print(f"  ✅ Telefone {telefone}: Válido")
            except ValueError as e:
                print(f"  ❌ Telefone {telefone}: {str(e)}")
    
    @staticmethod
    def exemplo_validacao_email_corporativo():
        """
        Demonstra validação de email corporativo.
        """
        emails_teste = [
            "joao@empresa.com.br",    # Válido
            "maria@gmail.com",        # Inválido - não corporativo
            "pedro@corporacao.com",   # Válido
            "email-invalido"          # Inválido - formato
        ]
        
        print("\n📧 Testando validação de email corporativo:")
        
        for email in emails_teste:
            try:
                validado = CustomValidators.validar_email_corporativo(email)
                print(f"  ✅ Email {email}: Válido")
            except ValueError as e:
                print(f"  ❌ Email {email}: {str(e)}")


# ==========================================
# DEMONSTRAÇÃO COMPLETA
# ==========================================

def executar_todos_exemplos():
    """
    Executa todos os exemplos de schemas.
    """
    print("=" * 80)
    print("🚀 DEMONSTRAÇÃO DOS SCHEMAS PYDANTIC")
    print("=" * 80)
    
    # Exemplos de funcionário
    print("\n📋 EXEMPLOS DE FUNCIONÁRIO:")
    print("-" * 40)
    FuncionarioExamples.exemplo_criacao_valida()
    print()
    FuncionarioExamples.exemplo_criacao_invalida()
    print()
    FuncionarioExamples.exemplo_atualizacao_parcial()
    print()
    FuncionarioExamples.exemplo_tentativa_atualizacao_campos_imutaveis()
    print()
    FuncionarioExamples.exemplo_consulta_com_filtros()
    
    # Exemplos de respostas
    print("\n📤 EXEMPLOS DE RESPOSTAS:")
    print("-" * 40)
    ResponseExamples.exemplo_resposta_sucesso_criacao()
    print()
    ResponseExamples.exemplo_resposta_lista_paginada()
    print()
    ResponseExamples.exemplo_resposta_erro_validacao()
    print()
    ResponseExamples.exemplo_resposta_erro_nao_encontrado()
    
    # Exemplos de health check
    print("\n🏥 EXEMPLOS DE HEALTH CHECK:")
    print("-" * 40)
    HealthExamples.exemplo_health_check_saudavel()
    print()
    HealthExamples.exemplo_health_check_com_problemas()
    
    # Exemplos de validadores
    print("\n🔍 EXEMPLOS DE VALIDADORES:")
    print("-" * 40)
    ValidatorExamples.exemplo_validacao_cpf()
    ValidatorExamples.exemplo_validacao_telefone()
    ValidatorExamples.exemplo_validacao_email_corporativo()
    
    print("\n" + "=" * 80)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 80)


if __name__ == "__main__":
    # Executa demonstração quando rodado diretamente
    executar_todos_exemplos()
