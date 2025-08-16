"""
Validadores para a camada de aplicação.

Contém validadores específicos para regras de negócio e validação
de dados que não pertencem ao domínio, mas são necessários na aplicação.
"""

import re
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

from app.application.exceptions import ValidationException


class CPFValidator:
    """
    Validador para CPF com algoritmo oficial da Receita Federal.
    """
    
    @staticmethod
    def validate(cpf: str) -> bool:
        """
        Valida se um CPF é válido segundo o algoritmo oficial.
        
        Args:
            cpf: String do CPF (pode conter pontos e traços)
            
        Returns:
            True se o CPF é válido, False caso contrário
        """
        if not cpf:
            return False
        
        # Remove formatação
        cpf_numbers = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf_numbers) != 11:
            return False
        
        # Verifica sequências iguais (111.111.111-11, 222.222.222-22, etc.)
        if cpf_numbers == cpf_numbers[0] * 11:
            return False
        
        # Calcula os dígitos verificadores
        def calculate_digit(cpf_partial: str, weights: List[int]) -> int:
            total = sum(int(digit) * weight for digit, weight in zip(cpf_partial, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Primeiro dígito verificador
        first_digit = calculate_digit(cpf_numbers[:9], list(range(10, 1, -1)))
        
        # Segundo dígito verificador
        second_digit = calculate_digit(cpf_numbers[:10], list(range(11, 1, -1)))
        
        # Verifica se os dígitos calculados conferem
        return cpf_numbers[9:11] == f"{first_digit}{second_digit}"
    
    @staticmethod
    def validate_and_raise(cpf: str, field_name: str = "cpf") -> None:
        """
        Valida CPF e levanta exceção se inválido.
        
        Args:
            cpf: String do CPF
            field_name: Nome do campo para a exceção
            
        Raises:
            ValidationException: Se o CPF é inválido
        """
        if not CPFValidator.validate(cpf):
            raise ValidationException(
                field=field_name,
                value=cpf,
                rule="CPF deve seguir algoritmo oficial da Receita Federal"
            )


class EmailValidator:
    """
    Validador para endereços de email.
    """
    
    # Regex básico para validação de email
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    @staticmethod
    def validate(email: str) -> bool:
        """
        Valida se um email tem formato válido.
        
        Args:
            email: String do email
            
        Returns:
            True se o email é válido, False caso contrário
        """
        if not email:
            return False
        
        return EmailValidator.EMAIL_PATTERN.match(email) is not None
    
    @staticmethod
    def validate_and_raise(email: str, field_name: str = "email") -> None:
        """
        Valida email e levanta exceção se inválido.
        
        Args:
            email: String do email
            field_name: Nome do campo para a exceção
            
        Raises:
            ValidationException: Se o email é inválido
        """
        if not EmailValidator.validate(email):
            raise ValidationException(
                field=field_name,
                value=email,
                rule="deve ter formato válido (exemplo@dominio.com)"
            )


class TelefoneValidator:
    """
    Validador para números de telefone brasileiros.
    """
    
    # Regex para telefones brasileiros (celular e fixo)
    PHONE_PATTERN = re.compile(
        r'^\(?\d{2}\)?[\s-]?(?:9\d{8}|\d{8})$'
    )
    
    @staticmethod
    def validate(telefone: str) -> bool:
        """
        Valida se um telefone tem formato brasileiro válido.
        
        Args:
            telefone: String do telefone
            
        Returns:
            True se o telefone é válido, False caso contrário
        """
        if not telefone:
            return True  # Telefone é opcional
        
        # Remove formatação para validação
        phone_clean = re.sub(r'[^0-9]', '', telefone)
        
        # Verifica se tem 10 (fixo) ou 11 (celular) dígitos
        return len(phone_clean) in [10, 11] and TelefoneValidator.PHONE_PATTERN.match(telefone)
    
    @staticmethod
    def validate_and_raise(telefone: str, field_name: str = "telefone") -> None:
        """
        Valida telefone e levanta exceção se inválido.
        
        Args:
            telefone: String do telefone
            field_name: Nome do campo para a exceção
            
        Raises:
            ValidationException: Se o telefone é inválido
        """
        if telefone and not TelefoneValidator.validate(telefone):
            raise ValidationException(
                field=field_name,
                value=telefone,
                rule="deve ter formato brasileiro válido ((XX) XXXXX-XXXX ou (XX) XXXX-XXXX)"
            )


class DataValidator:
    """
    Validador para datas.
    """
    
    @staticmethod
    def validate_birth_date(data_nascimento: date) -> bool:
        """
        Valida se uma data de nascimento é válida.
        
        Args:
            data_nascimento: Data de nascimento
            
        Returns:
            True se a data é válida, False caso contrário
        """
        if not data_nascimento:
            return True  # Data de nascimento é opcional
        
        today = date.today()
        
        # Data deve ser no passado
        if data_nascimento >= today:
            return False
        
        # Pessoa não pode ter mais de 120 anos
        age = today.year - data_nascimento.year
        if age > 120:
            return False
        
        return True
    
    @staticmethod
    def validate_admission_date(data_admissao: date) -> bool:
        """
        Valida se uma data de admissão é válida.
        
        Args:
            data_admissao: Data de admissão
            
        Returns:
            True se a data é válida, False caso contrário
        """
        if not data_admissao:
            return True  # Data de admissão é opcional
        
        today = date.today()
        
        # Data não pode ser muito no futuro (máximo 1 ano)
        if data_admissao > today.replace(year=today.year + 1):
            return False
        
        return True
    
    @staticmethod
    def validate_and_raise_birth_date(
        data_nascimento: date, 
        field_name: str = "data_nascimento"
    ) -> None:
        """
        Valida data de nascimento e levanta exceção se inválida.
        """
        if data_nascimento and not DataValidator.validate_birth_date(data_nascimento):
            raise ValidationException(
                field=field_name,
                value=str(data_nascimento),
                rule="deve ser uma data no passado e a pessoa não pode ter mais de 120 anos"
            )
    
    @staticmethod
    def validate_and_raise_admission_date(
        data_admissao: date, 
        field_name: str = "data_admissao"
    ) -> None:
        """
        Valida data de admissão e levanta exceção se inválida.
        """
        if data_admissao and not DataValidator.validate_admission_date(data_admissao):
            raise ValidationException(
                field=field_name,
                value=str(data_admissao),
                rule="não pode ser mais de 1 ano no futuro"
            )


class SalarioValidator:
    """
    Validador para valores de salário.
    """
    
    @staticmethod
    def validate(salario: Decimal) -> bool:
        """
        Valida se um valor de salário é válido.
        
        Args:
            salario: Valor do salário
            
        Returns:
            True se o salário é válido, False caso contrário
        """
        if salario is None:
            return True  # Salário é opcional
        
        # Deve ser positivo
        if salario <= 0:
            return False
        
        # Deve ter no máximo 2 casas decimais
        if salario.as_tuple().exponent < -2:
            return False
        
        # Limite razoável para salário (R$ 1 milhão)
        if salario > Decimal('1000000.00'):
            return False
        
        return True
    
    @staticmethod
    def validate_and_raise(salario: Decimal, field_name: str = "salario") -> None:
        """
        Valida salário e levanta exceção se inválido.
        
        Args:
            salario: Valor do salário
            field_name: Nome do campo para a exceção
            
        Raises:
            ValidationException: Se o salário é inválido
        """
        if salario is not None and not SalarioValidator.validate(salario):
            raise ValidationException(
                field=field_name,
                value=str(salario),
                rule="deve ser positivo, ter no máximo 2 casas decimais e não exceder R$ 1.000.000,00"
            )


class StringValidator:
    """
    Validador para campos de texto.
    """
    
    @staticmethod
    def validate_name(nome: str, min_length: int = 2, max_length: int = 100) -> bool:
        """
        Valida se um nome é válido.
        
        Args:
            nome: Nome a ser validado
            min_length: Comprimento mínimo
            max_length: Comprimento máximo
            
        Returns:
            True se o nome é válido, False caso contrário
        """
        if not nome:
            return False
        
        nome_clean = nome.strip()
        
        if len(nome_clean) < min_length or len(nome_clean) > max_length:
            return False
        
        # Deve conter pelo menos uma letra
        if not re.search(r'[a-zA-ZÀ-ÿ]', nome_clean):
            return False
        
        return True
    
    @staticmethod
    def validate_and_raise_name(
        nome: str, 
        field_name: str,
        min_length: int = 2, 
        max_length: int = 100
    ) -> None:
        """
        Valida nome e levanta exceção se inválido.
        """
        if not StringValidator.validate_name(nome, min_length, max_length):
            raise ValidationException(
                field=field_name,
                value=nome,
                rule=f"deve ter entre {min_length} e {max_length} caracteres e conter pelo menos uma letra"
            )
