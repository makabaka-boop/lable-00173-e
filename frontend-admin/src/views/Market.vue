<template>
  <div class="market-container">

    <!-- 股票列表 -->
    <div class="stocks-section">
      <div class="list-header">
        <span>全部股票 ({{ filteredStocks.length }})</span>
        <div class="sort-buttons">
          <el-button 
            v-for="sort in sortOptions"
            :key="sort.value"
            :type="currentSort === sort.value ? 'primary' : 'default'"
            size="small"
            @click="currentSort = sort.value"
          >
            {{ sort.label }}
          </el-button>
        </div>
      </div>

      <el-table :data="filteredStocks" stripe style="width: 100%" empty-text="暂无数据">
        <el-table-column prop="code" label="代码" min-width="80" />
        <el-table-column prop="name" label="名称" min-width="100" />
        <el-table-column prop="price" label="现价" min-width="80" align="right">
          <template #default="{ row }"><span class="price">{{ formatNumber(row.price, 2) }}</span></template>
        </el-table-column>
        <el-table-column prop="change" label="涨跌" min-width="80" align="right">
          <template #default="{ row }"><span :style="{ color: getPriceColor(row.change) }">{{ getPriceSymbol(row.change) }} {{ formatNumber(Math.abs(row.change), 2) }}</span></template>
        </el-table-column>
        <el-table-column prop="changePercent" label="涨幅" min-width="70" align="right">
          <template #default="{ row }"><span :style="{ color: getPriceColor(row.changePercent) }">{{ formatPercent(row.changePercent) }}</span></template>
        </el-table-column>
        <el-table-column prop="high" label="最高" min-width="70" align="right">
          <template #default="{ row }">{{ formatNumber(row.high, 2) }}</template>
        </el-table-column>
        <el-table-column prop="low" label="最低" min-width="70" align="right">
          <template #default="{ row }">{{ formatNumber(row.low, 2) }}</template>
        </el-table-column>
        <el-table-column prop="volume" label="成交量" min-width="100" align="right">
          <template #default="{ row }">{{ formatLargeNumber(row.volume) }}</template>
        </el-table-column>
        <el-table-column prop="pe" label="市盈率" min-width="70" align="right">
          <template #default="{ row }">{{ formatNumber(row.pe, 2) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="120" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleViewChart(row)">查看</el-button>
            <el-button size="small" @click="handleBuy(row)">买入</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 股票详情抽屉 -->
    <el-drawer v-model="showDetail" title="股票详情" size="50%" @opened="handleDrawerOpened">
      <template v-if="selectedStock">
        <div class="detail-content">
          <div class="detail-header">
            <div class="stock-title">
              <h2>{{ selectedStock.name }}</h2>
              <span class="code">{{ selectedStock.code }}</span>
            </div>
            <div class="price-display">
              <div class="price">{{ formatNumber(selectedStock.price, 2) }}</div>
              <div class="change" :style="{ color: getPriceColor(selectedStock.change) }">
                {{ getPriceSymbol(selectedStock.change) }} {{ formatNumber(Math.abs(selectedStock.change), 2) }}
                ({{ formatPercent(selectedStock.changePercent) }})
              </div>
            </div>
          </div>
          <div class="detail-stats">
            <div class="stat-row">
              <span class="label">最高价</span>
              <span class="value">{{ formatNumber(selectedStock.high, 2) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">最低价</span>
              <span class="value">{{ formatNumber(selectedStock.low, 2) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">成交量</span>
              <span class="value">{{ formatLargeNumber(selectedStock.volume) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">市值</span>
              <span class="value">{{ formatLargeNumber(selectedStock.marketCap) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">市盈率</span>
              <span class="value">{{ formatNumber(selectedStock.pe, 2) }}</span>
            </div>
          </div>
          <div class="chart-section">
            <h3>K线图</h3>
            <Chart ref="chartRef" type="candlestick" :data="marketStore.klineData" />
          </div>
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="handleBuy(selectedStock)">买入</el-button>
            <el-button size="large" @click="showDetail = false">关闭</el-button>
          </div>
        </div>
      </template>
    </el-drawer>

    <!-- 买入对话框 -->
    <el-dialog v-model="showBuyDialog" title="买入" width="500px">
      <template v-if="buyStock">
        <el-form :model="buyForm" label-width="100px">
          <el-form-item label="股票">
            {{ buyStock.name }} ({{ buyStock.code }})
          </el-form-item>
          <el-form-item label="现价">
            {{ formatNumber(buyStock.price, 2) }}
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="buyForm.quantity" :min="1" :step="100" />
          </el-form-item>
          <el-form-item label="总金额">
            {{ formatCurrency(buyForm.quantity * buyStock.price) }}
          </el-form-item>
        </el-form>
      </template>
      <template #footer>
        <el-button @click="showBuyDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmBuy">确认买入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useMarketStore } from '@/stores/market'
import { formatNumber, formatPercent, getPriceColor, getPriceSymbol, formatLargeNumber, formatCurrency } from '@/utils/format'
import { marketAPI, tradingAPI } from '@/utils/api'
import Chart from '@/components/Chart.vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import type { Stock } from '@/types'

const marketStore = useMarketStore()

const searchQuery = ref('')
const currentSort = ref('default')
const showDetail = ref(false)
const showBuyDialog = ref(false)
const selectedStock = ref<Stock | null>(null)
const buyStock = ref<Stock | null>(null)
const buyForm = ref({ quantity: 100 })
const chartRef = ref<InstanceType<typeof Chart>>()

const sortOptions = [
  { label: '默认', value: 'default' },
  { label: '涨幅', value: 'change' },
  { label: '成交量', value: 'volume' },
]

const filteredStocks = computed(() => {
  let result = marketStore.stocks

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(s => 
      s.code.includes(query) || s.name.toLowerCase().includes(query)
    )
  }

  if (currentSort.value === 'change') {
    result = [...result].sort((a, b) => b.changePercent - a.changePercent)
  } else if (currentSort.value === 'volume') {
    result = [...result].sort((a, b) => b.volume - a.volume)
  }

  return result
})

const handleSearch = () => {
  // 搜索逻辑由 computed 处理
}

const handleViewChart = async (stock: Stock) => {
  selectedStock.value = stock
  marketStore.setSelectedStock(stock)
  
  try {
    const response: any = await marketAPI.getKline(stock.code)
    if (response.code === 200) {
      marketStore.setKlineData(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch kline data:', error)
  }
  
  showDetail.value = true
}

// drawer 打开后触发图表 resize
const handleDrawerOpened = () => {
  // 多次尝试 resize，确保图表能够正确自适应
  nextTick(() => {
    setTimeout(() => {
      chartRef.value?.chart?.resize()
    }, 100)
    setTimeout(() => {
      chartRef.value?.chart?.resize()
    }, 300)
    setTimeout(() => {
      chartRef.value?.chart?.resize()
    }, 500)
  })
}

// 监听 K 线数据变化，数据更新后也触发 resize
watch(() => marketStore.klineData, () => {
  if (showDetail.value && chartRef.value?.chart) {
    nextTick(() => {
      setTimeout(() => {
        chartRef.value?.chart?.resize()
      }, 100)
    })
  }
}, { deep: true })

const handleBuy = (stock: Stock) => {
  buyStock.value = stock
  buyForm.value.quantity = 100
  showBuyDialog.value = true
}

const confirmBuy = async () => {
  if (!buyStock.value) return

  try {
    const userId = localStorage.getItem('userId')
    const response: any = await tradingAPI.createOrder({
      user_id: parseInt(userId || '1'),
      code: buyStock.value.code,
      name: buyStock.value.name,
      type: 'buy',
      quantity: buyForm.value.quantity,
      price: buyStock.value.price,
      totalAmount: buyForm.value.quantity * buyStock.value.price,
    })

    if (response.code === 200) {
      showBuyDialog.value = false
      ElMessage.success('买入成功')
    } else {
      ElMessage.error(response.message || '买入失败')
    }
  } catch (error) {
    ElMessage.error('买入失败，请重试')
  }
}

onMounted(async () => {
  try {
    const response: any = await marketAPI.getStocks()
    if (response.code === 200) {
      marketStore.setStocks(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch stocks:', error)
    ElMessage.error('获取股票列表失败')
  }
})
</script>

<style scoped lang="scss">
.market-container {
  padding: 24px;
}

.search-bar {
  max-width: 400px;
}

.stocks-section {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);

  span {
    font-weight: 500;
    color: var(--el-text-color-primary);
  }
}

.sort-buttons {
  display: flex;
  gap: 8px;
}

.price {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.detail-content {
  padding: 16px 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.stock-title {
  h2 {
    margin: 0 0 8px 0;
    font-size: 24px;
    color: var(--el-text-color-primary);
  }

  .code {
    color: var(--el-text-color-regular);
    font-size: 12px;
  }
}

.price-display {
  text-align: right;

  .price {
    font-size: 28px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }

  .change {
    font-size: 14px;
    margin-top: 4px;
  }
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 4px;

  .label {
    color: var(--el-text-color-regular);
  }

  .value {
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.chart-section {
  margin-bottom: 24px;
  width: 100%;
  overflow: hidden;

  h3 {
    margin-bottom: 16px;
    font-size: 16px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }

  :deep(.chart-container) {
    width: 100%;
    height: 400px;
    min-height: 400px;
  }
}

.action-buttons {
  display: flex;
  gap: 12px;

  :deep(.el-button) {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .market-container {
    padding: 16px;
  }

  .stocks-section {
    padding: 16px;
  }

  .detail-stats {
    grid-template-columns: 1fr;
  }
}
</style>
