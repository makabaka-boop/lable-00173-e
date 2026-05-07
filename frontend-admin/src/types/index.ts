// 用户信息
export interface User {
  id: string | number
  name: string
  email: string
  phone?: string
  avatar?: string
  balance: number
  totalAssets: number
  address?: string
  bio?: string
  createdAt?: number
}

// 股票信息
export interface Stock {
  code: string
  name: string
  price: number
  change: number
  changePercent: number
  high: number
  low: number
  volume: number
  marketCap: number
  pe: number
  timestamp: number
}

// 持仓信息
export interface Position {
  id: string | number
  code: string
  name: string
  quantity: number
  costPrice: number
  currentPrice: number
  profit: number
  profitPercent: number
  marketValue: number
}

// 交易订单
export interface Order {
  id: string | number
  code: string
  name: string
  type: 'buy' | 'sell'
  quantity: number
  price: number
  totalAmount: number
  status: 'pending' | 'completed' | 'cancelled'
  timestamp: number
  executedTime?: number
}

// 交易历史
export interface TradeHistory {
  id: string | number
  code: string
  name: string
  type: 'buy' | 'sell'
  quantity: number
  price: number
  totalAmount: number
  timestamp: number
  profit?: number
}

// K线数据
export interface KlineData {
  time: number
  open: number
  high: number
  low: number
  close: number
  volume: number
}

// 回测结果
export interface BacktestResult {
  id: string | number
  name: string
  startDate: number
  endDate: number
  initialCapital: number
  finalCapital: number
  totalReturn: number
  returnPercent: number
  maxDrawdown: number
  sharpeRatio: number
  winRate: number
  totalTrades: number
  profitableTrades: number
  status: 'running' | 'completed' | 'failed'
  createdAt: number
}

// 回测参数
export interface BacktestParams {
  name: string
  code: string
  startDate: number
  endDate: number
  initialCapital: number
  strategy: 'ma' | 'rsi' | 'macd'
  parameters: Record<string, number>
}

// 市场数据
export interface MarketData {
  timestamp: number
  stocks: Stock[]
  indices: {
    name: string
    value: number
    change: number
  }[]
}

// 账户统计
export interface AccountStats {
  totalAssets: number
  cash: number
  positions: Position[]
  totalProfit: number
  totalProfitPercent: number
  dayProfit: number
  dayProfitPercent: number
}
