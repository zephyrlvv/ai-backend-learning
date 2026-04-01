# W3：LangChain 基础（AI应用工程师核心技能）

**目标**：掌握行业标准框架 LangChain，构建专业的 AI 应用

---

## 什么是 LangChain？

**一句话**：LangChain 是构建大语言模型应用的 **JavaScript 框架**（类比 Vue/React 之于前端）。

**官方定位**：
> "LangChain is a framework for developing applications powered by language models."

**为什么学它**：
- ✅ 行业标准，招聘信息高频出现
- ✅ 解决手写字段拼接的痛点（Prompt管理、Memory、Chain）
- ✅ 生态丰富，集成 OpenAI/Anthropic/国产模型等

---

## W3 学习计划（3天）

### W3D1：LangChain 基础概念 + 安装

**核心概念**：
| 概念 | 类比 | 作用 |
|------|------|------|
| **LLM** | AI 模型实例 | 调用大模型的统一接口 |
| **Prompt Template** | Vue 模板字符串 | 管理提示词模板，支持变量插入 |
| **Chain** | 函数组合 | 将多个步骤链接成流水线 |

**安装**：
```bash
pip install langchain langchain-openai
```

**第一个程序**：
```python
from langchain import OpenAI, PromptTemplate, LLMChain

# 1. 初始化模型（硅基流动兼容 OpenAI 接口）
llm = OpenAI(
    api_key="你的key",
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-VL-32B-Instruct"
)

# 2. 定义 Prompt 模板（类比 Vue 模板）
template = """
你是一个友好的AI助手。

用户说：{user_input}

你的回复：
"""
prompt = PromptTemplate(
    input_variables=["user_input"],
    template=template
)

# 3. 创建 Chain（流水线）
chain = LLMChain(llm=llm, prompt=prompt)

# 4. 运行
result = chain.predict(user_input="你好")
print(result)
```

**对比手写版的优势**：
- Prompt 和代码分离，便于管理
- 支持多变量、复杂模板
- 可复用、可组合

---

### W3D2：LangChain Memory（解决 Token 叠加问题）

**问题回顾**：
- W2 手动管理 history，只简单截断 20 条
- 长对话 Token 爆炸，费用高

**LangChain 解决方案**：

| Memory 类型 | 原理 | 适用场景 |
|------------|------|---------|
| `ConversationBufferMemory` | 保留所有历史（W2的做法） | 短对话 |
| `ConversationSummaryMemory` | **自动摘要早期对话** | 长对话 |
| `VectorStoreRetrieverMemory` | **只检索相关问题** | 知识库问答 |

**ConversationSummaryMemory 示例**（推荐）：
```python
from langchain.memory import ConversationSummaryMemory

# 自动摘要早期对话
memory = ConversationSummaryMemory(
    llm=llm,  # 用同一个LLM做摘要
    max_token_limit=1000  # 超过就触发摘要
)

# 使用
chain = ConversationChain(
    llm=llm,
    memory=memory
)

# 第1轮
chain.predict(input="你好，我叫张三")
# 第10轮后，前5轮会被自动总结成一句话摘要
```

**摘要效果**：
```
原始：10轮对话，5000 tokens
摘要后：1段摘要 + 最近3轮，1000 tokens
AI 仍然知道"用户叫张三，之前问过XX问题"
```

---

### W3D3：完整 ChatBot + 前端联调

**整合内容**：
1. LangChain 后端（Memory + Streaming）
2. Vue3 前端（复用 W2 的界面）
3. 支持：
   - 流式输出（LangChain 的 Streaming 回调）
   - 自动摘要（长对话不丢上下文）
   - 持久化（结合 W2 的 SQLite）

**产出**：
> 一个基于 LangChain 的专业 ChatBot，具备：
> - 优雅的 Prompt 管理
> - 智能的 Memory 机制
> - 流式输出体验
> - 数据持久化

---

## LangChain vs 手写的对比

| 功能 | W2 手写版 | W3 LangChain 版 |
|------|----------|----------------|
| Prompt 管理 | 字符串拼接 | PromptTemplate 模板 |
| Memory | 简单截断20条 | 自动摘要/向量检索 |
| 模型切换 | 改代码 | 换一行配置 |
| 流式输出 | 手写 yield | Callback 回调机制 |
| 代码量 | 多且乱 | 少且规范 |
| 面试价值 | "我会调API" | "我掌握 LangChain 框架" |

---

## 面试要点

**必须会说**：
> "我使用 LangChain 框架构建 AI 应用，通过 PromptTemplate 管理提示词模板，
> 使用 ConversationSummaryMemory 解决长对话 Token 限制问题，
> 实现了记忆功能与流式输出的结合。"

**可能追问**：
- Q：LangChain 的 Chain 是什么？
  - A：将 LLM、Prompt、Memory 等组件链接成处理流程，类似函数组合或管道。

- Q：Memory 有哪些类型，怎么选？
  - A：Buffer（全保留）、Summary（自动摘要）、Vector（检索相关）。短对话用 Buffer，长对话用 Summary。

---

## 学习资源

- 官方文档：https://python.langchain.com/docs/get_started/introduction
- 中文教程：https://www.langchain.com.cn/（社区翻译）

---

**W2 已完成，准备进入 W3 LangChain！**
