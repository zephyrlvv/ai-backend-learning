<template>
    <div class="todo-app">
        <h1>📝 待办事项</h1>

        <!-- 添加新待办 -->
        <div class="add-todo">
            <input v-model="newTitle" placeholder="输入新待办..." @keyup.enter="addTodo" />
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

// 定义 Todo 类型（类似 TypeScript interface）
interface Todo {
    id: number
    title: string
    completed: boolean
}

// 响应式数据
const todos = ref<Todo[]>([])
const newTitle = ref('')
const loading = ref(false)

const API_URL = 'http://localhost:8000/todos'

// 计算属性（类似 Vue2 的 computed）
const completedCount = computed(() => todos.value.filter(t => t.completed).length)
const pendingCount = computed(() => todos.value.filter(t => !t.completed).length)

// 获取所有待办（页面加载时调用）
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
        todos.value.push(res.data)  // 添加到列表末尾
        newTitle.value = ''  // 清空输入框
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
        todo.completed = !todo.completed  // 本地更新，不用重新请求
    } catch (err) {
        alert('更新失败')
    }
}

// 删除待办
const deleteTodo = async (id: number) => {
    if (!confirm('确定删除吗？')) return

    try {
        await axios.delete(`${API_URL}/${id}`)
        todos.value = todos.value.filter(t => t.id !== id)  // 本地过滤掉删除的
    } catch (err) {
        alert('删除失败')
    }
}

// 页面加载时自动获取数据（类似 Vue2 的 mounted）
onMounted(() => {
    fetchTodos()
})
</script>

<style scoped>
.todo-app {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1 {
    text-align: center;
    color: #333;
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
    font-size: 14px;
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
    padding: 5px 10px;
    font-size: 12px;
}

.loading {
    text-align: center;
    padding: 20px;
    color: #999;
}

.stats {
    margin-top: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 4px;
    text-align: center;
    color: #666;
}
</style>