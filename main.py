from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import secrets
import string
import random

app = FastAPI()

# Carpeta static para imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def crear_contrasena(longitud=12):
    mayus = string.ascii_uppercase
    minus = string.ascii_lowercase
    numeros = string.digits
    simbolos = string.punctuation

    password = [
        secrets.choice(mayus),
        secrets.choice(minus),
        secrets.choice(numeros),
        secrets.choice(simbolos)
    ]

    todos = mayus + minus + numeros + simbolos

    for _ in range(longitud - 4):
        password.append(secrets.choice(todos))

    random.shuffle(password)
    return ''.join(password)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/generar")
def generar(longitud: int = 12):
    if longitud < 4:
        return {"password": "La longitud mínima es 4"}
    return {"password": crear_contrasena(longitud)}