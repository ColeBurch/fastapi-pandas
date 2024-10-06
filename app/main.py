from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from app.database import dropTable, createTable

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World!"}


@app.get("/initdb")
async def initdb():
    try:
        dropTable()
        createTable()
        return {"message": "Table dropped and created!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error {e}"
        )
