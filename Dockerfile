# Imagem base leve do Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas os arquivos necessários inicialmente (para cache otimizado)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Dá permissão de execução ao entrypoint
# Copia e garante permissão + corrige CRLF do entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod 755 /app/entrypoint.sh \
    && sed -i 's/\r$//' /app/entrypoint.sh

# Expõe a porta da API (default do uvicorn)
EXPOSE 8000

# Define o entrypoint para rodar Alembic + seed + API
ENTRYPOINT ["./entrypoint.sh"]
