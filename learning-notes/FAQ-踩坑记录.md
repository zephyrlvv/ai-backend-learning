# 学习踩坑记录与 FAQ

**说明**：本文档记录学习过程中遇到的有价值问题和解决方案，便于重启后快速恢复上下文。

---

## 🚨 环境问题（高频）

### 1. Node.js 版本冲突（W1D2）

**问题现象**：
```
npm error Class extends value undefined is not a constructor or null
```

**根本原因**：
- Node 24.x 是最新 Current 版，`create-vue` 尚未完全兼容
- npm 全局包缓存损坏，与 Node 版本混用

**解决方案**：
```powershell
# 降级到 Node 22 LTS（长期支持版）
nvm install 22.14.0
nvm use 22.14.0

# 或者使用 pnpm 绕过 npm 损坏问题
iwr https://get.pnpm.io/install.ps1 -useb | iex
pnpm create vue@latest .
```

**就业提示**：
> 企业项目建议使用 LTS 版本（偶数版本，如 20/22），避免使用 Current 版本。

---

### 2. Python 虚拟环境与前端环境混淆

**问题现象**：
在 `(venv)` 虚拟环境里执行 npm 命令。

**正确做法**：
```powershell
# 前端开发（不需要虚拟环境）
cd frontend
pnpm dev

# 后端开发（需要虚拟环境）
cd G:\kimiProject-pc
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

**记忆口诀**：
- 看到 `(venv)` → 这是 Python 环境，不要执行 npm/pnpm
- 执行 npm/pnpm → 先 `deactivate` 退出虚拟环境

---

## 🌐 API 与通信问题

### 3. CORS 跨域错误

**问题现象**：
浏览器控制台显示 CORS policy 阻止请求。

**根本原因**：
浏览器安全机制阻止跨域请求（端口不同即跨域）。

**解决方案**（后端配置）：
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**注意点**：
- `allow_origins` 必须精确匹配前端地址
- 修改后必须**重启** `uvicorn`

---

### 4. 422 Unprocessable Entity 错误

**问题现象**：
前端发送请求，后端返回 422。

**常见原因**：
1. 字段名不匹配（后端要 `msg`，前端传 `message`）
2. 缺少必填字段（Pydantic 字段没有默认值）
3. GET 请求传了 Body（应该用 `params`）
4. 类型错误（后端要 `int`，前端传了字符串）

**解决方案**：
- 检查 Pydantic 模型定义
- GET 用 `params`，POST 用 `data`
- 使用 `Optional[str] = None` 表示可选字段

---

## 🐍 Python 语法陷阱

### 5. Python 缩进导致逻辑错误（W1D4）

**问题现象**：
同样的 if 判断，缩进不同导致逻辑完全不同。

**错误代码**（嵌套逻辑）：
```python
if todo.id == todo_id:
    if data.title is not None:
        todo.title = data.title
        if data.completed is not None:  # ❌ 嵌套在里面
            todo.completed = data.completed
            return todo
```

**正确代码**（平级逻辑）：
```python
if todo.id == todo_id:
    if data.title is not None:
        todo.title = data.title
    
    if data.completed is not None:  # ✅ 平级
        todo.completed = data.completed
    
    return todo  # ✅ 无论改了哪个都返回
```

**关键区别**：
- Python 没有 `{}`，完全靠缩进表示代码块层级
- 缩进不对 = 逻辑完全错误

---

### 6. 路由缺少斜杠（W1D4）

**问题现象**：
```
Failed to parse URL from http://127.0.0.1:8000todos/{todo_id}
```

**原因**：
```python
# ❌ 错误
@app.delete("todos/{todo_id}")

# ✅ 正确
@app.delete("/todos/{todo_id}")
```

---

## 📋 核心概念澄清

### 7. BaseModel 是什么？

**一句话**：TypeScript Interface + Zod 验证。

**作用**：
1. 定义数据结构
2. 自动验证类型
3. 自动生成 API 文档

**示例**：
```python
class TodoCreate(BaseModel):
    title: str  # 必填，必须是字符串

class TodoUpdate(BaseModel):
    title: Optional[str] = None  # 可选，不传默认为 None
```

---

### 8. Optional 是什么？

**TypeScript 类比**：
```typescript
// TS
interface TodoUpdate {
  title?: string;  // 可选
}

// Python
class TodoUpdate(BaseModel):
    title: Optional[str] = None  # 可选
```

**含义**：这个字段可以是 `str` 类型，也可以是 `None`。

---

### 9. 模拟数据库 vs 真实数据库

**当前做法**（内存列表）：
```python
todos_db: List[Todo] = []  # 重启服务数据丢失
```

**真实场景**（SQLite/PostgreSQL）：
```python
# 数据持久化，重启后还在
# W4 企业知识库项目会学
```

**面试话术**：
> "目前使用内存列表模拟数据存储便于快速原型开发，后续会接入 SQLite/PostgreSQL 实现持久化。"

---

## 🎯 RESTful API 设计规范

### 10. GET vs POST 区别

| 方法 | 参数位置 | 用途 | 幂等性 |
|------|---------|------|--------|
| GET | URL (`params`) | 查询数据 | 幂等（多次请求结果相同） |
| POST | Body | 创建资源 | 非幂等（多次请求创建多个） |
| PUT | Body | 全量更新 | 幂等 |
| PATCH | Body | 部分更新 | 幂等 |
| DELETE | URL | 删除 | 幂等 |

**记忆口诀**：增 POST、删 DELETE、改 PUT/PATCH、查 GET

---

## 🔧 命名规范

### 11. Python 命名 vs JavaScript

| 类型 | Python 规范 | JavaScript 规范 |
|------|------------|-----------------|
| 函数/变量 | `snake_case` | `camelCase` |
| 类名 | `PascalCase` | `PascalCase` |
| 常量 | `UPPER_SNAKE_CASE` | `UPPER_SNAKE_CASE` |

**建议**：
- 后端保持 Python 规范（`get_user_list`）
- 前端保持 JS 规范（`getUserList`）
- 通过 axios 拦截器转换，或保持一致

---

## 📝 总结

**高频问题 Top 3**：
1. Node 版本不兼容 → 用 LTS 版本或 pnpm
2. CORS 报错 → 后端配置 allow_origins，重启服务
3. 422 错误 → 检查字段名、是否必填、GET/POST 用法

**面试常问概念**：
- CORS 原理和解决方案
- RESTful API 设计规范
- FastAPI 的 BaseModel 作用
- Python 类型提示（Optional、List、Dict）

---

*最后更新：2026-03-29*
