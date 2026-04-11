<template>
  <div style="max-width: 600px; margin: 20px auto; font-family: sans-serif;">
    <h2>AI 聊天（记忆版）</h2>
    <p>Session: {{ sid }}</p>
    
    <div style="border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px;">
      <div v-for="(m, i) in msgs" :key="i" style="margin: 10px 0; padding: 8px; background: #f0f0f0; border-radius: 4px;">
        <b>{{ m.role === 'user' ? '你' : 'AI' }}:</b> {{ m.content }}
      </div>
      <div v-if="reply" style="margin: 10px 0; padding: 8px; background: #e3f2fd; border-radius: 4px;">
        <b>AI:</b> {{ reply }}<span class="cursor">|</span>
      </div>
    </div>
    
    <div style="display: flex; gap: 10px;">
      <input v-model="text" @keyup.enter="send" style="flex: 1; padding: 8px;" placeholder="输入消息..." />
      <button @click="send" :disabled="loading">{{ loading ? '发送中' : '发送' }}</button>
      <button @click="clear" style="background: #ff4444; color: white;">清空</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const msgs = ref([])
const text = ref('')
const reply = ref('')
const loading = ref(false)
const sid = ref('')

onMounted(() => {
  sid.value = localStorage.getItem('sid') || 's' + Date.now()
  localStorage.setItem('sid', sid.value)
})

const send = () => {
  if (!text.value.trim() || loading.value) return
  
  msgs.value.push({ role: 'user', content: text.value })
  
  const currentMsg = text.value
  text.value = ''
  reply.value = ''
  loading.value = true
  
  let isDone = false
  let hasAdded = false
  
  const addMessage = (content) => {
    if (!hasAdded) {
      hasAdded = true
      msgs.value.push({ role: 'ai', content })
      reply.value = ''
      loading.value = false
    }
  }
  
  const es = new EventSource(
    `http://localhost:8000/chat/memory/stream?msg=${encodeURIComponent(currentMsg)}&session_id=${sid.value}`
  )
  
  es.onmessage = (e) => {
    const data = e.data
    
    if (data === '[DONE]') {
      isDone = true
      es.close()
      addMessage(reply.value || '（无回复）')
      return
    }
    
    if (data.startsWith('[ERROR]')) {
      isDone = true
      es.close()
      addMessage('抱歉，服务出错')
      return
    }
    
    reply.value += data
  }
  
  // 关键：延迟处理 onerror，给 onmessage 处理 [DONE] 的机会
  es.onerror = () => {
    es.close()
    setTimeout(() => {
      // 如果 100ms 后还没完成，才显示错误
      if (!isDone && !hasAdded) {
        addMessage('连接出错，请重试')
      }
    }, 100)
  }
}

const clear = async () => {
  await fetch(`http://localhost:8000/chat/memory/clear?session_id=${sid.value}`, { method: 'POST' })
  msgs.value = []
  sid.value = 's' + Date.now()
  localStorage.setItem('sid', sid.value)
}
</script>

<style scoped>
.cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
</style>
