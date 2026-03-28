<template>
    <div class="chat-box">
        <h1>🤖 AI 聊天助手</h1>
        <p>Vue3 前端 ↔ Python 后端 联调 Demo</p>

        <!-- 输入区域 -->
        <div class="input-area">
            <input v-model="message" placeholder="输入消息..." @keyup.enter="sendMessage" />
            <button @click="sendMessage" :disabled="loading">
                {{ loading ? '发送中...' : '发送' }}
            </button>
        </div>
        <!-- 新增：POST 请求测试 -->
        <div class="post-section" style="margin-top: 30px; border-top: 2px dashed #ccc; padding-top: 20px;">
            <h3>📝 POST 请求测试</h3>
            <input v-model="userId" placeholder="输入用户ID（可选）" />
            <button @click="sendPost" :disabled="loading">
                POST 方式发送
            </button>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="error">
            ❌ {{ error }}
        </div>

        <!-- 后端响应 -->
        <div v-if="response" class="response">
            <h3>后端返回：</h3>
            <pre>{{ JSON.stringify(response, null, 2) }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// 响应式数据（类似 Python 的变量，但界面会自动更新）
const message = ref('')      // 输入框内容
const response = ref(null)   // 后端返回的数据
const loading = ref(false)   // 加载状态
const error = ref('')        // 错误信息
const userId = ref('')


// 发送消息函数
const sendMessage = async () => {
    // 校验：空消息不发
    if (!message.value.trim()) {
        error.value = '请输入消息'
        return
    }

    // 重置状态
    loading.value = true
    error.value = ''
    response.value = null

    try {
        // 调用 Python 后端 API
        const res = await axios.get('http://localhost:8000/chat', {
            params: {
                msg: message.value  // 对应 Python 函数的 msg 参数
            }
        })

        // 保存响应数据
        response.value = res.data
        console.log('后端返回：', res.data)

    } catch (err: any) {
        console.error('请求失败：', err)
        error.value = err.response?.data?.detail || '请求失败，请检查后端是否启动'
    } finally {
        loading.value = false
    }
}

// 添加 POST 请求函数
const sendPost = async () => {
    if (!message.value.trim()) {
        error.value = '请输入消息'
        return
    }

    loading.value = true
    error.value = ''
    response.value = null

    try {
        // POST 请求：参数放在 data 里，不是 params
        const res = await axios.post('http://localhost:8000/chat', {
            msg: message.value,
            userId: userId.value
        })

        response.value = res.data

    } catch (err: any) {
        error.value = err.response?.data?.detail || '请求失败'
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
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

h1 {
    color: #333;
    margin-bottom: 10px;
}

p {
    color: #666;
    margin-bottom: 20px;
}

.input-area {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

input:focus {
    outline: none;
    border-color: #007bff;
}

button {
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

button:hover:not(:disabled) {
    background: #0056b3;
}

button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.error {
    color: #dc3545;
    padding: 10px;
    background: #f8d7da;
    border-radius: 4px;
    margin-bottom: 20px;
}

.response {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 4px;
    border-left: 4px solid #28a745;
}

.response h3 {
    margin-top: 0;
    color: #28a745;
}

pre {
    color: black;
    background: white;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
    margin: 0;
}
</style>