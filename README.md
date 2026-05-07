# 证券交易系统

一套功能完整、架构合理的证券交易系统，采用 Python 和 Vue 3 开发。系统包含用户界面显示模块、数据管理模块、交易执行模块和数据回测模块。

## How to Run

### 前置要求
- Docker 和 Docker Compose
- 或者本地环境：Python 3.11+、Node.js 18+

### 使用 Docker Compose 运行（推荐）

```bash
# 构建并启动所有服务
docker-compose up --build -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

启动后访问：
- 前端应用：http://localhost:8080
- 后端 API：http://localhost:8000

### 本地开发运行

**后端：**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**前端：**
```bash
cd frontend-admin
npm install
npm run dev
```

## Services

### 后端服务 (Backend)
- **框架**：Flask
- **数据库**：SQLite
- **端口**：8000
- **主要功能**：
  - 用户认证与管理（JWT Token认证）
  - 股票行情数据管理
  - 交易订单处理
  - 持仓管理
  - 交易历史记录
  - 策略回测
  - 操作日志记录与查询

### 前端服务 (Frontend)
- **框架**：Vue 3 + TypeScript
- **UI 库**：Element Plus
- **构建工具**：Vite
- **端口**：80
- **主要功能**：
  - 行情中心：实时股票行情展示
  - 交易管理：订单创建与执行
  - 持仓管理：持仓查看与调整
  - 策略回测：回测结果分析
  - 个人资料：用户信息管理

## 测试账号

| 用户名 | 密码 | 说明 |
|--------|------|------|
| admin | 123456 | 管理员账号 |


## 项目介绍

### 题目内容

设计并开发一套功能完整、架构合理的证券交易系统，采用Python作为主要开发语言。该系统需包含以下核心模块：用户界面显示模块、数据管理模块、交易执行模块和数据回测模块。在进入实际开发阶段前，需首先完成详细的产品需求文档和系统架构设计文档。产品文档应明确系统功能需求、非功能需求、用户角色与权限、业务流程等内容；架构设计文档应包含系统总体架构图、模块划分、技术选型、接口设计、数据流程图、安全策略及性能优化方案等关键内容。确保文档内容专业、详尽、可落地，为后续开发工作提供清晰指导。

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端应用 (Vue 3)                      │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ 行情中心     │ 交易管理     │ 持仓管理     │         │
│  └──────────────┴──────────────┴──────────────┘         │
│  ┌──────────────┬──────────────┐                        │
│  │ 策略回测     │ 个人资料     │                        │
│  └──────────────┴──────────────┘                        │
└─────────────────────────────────────────────────────────┘
                        ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                  后端 API (Flask)                        │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ 认证模块     │ 行情模块     │ 交易模块     │         │
│  └──────────────┴──────────────┴──────────────┘         │
│  ┌──────────────┬──────────────┐                        │
│  │ 持仓模块     │ 回测模块     │                        │
│  └──────────────┴──────────────┘                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              数据层 (SQLite Database)                    │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ 用户表       │ 股票表       │ 订单表       │         │
│  └──────────────┴──────────────┴──────────────┘         │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │ 持仓表       │ 交易表       │ 回测表       │         │
│  └──────────────┴──────────────┴──────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 核心功能模块

#### 1. 用户界面显示模块
- 响应式设计，支持桌面和移动设备
- 实时行情展示
- 交易界面
- 数据可视化（K线图、统计图表）

#### 2. 数据管理模块
- 用户信息管理
- 股票基础数据管理
- K线数据存储
- 交易历史记录

#### 3. 交易执行模块
- 订单创建与管理
- 订单执行与成交
- 持仓自动更新
- 交易记录生成

#### 4. 数据回测模块
- 策略参数配置
- 回测执行
- 性能指标计算
- 结果分析与导出

### 技术栈

**后端：**
- Python 3.11
- Flask - Web 框架
- SQLAlchemy - ORM
- Flask-CORS - 跨域支持
- PyJWT - JWT Token认证
- Werkzeug - 密码哈希

**前端：**
- Vue 3 - 前端框架
- TypeScript - 类型安全
- Vite - 构建工具
- Element Plus - UI 组件库
- ECharts - 数据可视化
- Pinia - 状态管理

**部署：**
- Docker - 容器化
- Docker Compose - 容器编排
- Nginx - Web 服务器

### 主要特性

✅ 完整的用户认证系统（JWT Token + 密码加密）
✅ 实时股票行情展示
✅ 灵活的交易订单管理
✅ 自动持仓跟踪
✅ 策略回测功能
✅ 响应式用户界面
✅ 跨平台支持（Docker）
✅ RESTful API 设计
✅ 模块化架构设计（路由/服务/工具分层）
✅ 完整的操作日志记录系统

### 数据流程

1. **用户登录** → 认证 → 获取用户信息
2. **查看行情** → 获取股票列表 → 显示 K 线图
3. **创建订单** → 验证 → 保存订单
4. **执行订单** → 更新持仓 → 生成交易记录
5. **查看持仓** → 计算收益 → 显示统计数据
6. **运行回测** → 执行策略 → 生成报告

### 安全策略

- **密码加密**：使用 Werkzeug 的 pbkdf2:sha256 哈希算法加密存储
- **JWT Token认证**：Token包含过期时间（24小时），自动验证
- **权限验证**：所有需要认证的路由都验证用户只能访问自己的资源
- **CORS 跨域保护**：配置了跨域资源共享策略
- **请求验证**：统一的Token验证装饰器
- **数据隔离**：用户数据完全隔离，无法访问他人数据

### 性能优化

- 数据库查询优化
- 前端组件懒加载
- 缓存策略
- 异步处理

## 项目结构

```
.
├── backend/                    # 后端应用
│   ├── app.py                 # Flask 应用入口
│   ├── models.py              # 数据模型
│   ├── requirements.txt        # Python 依赖
│   ├── migrate_passwords.py   # 密码迁移脚本
│   ├── .env                   # 环境变量
│   ├── Dockerfile             # 后端容器配置
│   ├── routes/                # 路由层
│   │   ├── auth_routes.py     # 认证路由
│   │   ├── user_routes.py     # 用户路由
│   │   ├── market_routes.py   # 市场路由
│   │   ├── trading_routes.py  # 交易路由
│   │   ├── position_routes.py # 持仓路由
│   │   ├── backtest_routes.py # 回测路由
│   │   └── log_routes.py      # 日志路由
│   ├── services/              # 业务逻辑层
│   │   ├── auth_service.py    # 认证服务
│   │   ├── user_service.py    # 用户服务
│   │   ├── market_service.py  # 市场服务
│   │   ├── trading_service.py # 交易服务
│   │   ├── position_service.py # 持仓服务
│   │   ├── backtest_service.py # 回测服务
│   │   └── log_service.py     # 日志服务
│   ├── utils/                 # 工具函数层
│   │   ├── auth.py            # 认证工具（密码哈希、JWT）
│   │   ├── decorators.py      # 装饰器（Token验证）
│   │   └── logging.py         # 日志配置和工具
│   └── logs/                  # 日志文件目录
│       ├── app.log            # 应用日志
│       └── error.log          # 错误日志
├── frontend-admin/            # 前端应用
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── utils/             # 工具函数
│   │   └── types/             # TypeScript 类型
│   ├── package.json           # Node 依赖
│   ├── vite.config.ts         # Vite 配置
│   └── Dockerfile             # 前端容器配置
├── docker-compose.yml         # Docker Compose 配置
├── .gitignore                 # Git 忽略文件
└── README.md                  # 项目说明
```

## 后端架构说明

### 模块化架构

系统采用三层架构设计：

1. **路由层 (routes/)**：处理 HTTP 请求和响应，参数验证和权限检查
2. **服务层 (services/)**：包含所有业务逻辑，数据库操作
3. **工具层 (utils/)**：提供认证、日志等通用工具函数

### 安全特性

#### 1. 密码加密

- 使用 `Werkzeug` 的 `generate_password_hash` 和 `check_password_hash` 进行密码哈希
- 密码存储格式：`pbkdf2:sha256:...`
- 如果数据库已存在明文密码，可以运行 `python backend/migrate_passwords.py` 进行迁移

#### 2. JWT Token 认证

- 使用 `PyJWT` 库生成和验证 JWT token
- Token 包含用户ID、过期时间（24小时）、签发时间
- Token 格式：`Bearer <token>`（在 Authorization header 中）
- 实现了 `token_required` 装饰器，自动验证 token 有效性

#### 3. 权限验证

- 所有需要认证的路由都验证用户只能访问自己的资源
- 统一的 Token 验证装饰器
- 确保用户只能操作自己的数据

### 环境变量配置

创建或更新 `backend/.env` 文件：

```env
DATABASE_URL=sqlite:///trading_system.db
JWT_SECRET=your-secret-key-change-in-production
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

**重要**：生产环境必须设置强密码的 `JWT_SECRET`！

### API 使用示例

**登录获取Token**：
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "123456"
}

响应：
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {...},
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**使用Token访问受保护接口**：
```bash
GET /api/user/profile/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 日志记录功能

### 功能特性

系统实现了完整的操作日志记录功能：

1. **日志配置**：文件日志自动轮转（10MB，保留10个备份），单独错误日志，控制台日志
2. **操作日志**：记录所有关键操作（登录、交易、回测等）
3. **日志查询**：提供完整的日志查询和统计API
4. **权限控制**：用户只能查看和删除自己的日志

### 已集成的操作日志

- **认证操作**：login, logout
- **用户操作**：user_update
- **交易操作**：order_create, order_execute, order_cancel
- **回测操作**：backtest_run, backtest_delete

### 日志查询 API

#### 获取日志列表
```http
GET /api/logs?user_id=1&operation_type=login&result=success&page=1&per_page=20
Authorization: Bearer <token>
```

#### 获取日志统计信息
```http
GET /api/logs/statistics?user_id=1&start_date=2024-01-01&end_date=2024-12-31
Authorization: Bearer <token>
```

#### 清理旧日志
```http
POST /api/logs/cleanup
Content-Type: application/json
Authorization: Bearer <token>

{
  "days": 90
}
```

### 日志文件位置

日志文件存储在 `backend/logs/` 目录：
- `app.log`: 应用日志（所有级别）
- `error.log`: 错误日志（ERROR级别及以上）

## 开发指南

### 添加新功能

1. **后端路由**：在 `backend/routes/` 中创建新的路由文件
2. **后端服务**：在 `backend/services/` 中创建对应的服务文件
3. **前端页面**：在 `frontend-admin/src/views` 中创建新页面
4. **更新 API**：在 `frontend-admin/src/utils/api.ts` 中添加API调用
5. **更新状态**：在 `frontend-admin/src/stores` 中修改状态管理

### 添加日志记录

在服务方法中使用日志工具：

```python
from utils.logging import log_operation_sync, OPERATION_TYPES, OPERATION_RESULT

log_operation_sync(
    operation_type=OPERATION_TYPES['ORDER_CREATE'],
    user_id=user_id,
    result=OPERATION_RESULT['SUCCESS'],
    description='创建订单成功',
    details={'order_id': 123},
    ip_address=get_client_ip(),
    user_agent=get_user_agent()
)
```

### 数据库迁移

当修改数据模型时，需要重新初始化数据库：

```bash
# 删除旧数据库
rm backend/instance/trading_system.db

# 重启服务
docker-compose restart backend
```

### 密码迁移

如果数据库已存在明文密码：

```bash
cd backend
python migrate_passwords.py
```

## 注意事项

1. **Token过期**：Token 24小时后过期，用户需要重新登录
2. **JWT密钥**：生产环境必须设置强密码的 `JWT_SECRET`
3. **日志存储**：定期清理旧日志，避免占用过多存储空间
4. **敏感信息**：不要在日志中记录敏感信息（如密码、token等）
5. **日志级别**：生产环境建议使用 INFO 或 WARNING 级别

## 许可证

MIT

