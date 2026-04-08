from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatOpenAI(
    api_key="xxx",
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-VL-32B-Instruct",
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个 helpful 的 AI 助手，记住用户的信息"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
chain = prompt | llm
store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversation = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

print("=== 第1轮 ===")
res1 = conversation.invoke(
    {"input": "你好，我叫张三，是一名前端工程师"},
    config={"configurable": {"session_id": "user1"}},
)
print(res1.content)

print("\n=== 查看存储的历史消息 ===")
history = get_session_history("user1")
for msg in history.messages:
    print(f"[{msg.type}] {msg.content[:50]}...")
