from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, List, Optional

import time, random
from openai import OpenAI
from typing import Iterator

app = FastAPI()

# 关键：允许 Vue 前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue 的地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/search")
def searchFn(*filters: str) -> dict[str, Any]:
    filter_dict = {}
    for i, filterParams in enumerate(filters):
        if "=" in filterParams:
            key, value = filterParams.split("=", 1)
            filter_dict[key] = value
        else:
            filter_dict[f"filter_{i}"] = filterParams
    print("----------", filter_dict)
    return {"filters": filter_dict}


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


# ========== 模拟数据库 ==========
todos_db: List[Todo] = [
    Todo(id=1, title="学习 FastAPI", completed=False),
    Todo(id=2, title="完成 Vue 联调", completed=True),
]
next_id = 3


@app.get("/todos")
def get_todos():
    """获取待办"""
    return todos_db


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """获取个人待办"""
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="待办事项不存在")


@app.post("/todos")
def create_todo(data: TodoCreate):
    """创建待办"""
    global next_id
    new_todo = Todo(id=next_id, title=data.title)
    todos_db.append(new_todo)
    next_id += 1
    return new_todo


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate):
    """更新待办"""
    for todo in todos_db:
        if todo.id == todo_id:
            if data.title is not None:
                todo.title = data.title
            if data.completed is not None:
                todo.completed = data.completed
            return todo
    raise HTTPException(status_code=404, detail="待办事项不存在")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """删除待办"""
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            deleted = todos_db.pop(index)
            return {"message": "删除成功", "todo": deleted}
    raise HTTPException(status_code=404, detail="待办事项不存在")


@app.get("/stream")
def stream():
    def generate():
        text = "这是流式输出效果"
        for char in text:
            yield f"data:{char}\n\n"  # SSE 格式要求
            time.sleep(0.05)  # 每个字延迟 50ms

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/chat/stream")
def chat_stream(msg: str):
    """模拟ai回复"""

    def generate():
        responses = [
            f"收到你的消息：{msg}。这是一个很有意思的问题！",
            f"关于「{msg}」，我的看法是这样的...",
            f"你提到了{msg}，让我深入思考一下...",
        ]
        response = random.choice(responses)

        # 逐字返回
        for char in response:
            yield f"data:{char}\n\n"
            time.sleep(0.03)
        yield "data:[DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


# 硅基流动配置
client = OpenAI(
    api_key="sk-rykwqcswnxdbhynbbtnlvcovysldjumrgeqrmvcaadexgjao",  # 从硅基流动控制台复制
    base_url="https://api.siliconflow.cn/v1",  # 硅基流动的接口地址
)


@app.get("/chat/ai")
def chat_ai(msg: str):
    def generate() -> Iterator[str]:
        try:
            res = client.chat.completions.create(
                model="Qwen/Qwen3-VL-32B-Instruct",
                messages=[{"role": "user", "content": msg}],
                stream=True,
            )
            for chunk in res:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    yield f"data:{text}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
