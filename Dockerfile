# Use a imagem oficial do Python como base
FROM python:3.11

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

# Instala o Git
RUN apt-get update && apt-get install -y git

# Copia o script para dentro do contêiner
COPY git_pull_script.sh /usr/local/bin/git_pull_script.sh

# Define o script como executável
RUN chmod +x /usr/local/bin/git_pull_script.sh

# Instala o cron
RUN apt-get update && apt-get install -y cron

# Copia o arquivo de cron para dentro do contêiner
COPY cronjob /etc/cron.d/cronjob

# Habilita o cron
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log

# Comando para iniciar o servidor Uvicorn
CMD ["python", "api.py"]
