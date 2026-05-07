<template>
  <div class="positions-container">
    <div class="positions-header">
      <div class="header-stats">
        <div class="stat">
          <span class="label">总市值</span>
          <span class="value">{{ formatCurrency(totalMarketValue) }}</span>
        </div>
        <div class="stat">
          <span class="label">总收益</span>
          <span class="value" :style="{ color: getPriceColor(totalProfit) }">
            {{ formatCurrency(totalProfit) }}
          </span>
        </div>
        <div class="stat">
          <span class="label">收益率</span>
          <span class="value" :style="{ color: getPriceColor(totalProfitPercent) }">
            {{ formatPercent(totalProfitPercent) }}
          </span>
        </div>
      </div>
    </div>

    <!-- 持仓列表 -->
    <div class="positions-list">
      <el-table :data="filteredPositions" stripe style="width: 100%" empty-text="暂无数据">
        <el-table-column prop="code" label="代码" min-width="100" />
        <el-table-column prop="name" label="名称" min-width="120" />
        <el-table-column prop="quantity" label="持仓数量" min-width="120" align="right" />
        <el-table-column prop="costPrice" label="成本价" min-width="100" align="right">
          <template #default="{ row }">
            {{ formatNumber(row.costPrice, 2) }}
          </template>
        </el-table-column>
        <el-table-column prop="currentPrice" label="现价" min-width="100" align="right">
          <template #default="{ row }">
            {{ formatNumber(row.currentPrice, 2) }}
          </template>
        </el-table-column>
        <el-table-column prop="marketValue" label="市值" min-width="120" align="right">
          <template #default="{ row }">
            {{ formatCurrency(row.marketValue) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="收益" min-width="120" align="right">
          <template #default="{ row }">
            <span :style="{ color: getPriceColor(row.profit) }">
              {{ formatCurrency(row.profit) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="profitPercent" label="收益率" min-width="100" align="right">
          <template #default="{ row }">
            <span :style="{ color: getPriceColor(row.profitPercent) }">
              {{ formatPercent(row.profitPercent) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="150" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleAddPosition(row)">
              加仓
            </el-button>
            <el-button type="danger" size="small" @click="handleReducePosition(row)">
              减仓
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 加仓/减仓对话框 -->
    <el-dialog v-model="showDialog" :title="dialogTitle" width="500px">
      <template v-if="selectedPosition">
        <el-form :model="positionForm" label-width="100px">
          <el-form-item label="股票">
            {{ selectedPosition.name }} ({{ selectedPosition.code }})
          </el-form-item>
          <el-form-item label="现价">
            {{ formatNumber(selectedPosition.currentPrice, 2) }}
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="positionForm.quantity" :min="1" :step="100" />
          </el-form-item>
          <el-form-item label="总金额">
            {{ formatCurrency(positionForm.quantity * selectedPosition.currentPrice) }}
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmOperation">
          {{ operationType === 'add' ? '确认加仓' : '确认减仓' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { formatNumber, formatCurrency, formatPercent, getPriceColor } from '@/utils/format'
import { positionsAPI } from '@/utils/api'
import { ElMessage } from 'element-plus'
import type { Position } from '@/types'

const userStore = useUserStore()

const showDialog = ref(false)
const selectedPosition = ref<Position | null>(null)
const operationType = ref<'add' | 'reduce'>('add')
const positionForm = ref({ quantity: 100 })

const filteredPositions = computed(() => {
  return userStore.positions.filter(p => p.quantity > 0)
})

const totalMarketValue = computed(() => {
  return filteredPositions.value.reduce((sum, p) => sum + p.marketValue, 0)
})

const totalProfit = computed(() => {
  return filteredPositions.value.reduce((sum, p) => sum + p.profit, 0)
})

const totalProfitPercent = computed(() => {
  if (totalMarketValue.value === 0) return 0
  return (totalProfit.value / (totalMarketValue.value - totalProfit.value)) * 100
})

const dialogTitle = computed(() => {
  return operationType.value === 'add' ? '加仓' : '减仓'
})

const handleAddPosition = (position: Position) => {
  selectedPosition.value = position
  operationType.value = 'add'
  positionForm.value.quantity = 100
  showDialog.value = true
}

const handleReducePosition = (position: Position) => {
  selectedPosition.value = position
  operationType.value = 'reduce'
  positionForm.value.quantity = Math.min(100, position.quantity)
  showDialog.value = true
}

const confirmOperation = async () => {
  if (!selectedPosition.value) return

  if (operationType.value === 'reduce' && positionForm.value.quantity > selectedPosition.value.quantity) {
    ElMessage.error('减仓数量不能超过持仓数量')
    return
  }

  try {
    let newQuantity = selectedPosition.value.quantity
    
    if (operationType.value === 'add') {
      newQuantity += positionForm.value.quantity
    } else {
      newQuantity -= positionForm.value.quantity
    }

    const response: any = await positionsAPI.updatePosition(selectedPosition.value.id, {
      quantity: newQuantity,
      cost_price: selectedPosition.value.costPrice,
      current_price: selectedPosition.value.currentPrice,
    })
    
    if (response.code === 200) {
      const message = operationType.value === 'add' ? '加仓成功' : '减仓成功'
      ElMessage.success(message)
      showDialog.value = false
      // 刷新持仓列表
      await fetchPositions()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const fetchPositions = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response: any = await positionsAPI.getPositions(parseInt(userId || '1'))
    if (response.code === 200) {
      userStore.setPositions(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch positions:', error)
  }
}

onMounted(async () => {
  await fetchPositions()
})
</script>

<style scoped lang="scss">
.positions-container {
  padding: 24px;
}

.positions-header {
  margin-bottom: 24px;

  h1 {
    font-size: 28px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin-bottom: 16px;
  }
}

.header-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat {
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-sm);

  .label {
    color: var(--el-text-color-regular);
    font-size: 12px;
  }

  .value {
    font-size: 20px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.positions-list {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

@media (max-width: 768px) {
  .positions-container {
    padding: 16px;
  }

  .header-stats {
    grid-template-columns: 1fr;
  }

  .positions-list {
    padding: 16px;
  }
}
</style>
