import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'
  : 'http://localhost:8000/api'

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data as ApiResponse,
  (error) => {
    // 只在非登录请求时处理 401 错误
    if (error.response?.status === 401 && !error.config.url?.includes('/auth/login')) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ==================== 认证接口 ====================

export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
}

// ==================== 用户接口 ====================

export const userAPI = {
  getProfile: (userId: number) => api.get(`/user/profile/${userId}`),
  updateProfile: (userId: number, data: any) =>
    api.put(`/user/profile/${userId}`, data),
  getAccountStats: (userId: number) => api.get(`/user/account-stats/${userId}`),
}

// ==================== 行情接口 ====================

export const marketAPI = {
  getStocks: () => api.get('/market/stocks'),
  getStock: (code: string) => api.get(`/market/stock/${code}`),
  getKline: (code: string) => api.get(`/market/kline/${code}`),
}

// ==================== 交易接口 ====================

export const tradingAPI = {
  getOrders: (userId: number) => api.get(`/trading/orders/${userId}`),
  createOrder: (data: any) => api.post('/trading/orders', data),
  executeOrder: (orderId: number) => api.put(`/trading/orders/${orderId}/execute`),
  cancelOrder: (orderId: number) => api.put(`/trading/orders/${orderId}/cancel`),
  getTrades: (userId: number) => api.get(`/trading/trades/${userId}`),
}

// ==================== 持仓接口 ====================

export const positionsAPI = {
  getPositions: (userId: number) => api.get(`/positions/${userId}`),
  createPosition: (data: any) => api.post('/positions', data),
  updatePosition: (positionId: number, data: any) => api.put(`/positions/${positionId}`, data),
}

// ==================== 回测接口 ====================

export const backtestAPI = {
  getResults: (userId: number): Promise<ApiResponse> => api.get(`/backtest/results/${userId}`),
  runBacktest: (data: any): Promise<ApiResponse> => api.post('/backtest/run', data),
  deleteBacktest: (backtestId: number): Promise<ApiResponse> => api.delete(`/backtest/results/${backtestId}`),
}

// ==================== 健康检查 ====================

export const healthAPI = {
  check: () => api.get('/health'),
}

export default api
