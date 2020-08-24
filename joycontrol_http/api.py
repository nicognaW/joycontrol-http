from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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
async def restart():
    from joycontrol_http import q, isServerRunning
    q.put({"msg": "restart"})
    return {"q": q.qsize(), "isServerRunning": isServerRunning}
