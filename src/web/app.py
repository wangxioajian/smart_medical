import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from configuration.config import *
from web.schemas import   *
from service import ChatService

app = FastAPI()
app.mount("/static", StaticFiles(directory=WEB_STATIC_DIR), name="static")

service = ChatService()

@app.get("/")
def read_root():
    return RedirectResponse("/static/index.html")

@app.post("/chat")
def read_item(question: Question) -> Answer:
    result = service.chat(question)
    return Answer(message=result)

if __name__ == "__main__":
    uvicorn.run('web.app:app', host="0.0.0.0", port=8000)