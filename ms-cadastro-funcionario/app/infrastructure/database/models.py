"""
Modelos de dados para MongoDB - mapeamento entre entidade de domínio e documentos.
"""
from typing import Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
from bson import ObjectId

from app.domain.entities.funcionario import Funcionario
from app.domain.entities.value_objects import Email, Cargo, Telefone


class FuncionarioModel:
    """
    Modelo para mapeamento entre entidade Funcionario e documento MongoDB.
    
    Responsável por converter entre a representação de domínio e
    a representação de persistência no banco de dados.
    """
    
    @staticmethod
    def from_entity(funcionario: Funcionario) -> Dict[str, Any]:
        """
        Converte entidade de domínio para documento MongoDB.
        
        Args:
            funcionario: Instância da entidade Funcionario
            
        Returns:
            Dict representando o documento para MongoDB
        """
        document = {
            "nome_completo": funcionario.nome_completo,  # Corrigido: usar nome_completo
            "email": funcionario.email.value,
            "cargo": funcionario.cargo.value,
            "data_admissao": datetime.combine(funcionario.data_admissao, datetime.min.time()),  # Converter para datetime
            "ativo": funcionario.ativo,
            "created_at": funcionario.created_at,  # Salvar como Date, não string
            "updated_at": funcionario.updated_at if funcionario.updated_at else None
        }
        
        # Campos opcionais
        if funcionario.telefone:
            document["telefone"] = funcionario.telefone.value
        
        if funcionario.departamento:
            document["departamento"] = funcionario.departamento
            
        # CPF se existir na entidade (não é padrão)
        if hasattr(funcionario, 'cpf') and getattr(funcionario, 'cpf', None):
            document["cpf"] = funcionario.cpf
            
        # Data nascimento se existir na entidade (não é padrão)
        if hasattr(funcionario, 'data_nascimento') and getattr(funcionario, 'data_nascimento', None):
            data_nascimento = getattr(funcionario, 'data_nascimento')
            if isinstance(data_nascimento, date):
                document["data_nascimento"] = datetime.combine(data_nascimento, datetime.min.time())
            else:
                document["data_nascimento"] = data_nascimento
            
        # Salário como número, não string
        if funcionario.salario is not None:
            document["salario"] = float(funcionario.salario)  # Converter Decimal para float
        
        # Se tem ID, incluir (para updates)
        if funcionario.id:
            document["_id"] = ObjectId(funcionario.id)
        
        return document
    
    @staticmethod
    def to_entity(document: Dict[str, Any]) -> Funcionario:
        """
        Converte documento MongoDB para entidade de domínio.
        
        Args:
            document: Documento do MongoDB
            
        Returns:
            Instância da entidade Funcionario
        """
        # Criar Value Objects
        email = Email(document["email"])
        cargo = Cargo(document["cargo"])
        
        telefone = None
        if document.get("telefone"):
            telefone = Telefone(document["telefone"])
        
        # Converter datas com suporte a ambos os formatos (Date e string)
        def convert_date_field(field_value, is_date_only=False):
            if field_value is None:
                return None
            if isinstance(field_value, str):
                dt = datetime.fromisoformat(field_value.replace('Z', '+00:00'))
                return dt.date() if is_date_only else dt
            elif isinstance(field_value, datetime):
                return field_value.date() if is_date_only else field_value
            elif isinstance(field_value, date) and not is_date_only:
                return datetime.combine(field_value, datetime.min.time())
            else:
                return field_value
        
        data_admissao = convert_date_field(document["data_admissao"], is_date_only=True)
        created_at = convert_date_field(document["created_at"], is_date_only=False)
        updated_at = convert_date_field(document.get("updated_at"), is_date_only=False)
        
        # Suporte a data_nascimento
        data_nascimento = None
        if document.get("data_nascimento"):
            data_nascimento = convert_date_field(document["data_nascimento"], is_date_only=True)
        
        # Criar instância do Funcionario
        # Suporte a ambos os nomes de campo para compatibilidade (nome antigo vs nome_completo novo)
        nome_completo = document.get("nome_completo") or document.get("nome")
        if not nome_completo:
            raise ValueError("Campo nome_completo ou nome é obrigatório")
            
        # Converter salário com suporte a string e número
        salario = None
        if document.get("salario") is not None:
            try:
                salario = Decimal(str(document["salario"]))
            except (ValueError, TypeError):
                salario = None
        
        funcionario = Funcionario(
            nome_completo=nome_completo,
            email=email,
            cargo=cargo,
            data_admissao=data_admissao,
            telefone=telefone,
            departamento=document.get("departamento"),
            salario=salario,
            ativo=document.get("ativo", document.get("ativo", True)),
            created_at=created_at,
            updated_at=updated_at
        )
        
        # Definir campos adicionais apenas se existirem no documento E na entidade
        if document.get("cpf") and hasattr(funcionario, 'cpf'):
            setattr(funcionario, 'cpf', document["cpf"])
        
        if data_nascimento and hasattr(funcionario, 'data_nascimento'):
            setattr(funcionario, 'data_nascimento', data_nascimento)
        
        # Definir ID se existir
        if "_id" in document:
            funcionario.id = str(document["_id"])
        
        return funcionario
    
    @staticmethod
    def to_update_document(
        funcionario: Funcionario,
        campos_permitidos: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Converte entidade para documento de atualização (apenas campos modificáveis).
        
        Args:
            funcionario: Instância da entidade Funcionario
            campos_permitidos: Lista de campos que podem ser atualizados
            
        Returns:
            Dict com operadores de atualização do MongoDB
        """
        if campos_permitidos is None:
            # Campos que podem ser atualizados (email e data_admissao são imutáveis)
            campos_permitidos = [
                "nome", "cargo", "telefone", "departamento", "salario",
                "ativo", "updated_at"
            ]
        
        set_operations = {}
        unset_operations = {}
        
        # Campos obrigatórios que podem ser atualizados
        if "nome" in campos_permitidos or "nome_completo" in campos_permitidos:
            set_operations["nome_completo"] = funcionario.nome_completo  # Usar nome_completo consistentemente
        
        if "cargo" in campos_permitidos:
            set_operations["cargo"] = funcionario.cargo.value
        
        if "ativo" in campos_permitidos:
            set_operations["ativo"] = funcionario.ativo
        
        # Campo de atualização sempre deve ser definido
        if "updated_at" in campos_permitidos:
            set_operations["updated_at"] = funcionario.updated_at if funcionario.updated_at else datetime.now()  # Date, não string
        
        # Campos opcionais
        if "telefone" in campos_permitidos:
            if funcionario.telefone:
                set_operations["telefone"] = funcionario.telefone.value
            else:
                unset_operations["telefone"] = ""
        
        if "departamento" in campos_permitidos:
            if funcionario.departamento:
                set_operations["departamento"] = funcionario.departamento
            else:
                unset_operations["departamento"] = ""
        
        if "salario" in campos_permitidos:
            if funcionario.salario is not None:
                set_operations["salario"] = float(funcionario.salario)
            else:
                unset_operations["salario"] = ""
        
        # Construir documento de update
        update_doc = {}
        
        if set_operations:
            update_doc["$set"] = set_operations
        
        if unset_operations:
            update_doc["$unset"] = unset_operations
        
        return update_doc
    
    @staticmethod
    def validate_document(document: Dict[str, Any]) -> bool:
        """
        Valida se um documento MongoDB está no formato esperado.
        
        Args:
            document: Documento do MongoDB
            
        Returns:
            True se válido, False caso contrário
        """
        required_fields = [
            "email", "cargo", "data_admissao", 
            "ativo", "created_at"
        ]
        
        # Verificar campos obrigatórios
        for field in required_fields:
            if field not in document:
                return False
                
        # Nome pode ser "nome" (formato antigo) ou "nome_completo" (formato novo)
        if not (document.get("nome") or document.get("nome_completo")):
            return False
        
        # Verificar tipos básicos
        nome_field = document.get("nome_completo") or document.get("nome")
        if not isinstance(nome_field, str):
            return False
        
        if not isinstance(document["email"], str):
            return False
        
        if not isinstance(document["cargo"], str):
            return False
        
        if not isinstance(document["ativo"], bool):
            return False
        
        # Verificar formato de datas (ISO format ou datetime)
        try:
            # Verificar data_admissao
            if isinstance(document["data_admissao"], str):
                datetime.fromisoformat(document["data_admissao"])
            elif not isinstance(document["data_admissao"], (datetime, date)):
                return False
                
            # Verificar created_at
            if isinstance(document["created_at"], str):
                datetime.fromisoformat(document["created_at"])
            elif not isinstance(document["created_at"], datetime):
                return False
            
            # Verificar updated_at se existe
            if document.get("updated_at"):
                if isinstance(document["updated_at"], str):
                    datetime.fromisoformat(document["updated_at"])
                elif not isinstance(document["updated_at"], datetime):
                    return False
        except ValueError:
            return False
        
        # Verificar campos opcionais se existirem
        if "telefone" in document and not isinstance(document["telefone"], str):
            return False
        
        if "departamento" in document and not isinstance(document["departamento"], str):
            return False
        
        return True
    
    @staticmethod
    def get_projection_fields() -> Dict[str, int]:
        """
        Retorna os campos de projeção padrão para queries otimizadas.
        
        Returns:
            Dict com campos de projeção
        """
        return {
            "_id": 1,
            "nome_completo": 1,  # Usar nome_completo consistentemente
            "nome": 1,  # Manter compatibilidade com dados antigos
            "email": 1,
            "cargo": 1,
            "data_admissao": 1,
            "telefone": 1,
            "departamento": 1,
            "cpf": 1,
            "data_nascimento": 1,
            "salario": 1,
            "ativo": 1,
            "created_at": 1,
            "updated_at": 1
        }
    
    @staticmethod
    def get_summary_projection() -> Dict[str, int]:
        """
        Retorna projeção para listagem resumida (sem todos os campos).
        
        Returns:
            Dict com campos básicos
        """
        return {
            "_id": 1,
            "nome_completo": 1,  # Usar nome_completo consistentemente
            "nome": 1,  # Manter compatibilidade
            "email": 1,
            "cargo": 1,
            "departamento": 1,
            "ativo": 1
        }
