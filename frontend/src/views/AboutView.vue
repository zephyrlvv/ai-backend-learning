<template>
    <div class="month-picker-demo">
        <h3>月度趋势选择器</h3>

        <el-date-picker 
            v-model="secondDate" 
            type="monthrange" 
            range-separator="至" 
            start-placeholder="开始月份"
            end-placeholder="结束月份" 
            value-format="YYYY-MM"
            :disabled-date="disabledDate"
            @calendar-change="handleCalendarChange"
            @change="handleChange"
            @visible-change="handleVisibleChange"
        />

        <div class="info">
            <p>当前选择：{{ secondDate || '未选择' }}</p>
            <p>选择中：{{ tempDate ? formatDate(tempDate) : '无' }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const secondDate = ref([])
const tempDate = ref(null)  // 当前正在选择的日期

const formatDate = (date) => {
    if (!date) return 'null'
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`
}

const getYearMonth = (date) => {
    return date.getFullYear() * 100 + date.getMonth()
}

// 解析 YYYY-MM 字符串为 Date
const parseDateStr = (str) => {
    if (!str) return null
    const [y, m] = str.split('-').map(Number)
    return new Date(y, m - 1, 1)
}

// 关键修复：监听面板展开/收起
const handleVisibleChange = (visible) => {
    console.log('visible-change:', visible)
    if (visible) {
        // 面板展开时，如果已有选择，用第一个作为锚点
        if (secondDate.value && secondDate.value.length > 0) {
            tempDate.value = parseDateStr(secondDate.value[0])
            console.log('面板展开，设置锚点:', formatDate(tempDate.value))
        }
    } else {
        // 面板收起时，如果完成了选择，重置 tempDate
        if (secondDate.value && secondDate.value.length === 2) {
            tempDate.value = null
            console.log('面板收起，重置')
        }
    }
}

const handleCalendarChange = (dates) => {
    console.log('calendar-change:', dates)
    
    if (dates && dates[0]) {
        tempDate.value = dates[0]
    } else {
        tempDate.value = null
    }
}

const handleChange = (val) => {
    console.log('change:', val)
    if (!val || val.length === 0) {
        // 清空操作
        secondDate.value = []
        tempDate.value = null
        console.log('已清空')
    }
}

const disabledDate = (time) => {
    const year = time.getFullYear()
    const timeYM = getYearMonth(time)
    const nowYM = getYearMonth(new Date())
    
    // 1. 禁用 2013 年之前
    if (year < 2013) return true
    
    // 2. 禁用未来月份
    if (timeYM > nowYM) return true
    
    // 3. 如果有锚点日期，限制±12个月
    if (tempDate.value) {
        const y = tempDate.value.getFullYear()
        const m = tempDate.value.getMonth()
        
        const minDate = new Date(y, m - 12, 1)
        const maxDate = new Date(y, m + 12, 1)
        
        const minYM = getYearMonth(minDate)
        const maxYM = getYearMonth(maxDate)
        
        if (timeYM < minYM || timeYM > maxYM) {
            return true
        }
    }
    
    return false
}
</script>

<style scoped>
.month-picker-demo {
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
}

.info {
    margin-top: 20px;
    padding: 15px;
    background: #f5f7fa;
    border-radius: 4px;
}
</style>
