"""
Configurações centralizadas para schemas Pydantic.

Este módulo centraliza configurações globais, constantes e
utilitários relacionados aos schemas da aplicação.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
import re


# ==========================================
# CONFIGURAÇÕES GLOBAIS
# ==========================================

class SchemaConfig:
    """
    Configurações globais para todos os schemas Pydantic.
    """
    
    # Configuração padrão para todos os schemas
    DEFAULT_CONFIG = {
        "str_strip_whitespace": True,
        "validate_assignment": True,
        "use_enum_values": True,
        "extra": "forbid",
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda dt: dt.isoformat() + "Z" if dt.tzinfo is None else dt.isoformat(),
            Decimal: lambda d: float(d)
        }
    }
    
    # Configuração para serialização JSON
    JSON_CONFIG = {
        "by_alias": True,
        "exclude_unset": False,
        "exclude_none": False
    }
    
    # Configuração para validação
    VALIDATION_CONFIG = {
        "validate_default": True,
        "validate_assignment": True,
        "strict": False
    }


# ==========================================
# CONSTANTES DE VALIDAÇÃO
# ==========================================

class ValidationConstants:
    """
    Constantes utilizadas nas validações dos schemas.
    """
    
    # Limites de tamanho para campos de texto
    NOME_MIN_LENGTH = 2
    NOME_MAX_LENGTH = 100
    SOBRENOME_MIN_LENGTH = 2
    SOBRENOME_MAX_LENGTH = 100
    EMAIL_MAX_LENGTH = 255
    TELEFONE_MAX_LENGTH = 20
    ENDERECO_MAX_LENGTH = 500
    
    # Padrões regex
    TELEFONE_BRASILEIRO_PATTERN = r'^(\+55\s?)?(\(\d{2}\)\s?|\d{2}\s?)[9]?\d{4}[-\s]?\d{4}$'
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    NOME_PATTERN = r'^[a-zA-ZÀ-ÿ\s\'\.]+$'
    
    # Valores monetários
    SALARIO_MIN_VALUE = Decimal('1320.00')  # Salário mínimo brasileiro 2024
    SALARIO_MAX_VALUE = Decimal('1000000.00')  # Limite máximo realista
    
    # Datas
    DATA_NASCIMENTO_MIN_YEAR = 1900
    DATA_NASCIMENTO_MAX_YEAR = datetime.now().year - 16  # Idade mínima 16 anos
    DATA_ADMISSAO_MIN_YEAR = 1950
    DATA_ADMISSAO_MAX_YEAR = datetime.now().year + 1  # Permite agendamento futuro
    
    # Paginação
    PAGE_SIZE_MIN = 1
    PAGE_SIZE_MAX = 100
    PAGE_SIZE_DEFAULT = 20
    PAGE_NUMBER_MIN = 1
    
    # IDs ObjectId MongoDB
    OBJECT_ID_PATTERN = r'^[a-f\d]{24}$'


# ==========================================
# MENSAGENS DE ERRO PADRONIZADAS
# ==========================================

class ErrorMessages:
    """
    Mensagens de erro padronizadas para validações.
    """
    
    # Mensagens gerais
    CAMPO_OBRIGATORIO = "Este campo é obrigatório"
    FORMATO_INVALIDO = "Formato inválido"
    VALOR_MUITO_PEQUENO = "Valor muito pequeno"
    VALOR_MUITO_GRANDE = "Valor muito grande"
    
    # Mensagens específicas - Nome
    NOME_MUITO_CURTO = f"Nome deve ter pelo menos {ValidationConstants.NOME_MIN_LENGTH} caracteres"
    NOME_MUITO_LONGO = f"Nome deve ter no máximo {ValidationConstants.NOME_MAX_LENGTH} caracteres"
    NOME_CARACTERES_INVALIDOS = "Nome deve conter apenas letras, espaços, apóstrofes e pontos"
    NOME_NAO_PODE_SER_VAZIO = "Nome não pode estar vazio ou conter apenas espaços"
    
    # Mensagens específicas - Email
    EMAIL_FORMATO_INVALIDO = "Formato de email inválido"
    EMAIL_MUITO_LONGO = f"Email deve ter no máximo {ValidationConstants.EMAIL_MAX_LENGTH} caracteres"
    EMAIL_DOMINIO_CORPORATIVO_OBRIGATORIO = "Email deve ser de um domínio corporativo válido"
    
    # Mensagens específicas - Telefone
    TELEFONE_FORMATO_INVALIDO = "Formato de telefone brasileiro inválido. Use: (11) 99999-9999 ou +55 11 99999-9999"
    TELEFONE_MUITO_LONGO = f"Telefone deve ter no máximo {ValidationConstants.TELEFONE_MAX_LENGTH} caracteres"
    
    # Mensagens específicas - CPF
    CPF_FORMATO_INVALIDO = "CPF deve conter apenas números"
    CPF_TAMANHO_INVALIDO = "CPF deve ter exatamente 11 dígitos"
    CPF_DIGITOS_INVALIDOS = "CPF possui dígitos verificadores inválidos"
    CPF_SEQUENCIA_INVALIDA = "CPF não pode ser uma sequência de números iguais"
    
    # Mensagens específicas - Salário
    SALARIO_MUITO_BAIXO = f"Salário deve ser pelo menos R$ {ValidationConstants.SALARIO_MIN_VALUE}"
    SALARIO_MUITO_ALTO = f"Salário deve ser no máximo R$ {ValidationConstants.SALARIO_MAX_VALUE}"
    SALARIO_FORMATO_INVALIDO = "Salário deve ser um valor monetário válido"
    
    # Mensagens específicas - Datas
    DATA_NASCIMENTO_MUITO_ANTIGA = f"Data de nascimento deve ser posterior a {ValidationConstants.DATA_NASCIMENTO_MIN_YEAR}"
    DATA_NASCIMENTO_MUITO_RECENTE = f"Funcionário deve ter pelo menos 16 anos de idade"
    DATA_ADMISSAO_MUITO_ANTIGA = f"Data de admissão deve ser posterior a {ValidationConstants.DATA_ADMISSAO_MIN_YEAR}"
    DATA_ADMISSAO_MUITO_RECENTE = "Data de admissão não pode ser muito no futuro"
    DATA_ADMISSAO_ANTES_NASCIMENTO = "Data de admissão não pode ser anterior à data de nascimento"
    
    # Mensagens específicas - Cargo
    CARGO_MUITO_CURTO = "Cargo deve ter pelo menos 2 caracteres"
    CARGO_MUITO_LONGO = "Cargo deve ter no máximo 100 caracteres"
    CARGO_CARACTERES_INVALIDOS = "Cargo deve conter apenas letras, números, espaços e símbolos básicos"
    
    # Mensagens específicas - Departamento
    DEPARTAMENTO_MUITO_CURTO = "Departamento deve ter pelo menos 2 caracteres"
    DEPARTAMENTO_MUITO_LONGO = "Departamento deve ter no máximo 100 caracteres"
    DEPARTAMENTO_CARACTERES_INVALIDOS = "Departamento deve conter apenas letras, números, espaços e símbolos básicos"
    
    # Mensagens específicas - Status
    STATUS_INVALIDO = "Status deve ser: ativo, inativo ou suspenso"
    
    # Mensagens específicas - Paginação
    PAGINA_NUMERO_INVALIDO = f"Número da página deve ser pelo menos {ValidationConstants.PAGE_NUMBER_MIN}"
    TAMANHO_PAGINA_MUITO_PEQUENO = f"Tamanho da página deve ser pelo menos {ValidationConstants.PAGE_SIZE_MIN}"
    TAMANHO_PAGINA_MUITO_GRANDE = f"Tamanho da página deve ser no máximo {ValidationConstants.PAGE_SIZE_MAX}"
    
    # Mensagens específicas - IDs
    ID_FORMATO_INVALIDO = "ID deve ser um ObjectId válido do MongoDB (24 caracteres hexadecimais)"
    
    # Mensagens específicas - Filtros
    FILTRO_DATA_INICIAL_MAIOR = "Data inicial não pode ser maior que data final"
    FILTRO_VALOR_INVALIDO = "Valor do filtro é inválido"


# ==========================================
# CONFIGURAÇÕES DE DOMÍNIOS CORPORATIVOS
# ==========================================

class CorporateConfig:
    """
    Configurações relacionadas a validações corporativas.
    """
    
    # Domínios de email corporativo aceitos
    DOMINIOS_CORPORATIVOS_ACEITOS = [
        "empresa.com.br",
        "corporacao.com",
        "companhia.com.br",
        "grupo.com.br",
        "holding.com.br"
    ]
    
    # Cargos válidos (pode ser expandido)
    CARGOS_VALIDOS = [
        "Desenvolvedor Junior",
        "Desenvolvedor Pleno",
        "Desenvolvedor Senior",
        "Tech Lead",
        "Arquiteto de Software",
        "Product Owner",
        "Scrum Master",
        "Analista de Sistemas",
        "Gerente de Projetos",
        "Diretor de Tecnologia"
    ]
    
    # Departamentos válidos
    DEPARTAMENTOS_VALIDOS = [
        "Tecnologia",
        "Recursos Humanos",
        "Financeiro",
        "Comercial",
        "Marketing",
        "Operações",
        "Jurídico",
        "Auditoria",
        "Compras",
        "Logística"
    ]
    
    # Status de funcionário válidos
    STATUS_FUNCIONARIO_VALIDOS = [
        "ativo",
        "inativo",
        "suspenso"
    ]


# ==========================================
# UTILITÁRIOS DE SCHEMA
# ==========================================

class SchemaUtils:
    """
    Utilitários para trabalhar com schemas.
    """
    
    @staticmethod
    def criar_exemplo_funcionario() -> Dict[str, Any]:
        """
        Cria um exemplo padrão de funcionário para documentação.
        
        Returns:
            Dict com dados de exemplo de funcionário
        """
        return {
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
            "status": "ativo"
        }
    
    @staticmethod
    def criar_exemplo_resposta_sucesso() -> Dict[str, Any]:
        """
        Cria um exemplo padrão de resposta de sucesso.
        
        Returns:
            Dict com estrutura de resposta de sucesso
        """
        return {
            "success": True,
            "message": "Operação realizada com sucesso",
            "data": SchemaUtils.criar_exemplo_funcionario(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    @staticmethod
    def criar_exemplo_resposta_erro() -> Dict[str, Any]:
        """
        Cria um exemplo padrão de resposta de erro.
        
        Returns:
            Dict com estrutura de resposta de erro
        """
        return {
            "success": False,
            "message": "Erro na validação dos dados",
            "error": {
                "type": "ValidationError",
                "details": [
                    {
                        "field": "email",
                        "message": "Formato de email inválido",
                        "value": "email-invalido"
                    }
                ]
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    @staticmethod
    def criar_exemplo_lista_paginada() -> Dict[str, Any]:
        """
        Cria um exemplo padrão de resposta paginada.
        
        Returns:
            Dict com estrutura de resposta paginada
        """
        return {
            "items": [SchemaUtils.criar_exemplo_funcionario()],
            "total": 1,
            "page": 1,
            "size": 20,
            "pages": 1
        }
    
    @staticmethod
    def validar_object_id(value: str) -> bool:
        """
        Valida se uma string é um ObjectId válido do MongoDB.
        
        Args:
            value: String para validar
            
        Returns:
            True se for um ObjectId válido
        """
        if not isinstance(value, str):
            return False
        
        return bool(re.match(ValidationConstants.OBJECT_ID_PATTERN, value))
    
    @staticmethod
    def limpar_telefone(telefone: str) -> str:
        """
        Remove formatação de um telefone brasileiro.
        
        Args:
            telefone: Telefone formatado
            
        Returns:
            Telefone apenas com números
        """
        return re.sub(r'[^\d]', '', telefone)
    
    @staticmethod
    def formatar_telefone(telefone: str) -> str:
        """
        Formata um telefone brasileiro.
        
        Args:
            telefone: Telefone apenas com números
            
        Returns:
            Telefone formatado
        """
        numeros = SchemaUtils.limpar_telefone(telefone)
        
        if len(numeros) == 11:
            return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
        elif len(numeros) == 10:
            return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
        
        return telefone
    
    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        """
        Remove formatação de um CPF.
        
        Args:
            cpf: CPF formatado
            
        Returns:
            CPF apenas com números
        """
        return re.sub(r'[^\d]', '', cpf)
    
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """
        Formata um CPF.
        
        Args:
            cpf: CPF apenas com números
            
        Returns:
            CPF formatado
        """
        numeros = SchemaUtils.limpar_cpf(cpf)
        
        if len(numeros) == 11:
            return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
        
        return cpf


# ==========================================
# CONFIGURAÇÕES DE PAGINAÇÃO
# ==========================================

class PaginationConfig:
    """
    Configurações específicas para paginação.
    """
    
    DEFAULT_PAGE = 1
    DEFAULT_SIZE = ValidationConstants.PAGE_SIZE_DEFAULT
    MIN_SIZE = ValidationConstants.PAGE_SIZE_MIN
    MAX_SIZE = ValidationConstants.PAGE_SIZE_MAX
    
    @classmethod
    def get_pagination_params(cls, page: Optional[int] = None, size: Optional[int] = None) -> Dict[str, int]:
        """
        Retorna parâmetros de paginação validados.
        
        Args:
            page: Número da página
            size: Tamanho da página
            
        Returns:
            Dict com parâmetros validados
        """
        validated_page = max(cls.DEFAULT_PAGE, page or cls.DEFAULT_PAGE)
        validated_size = max(
            cls.MIN_SIZE,
            min(cls.MAX_SIZE, size or cls.DEFAULT_SIZE)
        )
        
        return {
            "page": validated_page,
            "size": validated_size,
            "skip": (validated_page - 1) * validated_size
        }
