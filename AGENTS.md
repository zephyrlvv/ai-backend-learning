# 用户背景与学习路线

## 个人背景
- **当前身份**：前端开发工程师（5年 Vue 经验）
- **Python 基础**：⭐ 零基础（需要详细解释每一个概念）
- **学习目的**：为了就业转型，一切学习以就业为导向
- **转型目标**：AI 应用工程师 / RAG 开发 / Agent 工程师
- **学习阶段**：16周转型路线 - 第1天

### 教学提醒（给 AI 助手）
1. **解释每一个 Python 概念**：不要假设我懂任何 Python 语法，详细解释"为什么"
2. **就业导向**：说明每个知识点在实际工作中的应用场景
3. **循序渐进**：不跳过基础，确保理解再进入下一步
4. **结合前端经验**：用我已知的 Vue/JS/TS 知识类比解释 Python 概念

### 教学风格偏好
- **讲解方式**：文字解释 + 代码示例结合
- **前端技术栈**：Vue2 / Vue3 / 基础 TypeScript
- **类比方式**：用前端熟悉的概念（组件、生命周期、类型定义等）来解释 Python

---

## 📅 当前进度（自动更新区）

```yaml
当前日期: 2026-04-07
当前周次: W3 进行中
当前天数: W3D2（第2天）
阶段: 阶段一（3周）进行中
主题: LangChain Memory 组件（基础版）
目标: 掌握 RunnableWithMessageHistory 新版 Memory 用法
状态: W1 ✅ W2 ✅ W3D2 🔄 进行中
W1 完成内容: 
  - ✅ Todo List CRUD 完整实现
  - ✅ 全部接口联调成功
  - ✅ Git 提交代码
W2 完成内容: 
  - ✅ 接入真实 AI API（硅基流动 Qwen3-VL-32B）
  - ✅ 实现真正的 AI 流式对话
  - ✅ 添加 Memory 记忆功能（连续对话）
  - ✅ SQLite 持久化存储（重启后数据不丢失）
  - ✅ 修复 statiscCharts.vue 月份选择器 bug（双向12个月限制）
W2 阶段总结: 
  - 产出：带记忆功能的 AI 聊天机器人（流式输出 + 持久化）
  - 技术栈：FastAPI StreamingResponse + EventSource + SQLite
  - 面试点：流式输出原理、SSE vs WebSocket、数据库持久化设计
W3 计划（进行中）: 
  - ✅ W3D1: LangChain 基础（Chain、PromptTemplate）
  - 🔄 W3D2: LangChain Memory 组件（RunnableWithMessageHistory 新版用法）
  - 📝 W3D3: 整合到 FastAPI + 前端联调
  - ⏰ 学习时间：20:00-23:00（工作日）
学习文档: 
  - W2D1: learning-notes/W2D1-流式输出.md
  - FAQ: learning-notes/FAQ-踩坑记录.md（环境问题、422错误、Python陷阱等）
  - W3D1: learning-notes/W3-LangChain基础.md
  - W3D2: langchain_demo.py（本地 Memory 练习）
  - W3D2: main.py /chat/memory 接口（FastAPI 集成）
GitHub 仓库: https://github.com/你的用户名/ai-backend-learning（已推送）
环境状态: 
  - Vue 前端: http://localhost:5173（运行正常）
  - Python 后端: http://localhost:8000（运行正常）
  - 联调状态: ✅ 已打通
W3D2 完成内容（2026-04-07）:
  - ✅ 安装 langchain-community 依赖包
  - ✅ 学习新版 Memory 写法（LangChain 0.2+）
  - ✅ 理解 RunnableWithMessageHistory 核心概念
    - 类比前端高阶组件（HOC）
    - 参数含义：get_session_history、input_messages_key、history_messages_key
    - 数据流向：invoke → config → get_history → Prompt → LLM
  - ✅ 理解 StrOutputParser 作用（AIMessage → 字符串）
  - ✅ 理解 Chain 执行方向（从左到右 | 管道流）
  - ✅ 完成 memory_demo.py 本地测试
  - ✅ 在 main.py 添加 /chat/memory 接口（基础 Memory 版）
  - ⚠️ 踩坑记录：ConversationChain 和 ConversationSummaryMemory 已废弃
    - 旧版：langchain.chains.ConversationChain
    - 新版：langchain_core.runnables.history.RunnableWithMessageHistory
    - 旧版 Memory：ConversationSummaryMemory（自动摘要）在新版需自行实现
    - 新版基础 Memory：ChatMessageHistory + RunnableWithMessageHistory

面试要点（W3D2）:
  - RunnableWithMessageHistory 是 HOC 模式，给 Chain 添加记忆功能
  - Chain 执行方向从左到右（管道流）
  - LangChain 0.2+ 推荐 LCEL 写法（管道符 | 连接组件）
  - 区分业务数据（invoke 第一个参数）和运行时配置（config 参数）

最近谈话记录: 
  - 2026-04-07: W3D2 LangChain Memory 学习
    - 核心概念：RunnableWithMessageHistory、MessagesPlaceholder、ChatMessageHistory
    - API 参数详解：get_session_history 函数签名、key 的对应关系
    - Chain 数据流向详解
  - 2026-04-02: 讨论女同事生日礼物（40岁，喜欢旅游/抹茶/椰子，预算150元）
    - 推荐：白色恋人抹茶味12枚装 + DIY明信片
    - 备选：大福、马卡龙6枚、AKOKO曲奇
    - 避雷：毛绒玩具、香水、与父亲相关物品
  - 2026-04-02: 修复 Vue2 statiscCharts.vue 月份选择器 bug
    - 问题：选择后禁用逻辑错误、清空后未重置
    - 解决：使用 calendar-change + visible-change 事件，锚点日期双向限制±12个月
  - 2026-04-02: Python 生成器表达式 sum() 立即计算原理讲解
  - 2026-04-02: try/except 异常处理、Python 逻辑运算符（and/or/not）讲解
```

---

## 16周转型路线图

### 阶段一：Python + 基础（3周）
| 周次 | 主题 | 目标 | 产出 |
|------|------|------|------|
| W1 | Python 语法 + FastAPI | 能看懂并修改 AI 项目代码 | 用 Python 写一个简单 API 给 Vue 调用 |
| W2 | FastAPI + API 调用 | 后端服务框架，流式输出 | Vue3 聊天界面 ↔ Python 后端 联调成功 |
| W3 | LangChain 基础 | Chain、Memory、Prompt 模板 | 有历史记录功能的 ChatBot |

### 阶段二：项目一 - 企业知识库（5周）
| 周次 | 主题 | 重点内容 |
|------|------|----------|
| W4 | 文档处理 | Vue: 文件上传组件、进度条、格式校验<br>Python: PDF/Word 解析、文本清洗 |
| W5 | **RAG 核心（重点周）** | Python: 文档切分 → Embedding → 向量库 → 检索<br>Vue: 知识库管理列表、文档分段预览 |
| W6 | 问答优化 | Vue: 对话界面、引用原文展示（高亮定位）<br>Python: 上下文压缩、重排序、Prompt 优化 |
| W7 | 工程化 | Vue: 响应式布局、移动端适配<br>Python: 并发处理、错误重试、日志 |
| W8 | 部署上线 | 产出：有公开链接的 Demo，写技术博客一篇 |

### 阶段三：项目二 - AI 销售助手（5周）
| 周次 | 主题 | 重点内容 |
|------|------|----------|
| W9 | Agent 基础 | Vue: Prompt 配置界面、工具开关面板<br>Python: ReAct Agent、单工具调用 |
| W10 | **多 Agent 架构（重点周）** | Vue: 流程可视化（类似 Coze 的画布）<br>Python: Agent 编排、状态传递、任务分解 |
| W11 | 工具集成 | Vue: 工具配置表单、执行日志展示<br>Python: 搜索 API、浏览器自动化、数据抓取 |
| W12 | 复杂任务 | Vue: 长任务进度条、中间结果展示<br>Python: 断点续传、并行执行、结果汇总 |
| W13 | 产品化 | 产出：能演示的 Agent 系统，写技术博客一篇 |

### 阶段四：求职准备（3周）
| 周次 | 主题 | 重点内容 |
|------|------|----------|
| W14 | 作品集包装 | GitHub: 两个项目代码 + README 详细说明<br>博客: 3篇（RAG 实践 + Agent 架构 + 转型心得）<br>演示站: Vercel 部署前端，云服务器部署后端 |
| W15 | 简历 + 投递 | 简历重点: 5年 Vue 工程经验 + 独立完成 2 个 AI 全栈项目<br>投递策略: 优先「AI 应用工程师」「RAG 开发」「Agent 工程师」 |
| W16 | 面试冲刺 | 刷题: RAG 八股、Agent 设计模式、LLM 基础<br>复盘: 每轮面试后优化项目细节 |

---

## 技术栈
- **前端**：Vue 3（已有5年经验）
- **后端**：Python + FastAPI
- **AI 框架**：LangChain（即将学习）
- **部署**：Vercel（前端）、云服务器（后端）

## 项目环境
- Python 版本：3.10.6
- 虚拟环境：`./venv`
- 格式化工具：Black
- 主要依赖：FastAPI、Uvicorn

### 为什么要学这些？（就业视角）
| 技术 | 就业价值 |
|------|---------|
| FastAPI | 当前最热门的 Python 后端框架之一，AI 项目首选，面试高频考点 |
| 虚拟环境 | Python 开发的标配，面试必问，体现工程素养 |
| Black | 代码规范工具，企业级开发必备，简历加分项 |
| CORS/联调 | 前后端分离项目的核心技能，实际工作每天都在用 |
| LangChain | AI 应用工程师的核心竞争力，高薪岗位必备 |

---

## ⏰ 学习时间规划

| 时间 | 安排 |
|------|------|
| 工作日 | 20:00 后开始，学习 2.5-3 小时 |
| 工作日休息 | 中途需要安排休息时间 |
| 周末 | 周六+周日，共 6 小时 |

**明日（工作日）学习计划（20:00-23:00，含休息）：**

```
20:00-20:45（45分钟）
├── 用 Vite 创建 Vue3 项目
├── 安装 Axios
└── 写一个简单的按钮调用后端

【休息 10-15 分钟】

21:00-22:00（60分钟）
├── 给 FastAPI 添加 CORS 跨域配置
├── Vue 配置代理（如有需要）
├── 调试前后端通信
└── 实现双向传参（Vue 发消息 → Python 处理 → 返回结果）

【休息 10-15 分钟】

22:15-23:00（45分钟）
├── 美化界面（用你熟悉的 Vue 技能）
├── 测试不同接口（GET/POST）
└── 整理今日代码，提交 Git
```

预计明日产出：一个有输入框和按钮的 Vue 页面，点击后能把消息发到 Python 后端并显示返回结果。

---

## 📝 进度更新说明

**我（AI助手）会在每次对话结束时自动询问：**
> "今天完成了什么？需要更新进度吗？"

**记录原则（最大化记录）：**
- ✅ **详细记录每天的学习内容** - 不限篇幅，尽可能完整
- ✅ **记录遇到的问题和解决方案** - 这是宝贵的踩坑经验
- ✅ **记录对话中的关键信息** - 重要的技术点、面试技巧、经验总结
- ✅ **保留代码变更历史** - 关键的代码修改会记录版本
- ✅ **保留思考过程** - 从不懂到懂的过程对复盘很有价值

**记录格式示例：**
```markdown
### 2026-03-26（第1天）
**学习时间**：20:00-23:00（3小时）
**今日完成**：
1. ✅ 配置 Python 插件（Black 格式化）
   - 问题：格式化不生效 → 原因：代码有语法错误（3空格缩进）
   - 解决：修正缩进后 Black 正常工作
   - 知识点：Black 不会修复语法错误，只会格式化合法代码
2. ✅ 开启虚拟环境
   - 命令：`./venv/Scripts/Activate.ps1`
   - 注意：需要设置 PowerShell 执行策略
3. ✅ 启动 FastAPI 项目
   - 命令：`uvicorn main:app --reload`
   - 访问：http://127.0.0.1:8000

**关键对话摘要**：
- 解释了为什么 Black 不自动修复缩进（因为涉及意图猜测）
- 确定了学习方式：文字+代码结合，用前端知识类比
- 明确了学习时间：工作日20:00后2.5-3小时，周末6小时

**明日计划**：Vue3 项目联调

**面试要点**：
- 虚拟环境的作用：隔离项目依赖，避免版本冲突
- Black 的作用：统一代码风格，企业开发必备
```

**Token 不是问题** - 你明确要求详细记录，就算文件变大了，必要时我们再拆分。学习历程的完整性更重要。

---

*最后更新：2026-03-26*
