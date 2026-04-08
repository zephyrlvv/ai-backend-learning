<template>
    <div class="chat-container">
        <h1>🤖 AI 聊天助手</h1>

        <!-- 消息列表区域 -->
        <div class="message-list" ref="messageList">
            <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
                <div class="avatar">
                    {{ msg.role === 'user' ? '👤' : '🤖' }}
                </div>
                <div class="content">
                    <div class="text">{{ msg.content }}</div>
                    <div class="time">{{ msg.time }}</div>
                </div>
            </div>

            <!-- Loading 状态 -->
            <div v-if="isConnecting" class="message ai loading">
                <div class="avatar">🤖</div>
                <div class="content">
                    <div class="loading-text">
                        正在连接 AI<span class="dots"><span>.</span><span>.</span><span>.</span></span>
                    </div>
                </div>
            </div>

            <div v-if="isGenerating" class="message ai">
                <div class="avatar">🤖</div>
                <div class="content">
                    <div class="text">{{ currentReply }}<span class="cursor">▋</span></div>
                </div>
            </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
            <input v-model="inputMessage" placeholder="输入消息..." :disabled="isConnecting || isGenerating"
                @keyup.enter="sendMessage" />
            <button @click="sendMessage" :disabled="!inputMessage.trim() || isConnecting || isGenerating">
                {{ isConnecting || isGenerating ? '发送中...' : '发送' }}
            </button>
        </div>


    </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

interface Message {
    role: 'user' | 'ai'
    content: string
    time: string
}

const messages = ref<Message[]>([])
const inputMessage = ref('')
const currentReply = ref('')
const isConnecting = ref(false)
const isGenerating = ref(false)
const messageList = ref<HTMLDivElement>()

const sendMessage = () => {
    if (!inputMessage.value.trim() || isConnecting.value || isGenerating.value) return

    // 添加用户消息
    messages.value.push({
        role: 'user',
        content: inputMessage.value,
        time: new Date().toLocaleTimeString()
    })

    const userMsg = inputMessage.value
    inputMessage.value = ''
    currentReply.value = ''
    isConnecting.value = true

    // 滚动到底部
    scrollToBottom()

    // 调用 AI 流式接口
    const es = new EventSource(`http://localhost:8000/chat/myai?msg=${encodeURIComponent(userMsg)}`)

    es.onmessage = (e) => {
        console.log({ e });

        if (e.data === '[DONE]') {
            es.close()
            messages.value.push({
                role: 'ai',
                content: currentReply.value,
                time: new Date().toLocaleTimeString()
            })
            currentReply.value = ''
            isConnecting.value = false
            isGenerating.value = false
            scrollToBottom()
            return
        }

        if (isConnecting.value) {
            isConnecting.value = false
            isGenerating.value = true
        }

        currentReply.value += e.data
        scrollToBottom()
    }

    es.onerror = () => {
        es.close()
        isConnecting.value = false
        isGenerating.value = false
        messages.value.push({
            role: 'ai',
            content: '抱歉，连接出现错误。',
            time: new Date().toLocaleTimeString()
        })
        scrollToBottom()
    }
}

const scrollToBottom = () => {
    nextTick(() => {
        if (messageList.value) {
            messageList.value.scrollTop = messageList.value.scrollHeight
        }
    })
}
</script>

<style scoped>
.chat-container {
    /* max-width: 800px;
    margin: 0 auto;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f5f5f5; */
}

h1 {
    text-align: center;
    padding: 20px;
    margin: 0;
    background: white;
    border-bottom: 1px solid #e0e0e0;
    font-size: 20px;
}

/* 消息列表 */
.message-list {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

/* 单条消息 */
.message {
    display: flex;
    gap: 12px;
    max-width: 80%;
}

.message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.message.ai {
    align-self: flex-start;
}

/* 头像 */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
}

/* 消息内容 */
.content {
    background: white;
    color: black;
    padding: 12px 16px;
    border-radius: 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message.user .content {
    background: #007bff;
    color: black;
}

.text {
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}

.time {
    font-size: 12px;
    color: #999;
    margin-top: 4px;
}

.message.user .time {
    color: rgba(255, 255, 255, 0.7);
}

/* Loading 动画 */
.loading-text {
    color: #666;
    font-style: italic;
}

.dots span {
    animation: dots 1.5s infinite;
    display: inline-block;
}

.dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.dots span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes dots {

    0%,
    20% {
        opacity: 0;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

/* 生成中的光标 */
.cursor {
    animation: blink 1s infinite;
    margin-left: 2px;
}

@keyframes blink {

    0%,
    50% {
        opacity: 1;
    }

    51%,
    100% {
        opacity: 0;
    }
}

/* 输入区域 */
.input-area {
    display: flex;
    gap: 12px;
    padding: 20px;
    background: white;
    border-top: 1px solid #e0e0e0;
}

.input-area input {
    flex: 1;
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 24px;
    outline: none;
    font-size: 14px;
    transition: border-color 0.3s;
}

.input-area input:focus {
    border-color: #007bff;
}

.input-area input:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
}

.input-area button {
    padding: 12px 24px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 24px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
}

.input-area button:hover:not(:disabled) {
    background: #0056b3;
}

.input-area button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

/* 滚动条美化 */
.message-list::-webkit-scrollbar {
    width: 6px;
}

.message-list::-webkit-scrollbar-track {
    background: transparent;
}

.message-list::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
}

.message-list::-webkit-scrollbar-thumb:hover {
    background: #999;
}
</style>