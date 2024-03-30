#!/bin/bash

# Diretório onde o repositório será clonado
REPO_DIR="/caminho/para/repositorio"

# URL do repositório Git
REPO_URL="https://github.com/JohnPonciano/Ollama-embedchainAPI.git"

# Branch que será monitorada
BRANCH="homologacao"

# Verifica se o diretório do repositório existe, caso contrário, clona o repositório
if [ ! -d "$REPO_DIR" ]; then
    git clone -b $BRANCH $REPO_URL $REPO_DIR
fi

# Navega para o diretório do repositório
cd $REPO_DIR

# Faz pull das últimas alterações
git pull origin $BRANCH
