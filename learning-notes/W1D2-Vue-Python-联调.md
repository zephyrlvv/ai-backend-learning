# W1D2：Vue3 + Python 联调实战

## 📋 今日目标（就业导向）

**最终产出**：一个能运行的「Vue3 前端 ↔ Python 后端」完整 Demo

**面试价值**：能说出"我独立完成了前后端分离项目的联调，解决了跨域问题"

---

## ⏰ 时间安排（20:00-23:00，含休息）

### 阶段一：创建 Vue3 项目（20:00-20:45）

#### 1. 初始化项目

```bash
# 创建项目（在 G:\kimiProject-pc 目录下新建 frontend 文件夹）
cd G:\kimiProject-pc
mkdir frontend
cd frontend
npm create vue@latest .
```

**选项选择**（和你熟悉的一致）：
```
✔ Project name: frontend
✔ Add TypeScript? … Yes          # 你有 TS 基础
✔ Add JSX Support? … No
✔ Add Vue Router? … Yes          # 单页面应用需要
✔ Add Pinia? … No                # 今天用不到状态管理
✔ Add Vitest? … No
✔ Add Cypress? … No
```

**Python 知识点类比**：
> `npm create vue` 相当于 Python 的 `pip install`，都是安装工具。
> 区别：Python 先装到环境里，Node 是临时下载执行。

#### 2. 安装依赖并启动

```bash
npm install
npm run dev
```

浏览器访问 `http://localhost:5173`，看到 Vue 欢迎页面就算成功。

**就业提示**：
> 面试时如果问到"怎么创建 Vue3 项目"，要说 Vite（`npm create vue` 底层是 Vite），
> 别再说 Vue CLI 了，那是老项目用的。

#### 3. 安装 Axios

```bash
npm install axios
```

---

【休息 10-15 分钟】

---

### 阶段二：编写前端代码（21:00-21:30）

#### 1. 修改 `src/App.vue`

```vue
<template>
  <div class="chat-box">
    <h1>🤖 AI 聊天助手</h1>
    <p>Python 后端 + Vue3 前端联调 Demo</p>
    
    <div class="input-area">
      <input 
        v-model="message" 
        placeholder="输入消息..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">发送</button>
    </div>
    
    <div v-if="loading" class="loading">发送中...</div>
    
    <div v-if="response" class="response">
      <h3>后端返回：</h3>
      <pre>{{ JSON.stringify(response, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const message = ref('')
const response = ref(null)
const loading = ref(false)

const sendMessage = async () => {
  if (!message.value.trim()) return
  
  loading.value = true
  try {
    // 调用 Python 后端
    const res = await axios.get('http://localhost:8000/chat', {
      params: { msg: message.value }
    })
    response.value = res.data
  } catch (error) {
    console.error('请求失败：', error)
    alert('请求失败，请确保 Python 后端已启动（uvicorn main:app）')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-box {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.response {
  margin-top: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 4px;
}

pre {
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}
</style>
```

**代码解释**（Python 零基础友好）：

| Vue 代码 | Python 类比/解释 |
|---------|-----------------|
| `ref('')` | 类似 Python 的变量，但 Vue 会自动监听变化并更新界面 |
| `const sendMessage = async () => {}` | Python 3.5+ 也有 `async def`，都是处理异步操作 |
| `axios.get(...)` | 类似 Python 的 `requests.get()`，都是发 HTTP 请求 |
| `try...catch` | Python 里是 `try...except`，都是捕获错误 |
| `params: { msg: ... }` | 这是 URL 参数，Python 里 FastAPI 用 `@app.get("/chat")` 接收 |

---

### 阶段三：Python 后端配置 CORS（21:30-22:00）

#### 1. 修改 `main.py`

打开 `G:\kimiProject-pc\main.py`，添加 CORS 支持：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 新增：导入 CORS 中间件

app = FastAPI()

# 新增：添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许 Vue 的地址访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET/POST/PUT/DELETE 等）
    allow_headers=["*"],  # 允许所有请求头
)

# 原有代码保持不变
@app.get("/")
def hello():
    return {"message": "Hello, I'm your AI backend!"}

@app.get("/chat")
def chat(msg: str):
    return {"reply": f"你说了：{msg}", "backend": "Python"}
```

**详细解释**（零基础）：

**什么是 CORS？**
> 浏览器的**安全机制**。当网页（Vue，端口 5173）要访问另一个域名/端口的接口（Python，端口 8000），
> 浏览器会阻止，除非**被访问的服务器明确说"我允许"**。

**为什么后端解决更好？**
> - Vue 配置代理只在**开发环境**有效，打包后失效
> - Python 配置 CORS，开发/生产都有效，是**标准做法**

**类比前端**：
> `CORSMiddleware` 类似 Vue Router 的**导航守卫**，每个请求进来先经过它检查，
> 判断来源是否在白名单里（`allow_origins`）。

#### 2. 重启 Python 后端

```powershell
cd G:\kimiProject-pc
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

**注意**：修改 `main.py` 后必须重启，不然 CORS 配置不生效。

---

### 阶段四：联调测试（22:00-22:30）

#### 1. 确保两端都在运行

| 服务 | 地址 | 状态检查 |
|------|------|---------|
| Python 后端 | http://localhost:8000 | 浏览器能打开看到 JSON |
| Vue 前端 | http://localhost:5173 | 能看到输入框和按钮 |

#### 2. 测试步骤

1. 在 Vue 页面输入框里打字，比如"你好"
2. 点击「发送」按钮
3. 下方应该显示后端返回的 JSON：
   ```json
   {
     "reply": "你说了：你好",
     "backend": "Python"
   }
   ```

**如果报错**：
- **"Network Error"**：Python 没启动，或 CORS 配置没生效（重启 Python）
- **404 Not Found**：检查 URL 拼写，FastAPI 路由是 `/chat` 不是 `/chat/`

---

【休息 10-15 分钟】

---

### 阶段五：拓展练习（22:45-23:00）

如果能提前完成，可以尝试：

#### 练习 1：POST 请求

**Vue 修改**：
```typescript
// 把 axios.get 改成 axios.post
const res = await axios.post('http://localhost:8000/chat', {
  msg: message.value
})
```

**Python 修改**：
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    msg: str

@app.post("/chat")  # 改成 @app.post
def chat(data: ChatRequest):  # 参数改为接收 Body
    return {"reply": f"你说了：{data.msg}", "backend": "Python"}
```

**面试考点**：
> GET 请求参数在 URL 里（有长度限制），POST 在 Body 里（适合大数据）。
> 面试常问：GET 和 POST 的区别？什么时候用 POST？

#### 练习 2：Git 提交

```bash
cd G:\kimiProject-pc
git init  # 如果还没初始化
git add .
git commit -m "feat: Vue3 + Python 联调完成，实现前后端通信"
```

**就业提示**：
> 养成每天提交代码的习惯，面试时可以展示 GitHub 的 commit 记录。

---

## 📝 今日学习检查清单

完成后打勾：

- [ ] Vue3 项目创建成功，能看到欢迎页面
- [ ] 安装了 Axios
- [ ] 编写了带输入框和按钮的界面
- [ ] Python 添加了 CORS 配置
- [ ] 前后端成功通信，能看到返回数据
- [ ] （可选）尝试了 POST 请求
- [ ] （可选）提交了 Git

---

## 💼 面试要点总结

**今天学的内容，面试可以这样说：**

> "我独立完成了 Vue3 + Python FastAPI 的前后端联调项目。
> 过程中遇到了跨域问题，通过在后端配置 CORS 中间件解决，
> 理解了浏览器同源策略的限制和解决方案。
> 实现了 GET/POST 两种请求方式的数据交互。"

**可能追问及答案：**

**Q：什么是 CORS？**
> A：跨域资源共享，浏览器的安全机制。不同域名/端口的请求会被阻止，
> 需要服务器端设置 `Access-Control-Allow-Origin` 响应头允许特定来源。

**Q：除了后端配置 CORS，还有什么方案？**
> A：开发环境可以用 Vue 代理（devServer.proxy），生产环境建议用 Nginx 反向代理，
> 或者后端直接配置 CORS 是最通用的方案。

**Q：FastAPI 是什么？**
> A：Python 的现代 Web 框架，特点是自动生成 API 文档、类型提示支持、异步高性能，
> 特别适合构建 AI 服务的后端 API。

---

*明日计划预览：W1D3 将学习 Python 基础语法，理解变量、函数、列表、字典等概念*
