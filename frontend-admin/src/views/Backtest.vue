<template>
  <div class="backtest-container">

    <el-tabs v-model="activeTab">
      <!-- 新建回测 -->
      <el-tab-pane label="新建回测" name="create">
        <div class="create-form">
          <el-form :model="backtestParams" label-width="120px">
            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="回测名称">
                  <el-input v-model="backtestParams.name" placeholder="输入回测名称" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="股票代码">
                  <el-input v-model="backtestParams.code" placeholder="输入股票代码" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="开始日期">
                  <el-date-picker
                    v-model="backtestParams.startDate"
                    type="date"
                    placeholder="选择开始日期"
                    format="YYYY-MM-DD"
                    value-format="x"
                  />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="结束日期">
                  <el-date-picker
                    v-model="backtestParams.endDate"
                    type="date"
                    placeholder="选择结束日期"
                    format="YYYY-MM-DD"
                    value-format="x"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="初始资金">
                  <el-input-number v-model="backtestParams.initialCapital" :min="1000" :step="10000" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="策略类型">
                  <el-select v-model="backtestParams.strategy">
                    <el-option label="均线策略" value="ma" />
                    <el-option label="RSI策略" value="rsi" />
                    <el-option label="MACD策略" value="macd" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="策略参数">
              <div class="params-grid">
                <div class="param-item">
                  <span class="param-label">快速周期</span>
                  <el-input-number v-model="backtestParams.parameters.fast" :min="1" :step="1" />
                </div>
                <div class="param-item">
                  <span class="param-label">慢速周期</span>
                  <el-input-number v-model="backtestParams.parameters.slow" :min="1" :step="1" />
                </div>
                <div class="param-item">
                  <span class="param-label">信号周期</span>
                  <el-input-number v-model="backtestParams.parameters.signal" :min="1" :step="1" />
                </div>
              </div>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" @click="startBacktest">
                开始回测
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <!-- 回测结果 -->
      <el-tab-pane label="回测结果" name="results">
        <div class="results-section">
          <div class="results-grid">
            <div 
              v-for="result in backtestStore.results"
              :key="result.id"
              class="result-card"
              @click="viewResult(result)"
            >
              <div class="result-header">
                <h3>{{ result.name }}</h3>
                <el-tag :type="result.status === 'completed' ? 'success' : 'info'">
                  {{ result.status === 'completed' ? '已完成' : '运行中' }}
                </el-tag>
              </div>

              <div class="result-stats">
                <div class="stat-row">
                  <span class="label">初始资金</span>
                  <span class="value">{{ formatCurrency(result.initialCapital) }}</span>
                </div>
                <div class="stat-row">
                  <span class="label">最终资金</span>
                  <span class="value">{{ formatCurrency(result.finalCapital) }}</span>
                </div>
                <div class="stat-row">
                  <span class="label">总收益</span>
                  <span class="value" :style="{ color: getPriceColor(result.totalReturn) }">
                    {{ formatCurrency(result.totalReturn) }}
                  </span>
                </div>
                <div class="stat-row">
                  <span class="label">收益率</span>
                  <span class="value" :style="{ color: getPriceColor(result.returnPercent) }">
                    {{ formatPercent(result.returnPercent) }}
                  </span>
                </div>
                <div class="stat-row">
                  <span class="label">最大回撤</span>
                  <span class="value">{{ formatPercent(result.maxDrawdown) }}</span>
                </div>
                <div class="stat-row">
                  <span class="label">夏普比率</span>
                  <span class="value">{{ formatNumber(result.sharpeRatio, 2) }}</span>
                </div>
                <div class="stat-row">
                  <span class="label">胜率</span>
                  <span class="value">{{ formatPercent(result.winRate) }}</span>
                </div>
                <div class="stat-row">
                  <span class="label">交易次数</span>
                  <span class="value">{{ result.totalTrades }}</span>
                </div>
              </div>

              <div class="result-footer">
                <span class="time">{{ formatDate(result.createdAt, 'YYYY-MM-DD') }}</span>
                <el-button type="primary" size="small" @click.stop="viewResult(result)">
                  查看详情
                </el-button>
              </div>
            </div>
          </div>

          <el-empty v-if="backtestStore.results.length === 0" description="暂无回测结果" />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 详情对话框 -->
    <el-dialog v-model="showDetail" title="回测详情" width="900px">
      <template v-if="backtestStore.currentResult">
        <div class="detail-content">
          <h3>{{ backtestStore.currentResult.name }}</h3>

          <div class="detail-stats">
            <div class="stat-group">
              <div class="stat-item">
                <span class="label">初始资金</span>
                <span class="value">{{ formatCurrency(backtestStore.currentResult.initialCapital) }}</span>
              </div>
              <div class="stat-item">
                <span class="label">最终资金</span>
                <span class="value">{{ formatCurrency(backtestStore.currentResult.finalCapital) }}</span>
              </div>
              <div class="stat-item">
                <span class="label">总收益</span>
                <span class="value" :style="{ color: getPriceColor(backtestStore.currentResult.totalReturn) }">
                  {{ formatCurrency(backtestStore.currentResult.totalReturn) }}
                </span>
              </div>
              <div class="stat-item">
                <span class="label">收益率</span>
                <span class="value" :style="{ color: getPriceColor(backtestStore.currentResult.returnPercent) }">
                  {{ formatPercent(backtestStore.currentResult.returnPercent) }}
                </span>
              </div>
            </div>

            <div class="stat-group">
              <div class="stat-item">
                <span class="label">最大回撤</span>
                <span class="value">{{ formatPercent(backtestStore.currentResult.maxDrawdown) }}</span>
              </div>
              <div class="stat-item">
                <span class="label">夏普比率</span>
                <span class="value">{{ formatNumber(backtestStore.currentResult.sharpeRatio, 2) }}</span>
              </div>
              <div class="stat-item">
                <span class="label">胜率</span>
                <span class="value">{{ formatPercent(backtestStore.currentResult.winRate) }}</span>
              </div>
              <div class="stat-item">
                <span class="label">交易次数</span>
                <span class="value">{{ backtestStore.currentResult.totalTrades }}</span>
              </div>
            </div>

            <div class="stat-group">
              <div class="stat-item">
                <span class="label">盈利交易</span>
                <span class="value">{{ backtestStore.currentResult.profitableTrades }}</span>
              </div>
              <div class="stat-item">
                <span class="label">亏损交易</span>
                <span class="value">{{ backtestStore.currentResult.totalTrades - backtestStore.currentResult.profitableTrades }}</span>
              </div>
              <div class="stat-item">
                <span class="label">回测周期</span>
                <span class="value">{{ formatDate(backtestStore.currentResult.startDate, 'YYYY-MM-DD') }} 至 {{ formatDate(backtestStore.currentResult.endDate, 'YYYY-MM-DD') }}</span>
              </div>
            </div>
          </div>

          <div class="chart-section">
            <h4>交易统计</h4>
            <div class="stats-table">
              <div class="stats-row">
                <span class="label">总交易次数</span>
                <span class="value">{{ backtestStore.currentResult.totalTrades }}</span>
              </div>
              <div class="stats-row">
                <span class="label">盈利交易</span>
                <span class="value" style="color: #67c23a">{{ backtestStore.currentResult.profitableTrades }}</span>
              </div>
              <div class="stats-row">
                <span class="label">亏损交易</span>
                <span class="value" style="color: #f56c6c">{{ backtestStore.currentResult.totalTrades - backtestStore.currentResult.profitableTrades }}</span>
              </div>
              <div class="stats-row">
                <span class="label">胜率</span>
                <span class="value">{{ formatPercent(backtestStore.currentResult.winRate) }}</span>
              </div>
              <div class="stats-row">
                <span class="label">最大回撤</span>
                <span class="value">{{ formatPercent(backtestStore.currentResult.maxDrawdown) }}</span>
              </div>
              <div class="stats-row">
                <span class="label">夏普比率</span>
                <span class="value">{{ formatNumber(backtestStore.currentResult.sharpeRatio, 2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <el-button type="danger" @click="deleteResult">删除</el-button>
        <el-button @click="showDetail = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBacktestStore } from '@/stores/backtest'
import { formatCurrency, formatNumber, formatPercent, formatDate, getPriceColor } from '@/utils/format'
import { backtestAPI } from '@/utils/api'
import Chart from '@/components/Chart.vue'
import { ElMessage } from 'element-plus'
import type { BacktestParams, BacktestResult } from '@/types'

const backtestStore = useBacktestStore()
const activeTab = ref('create')
const showDetail = ref(false)

const backtestParams = ref<BacktestParams>({
  name: '',
  code: '',
  startDate: Date.now() - 365 * 86400000,
  endDate: Date.now(),
  initialCapital: 100000,
  strategy: 'ma',
  parameters: {
    fast: 12,
    slow: 26,
    signal: 9,
  },
})

const startBacktest = async () => {
  if (!backtestParams.value.name || !backtestParams.value.code) {
    ElMessage.error('请填写回测名称和股票代码')
    return
  }

  try {
    const userId = localStorage.getItem('userId')
    const response: any = await backtestAPI.runBacktest({
      user_id: parseInt(userId || '1'),
      name: backtestParams.value.name,
      code: backtestParams.value.code,
      strategy: backtestParams.value.strategy,
      parameters: backtestParams.value.parameters,
      startDate: backtestParams.value.startDate,
      endDate: backtestParams.value.endDate,
      initialCapital: backtestParams.value.initialCapital,
    })

    if (response.code === 200) {
      backtestStore.addResult(response.data)
      resetForm()
      ElMessage.success('回测已提交')
      activeTab.value = 'results'
    } else {
      ElMessage.error(response.message || '提交失败')
    }
  } catch (error) {
    ElMessage.error('提交失败，请重试')
  }
}

const resetForm = () => {
  backtestParams.value = {
    name: '',
    code: '',
    startDate: Date.now() - 365 * 86400000,
    endDate: Date.now(),
    initialCapital: 100000,
    strategy: 'ma',
    parameters: {
      fast: 12,
      slow: 26,
      signal: 9,
    },
  }
}

const viewResult = (result: BacktestResult) => {
  backtestStore.setCurrentResult(result)
  showDetail.value = true
}


const deleteResult = async () => {
  if (backtestStore.currentResult) {
    try {
      const response: any = await backtestAPI.deleteBacktest(parseInt(backtestStore.currentResult.id.toString()))
      if (response.code === 200) {
        backtestStore.deleteResult(backtestStore.currentResult.id.toString())
        showDetail.value = false
        ElMessage.success('已删除')
        // 重新获取回测结果列表
        await fetchBacktestResults()
      } else {
        ElMessage.error(response.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败，请重试')
    }
  }
}

const fetchBacktestResults = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const response: any = await backtestAPI.getResults(parseInt(userId || '1'))
    if (response.code === 200) {
      backtestStore.setResults(response.data)
    }
  } catch (error) {
    console.error('Failed to fetch backtest results:', error)
  }
}

onMounted(async () => {
  await fetchBacktestResults()
})
</script>

<style scoped lang="scss">
.backtest-container {
  padding: 24px;
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
}

.create-form {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 24px;
  margin-top: 0;
  box-shadow: none;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 8px;

  .param-label {
    font-size: 12px;
    color: var(--el-text-color-regular);
  }
}

.results-section {
  padding: 24px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.result-card {
  background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--el-border-color-light);

  h3 {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.result-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;

  .label {
    color: var(--el-text-color-regular);
  }

  .value {
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.result-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-light);

  .time {
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

.detail-content {
  padding: 0;

  h3 {
    font-size: 18px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin-top: 16px;
    margin-bottom: 16px;
  }

  h4 {
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin-bottom: 12px;
  }
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-group {
  background: var(--el-fill-color-light);
  border-radius: 8px;
  padding: 12px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;

  .label {
    font-size: 12px;
    color: var(--el-text-color-regular);
  }

  .value {
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.chart-section {
  margin-bottom: 24px;

  h4 {
    margin-bottom: 16px;
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.stats-table {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.stats-row {
  background: var(--el-fill-color-lighter);
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;

  .label {
    font-size: 12px;
    color: var(--el-text-color-regular);
  }

  .value {
    font-size: 16px;
    font-weight: 600;
    color: var(--el-text-color-primary);
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
  .backtest-container {
    padding: 16px;
  }

  .create-form {
    padding: 16px;
  }

  .results-grid {
    grid-template-columns: 1fr;
  }

  .detail-stats {
    grid-template-columns: 1fr;
  }
}
</style>
