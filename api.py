from fastapi import FastAPI, File, HTTPException,UploadFile,Body
from embedchain import App
from pathlib import Path
from typing import List
import os
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set Hugging Face access token
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"

# Configurações
CONFIG_PATH = "config.yaml"
HOST = "0.0.0.0"
PORT = 8000
DOCUMENTS_DIR = "./docs"

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Função para carregar o aplicativo Embedchain
def get_embedchain_app():
    embedchain_app = App.from_config(config_path=CONFIG_PATH)
    return embedchain_app

embedchain_app = get_embedchain_app()

# Verifica se o diretório documentos existe e, se não, o cria
if not os.path.exists(DOCUMENTS_DIR):
    os.makedirs(DOCUMENTS_DIR)

# Classe de manipulador de eventos do sistema de arquivos
class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_created(self, event):
        # Se um arquivo for criado, adiciona ao Embedchain
        if not event.is_directory:
            embedchain_app.add(str(event.src_path), data_type="file")

# Função para adicionar diretório e iniciar monitoramento de alterações
def add_and_monitor_directory(dir_path):
    try:
        embedchain_app.add(str(dir_path), data_type="directory")

        # Inicia o observador para monitorar alterações no diretório
        observer = Observer()
        observer.schedule(MyHandler(), dir_path, recursive=True)
        observer.start()

        return {"message": f"Diretório '{dir_path}' adicionado com sucesso. Novas mudanças serão monitoradas."}
    except Exception as e:
        print(f"Erro ao adicionar diretório: {e}")
        return {"error": "Ocorreu um erro ao adicionar o diretório."}

# Rota para adicionar diretório e iniciar monitoramento de alterações
@app.post("/add/diretorio")
async def add_directory(path: str):
    dir_path = Path(path)
    if not dir_path.is_dir():
        return {"error": f"O caminho '{path}' não é um diretório válido."}
    
    return add_and_monitor_directory(dir_path)

# Rota para adicionar documentos ao diretório documentos
@app.post("/add/documentos")
async def add_documents(files: List[UploadFile] = File(...)):
    try:
        for file in files:
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension in {'.pdf', '.txt'}:
                file_path = os.path.join(DOCUMENTS_DIR, file.filename)
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                embedchain_app.add(file_path, data_type="pdf_file" if file_extension == '.pdf' else "text")
            else:
                print(f"Tipo de arquivo não suportado: {file.filename}")
        return {"message": f"{len(files)} documentos adicionados com sucesso ao diretório 'documentos'."}
    except Exception as e:
        print(f"Erro ao adicionar documentos: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao adicionar os documentos.")

    os.makedirs(DOCUMENTS_DIR)

# Rota para consulta
@app.post("/query")
async def query(data: dict = Body(...)):
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="O campo 'question' é obrigatório.")
    
    try:
        response = embedchain_app.query(question)
        return {"answer": response}
    except Exception as e:
        print(f"Erro durante a consulta: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao processar sua consulta.")

# Inicia o aplicativo FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
