from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

LOCK_FILE = "/tmp/process.lock"
ROOT_SCRIPT = "/app/datawarehouse/scripts/ia-qualificarpartes/root.sh"
WORK_DIR = "/app/datawarehouse/scripts/ia-qualificarpartes"


@app.get("/ping")
def ping():
    return {"message": "ativo"}


@app.get("/")
def health():
    return {"status": "API ativa"}


@app.post("/executar")
def executar():

    if os.path.exists(LOCK_FILE):
        return {"status": "Processo já em execução"}

    open(LOCK_FILE, "w").close()

    try:
        result = subprocess.run(
            ["bash", ROOT_SCRIPT],
            cwd=WORK_DIR,
            capture_output=True,
            text=True
        )

        return {
            "status": "Processo finalizado",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.CalledProcessError as e:
        return {"erro": str(e)}

    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    try:
        subprocess.run(
            ["bash", ROOT_SCRIPT],
            cwd=WORK_DIR,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        return {"erro": str(e)}
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

    return {"status": "Processo finalizado"}
