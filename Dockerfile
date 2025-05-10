# Dockerfile para Site_utilidades
FROM python:3.12-slim

# Instala o uv (gerenciador de dependências)
RUN pip install --upgrade pip && pip install uv

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências e código
COPY pyproject.toml ./
COPY . .

# Instala dependências
RUN uv venv && uv sync

# Define variável de ambiente para evitar buffer no output
ENV PYTHONUNBUFFERED=1

# Comando padrão para rodar o app
CMD ["uv", "run", "python", "app.py"]
