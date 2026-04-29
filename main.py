from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import secrets
import string
import random
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ---------------- GENERADOR ----------------
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

# ---------------- EVALUAR ----------------
def evaluar_contrasena(password):
    score = 0
    sugerencias = []

    # 🔥 SCORE (nivel)
    if len(password) >= 13:
        score += 2
    elif len(password) >= 9:
        score += 1

    if any(c.isupper() for c in password):
        score += 1
    else:
        sugerencias.append("Agregar mayúsculas")

    if any(c.islower() for c in password):
        score += 1
    else:
        sugerencias.append("Agregar minúsculas")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        sugerencias.append("Agregar números")

    if any(c in string.punctuation for c in password):
        score += 1
    else:
        sugerencias.append("Agregar símbolos")

    # 🔥 SUGERENCIA DE LONGITUD (separada del score)
    if len(password) < 12:
        sugerencias.append("Aumentar longitud (mínimo 12)")

    return score, sugerencias

# ---------------- MEJORAR ----------------
def mejorar_contrasena(password):
    nueva = list(password)

    if not any(c.isupper() for c in nueva):
        nueva.append(secrets.choice(string.ascii_uppercase))

    if not any(c.islower() for c in nueva):
        nueva.append(secrets.choice(string.ascii_lowercase))

    if not any(c.isdigit() for c in nueva):
        nueva.append(secrets.choice(string.digits))

    if not any(c in string.punctuation for c in nueva):
        nueva.append(secrets.choice(string.punctuation))

    while len(nueva) < 12:
        nueva.append(secrets.choice(string.ascii_letters + string.digits + string.punctuation))

    random.shuffle(nueva)
    return ''.join(nueva)

# ---------------- RUTAS ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get("/generar")
def generar(longitud: int = 12):
    if longitud < 4:
        return {"password": "La longitud mínima es 4"}
    return {"password": crear_contrasena(longitud)}

@app.get("/evaluar")
def evaluar(password: str):
    score, sugerencias = evaluar_contrasena(password)
    return {"score": score, "sugerencias": sugerencias}

@app.get("/mejorar")
def mejorar(password: str):
    nueva = mejorar_contrasena(password)
    return {"password_mejorada": nueva}