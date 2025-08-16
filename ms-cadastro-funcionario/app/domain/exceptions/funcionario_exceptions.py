"""
Exceções de Domínio para Funcionários

Define todas as exceções específicas para regras de negócio
relacionadas ao domínio de funcionários.
"""


class FuncionarioException(Exception):
    """Exceção base para todas as exceções do domínio de funcionários."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"


class FuncionarioNaoEncontradoException(FuncionarioException):
    """Exceção lançada quando um funcionário não é encontrado."""
    
    def __init__(self, funcionario_id: str = None, email: str = None):
        if funcionario_id:
            message = f"Funcionário com ID '{funcionario_id}' não foi encontrado."
        elif email:
            message = f"Funcionário com email '{email}' não foi encontrado."
        else:
            message = "Funcionário não encontrado."
        
        super().__init__(message, "FUNCIONARIO_NAO_ENCONTRADO")


class EmailDuplicadoException(FuncionarioException):
    """Exceção lançada quando se tenta cadastrar um email que já existe."""
    
    def __init__(self, email: str):
        message = f"O email '{email}' já está sendo usado por outro funcionário."
        super().__init__(message, "EMAIL_DUPLICADO")


class FuncionarioAtivoEmProjetosException(FuncionarioException):
    """Exceção lançada quando se tenta excluir um funcionário ativo em projetos."""
    
    def __init__(self, funcionario_id: str = None, nome: str = None):
        if nome:
            message = f"O funcionário '{nome}' está ativo em projetos e não pode ser excluído."
        elif funcionario_id:
            message = f"O funcionário (ID: {funcionario_id}) está ativo em projetos e não pode ser excluído."
        else:
            message = "Funcionário está ativo em projetos e não pode ser excluído."
        
        super().__init__(message, "FUNCIONARIO_ativo")


class DadosInvalidosException(FuncionarioException):
    """Exceção lançada quando dados fornecidos são inválidos."""
    
    def __init__(self, campo: str, valor: str = None, regra: str = None):
        if regra and valor:
            message = f"Campo '{campo}' com valor '{valor}' é inválido: {regra}"
        elif regra:
            message = f"Campo '{campo}' é inválido: {regra}"
        else:
            message = f"Campo '{campo}' contém dados inválidos."
        
        super().__init__(message, "DADOS_INVALIDOS")


class CargoInvalidoException(FuncionarioException):
    """Exceção lançada quando um cargo inválido é fornecido."""
    
    def __init__(self, cargo: str, cargos_validos: list = None):
        if cargos_validos:
            cargos_str = "', '".join(cargos_validos)
            message = f"Cargo '{cargo}' não é válido. Cargos aceitos: '{cargos_str}'."
        else:
            message = f"Cargo '{cargo}' não é válido."
        
        super().__init__(message, "CARGO_INVALIDO")


class ErroOperacaoException(FuncionarioException):
    """Exceção lançada quando ocorre um erro durante operações de repositório."""
    
    def __init__(self, message: str, operation: str = None):
        if operation:
            full_message = f"Erro na operação '{operation}': {message}"
        else:
            full_message = f"Erro na operação: {message}"
        
        super().__init__(full_message, "ERRO_OPERACAO")
