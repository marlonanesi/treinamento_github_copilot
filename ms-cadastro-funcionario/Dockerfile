# Stage 1: builder (usado para desenvolvimento e cache de dependências)
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências de compilação + certificações
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ ca-certificates && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências (incluindo uvicorn p/ rodar no dev)
COPY requirements/ /tmp/requirements/
RUN pip install --no-cache-dir -r /tmp/requirements/base.txt \
    && pip install --no-cache-dir uvicorn[standard]==0.24.0

# Copia código da aplicação
COPY app/ ./app/
COPY main.py ./
COPY requirements.txt ./

# Criar usuário para não rodar como root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser && \
    mkdir -p /app/logs && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

# Stage 2: runtime (produção)
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Dependências mínimas para rodar
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*

# Instala apenas as libs do base.txt
COPY requirements/ /tmp/requirements/
RUN pip install --no-cache-dir -r /tmp/requirements/base.txt

# Copia apenas o código necessário
COPY app/ ./app/
COPY main.py ./
COPY requirements.txt ./

# Usuário não root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser && \
    mkdir -p /app/logs && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

# Healthcheck simples
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import http.client as h;c=h.HTTPConnection('localhost',8000,timeout=5);c.request('GET','/health');r=c.getresponse(); exit(0 if r.status==200 else 1)"

# Comando padrão de execução em produção
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
