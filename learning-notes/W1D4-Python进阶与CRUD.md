# W1D4：Python 进阶技巧 + 待办事项 CRUD 实战

**今日目标**：实现一个完整的「待办事项」API，支持增删改查，前端用列表展示

---

## 📚 第一阶段：Python 实用技巧（20分钟）

### 1. 列表推导式（List Comprehension）

**是什么**：一行代码生成列表，类似 JS 的 `map` + `filter`

**对比学习**：

```javascript
// JavaScript 写法
const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(n => n * n);           // [1, 4, 9, 16, 25]
const evens = numbers.filter(n => n % 2 === 0);    // [2, 4]
```

```python
# Python 列表推导式
numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]                # [1, 4, 9, 16, 25]
evens = [n for n in numbers if n % 2 == 0]        # [2, 4]

# 带条件的推导
labels = ["偶数" if n % 2 == 0 else "奇数" for n in numbers]
# ['奇数', '偶数', '奇数', '偶数', '奇数']
```

**就业价值**：处理数据时特别常用，AI 项目里经常要处理列表数据

---

### 2. 字典常用操作

```python
# 假设这是从数据库查出来的用户数据
users = [
    {"id": 1, "name": "张三", "age": 25},
    {"id": 2, "name": "李四", "age": 30},
    {"id": 3, "name": "王五", "age": 25},
]

# 1. 按条件筛选（找年龄25的）
filtered = [u for u in users if u["age"] == 25]

# 2. 提取某个字段（只取名字）
names = [u["name"] for u in users]

# 3. 转成字典格式（id 为 key，方便查找）
user_dict = {u["id"]: u for u in users}
# {1: {"id": 1, "name": "张三"...}, 2: {...}}

# 4. 查找特定用户（比遍历列表快）
user = user_dict.get(2)  # 直接拿到李四，O(1)复杂度
```

**与 JS 对比**：

| 操作 | JavaScript | Python |
|------|-----------|--------|
| 查找元素 | `users.find(u => u.id === 2)` | `next(u for u in users if u["id"] == 2)` |
| 转成 Map | `new Map(users.map(u => [u.id, u]))` | `{u["id"]: u for u in users}` |
| 获取字段 | `users.map(u => u.name)` | `[u["name"] for u in users]` |

---

## 📚 第二阶段：FastAPI 参数详解（30分钟）

### FastAPI 三种参数类型

```python
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

app = FastAPI()

# ========== 1. 路径参数（Path Parameters）==========
# URL: /items/123
# 用于：资源标识，如用户ID、商品ID
@app.get("/items/{item_id}")
def get_item(item_id: int = Path(..., description="商品ID")):
    return {"item_id": item_id}

# ========== 2. 查询参数（Query Parameters）==========
# URL: /search?keyword=手机&page=1&size=10
# 用于：筛选、分页、排序
@app.get("/search")
def search(
    keyword: str = Query(None, description="搜索关键词"),
    page: int = Query(1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量")
):
    return {"keyword": keyword, "page": page, "size": size}

# ========== 3. 请求体（Request Body）==========
# 用于：POST/PUT 传递复杂数据
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False  # 默认值

@app.post("/items")
def create_item(item: Item = Body(...)):
    return {"item": item, "total": item.price * 0.9 if item.is_offer else item.price}
```

**类比 Vue Router**：

| FastAPI | Vue Router |
|---------|-----------|
| `@app.get("/items/{id}")` | `/user/:id`（动态路由）|
| `Query(...)` | `?page=1&size=10`（查询参数）|
| `Body(...)` | `props` 传递对象 |

---

## 🚀 第三阶段：实战「待办事项」API（90分钟）

### 需求
实现一个 Todo List 后端：
- ✅ 查看所有待办事项
- ✅ 添加新待办
- ✅ 标记完成/未完成
- ✅ 删除待办

### 后端代码（main.py）

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS 配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 数据模型 ==========
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

# ========== 模拟数据库（实际项目用真实数据库）==========
todos_db: List[Todo] = [
    Todo(id=1, title="学习 FastAPI", completed=False),
    Todo(id=2, title="完成 Vue 联调", completed=True),
]
next_id = 3

# ========== API 接口 ==========

# 1. 获取所有待办（GET）
@app.get("/todos", response_model=List[Todo])
def get_todos():
    """获取所有待办事项"""
    return todos_db

# 2. 获取单个待办（GET）
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    """获取指定ID的待办"""
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="待办事项不存在")

# 3. 创建待办（POST）
@app.post("/todos", response_model=Todo)
def create_todo(data: TodoCreate):
    """创建新待办"""
    global next_id
    new_todo = Todo(id=next_id, title=data.title)
    todos_db.append(new_todo)
    next_id += 1
    return new_todo

# 4. 更新待办（PUT）
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate):
    """更新待办（修改标题或完成状态）"""
    for todo in todos_db:
        if todo.id == todo_id:
            if data.title is not None:
                todo.title = data.title
            if data.completed is not None:
                todo.completed = data.completed
            return todo
    raise HTTPException(status_code=404, detail="待办事项不存在")

# 5. 删除待办（DELETE）
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """删除待办"""
    global todos_db
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            deleted = todos_db.pop(i)
            return {"message": "删除成功", "todo": deleted}
    raise HTTPException(status_code=404, detail="待办事项不存在")

# 6. 标记完成（PATCH - 部分更新）
@app.patch("/todos/{todo_id}/complete")
def complete_todo(todo_id: int):
    """标记为完成"""
    for todo in todos_db:
        if todo.id == todo_id:
            todo.completed = True
            return todo
    raise HTTPException(status_code=404, detail="待办事项不存在")
```

---

### 前端代码（Vue）

修改 `App.vue`：

```vue
<template>
  <div class="todo-app">
    <h1>📝 待办事项列表</h1>
    
    <!-- 添加新待办 -->
    <div class="add-todo">
      <input 
        v-model="newTitle" 
        placeholder="输入新待办..."
        @keyup.enter="addTodo"
      />
      <button @click="addTodo">添加</button>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>
    
    <!-- 待办列表 -->
    <ul class="todo-list" v-else>
      <li v-for="todo in todos" :key="todo.id" :class="{ completed: todo.completed }">
        <span @click="toggleComplete(todo)">
          {{ todo.completed ? '✅' : '⭕' }} {{ todo.title }}
        </span>
        <button @click="deleteTodo(todo.id)" class="delete">删除</button>
      </li>
    </ul>
    
    <!-- 统计 -->
    <div class="stats">
      总计: {{ todos.length }} | 
      已完成: {{ completedCount }} | 
      待完成: {{ pendingCount }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Todo {
  id: number
  title: string
  completed: boolean
}

const todos = ref<Todo[]>([])
const newTitle = ref('')
const loading = ref(false)

const API_URL = 'http://localhost:8000/todos'

// 计算属性（类似 Vue2 的 computed）
const completedCount = computed(() => todos.value.filter(t => t.completed).length)
const pendingCount = computed(() => todos.value.filter(t => !t.completed).length)

// 获取所有待办
const fetchTodos = async () => {
  loading.value = true
  try {
    const res = await axios.get(API_URL)
    todos.value = res.data
  } catch (err) {
    alert('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 添加待办
const addTodo = async () => {
  if (!newTitle.value.trim()) return
  
  try {
    const res = await axios.post(API_URL, {
      title: newTitle.value
    })
    todos.value.push(res.data)
    newTitle.value = ''
  } catch (err) {
    alert('添加失败')
  }
}

// 切换完成状态
const toggleComplete = async (todo: Todo) => {
  try {
    await axios.put(`${API_URL}/${todo.id}`, {
      completed: !todo.completed
    })
    todo.completed = !todo.completed
  } catch (err) {
    alert('更新失败')
  }
}

// 删除待办
const deleteTodo = async (id: number) => {
  if (!confirm('确定删除吗？')) return
  
  try {
    await axios.delete(`${API_URL}/${id}`)
    todos.value = todos.value.filter(t => t.id !== id)
  } catch (err) {
    alert('删除失败')
  }
}

// 页面加载时获取数据
onMounted(() => {
  fetchTodos()
})
</script>

<style scoped>
.todo-app {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
}

.add-todo {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.add-todo input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.todo-list li:hover {
  background: #f5f5f5;
}

.todo-list li.completed span {
  text-decoration: line-through;
  color: #999;
}

.delete {
  background: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.stats {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: center;
  color: #666;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #999;
}
</style>
```

---

## 📋 今日检查清单

- [ ] 理解列表推导式 `[x for x in list if condition]`
- [ ] 理解字典推导式 `{k: v for k, v in items}`
- [ ] 理解 FastAPI 的 Path/Query/Body 三种参数
- [ ] 理解 HTTP 方法：GET/POST/PUT/PATCH/DELETE
- [ ] 实现 Todo API 后端（5个接口）
- [ ] 实现 Todo 前端界面（增删改查）
- [ ] 前后端联调成功，功能正常
- [ ] Git 提交今日代码

---

## 💼 面试要点

**今天学的内容，面试可以这样说：**

> "我实现了完整的 CRUD 待办事项应用。后端使用 FastAPI 提供 RESTful API，
> 支持 GET 查询、POST 创建、PUT 更新、DELETE 删除。
> 前端使用 Vue3 的 composition API 和计算属性，实现了响应式数据展示。
> 理解了 HTTP 方法对应的 CRUD 操作，以及 RESTful 接口设计规范。"

**RESTful API 规范**（面试常问）：
- `GET /todos` → 查询列表（Read）
- `GET /todos/1` → 查询单个（Read）
- `POST /todos` → 创建（Create）
- `PUT /todos/1` → 全量更新（Update）
- `PATCH /todos/1` → 部分更新（Update）
- `DELETE /todos/1` → 删除（Delete）

---

*开始吧！有问题随时问我 💪*
