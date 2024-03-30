# Use a imagem oficial do Python como base
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python usando o pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código fonte para o diretório de trabalho
COPY . .

# Exponha a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["sh", "-c", "if [ \"$BRANCH\" = \"main\" ]; then uvicorn api:app --host 0.0.0.0 --port 8000; else echo 'Running in homologation mode'; fi"]
