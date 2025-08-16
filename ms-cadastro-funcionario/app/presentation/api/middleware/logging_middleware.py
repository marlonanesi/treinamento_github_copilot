"""
Middleware de logging para requisições HTTP.

Este módulo implementa middleware que captura e loga informações
sobre requisições e respostas para debugging e monitoramento.
"""

import logging
import time
import uuid
from typing import Callable, Dict, Any, Optional
from datetime import datetime

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de requisições e respostas HTTP.
    
    Captura informações de timing, status codes, IPs de origem
    e outros dados relevantes para monitoramento.
    """
    
    def __init__(
        self,
        app,
        log_requests: bool = True,
        log_responses: bool = True,
        log_body: bool = False,
        log_headers: bool = False,
        exclude_paths: Optional[list] = None
    ):
        """
        Inicializa o middleware.
        
        Args:
            app: Aplicação FastAPI
            log_requests: Se deve logar requisições
            log_responses: Se deve logar respostas
            log_body: Se deve logar corpo das mensagens
            log_headers: Se deve logar headers
            exclude_paths: Paths a serem excluídos do log
        """
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_body = log_body
        self.log_headers = log_headers
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json", "/favicon.ico"]
        
        # Configurar logger específico
        self.request_logger = logging.getLogger("app.requests")
        self.response_logger = logging.getLogger("app.responses")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa requisição através do middleware.
        
        Args:
            request: Requisição HTTP
            call_next: Próximo middleware/endpoint
            
        Returns:
            Resposta HTTP processada
        """
        # Verificar se deve excluir este path
        if self._should_exclude_path(request.url.path):
            return await call_next(request)
        
        # Gerar correlation ID único para a requisição
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        
        # Iniciar timing
        start_time = time.time()
        
        # Logar requisição
        if self.log_requests:
            await self._log_request(request, correlation_id)
        
        # Processar requisição
        try:
            response = await call_next(request)
        except Exception as exc:
            # Logar erro
            processing_time = time.time() - start_time
            await self._log_error(request, exc, correlation_id, processing_time)
            raise
        
        # Calcular tempo de processamento
        processing_time = time.time() - start_time
        
        # Adicionar headers de tracking
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Processing-Time"] = f"{processing_time:.4f}s"
        
        # Logar resposta
        if self.log_responses:
            await self._log_response(request, response, correlation_id, processing_time)
        
        return response
    
    def _should_exclude_path(self, path: str) -> bool:
        """
        Verifica se o path deve ser excluído do log.
        
        Args:
            path: Path da requisição
            
        Returns:
            True se deve excluir
        """
        return any(excluded in path for excluded in self.exclude_paths)
    
    async def _log_request(self, request: Request, correlation_id: str):
        """
        Loga informações da requisição.
        
        Args:
            request: Requisição HTTP
            correlation_id: ID de correlação
        """
        # Informações básicas
        log_data = {
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "timestamp": datetime.utcnow().isoformat(),
            "event": "request_received"
        }
        
        # Headers se solicitado
        if self.log_headers:
            log_data["headers"] = dict(request.headers)
        
        # Body se solicitado (cuidado com dados sensíveis)
        if self.log_body:
            try:
                # Ler body apenas se não foi consumido
                if hasattr(request, "_body"):
                    body = request._body
                else:
                    body = await request.body()
                    request._body = body
                
                if body:
                    # Limitar tamanho do log do body
                    body_str = body.decode("utf-8")[:1000]  # Primeiros 1000 chars
                    log_data["body_preview"] = body_str
                    log_data["body_size"] = len(body)
            except Exception:
                log_data["body_error"] = "Could not read request body"
        
        self.request_logger.info("HTTP Request", extra=log_data)
    
    async def _log_response(
        self, 
        request: Request, 
        response: Response, 
        correlation_id: str,
        processing_time: float
    ):
        """
        Loga informações da resposta.
        
        Args:
            request: Requisição original
            response: Resposta HTTP
            correlation_id: ID de correlação
            processing_time: Tempo de processamento
        """
        log_data = {
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time_seconds": round(processing_time, 4),
            "response_size": self._get_response_size(response),
            "timestamp": datetime.utcnow().isoformat(),
            "event": "response_sent"
        }
        
        # Headers da resposta se solicitado
        if self.log_headers:
            log_data["response_headers"] = dict(response.headers)
        
        # Determinar nível de log baseado no status code
        if response.status_code >= 500:
            log_level = "error"
        elif response.status_code >= 400:
            log_level = "warning"
        else:
            log_level = "info"
        
        getattr(self.response_logger, log_level)("HTTP Response", extra=log_data)
    
    async def _log_error(
        self,
        request: Request,
        exception: Exception,
        correlation_id: str,
        processing_time: float
    ):
        """
        Loga erros durante o processamento.
        
        Args:
            request: Requisição original
            exception: Exceção ocorrida
            correlation_id: ID de correlação
            processing_time: Tempo até o erro
        """
        log_data = {
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "processing_time_seconds": round(processing_time, 4),
            "timestamp": datetime.utcnow().isoformat(),
            "event": "request_error"
        }
        
        self.request_logger.error("HTTP Request Error", extra=log_data, exc_info=True)
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Obtém IP do cliente considerando proxies.
        
        Args:
            request: Requisição HTTP
            
        Returns:
            IP do cliente
        """
        # Verificar headers de proxy
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # IP direto
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _get_response_size(self, response: Response) -> Optional[int]:
        """
        Obtém tamanho da resposta se disponível.
        
        Args:
            response: Resposta HTTP
            
        Returns:
            Tamanho em bytes ou None
        """
        content_length = response.headers.get("content-length")
        if content_length:
            try:
                return int(content_length)
            except ValueError:
                pass
        
        # Para StreamingResponse, não temos o tamanho
        if isinstance(response, StreamingResponse):
            return None
        
        # Tentar estimar do body se disponível
        if hasattr(response, "body") and response.body:
            return len(response.body)
        
        return None


class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware especializado em logging de performance.
    
    Foca em métricas de timing e identificação de endpoints lentos.
    """
    
    def __init__(
        self,
        app,
        slow_request_threshold: float = 1.0,  # segundos
        log_all_requests: bool = False
    ):
        """
        Inicializa middleware de performance.
        
        Args:
            app: Aplicação FastAPI
            slow_request_threshold: Threshold para requisições lentas
            log_all_requests: Se deve logar todas as requisições
        """
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.log_all_requests = log_all_requests
        self.performance_logger = logging.getLogger("app.performance")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa requisição focando em performance.
        
        Args:
            request: Requisição HTTP
            call_next: Próximo middleware/endpoint
            
        Returns:
            Resposta HTTP processada
        """
        start_time = time.perf_counter()
        
        # Processar requisição
        response = await call_next(request)
        
        # Calcular tempo
        processing_time = time.perf_counter() - start_time
        
        # Logar se requisição lenta ou se configurado para logar todas
        should_log = (
            processing_time > self.slow_request_threshold or 
            self.log_all_requests
        )
        
        if should_log:
            performance_data = {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "processing_time_seconds": round(processing_time, 6),
                "is_slow": processing_time > self.slow_request_threshold,
                "timestamp": datetime.utcnow().isoformat(),
                "event": "performance_metric"
            }
            
            log_level = "warning" if processing_time > self.slow_request_threshold else "info"
            message = f"{'SLOW REQUEST' if processing_time > self.slow_request_threshold else 'REQUEST'} - {processing_time:.4f}s"
            
            getattr(self.performance_logger, log_level)(message, extra=performance_data)
        
        # Adicionar header de timing
        response.headers["X-Processing-Time"] = f"{processing_time:.6f}"
        
        return response


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware para coleta de métricas básicas.
    
    Coleta estatísticas sobre requisições para monitoramento.
    """
    
    def __init__(self, app):
        """
        Inicializa middleware de métricas.
        
        Args:
            app: Aplicação FastAPI
        """
        super().__init__(app)
        self.metrics = {
            "total_requests": 0,
            "total_errors": 0,
            "total_processing_time": 0.0,
            "requests_by_method": {},
            "requests_by_status": {},
            "start_time": datetime.utcnow()
        }
        self.metrics_logger = logging.getLogger("app.metrics")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa requisição coletando métricas.
        
        Args:
            request: Requisição HTTP
            call_next: Próximo middleware/endpoint
            
        Returns:
            Resposta HTTP processada
        """
        start_time = time.time()
        
        # Processar requisição
        response = await call_next(request)
        
        # Calcular tempo
        processing_time = time.time() - start_time
        
        # Atualizar métricas
        self._update_metrics(request, response, processing_time)
        
        return response
    
    def _update_metrics(self, request: Request, response: Response, processing_time: float):
        """
        Atualiza métricas internas.
        
        Args:
            request: Requisição HTTP
            response: Resposta HTTP
            processing_time: Tempo de processamento
        """
        # Total de requisições
        self.metrics["total_requests"] += 1
        
        # Total de erros
        if response.status_code >= 400:
            self.metrics["total_errors"] += 1
        
        # Tempo total de processamento
        self.metrics["total_processing_time"] += processing_time
        
        # Por método
        method = request.method
        self.metrics["requests_by_method"][method] = (
            self.metrics["requests_by_method"].get(method, 0) + 1
        )
        
        # Por status
        status = response.status_code
        self.metrics["requests_by_status"][status] = (
            self.metrics["requests_by_status"].get(status, 0) + 1
        )
        
        # Log periódico (a cada 100 requisições)
        if self.metrics["total_requests"] % 100 == 0:
            self._log_metrics_summary()
    
    def _log_metrics_summary(self):
        """
        Loga resumo das métricas coletadas.
        """
        uptime = datetime.utcnow() - self.metrics["start_time"]
        avg_processing_time = (
            self.metrics["total_processing_time"] / self.metrics["total_requests"]
            if self.metrics["total_requests"] > 0 else 0
        )
        
        error_rate = (
            (self.metrics["total_errors"] / self.metrics["total_requests"]) * 100
            if self.metrics["total_requests"] > 0 else 0
        )
        
        metrics_summary = {
            "total_requests": self.metrics["total_requests"],
            "total_errors": self.metrics["total_errors"],
            "error_rate_percent": round(error_rate, 2),
            "average_processing_time": round(avg_processing_time, 4),
            "uptime_seconds": uptime.total_seconds(),
            "requests_by_method": self.metrics["requests_by_method"],
            "requests_by_status": self.metrics["requests_by_status"],
            "timestamp": datetime.utcnow().isoformat(),
            "event": "metrics_summary"
        }
        
        self.metrics_logger.info("Metrics Summary", extra=metrics_summary)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas atuais.
        
        Returns:
            Dict com métricas atuais
        """
        uptime = datetime.utcnow() - self.metrics["start_time"]
        avg_processing_time = (
            self.metrics["total_processing_time"] / self.metrics["total_requests"]
            if self.metrics["total_requests"] > 0 else 0
        )
        
        return {
            **self.metrics,
            "uptime_seconds": uptime.total_seconds(),
            "average_processing_time": avg_processing_time,
            "current_time": datetime.utcnow().isoformat()
        }


# ==========================================
# CONFIGURAÇÃO DE LOGGING
# ==========================================

def setup_logging_middleware():
    """
    Configura loggers específicos para middleware.
    
    Returns:
        Dict com configurações de logging
    """
    # Configurar formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Configurar handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    
    # TODO: Adicionar file handler em produção
    
    # Configurar loggers
    loggers_config = [
        ("app.requests", logging.INFO),
        ("app.responses", logging.INFO), 
        ("app.performance", logging.WARNING),
        ("app.metrics", logging.INFO)
    ]
    
    for logger_name, level in loggers_config:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        logger.propagate = False  # Evitar duplicação
    
    return {
        "configured_loggers": [name for name, _ in loggers_config],
        "handlers": ["console"],
        "formatters": ["detailed", "simple"]
    }


# ==========================================
# FACTORY PARA MIDDLEWARE
# ==========================================

def create_logging_middleware(
    log_requests: bool = True,
    log_responses: bool = True,
    log_performance: bool = True,
    collect_metrics: bool = True,
    **kwargs
):
    """
    Factory para criação de middleware de logging.
    
    Args:
        log_requests: Ativar log de requisições
        log_responses: Ativar log de respostas
        log_performance: Ativar log de performance
        collect_metrics: Ativar coleta de métricas
        **kwargs: Argumentos adicionais
        
    Returns:
        Lista de middleware configurados
    """
    middleware_list = []
    
    if collect_metrics:
        middleware_list.append(MetricsMiddleware)
    
    if log_performance:
        middleware_list.append(PerformanceLoggingMiddleware)
    
    if log_requests or log_responses:
        middleware_list.append(
            lambda app: LoggingMiddleware(
                app,
                log_requests=log_requests,
                log_responses=log_responses,
                **kwargs
            )
        )
    
    return middleware_list
