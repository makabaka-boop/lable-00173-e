<template>
  <div class="stock-card" @click="handleClick">
    <div class="card-header">
      <div class="stock-info">
        <div class="stock-code">{{ stock.code }}</div>
        <div class="stock-name">{{ stock.name }}</div>
      </div>
      <div class="price-info">
        <div class="current-price">{{ formatNumber(stock.price, 2) }}</div>
        <div class="change" :style="{ color: getPriceColor(stock.change) }">
          {{ getPriceSymbol(stock.change) }} {{ formatNumber(Math.abs(stock.change), 2) }}
          ({{ formatPercent(stock.changePercent) }})
        </div>
      </div>
    </div>

    <div class="card-body">
      <div class="stat-item">
        <span class="label">最高</span>
        <span class="value">{{ formatNumber(stock.high, 2) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">最低</span>
        <span class="value">{{ formatNumber(stock.low, 2) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">成交量</span>
        <span class="value">{{ formatLargeNumber(stock.volume) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">市值</span>
        <span class="value">{{ formatLargeNumber(stock.marketCap) }}</span>
      </div>
    </div>

    <div class="card-footer">
      <el-button type="primary" size="small" @click.stop="handleBuy">买入</el-button>
      <el-button size="small" @click.stop="handleSell">卖出</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Stock } from '@/types'
import { formatNumber, formatPercent, getPriceColor, getPriceSymbol, formatLargeNumber } from '@/utils/format'

defineProps<{
  stock: Stock
}>()

const emit = defineEmits<{
  buy: [stock: Stock]
  sell: [stock: Stock]
  click: [stock: Stock]
}>()

const handleBuy = () => {
  emit('buy', props.stock)
}

const handleSell = () => {
  emit('sell', props.stock)
}

const handleClick = () => {
  emit('click', props.stock)
}

const props = defineProps<{
  stock: Stock
}>()
</script>

<style scoped lang="scss">
.stock-card {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--el-color-primary);
    transform: translateY(-2px);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.stock-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stock-code {
  font-weight: 600;
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.stock-name {
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.price-info {
  text-align: right;
}

.current-price {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.change {
  font-size: 12px;
  margin-top: 4px;
}

.card-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: var(--el-fill-color-lighter);
  border-radius: 4px;
}

.label {
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.value {
  color: var(--el-text-color-primary);
  font-weight: 500;
  font-size: 12px;
}

.card-footer {
  display: flex;
  gap: 8px;

  :deep(.el-button) {
    flex: 1;
  }
}
</style>
