from pathlib import Path

from engine.app import App
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from seamless import render
from seamless.extra.transports.socketio.middleware import SocketIOMiddleware

HERE = Path(__file__).parent


app = FastAPI()
app.add_middleware(SocketIOMiddleware)


@app.get("/static/{file_path:path}")
def read_static(file_path: str):
    return FileResponse(HERE / "static" / file_path)


@app.get("/{full_path:path}", response_class=HTMLResponse)
def read_root():
    return render(App())
