from fastapi import FastAPI, Body, UploadFile, File, HTTPException  # Adicione o HTTPException aqui
from uvicorn import run
from embedchain import App
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Set Hugging Face access token
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"

# Configurations
CONFIG_PATH = "config.yaml"
HOST = "0.0.0.0"
PORT = 8000
DOCUMENTS_DIR = "./documentos"

# Initialize FastAPI app
app = FastAPI()

# Function to load the Embedchain application
def get_embedchain_app():
    embedchain_app = App.from_config(config_path=CONFIG_PATH)
    return embedchain_app

embedchain_app = get_embedchain_app()

# Ensure that the documents directory exists
if not os.path.exists(DOCUMENTS_DIR):
    os.makedirs(DOCUMENTS_DIR)

# Router to add documents
@app.post("/add/documento")
async def add_document(file: UploadFile = File(...)):
    try:
        filename = file.filename
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        embedchain_app.add(file_path, data_type="file")
        return {"message": f"Documento '{filename}' adicionado com sucesso."}
    except Exception as e:
        print(f"Erro ao adicionar documento: {e}")
        return {"error": "Ocorreu um erro ao adicionar o documento."}

#directory (monitored)

async def add_directory(path: str = Body(...)):
    try:
        dir_path = Path(path)
        if not dir_path.is_dir():
            return {"error": f"O caminho '{path}' não é um diretório válido."}
        embedchain_app.add(str(dir_path), data_type="directory")
        return {"message": f"Diretório '{path}' adicionado com sucesso. Novas mudanças serão monitoradas."}
    except Exception as e:
        print(f"Erro ao adicionar diretório: {e}")
        return {"error": "Ocorreu um erro ao adicionar o diretório."}

# File system event handler
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        if file_path.parent != DOCUMENTS_DIR:
            return
        embedchain_app.add(str(file_path), data_type="file")
        print(f"Arquivo '{file_path.name}' adicionado ao Ollama.")

# File system observer to monitor the documents directory
observer = Observer()
observer.schedule(MyHandler(), DOCUMENTS_DIR, recursive=True)
observer.start()

# Router for querying
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

# Run the FastAPI app
if __name__ == "__main__":
    run(app, host=HOST, port=PORT)
