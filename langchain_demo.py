"""
W3D1: LangChain 基础入门
用前端开发者的视角理解 LangChain
"""

# ========== 1. LLM (类比 axios.create 创建实例) ==========
# LLM = Large Language Model, LangChain 对它的封装
# 类比前端: 就像 axios.create({ baseURL, headers }) 创建的请求实例

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="sk-rykwqcswnxdbhynbbtnlvcovysldjumrgeqrmvcaadexgjao",  # 硅基流动 key
    base_url="https://api.siliconflow.cn/v1",  # 硅基流动地址
    model="Qwen/Qwen3-VL-32B-Instruct",  # 模型名称
    temperature=0.7,  # 创造性参数: 0=保守, 1=随机
)

# 简单调用 (非流式)
print("=== 1. Simple LLM Call ===")
response = llm.invoke("Say hello in one short sentence")
print(f"Reply: {response.content}")
print()


# ========== 2. Prompt Template (类比 Vue 模板 {{ }}) ==========
# Prompt Template = 带变量的提示词模板
# 类比前端: 就像 Vue 的 `<template>Hello {{ name }}</template>`

from langchain_core.prompts import ChatPromptTemplate

# 定义模板 (使用 {variable} 占位)
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}. Answer questions clearly."),
    ("human", "{question}"),
])

# 填充变量 (类比 Vue 的 v-bind 传值)
print("=== 2. Prompt Template ===")
prompt = template.format_messages(
    role="Python teacher",
    question="What is list comprehension?"
)
print("Generated Prompt messages:")
for msg in prompt:
    print(f"  [{msg.type}] {msg.content}")
print()

# 用 LLM 执行
response = llm.invoke(prompt)
print(f"AI Reply: {response.content[:100]}...")  # 只显示前100字符
print()


# ========== 3. Chain (类比函数组合 / Promise 链) ==========
# Chain = 把多个步骤链接起来, 形成处理流水线
# 类比前端: 就像 `.then().then()` 或者函数式编程的 `compose`

# 新版 LangChain 推荐使用 LCEL 写法 (LangChain Expression Language)
print("=== 3. Chain (LCEL Style) ===")

# 用管道符 `|` 连接组件 (类似 Unix 管道或函数组合)
chain = template | llm

# 执行 (invoke 是统一的调用方式)
result = chain.invoke({
    "role": "career advisor",
    "question": "How to learn AI development?"
})

print(f"Chain Result: {result.content[:100]}...")
print()


# ========== 4. 输出格式化 ==========
# 可以用 StrOutputParser 把 AIMessage 转成纯字符串

from langchain_core.output_parsers import StrOutputParser

print("=== 4. With Output Parser ===")

# 完整的链: template -> llm -> parser
full_chain = template | llm | StrOutputParser()

# 执行后得到纯字符串, 不是 AIMessage 对象
result = full_chain.invoke({
    "role": "technical interviewer",
    "question": "What is RAG in AI?"
})

print(f"Result (string): {result[:100]}...")
print()

print("=== All examples completed! ===")
