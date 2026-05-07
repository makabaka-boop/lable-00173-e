# 证券交易系统 - API 文档

**文档版本**：1.0  
**最后更新**：2024年  
**API 基础 URL**：`http://localhost:8000/api`

---

## 目录

1. [认证接口](#认证接口)
2. [用户接口](#用户接口)
3. [行情接口](#行情接口)
4. [交易接口](#交易接口)
5. [持仓接口](#持仓接口)
6. [回测接口](#回测接口)
7. [错误处理](#错误处理)

---

## 认证接口

### 用户登录

**请求**
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "123456"
}
```

**响应**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "name": "管理员",
      "balance": 200000,
      "totalAssets": 500000,
      "createdAt": 1704067200000
    },
    "token": "token_1_1704067200000"
  }
}
```

### 用户登出

**请求**
```
POST /api/auth/logout
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "退出成功"
}
```

---

## 用户接口

### 获取用户资料

**请求**
```
GET /api/user/profile/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "name": "管理员",
    "phone": "13800138000",
    "address": "北京市",
    "bio": "系统管理员",
    "balance": 200000,
    "totalAssets": 500000,
    "createdAt": 1704067200000
  }
}
```

### 更新用户资料

**请求**
```
PUT /api/user/profile/{user_id}
Content-Type: application/json
Authorization: Bearer token_xxx

{
  "name": "新名称",
  "email": "newemail@example.com",
  "phone": "13900139000",
  "address": "上海市",
  "bio": "新简介"
}
```

**响应**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "newemail@example.com",
    "name": "新名称",
    "phone": "13900139000",
    "address": "上海市",
    "bio": "新简介",
    "balance": 200000,
    "totalAssets": 500000,
    "createdAt": 1704067200000
  }
}
```

### 获取账户统计

**请求**
```
GET /api/user/account-stats/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "totalAssets": 500000,
    "cash": 200000,
    "positions": [
      {
        "id": 1,
        "code": "000001",
        "name": "平安银行",
        "quantity": 1000,
        "costPrice": 12.0,
        "currentPrice": 12.5,
        "marketValue": 12500,
        "profit": 500,
        "profitPercent": 4.17
      }
    ],
    "totalProfit": 500,
    "totalProfitPercent": 4.17,
    "dayProfit": 100,
    "dayProfitPercent": 0.5
  }
}
```

---

## 行情接口

### 获取股票列表

**请求**
```
GET /api/market/stocks
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "code": "000001",
      "name": "平安银行",
      "price": 12.5,
      "change": 0.5,
      "changePercent": 4.17,
      "high": 13.0,
      "low": 12.0,
      "volume": 1000000,
      "marketCap": 100000000000,
      "pe": 8.5,
      "timestamp": 1704067200000
    }
  ]
}
```

### 获取单个股票信息

**请求**
```
GET /api/market/stock/{code}
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "code": "000001",
    "name": "平安银行",
    "price": 12.5,
    "change": 0.5,
    "changePercent": 4.17,
    "high": 13.0,
    "low": 12.0,
    "volume": 1000000,
    "marketCap": 100000000000,
    "pe": 8.5,
    "timestamp": 1704067200000
  }
}
```

### 获取 K 线数据

**请求**
```
GET /api/market/kline/{code}
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "time": 1704067200000,
      "open": 12.0,
      "high": 12.8,
      "low": 11.9,
      "close": 12.5,
      "volume": 1000000
    }
  ]
}
```

---

## 交易接口

### 获取订单列表

**请求**
```
GET /api/trading/orders/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "code": "000001",
      "name": "平安银行",
      "type": "buy",
      "quantity": 100,
      "price": 12.5,
      "totalAmount": 1250,
      "status": "pending",
      "timestamp": 1704067200000,
      "executedTime": null
    }
  ]
}
```

### 创建订单

**请求**
```
POST /api/trading/orders
Content-Type: application/json
Authorization: Bearer token_xxx

{
  "user_id": 1,
  "code": "000001",
  "name": "平安银行",
  "type": "buy",
  "quantity": 100,
  "price": 12.5,
  "totalAmount": 1250
}
```

**响应**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1,
    "code": "000001",
    "name": "平安银行",
    "type": "buy",
    "quantity": 100,
    "price": 12.5,
    "totalAmount": 1250,
    "status": "pending",
    "timestamp": 1704067200000,
    "executedTime": null
  }
}
```

### 执行订单

**请求**
```
PUT /api/trading/orders/{order_id}/execute
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "执行成功",
  "data": {
    "id": 1,
    "code": "000001",
    "name": "平安银行",
    "type": "buy",
    "quantity": 100,
    "price": 12.5,
    "totalAmount": 1250,
    "status": "completed",
    "timestamp": 1704067200000,
    "executedTime": 1704067300000
  }
}
```

### 撤销订单

**请求**
```
PUT /api/trading/orders/{order_id}/cancel
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "取消成功",
  "data": {
    "id": 1,
    "code": "000001",
    "name": "平安银行",
    "type": "buy",
    "quantity": 100,
    "price": 12.5,
    "totalAmount": 1250,
    "status": "cancelled",
    "timestamp": 1704067200000,
    "executedTime": null
  }
}
```

### 获取交易历史

**请求**
```
GET /api/trading/trades/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "code": "000001",
      "name": "平安银行",
      "type": "buy",
      "quantity": 100,
      "price": 12.5,
      "totalAmount": 1250,
      "profit": null,
      "timestamp": 1704067200000
    }
  ]
}
```

---

## 持仓接口

### 获取持仓列表

**请求**
```
GET /api/positions/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "code": "000001",
      "name": "平安银行",
      "quantity": 1000,
      "costPrice": 12.0,
      "currentPrice": 12.5,
      "marketValue": 12500,
      "profit": 500,
      "profitPercent": 4.17
    }
  ]
}
```

### 创建持仓

**请求**
```
POST /api/positions
Content-Type: application/json
Authorization: Bearer token_xxx

{
  "user_id": 1,
  "code": "000001",
  "name": "平安银行",
  "quantity": 1000,
  "cost_price": 12.0,
  "current_price": 12.5
}
```

**响应**
```json
{
  "code": 200,
  "message": "创建成功",
  "data": {
    "id": 1,
    "code": "000001",
    "name": "平安银行",
    "quantity": 1000,
    "costPrice": 12.0,
    "currentPrice": 12.5,
    "marketValue": 12500,
    "profit": 500,
    "profitPercent": 4.17
  }
}
```

### 更新持仓

**请求**
```
PUT /api/positions/{position_id}
Content-Type: application/json
Authorization: Bearer token_xxx

{
  "quantity": 1100,
  "cost_price": 12.0,
  "current_price": 12.5
}
```

**响应**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "code": "000001",
    "name": "平安银行",
    "quantity": 1100,
    "costPrice": 12.0,
    "currentPrice": 12.5,
    "marketValue": 13750,
    "profit": 825,
    "profitPercent": 6.88
  }
}
```

---

## 回测接口

### 获取回测结果

**请求**
```
GET /api/backtest/results/{user_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    {
      "id": 1,
      "name": "均线策略回测",
      "code": "000001",
      "strategy": "ma",
      "startDate": 1672531200000,
      "endDate": 1704067200000,
      "initialCapital": 100000,
      "finalCapital": 120000,
      "totalReturn": 20000,
      "returnPercent": 20,
      "maxDrawdown": -5,
      "sharpeRatio": 1.5,
      "winRate": 60,
      "totalTrades": 50,
      "profitableTrades": 30,
      "status": "completed",
      "createdAt": 1704067200000
    }
  ]
}
```

### 运行回测

**请求**
```
POST /api/backtest/run
Content-Type: application/json
Authorization: Bearer token_xxx

{
  "user_id": 1,
  "name": "均线策略回测",
  "code": "000001",
  "strategy": "ma",
  "parameters": {
    "fast": 12,
    "slow": 26,
    "signal": 9
  },
  "startDate": 1672531200000,
  "endDate": 1704067200000,
  "initialCapital": 100000
}
```

**响应**
```json
{
  "code": 200,
  "message": "回测完成",
  "data": {
    "id": 1,
    "name": "均线策略回测",
    "code": "000001",
    "strategy": "ma",
    "startDate": 1672531200000,
    "endDate": 1704067200000,
    "initialCapital": 100000,
    "finalCapital": 120000,
    "totalReturn": 20000,
    "returnPercent": 20,
    "maxDrawdown": -5,
    "sharpeRatio": 1.5,
    "winRate": 60,
    "totalTrades": 50,
    "profitableTrades": 30,
    "status": "completed",
    "createdAt": 1704067200000
  }
}
```

### 删除回测

**请求**
```
DELETE /api/backtest/results/{backtest_id}
Authorization: Bearer token_xxx
```

**响应**
```json
{
  "code": 200,
  "message": "删除成功"
}
```

---

## 健康检查

### 系统健康检查

**请求**
```
GET /api/health
```

**响应**
```json
{
  "code": 200,
  "message": "OK"
}
```

---

## 错误处理

### 错误响应格式

```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（需要登录） |
| 403 | 禁止访问（权限不足） |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

### 错误示例

**参数错误**
```json
{
  "code": 400,
  "message": "用户名和密码不能为空"
}
```

**未授权**
```json
{
  "code": 401,
  "message": "用户名或密码错误"
}
```

**资源不存在**
```json
{
  "code": 404,
  "message": "用户不存在"
}
```

---

## 认证说明

### Token 使用

所有需要认证的接口都需要在请求头中包含 Token：

```
Authorization: Bearer token_xxx
```

### Token 有效期

- Token 有效期：24 小时
- 过期后需要重新登录

---

## 速率限制

- 每个 IP 每分钟最多 60 个请求
- 超过限制将返回 429 Too Many Requests

---

## 附录

### A. 数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Integer | 整数 | 1, 100, -50 |
| Float | 浮点数 | 12.5, 3.14 |
| String | 字符串 | "admin", "000001" |
| Boolean | 布尔值 | true, false |
| DateTime | 时间戳 | 1704067200000 |
| JSON | JSON 对象 | {"key": "value"} |

### B. 时间格式

所有时间戳使用毫秒级 Unix 时间戳：
- 示例：1704067200000
- 转换：JavaScript 中使用 `new Date(1704067200000)`

### C. 测试工具

推荐使用以下工具测试 API：
- Postman：https://www.postman.com/
- Insomnia：https://insomnia.rest/
- curl：命令行工具
- VS Code REST Client 插件

### D. 示例请求

**使用 curl**
```bash
# 登录
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'

# 获取股票列表
curl http://localhost:8000/api/market/stocks

# 获取用户资料
curl -H "Authorization: Bearer token_xxx" \
  http://localhost:8000/api/user/profile/1
```

**使用 JavaScript/Fetch**
```javascript
// 登录
fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: '123456' })
})
.then(r => r.json())
.then(data => console.log(data))

// 获取股票列表
fetch('http://localhost:8000/api/market/stocks')
.then(r => r.json())
.then(data => console.log(data))
```
