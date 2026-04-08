from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Any, List, Optional

from dotenv import load_dotenv
import os

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

# 定义 Prompt 模板
langchain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. Answer in a friendly and concise way.",
        ),
        ("human", "{input}"),
    ]
)

# 创建 Chain: template -> llm -> parser
langchain_chain = langchain_prompt | langchain_llm | StrOutputParser()


@app.get("/chat/ai")
def chat_ai(msg: str, session_id: str = "default"):
    # 保存用户对话记录
    add_message("user", msg, session_id)

    def generate() -> Iterator[str]:
        try:
            history = get_messages(session_id, limit=20)
            # print('message---------',history)
            res = client.chat.completions.create(
                model="Qwen/Qwen3-VL-32B-Instruct",
                messages=history,
                stream=True,
                max_tokens=2048,
            )
            assistant_reply = ""
            for chunk in res:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    assistant_reply += text
                    yield f"data:{text}\n\n"
                    add_message("assistant", assistant_reply, session_id)
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/chat/clear")
def clear_history(session_id: str = "default"):
    clear_messages(session_id)
    return {"message": "对话历史已清空"}


# ========== LangChain 接口 ==========
@app.get("/chat/langchain")
def chat_langchain(msg: str):
    """
    使用 LangChain 的简化接口（非流式）
    演示 Chain 的基本用法
    """
    try:
        # 调用 Chain（自动完成：填充模板 -> 调用 LLM -> 解析输出）
        result = langchain_chain.invoke({"input": msg})
        return {"success": True, "message": result, "framework": "LangChain"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/chat/langchain/stream")
def chat_langchain_stream(msg: str):
    """
    使用 LangChain 的流式接口
    演示流式输出
    """
    from langchain_core.callbacks import StreamingStdOutCallbackHandler

    def generate():
        try:
            # LangChain 的流式需要特殊处理
            # 这里我们直接用底层接口实现流式
            for chunk in langchain_chain.stream({"input": msg}):
                yield f"data:{chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


my_template = ChatPromptTemplate.from_messages(
    [("system", "你是一个{role},回答风格是{style}"), ("human", "{msg}")]
)
my_chain = my_template | langchain_llm | StrOutputParser()


@app.get("/chat/myai")
def my_ai_interface(msg: str, role: str = "ai助手", style: str = "严谨"):
    try:
        res = my_chain.invoke({"role": role, "msg": msg, "style": style})
        return {"success": True, "message": res}
    except Exception as e:
        return {"success": False, "err": str(e)}


memory_store = {}


def get_memory_history(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ChatMessageHistory()
    return memory_store[session_id]


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
