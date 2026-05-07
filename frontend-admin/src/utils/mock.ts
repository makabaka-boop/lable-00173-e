import type { Stock, Position, Order, TradeHistory, KlineData, BacktestResult } from '@/types'

// 生成随机数
const random = (min: number, max: number) => Math.random() * (max - min) + min

// 模拟股票数据
export const generateMockStocks = (): Stock[] => {
  const stocks = [
    { code: '000001', name: '平安银行' },
    { code: '000858', name: '五粮液' },
    { code: '000651', name: '格力电器' },
    { code: '600000', name: '浦发银行' },
    { code: '600016', name: '民生银行' },
    { code: '600519', name: '贵州茅台' },
    { code: '601398', name: '工商银行' },
    { code: '601988', name: '中国银行' },
  ]

  return stocks.map(s => ({
    ...s,
    price: random(10, 500),
    change: random(-50, 50),
    changePercent: random(-5, 5),
    high: random(100, 600),
    low: random(5, 100),
    volume: Math.floor(random(1000000, 100000000)),
    marketCap: Math.floor(random(100000000000, 5000000000000)),
    pe: random(5, 50),
    timestamp: Date.now(),
  }))
}

// 模拟持仓数据
export const generateMockPositions = (): Position[] => {
  return [
    {
      id: '1',
      code: '000001',
      name: '平安银行',
      quantity: 1000,
      costPrice: 12.5,
      currentPrice: 13.2,
      profit: 700,
      profitPercent: 5.6,
      marketValue: 13200,
    },
    {
      id: '2',
      code: '600519',
      name: '贵州茅台',
      quantity: 50,
      costPrice: 1800,
      currentPrice: 1950,
      profit: 7500,
      profitPercent: 8.33,
      marketValue: 97500,
    },
    {
      id: '3',
      code: '000858',
      name: '五粮液',
      quantity: 200,
      costPrice: 95,
      currentPrice: 98,
      profit: 600,
      profitPercent: 3.16,
      marketValue: 19600,
    },
  ]
}

// 模拟订单数据
export const generateMockOrders = (): Order[] => {
  return [
    {
      id: '1',
      code: '000001',
      name: '平安银行',
      type: 'buy',
      quantity: 500,
      price: 13.5,
      totalAmount: 6750,
      status: 'completed',
      timestamp: Date.now() - 3600000,
      executedTime: Date.now() - 3500000,
    },
    {
      id: '2',
      code: '600519',
      name: '贵州茅台',
      type: 'buy',
      quantity: 10,
      price: 1950,
      totalAmount: 19500,
      status: 'pending',
      timestamp: Date.now() - 1800000,
    },
  ]
}

// 模拟交易历史
export const generateMockTradeHistory = (): TradeHistory[] => {
  return [
    {
      id: '1',
      code: '000001',
      name: '平安银行',
      type: 'buy',
      quantity: 1000,
      price: 12.5,
      totalAmount: 12500,
      timestamp: Date.now() - 86400000 * 5,
    },
    {
      id: '2',
      code: '600519',
      name: '贵州茅台',
      type: 'buy',
      quantity: 50,
      price: 1800,
      totalAmount: 90000,
      timestamp: Date.now() - 86400000 * 3,
    },
    {
      id: '3',
      code: '000858',
      name: '五粮液',
      type: 'buy',
      quantity: 200,
      price: 95,
      totalAmount: 19000,
      timestamp: Date.now() - 86400000,
    },
  ]
}

// 模拟K线数据
export const generateMockKlineData = (): KlineData[] => {
  const data: KlineData[] = []
  let basePrice = 100
  const now = Date.now()

  for (let i = 60; i >= 0; i--) {
    const change = random(-5, 5)
    const open = basePrice
    const close = basePrice + change
    const high = Math.max(open, close) + random(0, 3)
    const low = Math.min(open, close) - random(0, 3)

    data.push({
      time: now - i * 86400000,
      open,
      high,
      low,
      close,
      volume: Math.floor(random(1000000, 10000000)),
    })

    basePrice = close
  }

  return data
}

// 模拟回测结果
export const generateMockBacktestResults = (): BacktestResult[] => {
  return [
    {
      id: '1',
      name: '均线策略 - 2024年',
      startDate: Date.now() - 365 * 86400000,
      endDate: Date.now(),
      initialCapital: 100000,
      finalCapital: 145000,
      totalReturn: 45000,
      returnPercent: 45,
      maxDrawdown: -12.5,
      sharpeRatio: 1.8,
      winRate: 62,
      totalTrades: 50,
      profitableTrades: 31,
      status: 'completed',
      createdAt: Date.now() - 86400000 * 7,
    },
    {
      id: '2',
      name: 'RSI策略 - 2024年',
      startDate: Date.now() - 365 * 86400000,
      endDate: Date.now(),
      initialCapital: 100000,
      finalCapital: 128000,
      totalReturn: 28000,
      returnPercent: 28,
      maxDrawdown: -8.3,
      sharpeRatio: 1.5,
      winRate: 58,
      totalTrades: 45,
      profitableTrades: 26,
      status: 'completed',
      createdAt: Date.now() - 86400000 * 5,
    },
  ]
}
