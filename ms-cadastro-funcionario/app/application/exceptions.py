"""
Exceções específicas da camada de aplicação.
"""


class ApplicationException(Exception):
    """
    Exceção base para todas as exceções da camada de aplicação.
    """
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class ValidationException(ApplicationException):
    """
    Exceção para erros de validação de entrada de dados.
    """
    
    def __init__(self, field: str, value: str = None, rule: str = None):
        if value and rule:
            message = f"Campo '{field}' com valor '{value}' é inválido: {rule}"
        elif rule:
            message = f"Campo '{field}' é inválido: {rule}"
        else:
            message = f"Campo '{field}' contém dados inválidos"
        
        super().__init__(message, "VALIDATION_ERROR", {
            "field": field,
            "value": value,
            "rule": rule
        })


class BusinessRuleException(ApplicationException):
    """
    Exceção para violações de regras de negócio.
    """
    
    def __init__(self, rule: str, context: dict = None):
        message = f"Regra de negócio violada: {rule}"
        super().__init__(message, "BUSINESS_RULE_VIOLATION", context or {})


class ResourceNotFoundException(ApplicationException):
    """
    Exceção para recursos não encontrados.
    """
    
    def __init__(self, resource: str, identifier: str = None):
        if identifier:
            message = f"{resource} com identificador '{identifier}' não foi encontrado"
        else:
            message = f"{resource} não foi encontrado"
        
        super().__init__(message, "RESOURCE_NOT_FOUND", {
            "resource": resource,
            "identifier": identifier
        })


class DuplicateResourceException(ApplicationException):
    """
    Exceção para recursos duplicados.
    """
    
    def __init__(self, resource: str, field: str, value: str):
        message = f"{resource} com {field} '{value}' já existe no sistema"
        super().__init__(message, "DUPLICATE_RESOURCE", {
            "resource": resource,
            "field": field,
            "value": value
        })


class UnauthorizedOperationException(ApplicationException):
    """
    Exceção para operações não autorizadas.
    """
    
    def __init__(self, operation: str, reason: str = None):
        message = f"Operação '{operation}' não autorizada"
        if reason:
            message += f": {reason}"
        
        super().__init__(message, "UNAUTHORIZED_OPERATION", {
            "operation": operation,
            "reason": reason
        })
