# Dockerfile para Site_utilidades
FROM python:3.12-slim

# Instala o uv (gerenciador de dependências)
RUN pip install --upgrade pip && pip install uv

# Cria diretório de trabalho
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY pyproject.toml ./

# Instala dependências antes de copiar o restante do código
RUN uv sync

# Agora copia o restante do código
COPY . .

# Define variável de ambiente para evitar buffer no output
ENV PYTHONUNBUFFERED=1

# Expondo a porta padrão do Streamlit
EXPOSE 8501

# Comando padrão para rodar o Streamlit
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
