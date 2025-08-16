"""
Sistema de logging estruturado para o microserviço.

Este módulo fornece configurações avançadas de logging com suporte a JSON,
contexto de requisição e diferentes níveis de verbosidade para diferentes
ambientes.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from app.infrastructure.config.settings import get_settings


class JSONFormatter(logging.Formatter):
    """
    Formatter personalizado para logs em formato JSON.
    
    Converte LogRecord em JSON estruturado para melhor
    análise em ferramentas de observabilidade.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formata registro de log como JSON.
        
        Args:
            record: Registro de log do Python
            
        Returns:
            str: Log formatado como JSON
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "process": record.process
        }
        
        # Adicionar contexto extra se disponível
        if hasattr(record, 'correlation_id'):
            log_entry['correlation_id'] = record.correlation_id
            
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
            
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
            
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
            
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
            
        if hasattr(record, 'duration_ms'):
            log_entry['duration_ms'] = record.duration_ms
            
        # Adicionar informações de exceção
        if record.exc_info:
            log_entry['exception'] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
            
        # Adicionar stack info se disponível
        if record.stack_info:
            log_entry['stack_info'] = record.stack_info
            
        return json.dumps(log_entry, ensure_ascii=False)


class StructuredFormatter(logging.Formatter):
    """
    Formatter estruturado para desenvolvimento.
    
    Mais legível que JSON para desenvolvimento local,
    mas ainda mantém informações estruturadas.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formata registro com estrutura legível.
        
        Args:
            record: Registro de log
            
        Returns:
            str: Log formatado estruturado
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        base_format = (
            f"[{timestamp}] "
            f"{record.levelname:8} "
            f"{record.name:20} "
            f"| {record.getMessage()}"
        )
        
        # Adicionar contexto se disponível
        context_parts = []
        
        if hasattr(record, 'correlation_id'):
            context_parts.append(f"correlation_id={record.correlation_id}")
            
        if hasattr(record, 'endpoint'):
            context_parts.append(f"endpoint={record.endpoint}")
            
        if hasattr(record, 'method'):
            context_parts.append(f"method={record.method}")
            
        if hasattr(record, 'status_code'):
            context_parts.append(f"status={record.status_code}")
            
        if hasattr(record, 'duration_ms'):
            context_parts.append(f"duration={record.duration_ms}ms")
            
        if context_parts:
            base_format += f" [{', '.join(context_parts)}]"
            
        # Adicionar informações de localização em debug
        if record.levelno == logging.DEBUG:
            base_format += f" ({record.module}:{record.funcName}:{record.lineno})"
            
        return base_format


def setup_logging() -> None:
    """
    Configura o sistema de logging da aplicação.
    
    Define handlers, formatters e níveis baseados no
    ambiente de execução (development/production).
    """
    settings = get_settings()
    
    # Configurar logger raiz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remover handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Criar handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Escolher formatter baseado no ambiente
    if settings.is_production():
        # Produção: JSON estruturado
        formatter = JSONFormatter()
        console_handler.setLevel(logging.INFO)  # Mínimo INFO em produção
    else:
        # Desenvolvimento: formato legível
        formatter = StructuredFormatter()
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Configurar loggers específicos
    configure_specific_loggers(settings)
    
    # Log inicial de configuração
    logger = logging.getLogger(__name__)
    logger.info(
        "Sistema de logging configurado",
        extra={
            "log_level": settings.LOG_LEVEL,
            "environment": settings.ENVIRONMENT,
            "formatter": "JSON" if settings.is_production() else "Structured"
        }
    )


def configure_specific_loggers(settings) -> None:
    """
    Configura loggers específicos para bibliotecas externas.
    
    Args:
        settings: Configurações da aplicação
    """
    # FastAPI/Uvicorn
    logging.getLogger("uvicorn.access").setLevel(
        logging.INFO if settings.is_development() else logging.WARNING
    )
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Motor (MongoDB driver)
    logging.getLogger("motor").setLevel(
        logging.INFO if settings.is_development() else logging.WARNING
    )
    
    # Pymongo
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    
    # Pydantic
    logging.getLogger("pydantic").setLevel(logging.WARNING)
    
    # Outros
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Factory para obter logger configurado.
    
    Args:
        name: Nome do logger (geralmente __name__)
        
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Adapter para adicionar contexto automaticamente aos logs.
    
    Útil para manter contexto de requisição ao longo
    do processamento.
    """
    
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        """
        Inicializa adapter com contexto.
        
        Args:
            logger: Logger base
            context: Contexto a ser adicionado
        """
        super().__init__(logger, context)
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """
        Processa mensagem adicionando contexto.
        
        Args:
            msg: Mensagem de log
            kwargs: Argumentos do log
            
        Returns:
            tuple: Mensagem e kwargs processados
        """
        # Adicionar contexto ao extra
        extra = kwargs.get('extra', {})
        extra.update(self.extra)
        kwargs['extra'] = extra
        
        return msg, kwargs


def create_request_logger(
    correlation_id: Optional[str] = None,
    request_id: Optional[str] = None,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    user_id: Optional[str] = None
) -> LoggerAdapter:
    """
    Cria logger com contexto de requisição.
    
    Args:
        correlation_id: ID de correlação
        request_id: ID da requisição
        endpoint: Endpoint chamado
        method: Método HTTP
        user_id: ID do usuário (se autenticado)
        
    Returns:
        LoggerAdapter: Logger com contexto
    """
    base_logger = get_logger("request")
    
    context = {}
    if correlation_id:
        context['correlation_id'] = correlation_id
    if request_id:
        context['request_id'] = request_id
    if endpoint:
        context['endpoint'] = endpoint
    if method:
        context['method'] = method
    if user_id:
        context['user_id'] = user_id
        
    return LoggerAdapter(base_logger, context)


# Inicializar sistema de logging ao importar
setup_logging()
