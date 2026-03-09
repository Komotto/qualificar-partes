from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

LOCK_FILE = "/tmp/process.lock"
ROOT_SCRIPT = "/app/datawarehouse/scripts/ia-qualificarpartes/root.sh"
SCRIPT_DIR = "/app/datawarehouse/scripts/ia-qualificarpartes"

@app.get("/ping")
def ping():
    return {"message": "ativa"}

@app.get("/")
def health():
    return {"status": "API ativa"}

@app.post("/executar")
def executar():
    if os.path.exists(LOCK_FILE):
        return {"status": "Processo já em execução"}

    open(LOCK_FILE, "w").close()

    try:
        subprocess.run(
    ["bash", ROOT_SCRIPT],
    cwd="/app/datawarehouse/scripts/ia-qualificarpartes",
    check=True
    )
    except subprocess.CalledProcessError as e:
        return {"erro": str(e)}
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

    return {"status": "Processo finalizado"}
