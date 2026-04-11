from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, List, Optional

from dotenv import load_dotenv
import os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 加载 .env 文件
load_dotenv()
# 读取环境变量
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = os.getenv("SILICONFLOW_BASE_URL")
# 如果读取失败，给出提示
if not API_KEY:
    raise ValueError("请在 .env 文件里设置 SILICONFLOW_API_KEY")

import time, random
from openai import OpenAI
from typing import Iterator

from database import init_db, add_message, get_messages, clear_messages

# ========== LangChain 导入 ==========
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

app = FastAPI()
init_db()

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


# 硅基流动配置
client = OpenAI(
    api_key=API_KEY,  # 从硅基流动控制台复制
    base_url=BASE_URL,  # 硅基流动的接口地址
)

# ========== LangChain 配置 ==========
# 初始化 LLM（硅基流动兼容 OpenAI 接口）
langchain_llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="Qwen/Qwen3-VL-32B-Instruct",
    temperature=0.7,
)

memory_store = {}


class PersistentChatMessageHistory(BaseChatMessageHistory):
    """
    自定义持久化聊天历史
    - 继承 BaseChatMessageHistory 接口
    - 使用 SQLite 存储（W2 的 database.py）
    """

    def __init__(self, session_id: str):
        self.session_id = session_id

    @property
    def messages(self):
        """读取历史消息（从数据库）"""
        rows = get_messages(self.session_id, limit=50)

        # 转换成 LangChain 的 Message 对象
        messages = []
        for row in rows:
            if row["role"] == "user":
                messages.append(HumanMessage(content=row["content"]))
            elif row["role"] == "assistant":
                messages.append(AIMessage(content=row["content"]))
        return messages

    def add_message(self, message):
        """添加消息（保存到数据库）"""
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            role = "unknown"
        add_message(role, message.content, self.session_id)

    def clear(self):
        """清空历史"""
        clear_messages(self.session_id)


def get_memory_history(session_id: str):
    return PersistentChatMessageHistory(session_id)


memory_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个 helpful 的 AI 助手，记住用户的信息"),
        MessagesPlaceholder(variable_name="history"),  # 历史消息插入这里
        ("human", "{input}"),
    ]
)

memory_chain = memory_prompt | langchain_llm | StrOutputParser()

# 包装成带 Memory 的 Chain
memory_conversation = RunnableWithMessageHistory(
    memory_chain,
    get_memory_history,
    input_messages_key="input",
    history_messages_key="history",
)


@app.get("/chat/memory")
def chat_with_memory(msg: str, session_id: str = "default"):
    """非流式 Memory 接口"""
    try:
        response = memory_conversation.invoke(
            {"input": msg}, config={"configurable": {"session_id": session_id}}
        )
        history = get_memory_history(session_id)
        return {
            "success": True,
            "msg": response,
            "session_id": session_id,
            "history_count": len(history.messages),
        }
    except Exception as e:
        return {"success": False, "msg": str(e)}


@app.get("/chat/memory/stream")
def chat_with_memory_stream(msg: str, session_id: str = "default"):
    def generate():
        try:
            for chunk in memory_conversation.stream(
                {"input": msg}, config={"configurable": {"session_id": session_id}}
            ):
                yield f"data:{chunk}\n\n"
            yield f"data:[done]\n\n"
        except Exception as e:
            yield f"errorInfo {e}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
