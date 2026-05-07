<template>
  <div class="chart-container" ref="chartRef"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'

interface Props {
  type: 'line' | 'candlestick' | 'bar'
  data: any[]
  options?: Record<string, any>
}

const props = withDefaults(defineProps<Props>(), { type: 'line' })
const chartRef = ref<HTMLElement>()
let chart: ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return
  const baseOption: any = {
    responsive: true,
    grid: { left: '10%', right: '10%', top: '10%', bottom: '10%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: props.data.map(d => new Date(d.time).toLocaleDateString()),
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#d0d0d0' } },
    },
    yAxis: { 
      type: 'value',
      axisLine: { lineStyle: { color: '#d0d0d0' } },
      splitLine: { lineStyle: { color: '#f0f0f0' } },
    },
    tooltip: { 
      trigger: 'axis', 
      backgroundColor: 'rgba(0, 0, 0, 0.8)', 
      borderColor: 'transparent', 
      textStyle: { color: '#fff' },
      formatter: (params: any) => {
        if (Array.isArray(params) && params.length > 0) {
          const data = params[0].data
          if (props.type === 'candlestick') {
            return `开: ${data[0].toFixed(2)}<br/>收: ${data[1].toFixed(2)}<br/>低: ${data[2].toFixed(2)}<br/>高: ${data[3].toFixed(2)}`
          }
        }
        return ''
      }
    },
    ...props.options,
  }

  if (props.type === 'line') {
    baseOption.series = [{
      data: props.data.map(d => d.close),
      type: 'line',
      smooth: true,
      itemStyle: { color: '#0066cc' },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(0, 102, 204, 0.3)' },
        { offset: 1, color: 'rgba(0, 102, 204, 0)' },
      ]) },
    }]
  } else if (props.type === 'candlestick') {
    baseOption.series = [{
      data: props.data.map(d => [d.open, d.close, d.low, d.high]),
      type: 'candlestick',
      itemStyle: { 
        color: '#ff4d4f', 
        color0: '#00b96b', 
        borderColor: '#ff4d4f', 
        borderColor0: '#00b96b',
        borderWidth: 1,
      },
      markPoint: undefined,
      markLine: {
        data: [
          { type: 'average', name: '平均值' }
        ],
        label: {
          formatter: (params: any) => {
            return params.value?.toFixed(2) || ''
          }
        }
      }
    }]
  } else if (props.type === 'bar') {
    baseOption.series = [{
      data: props.data.map(d => d.volume),
      type: 'bar',
      itemStyle: { color: '#0066cc' },
    }]
  }
  chart.setOption(baseOption)
}

const handleResize = () => { 
  if (chart) {
    chart.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
  
  // 使用 ResizeObserver 监听容器尺寸变化
  if (chartRef.value && window.ResizeObserver) {
    const resizeObserver = new ResizeObserver(() => {
      handleResize()
    })
    resizeObserver.observe(chartRef.value)
  }
})

watch(() => props.data, () => {
  updateChart()
  // 数据更新后也触发 resize
  nextTick(() => {
    handleResize()
  })
}, { deep: true })

defineExpose({ chart })
</script>

<style scoped lang="scss">
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
