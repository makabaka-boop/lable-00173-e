# 证券交易系统 - 文档中心

欢迎来到证券交易系统的文档中心。本文档包含了系统的完整设计、部署和使用指南。

---

## 📚 文档列表

### 1. [产品需求文档 (PRD.md)](./PRD.md)
详细的产品需求文档，包含：
- 产品概述和目标
- 功能需求（6 个主要模块）
- 非功能需求（性能、安全、可用性等）
- 用户角色与权限
- 业务流程图
- 数据需求和数据模型

**适合人群**：产品经理、需求分析师、项目经理

### 2. [系统架构设计文档 (ARCHITECTURE.md)](./ARCHITECTURE.md)
完整的系统架构设计，包含：
- 系统总体架构图
- 模块划分和职责
- 技术选型说明
- RESTful API 设计
- 数据流程图
- 安全策略
- 性能优化方案
- 部署架构

**适合人群**：架构师、技术负责人、高级开发工程师

### 3. [API 接口文档 (API.md)](./API.md)
详细的 API 接口文档，包含：
- 所有 API 端点
- 请求/响应示例
- 参数说明
- 错误处理
- 认证说明
- 测试示例

**适合人群**：前端开发工程师、后端开发工程师、测试工程师

### 4. [部署指南 (DEPLOYMENT.md)](./DEPLOYMENT.md)
完整的部署和运维指南，包含：
- 环境要求
- 本地开发部署
- Docker 部署
- 生产环境部署
- 故障排查
- 维护指南

**适合人群**：运维工程师、DevOps 工程师、系统管理员

---

## 🚀 快速开始

### 本地开发

```bash
# 后端
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# 前端（新终端）
cd frontend-admin
npm install
npm run dev
```

### Docker 部署

```bash
docker-compose up --build -d
```

访问：
- 前端：http://localhost:8080
- 后端 API：http://localhost:8000

---

## 📖 文档导航

### 按角色查看

**产品经理**
1. 阅读 [PRD.md](./PRD.md) - 了解产品功能和需求
2. 查看 [ARCHITECTURE.md](./ARCHITECTURE.md) - 了解系统设计

**开发工程师**
1. 阅读 [ARCHITECTURE.md](./ARCHITECTURE.md) - 了解系统架构
2. 查看 [API.md](./API.md) - 了解接口设计
3. 参考 [DEPLOYMENT.md](./DEPLOYMENT.md) - 了解部署方式

**运维工程师**
1. 阅读 [DEPLOYMENT.md](./DEPLOYMENT.md) - 了解部署和运维
2. 查看 [ARCHITECTURE.md](./ARCHITECTURE.md) - 了解系统架构

**测试工程师**
1. 阅读 [PRD.md](./PRD.md) - 了解功能需求
2. 查看 [API.md](./API.md) - 了解接口规范
3. 参考 [DEPLOYMENT.md](./DEPLOYMENT.md) - 了解测试环境部署

---

## 🔍 主要内容概览

### 系统功能

| 模块 | 功能 | 说明 |
|------|------|------|
| 认证 | 用户登录/登出 | 基于 Token 的认证 |
| 行情 | 股票查看、K线图 | 实时行情展示 |
| 交易 | 订单创建、执行、管理 | 完整的交易流程 |
| 持仓 | 持仓查看、调整 | 持仓管理和统计 |
| 回测 | 策略回测、结果分析 | 历史数据模拟交易 |
| 用户 | 资料管理、账户统计 | 个人信息管理 |

### 技术栈

**后端**
- Python 3.11 + Flask
- SQLAlchemy ORM
- SQLite 数据库

**前端**
- Vue 3 + TypeScript
- Vite 构建工具
- Element Plus UI 库
- ECharts 数据可视化

**部署**
- Docker 容器化
- Docker Compose 编排
- Nginx 反向代理

---

## 📋 文档清单

- [x] 产品需求文档 (PRD)
- [x] 系统架构设计文档
- [x] API 接口文档
- [x] 部署指南
- [x] 数据库设计
- [x] 安全策略
- [x] 性能优化方案

---

## 🔗 相关资源

### 项目文件

- [README.md](../README.md) - 项目主文档
- [docker-compose.yml](../docker-compose.yml) - Docker 编排配置
- [backend/](../backend/) - 后端代码
- [frontend-admin/](../frontend-admin/) - 前端代码

### 外部资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Vue 3 官方文档](https://vuejs.org/)
- [Docker 官方文档](https://docs.docker.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)

---

## 📞 支持

如有问题或建议，请：
1. 查看相关文档
2. 检查 [DEPLOYMENT.md](./DEPLOYMENT.md) 中的故障排查部分
3. 提交 Issue 或 Pull Request

---

## 📝 文档维护

- **最后更新**：2024年
- **维护者**：开发团队
- **更新频率**：根据需要更新

---

## 📄 许可证

本文档采用 CC BY-SA 4.0 许可证。

---

**祝你使用愉快！** 🎉
