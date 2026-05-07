// 格式化数字
export const formatNumber = (num: number, decimals: number = 2): string => {
  return num.toFixed(decimals)
}

// 格式化货币
export const formatCurrency = (num: number): string => {
  return '¥' + num.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// 格式化百分比
export const formatPercent = (num: number, decimals: number = 2): string => {
  return num.toFixed(decimals) + '%'
}

// 格式化大数字（万、亿）
export const formatLargeNumber = (num: number): string => {
  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + '亿'
  }
  if (num >= 10000) {
    return (num / 10000).toFixed(2) + '万'
  }
  return num.toString()
}

// 格式化日期
export const formatDate = (timestamp: number, format: string = 'YYYY-MM-DD HH:mm:ss'): string => {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

// 格式化时间差
export const formatTimeDiff = (timestamp: number): string => {
  const diff = Date.now() - timestamp
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

// 获取涨跌颜色
export const getPriceColor = (change: number): string => {
  if (change > 0) return '#ff4d4f'
  if (change < 0) return '#00b96b'
  return '#666666'
}

// 获取涨跌符号
export const getPriceSymbol = (change: number): string => {
  if (change > 0) return '▲'
  if (change < 0) return '▼'
  return '—'
}
