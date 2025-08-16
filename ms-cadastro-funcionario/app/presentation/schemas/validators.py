"""
Validadores customizados para os schemas Pydantic.

Este módulo contém validadores específicos para campos que requerem
validações customizadas além das fornecidas pelo Pydantic.
"""

import re
from datetime import date, datetime
from typing import Any, Optional
from email_validator import validate_email, EmailNotValidError


class CustomValidators:
    """
    Classe com validadores customizados para campos específicos.
    
    Todos os métodos são estáticos para facilitar uso em validators do Pydantic.
    """
    
    # Regex para validação de telefone brasileiro
    PHONE_REGEX = re.compile(
        r'^\(?\d{2}\)?[\s-]?(?:9?\d{4})[\s-]?\d{4}$'
    )
    
    # Regex para validação de nome (apenas letras, espaços e acentos)
    NAME_REGEX = re.compile(
        r'^[A-Za-zÀ-ÿ\s]+$'
    )
    
    @staticmethod
    def validar_nome_completo(nome: str) -> str:
        """
        Valida e normaliza nome completo.
        
        Regras:
        - Mínimo 2 palavras
        - Apenas letras, espaços e acentos
        - Cada palavra deve ter pelo menos 2 caracteres
        - Capitaliza adequadamente
        
        Args:
            nome: Nome a ser validado
            
        Returns:
            Nome validado e normalizado
            
        Raises:
            ValueError: Se o nome não atender aos critérios
        """
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome é obrigatório")
        
        # Remove espaços extras e normaliza
        nome_clean = ' '.join(nome.strip().split())
        
        # Verifica se tem pelo menos 2 palavras
        palavras = nome_clean.split()
        if len(palavras) < 2:
            raise ValueError("Nome deve conter pelo menos 2 palavras (nome e sobrenome)")
        
        # Verifica se cada palavra tem pelo menos 2 caracteres
        for palavra in palavras:
            if len(palavra) < 2:
                raise ValueError("Cada palavra do nome deve ter pelo menos 2 caracteres")
        
        # Verifica se contém apenas letras, espaços e acentos
        if not CustomValidators.NAME_REGEX.match(nome_clean):
            raise ValueError("Nome deve conter apenas letras, espaços e acentos")
        
        # Capitaliza adequadamente (primeira letra de cada palavra maiúscula)
        nome_formatted = nome_clean.title()
        
        # Trata casos especiais de preposições e artigos
        preposicoes = ['de', 'da', 'do', 'das', 'dos', 'e']
        palavras_formatadas = []
        
        for palavra in nome_formatted.split():
            if palavra.lower() in preposicoes and len(palavras_formatadas) > 0:
                palavras_formatadas.append(palavra.lower())
            else:
                palavras_formatadas.append(palavra)
        
        return ' '.join(palavras_formatadas)
    
    @staticmethod
    def validar_telefone_brasileiro(telefone: Optional[str]) -> Optional[str]:
        """
        Valida e normaliza telefone brasileiro.
        
        Formatos aceitos:
        - (11) 99999-9999
        - (11) 9999-9999
        - 11 99999-9999
        - 1199999999
        - 11999999999
        
        Args:
            telefone: Telefone a ser validado
            
        Returns:
            Telefone normalizado no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
            
        Raises:
            ValueError: Se o telefone não for válido
        """
        if not telefone:
            return None
        
        # Remove todos os caracteres não numéricos
        digitos = re.sub(r'[^0-9]', '', telefone)
        
        # Verifica se tem 10 ou 11 dígitos
        if len(digitos) not in [10, 11]:
            raise ValueError(
                "Telefone deve conter 10 dígitos (fixo) ou 11 dígitos (celular)"
            )
        
        # Verifica se o código de área é válido (11 a 99)
        codigo_area = int(digitos[:2])
        if codigo_area < 11 or codigo_area > 99:
            raise ValueError("Código de área deve estar entre 11 e 99")
        
        # Formatar baseado no número de dígitos
        if len(digitos) == 11:
            # Celular: (XX) 9XXXX-XXXX
            if not digitos[2] == '9':
                raise ValueError("Número de celular deve começar com 9 após o código de área")
            return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
        else:
            # Fixo: (XX) XXXX-XXXX
            if digitos[2] == '9':
                raise ValueError("Número fixo não pode começar com 9")
            return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    
    @staticmethod
    def validar_email_corporativo(email: str) -> str:
        """
        Valida email usando email-validator e aplica regras específicas.
        
        Args:
            email: Email a ser validado
            
        Returns:
            Email normalizado (lowercase)
            
        Raises:
            ValueError: Se o email não for válido
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email é obrigatório")
        
        try:
            # Usa a biblioteca email-validator para validação completa
            validation_result = validate_email(email)
            email_normalizado = validation_result.email
            
            # Converte para minúsculo
            email_normalizado = email_normalizado.lower()
            
            # Validações adicionais específicas da empresa se necessário
            # Por exemplo, domínios não permitidos, etc.
            dominios_bloqueados = [
                'tempmail.com',
                '10minutemail.com',
                'guerrillamail.com'
            ]
            
            dominio = email_normalizado.split('@')[1]
            if dominio in dominios_bloqueados:
                raise ValueError(f"Domínio {dominio} não é permitido")
            
            return email_normalizado
            
        except EmailNotValidError as e:
            raise ValueError(f"Email inválido: {str(e)}")
    
    @staticmethod
    def normalizar_cargo(cargo: str) -> str:
        """
        Normaliza cargo removendo espaços extras e aplicando capitalização.
        
        Args:
            cargo: Cargo a ser normalizado
            
        Returns:
            Cargo normalizado
            
        Raises:
            ValueError: Se o cargo estiver vazio após normalização
        """
        if not cargo or not isinstance(cargo, str):
            raise ValueError("Cargo é obrigatório")
        
        # Remove espaços extras e capitaliza adequadamente
        cargo_clean = ' '.join(cargo.strip().split())
        
        if not cargo_clean:
            raise ValueError("Cargo não pode estar vazio")
        
        # Capitaliza primeira letra de cada palavra
        return cargo_clean.title()
    
    @staticmethod
    def normalizar_departamento(departamento: Optional[str]) -> Optional[str]:
        """
        Normaliza departamento removendo espaços extras e aplicando capitalização.
        
        Args:
            departamento: Departamento a ser normalizado
            
        Returns:
            Departamento normalizado ou None
        """
        if not departamento:
            return None
        
        # Remove espaços extras e capitaliza adequadamente
        dept_clean = ' '.join(departamento.strip().split())
        
        if not dept_clean:
            return None
        
        # Capitaliza primeira letra de cada palavra
        return dept_clean.title()
    
    @staticmethod
    def validar_data_admissao(data_admissao: date) -> date:
        """
        Valida data de admissão.
        
        Regras:
        - Não pode ser futura
        - Não pode ser anterior a 1900
        
        Args:
            data_admissao: Data de admissão
            
        Returns:
            Data validada
            
        Raises:
            ValueError: Se a data não atender aos critérios
        """
        if not data_admissao:
            raise ValueError("Data de admissão é obrigatória")
        
        hoje = date.today()
        
        # Não pode ser futura
        if data_admissao > hoje:
            raise ValueError("Data de admissão não pode ser futura")
        
        # Não pode ser anterior a 1900
        if data_admissao.year < 1900:
            raise ValueError("Data de admissão não pode ser anterior a 1900")
        
        return data_admissao
    
    @staticmethod
    def validar_data_nascimento(data_nascimento: Optional[date]) -> Optional[date]:
        """
        Valida data de nascimento.
        
        Regras:
        - Não pode ser futura
        - Pessoa não pode ter mais de 120 anos
        - Pessoa deve ter pelo menos 16 anos
        
        Args:
            data_nascimento: Data de nascimento
            
        Returns:
            Data validada ou None
            
        Raises:
            ValueError: Se a data não atender aos critérios
        """
        if not data_nascimento:
            return None
        
        hoje = date.today()
        
        # Não pode ser futura
        if data_nascimento > hoje:
            raise ValueError("Data de nascimento não pode ser futura")
        
        # Calcula idade
        idade = hoje.year - data_nascimento.year
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        # Pessoa deve ter pelo menos 16 anos
        if idade < 16:
            raise ValueError("Funcionário deve ter pelo menos 16 anos")
        
        # Pessoa não pode ter mais de 120 anos
        if idade > 120:
            raise ValueError("Idade não pode ser superior a 120 anos")
        
        return data_nascimento
    
    @staticmethod
    def validar_salario(salario: Optional[Any]) -> Optional[float]:
        """
        Valida valor de salário.
        
        Args:
            salario: Salário a ser validado
            
        Returns:
            Salário validado como float ou None
            
        Raises:
            ValueError: Se o salário não for válido
        """
        if salario is None:
            return None
        
        try:
            salario_float = float(salario)
        except (ValueError, TypeError):
            raise ValueError("Salário deve ser um número válido")
        
        if salario_float <= 0:
            raise ValueError("Salário deve ser maior que zero")
        
        # Limite máximo razoável (R$ 1 milhão)
        if salario_float > 1000000:
            raise ValueError("Salário não pode exceder R$ 1.000.000,00")
        
        # Arredonda para 2 casas decimais
        return round(salario_float, 2)
