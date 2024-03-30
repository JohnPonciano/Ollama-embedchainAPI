# Use a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências usando pip
RUN pip install -r requirements.txt

# Copie o restante do código-fonte para o diretório de trabalho
COPY . .

# Exponha a porta em que a sua API vai rodar
EXPOSE 8000

# Comando para executar a sua aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
