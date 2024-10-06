from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from app.database import dropTable, createTable
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})


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
