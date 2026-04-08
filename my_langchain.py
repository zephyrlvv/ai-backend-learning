from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    api_key="sk-rykwqcswnxdbhynbbtnlvcovysldjumrgeqrmvcaadexgjao",
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-VL-32B-Instruct",
    temperature=0.7,
)

# response = llm.invoke(f"hello,what's your name?")
# print(response.content)

template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，回答要{style}"),
        ("human", "{question}"),
    ]
)

filled_prompt = template.format_messages(
    role="Python 老师", style="通俗易懂", question="什么是函数？"
)


# response = llm.invoke(filled_prompt)
# print(response.content)


chain = template | llm | StrOutputParser()
result = chain.invoke(
    {"role": "JavaScript专家", "style": "严谨", "question": "async/await 是什么？"}
)
print(result)
