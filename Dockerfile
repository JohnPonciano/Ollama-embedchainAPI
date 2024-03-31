# Use a imagem oficial do Python como base
FROM python:3.9

# Instale o git
RUN apt-get update && apt-get install -y git

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Clona o repositório do Git na branch homologacao
RUN git clone --single-branch --branch homologacao https://github.com/JohnPonciano/Ollama-embedchainAPI.git .
# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta em que a sua API vai rodar
EXPOSE 8000

# Comando para executar a sua aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
