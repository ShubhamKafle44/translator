from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"),name ="static")

templates = Jinja2Templates(directory = "templates")

@app.get('/', response_class = HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})