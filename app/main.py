from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app import schemas
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db, engine, SessionLocal
from typing import List
from app import models
from app import utils
import uuid
models.Base.metadata.create_all(bind = engine)
app = FastAPI()



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get('/', response_class = HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/translate')
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task =  crud.create_translation_task(db, request.text, request.languages)
    print(task)
    background_tasks.add_task(utils.perform_translation, task.id, request.text, request.languages, db)
    return {"task_id": {task.id}}

@app.get('/translate/{task_id}', response_model= schemas.TranslationStatus)
def get_translate(task_id: int, db: Session = Depends(get_db)):
    task =  crud.get_translation_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail= "task not found")
    return {"task_id": {task_id}, "status": task.status, "translation" : task.translation}



@app.get('/translate/content/{task_id}')
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    task =  crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail= "task not found")
    return task