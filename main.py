from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 关键：允许 Vue 前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue 的地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    msg: str
    userId: str = "randomId"


@app.post("/chat")
def chat_post(data: ChatRequest):
    return {"reply": f"当前id为{data.userId},另外推送消息{data.msg}", "method": "post"}


@app.get("/")
def hello():
    return {"message": "Hello, I'm your AI backend!"}


@app.get("/chat")
def chat(msg: str):
    return {"reply": f"你说了：{msg}", "backend": "Python"}
