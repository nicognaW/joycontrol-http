import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .Command import Command

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.18.132",
]

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/restart")
@app.post("/api/restart")
async def restart():
    from joycontrol_http import q, isServerRunning
    q.put(Command("main", "restart"))
    return {"q": q.qsize(), "isServerRunning": isServerRunning}


@app.post("/api/btn")
@app.get("/api/btn")
async def btn(btn_name, mode="push"):
    from joycontrol_http import controller_state
    logging.debug(f"以[{mode}]模式操作按钮 [{btn_name}]")
    logging.debug(controller_state)
