<template>
  <div class="trading-container">

    <el-tabs v-model="activeTab">
      <!-- 待处理订单 -->
      <el-tab-pane label="待处理订单" name="pending">
        <div class="tab-content">
          <el-table :data="pendingOrders" stripe style="width: 100%" empty-text="暂无数据" :border="false">
            <el-table-column prop="code" label="代码" min-width="100" />
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="type" label="类型" min-width="80" align="center">
              <template #default="{ row }">
                <el-tag :type="row.type === 'buy' ? 'danger' : 'success'">
                  {{ row.type === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" min-width="100" align="right" />
            <el-table-column prop="price" label="价格" min-width="100" align="right">
              <template #default="{ row }">
                {{ formatNumber(row.price, 2) }}
              </template>
            </el-table-column>
            <el-table-column prop="totalAmount" label="金额" min-width="120" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.totalAmount) }}
              </template>
            </el-table-column>
            <el-table-column prop="timestamp" label="下单时间" min-width="180">
              <template #default="{ row }">
                {{ formatDate(row.timestamp) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" min-width="150" align="center">
              <template #default="{ row }">
                <el-button type="success" size="small" @click="executeOrder(row)">
                  成交
                </el-button>
                <el-button type="danger" size="small" @click="cancelOrder(row)">
                  撤销
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 已成交订单 -->
      <el-tab-pane label="已成交订单" name="completed">
        <div class="tab-content">
          <el-table :data="completedOrders" stripe style="width: 100%" empty-text="暂无数据" :border="false">
            <el-table-column prop="code" label="代码" min-width="100" />
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="type" label="类型" min-width="80" align="center">
              <template #default="{ row }">
                <el-tag :type="row.type === 'buy' ? 'danger' : 'success'">
                  {{ row.type === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" min-width="100" align="right" />
            <el-table-column prop="price" label="价格" min-width="100" align="right">
              <template #default="{ row }">
                {{ formatNumber(row.price, 2) }}
              </template>
            </el-table-column>
            <el-table-column prop="totalAmount" label="金额" min-width="120" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.totalAmount) }}
              </template>
            </el-table-column>
            <el-table-column prop="executedTime" label="成交时间" min-width="180">
              <template #default="{ row }">
                {{ formatDate(row.executedTime || row.timestamp) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <!-- 已撤销订单 -->
      <el-tab-pane label="已撤销订单" name="cancelled">
        <div class="tab-content">
          <el-table :data="cancelledOrders" stripe style="width: 100%" empty-text="暂无数据" :border="false">
            <el-table-column prop="code" label="代码" min-width="100" />
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="type" label="类型" min-width="80" align="center">
              <template #default="{ row }">
                <el-tag :type="row.type === 'buy' ? 'danger' : 'success'">
                  {{ row.type === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" min-width="100" align="right" />
            <el-table-column prop="price" label="价格" min-width="100" align="right">
              <template #default="{ row }">
                {{ formatNumber(row.price, 2) }}
              </template>
            </el-table-column>
            <el-table-column prop="totalAmount" label="金额" min-width="120" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.totalAmount) }}
              </template>
            </el-table-column>
            <el-table-column prop="timestamp" label="下单时间" min-width="180">
              <template #default="{ row }">
                {{ formatDate(row.timestamp) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 新建订单 -->
    <div class="new-order-section">
      <h2>新建订单</h2>
      <el-form :model="newOrder" label-width="100px">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="股票代码">
              <el-input v-model="newOrder.code" placeholder="输入股票代码" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="交易类型">
              <el-select v-model="newOrder.type">
                <el-option label="买入" value="buy" />
                <el-option label="卖出" value="sell" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="数量">
              <el-input-number v-model="newOrder.quantity" :min="1" :step="100" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="6">
            <el-form-item label="价格">
              <el-input-number v-model="newOrder.price" :min="0.01" :step="0.01" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="submitOrder">提交订单</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useTradingStore } from '@/stores/trading'
import { formatNumber, formatCurrency, formatDate } from '@/utils/format'
import { tradingAPI } from '@/utils/api'
import { ElMessage } from 'element-plus'
import type { Order } from '@/types'

const tradingStore = useTradingStore()
const activeTab = ref('pending')

const newOrder = ref({
  code: '',
  type: 'buy' as 'buy' | 'sell',
  quantity: 100,
  price: 0,
})

const pendingOrders = computed(() => 
  tradingStore.orders.filter(o => o.status === 'pending')
)

const completedOrders = computed(() => 
  tradingStore.orders.filter(o => o.status === 'completed')
)

const cancelledOrders = computed(() => 
  tradingStore.orders.filter(o => o.status === 'cancelled')
)

const executeOrder = async (order: Order) => {
  try {
    const response = await tradingAPI.executeOrder(parseInt(order.id))
    if (response.code === 200) {
      tradingStore.updateOrder(order.id, {
        status: 'completed',
        executedTime: Date.now(),
      })
      ElMessage.success('订单已成交')
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const cancelOrder = async (order: Order) => {
  try {
    const response = await tradingAPI.cancelOrder(parseInt(order.id))
    if (response.code === 200) {
      tradingStore.cancelOrder(order.id)
      ElMessage.success('订单已撤销')
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const submitOrder = async () => {
  if (!newOrder.value.code) {
    ElMessage.error('请输入股票代码')
    return
  }

  try {
    const userId = localStorage.getItem('userId')
    const response = await tradingAPI.createOrder({
      user_id: parseInt(userId || '1'),
      code: newOrder.value.code,
      name: '股票名称',
      type: newOrder.value.type,
      quantity: newOrder.value.quantity,
      price: newOrder.value.price,
      totalAmount: newOrder.value.quantity * newOrder.value.price,
    })

    if (response.code === 200) {
      resetForm()
      ElMessage.success('订单已提交')
      // 刷新订单列表
      await fetchOrders()
    } else {
      ElMessage.error(response.message || '提交失败')
    }
  } catch (error) {
    ElMessage.error('提交失败，请重试')
  }
}

const fetchOrders = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response = await tradingAPI.getOrders(parseInt(userId || '1'))
    if (response.code === 200) {
      tradingStore.setOrders(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch orders:', error)
  }
}

const resetForm = () => {
  newOrder.value = {
    code: '',
    type: 'buy',
    quantity: 100,
    price: 0,
  }
}

onMounted(async () => {
  await fetchOrders()
})
</script>

<style scoped lang="scss">
.trading-container {
  padding: 24px;
}


.tab-content {
  padding: 24px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.new-order-section {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 24px;
  margin-top: 24px;
  box-shadow: var(--shadow-sm);

  h2 {
    font-size: 18px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin-bottom: 16px;
  }
}

:deep(.el-tabs) {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 0;
  box-shadow: var(--shadow-sm);

  .el-tabs__header {
    border-bottom: 1px solid var(--el-border-color-light);
    padding: 0 24px;
  }

  .el-tabs__nav-scroll {
    padding: 0;
  }

  .el-tabs__content {
    padding: 0;
  }

  .el-table {
    border: none !important;
  }

  .el-table__header-wrapper {
    border: none !important;
  }

  .el-table__body-wrapper {
    border: none !important;
  }
}

@media (max-width: 768px) {
  .trading-container {
    padding: 16px;
  }

  .new-order-section {
    padding: 16px;
  }
}
</style>
