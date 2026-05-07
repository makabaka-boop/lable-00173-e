# 证券交易系统 - 部署指南

**文档版本**：1.0  
**最后更新**：2024年

---

## 目录

1. [环境要求](#环境要求)
2. [本地开发部署](#本地开发部署)
3. [Docker 部署](#docker-部署)
4. [生产环境部署](#生产环境部署)
5. [故障排查](#故障排查)
6. [维护指南](#维护指南)

---

## 环境要求

### 1.1 系统要求

- **操作系统**：Linux、macOS、Windows
- **CPU**：2 核及以上
- **内存**：4GB 及以上
- **磁盘**：10GB 及以上

### 1.2 软件要求

**本地开发**：
- Python 3.11+
- Node.js 18+
- npm 或 yarn

**Docker 部署**：
- Docker 20.10+
- Docker Compose 2.0+

### 1.3 网络要求

- 互联网连接
- 防火墙开放必要端口（8000、8080）

---

## 本地开发部署

### 2.1 后端部署

**1. 克隆项目**
```bash
git clone <repository-url>
cd <project-directory>
```

**2. 创建虚拟环境**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

**3. 安装依赖**
```bash
pip install -r requirements.txt
```

**4. 配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库等参数
```

**5. 启动应用**
```bash
python app.py
```

应用将在 http://localhost:8000 启动

### 2.2 前端部署

**1. 进入前端目录**
```bash
cd frontend-admin
```

**2. 安装依赖**
```bash
npm install
```

**3. 启动开发服务器**
```bash
npm run dev
```

应用将在 http://localhost:5173 启动

### 2.3 验证部署

访问以下地址验证部署成功：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000/api/health

---

## Docker 部署

### 3.1 前置条件

确保已安装 Docker 和 Docker Compose：
```bash
docker --version
docker-compose --version
```

### 3.2 构建和启动

**1. 构建镜像**
```bash
docker-compose build
```

**2. 启动服务**
```bash
docker-compose up -d
```

**3. 查看日志**
```bash
docker-compose logs -f
```

**4. 验证服务**
```bash
# 检查容器状态
docker-compose ps

# 测试后端 API
curl http://localhost:8000/api/health

# 访问前端
# 打开浏览器访问 http://localhost:8080
```

### 3.3 常用命令

```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh

# 删除所有容器和镜像
docker-compose down -v
docker system prune -a
```

### 3.4 数据持久化

数据库文件存储在 `backend/trading_system.db`，容器停止后数据不会丢失。

---

## 生产环境部署

### 4.1 服务器准备

**1. 购买服务器**
- 云服务商：阿里云、腾讯云、AWS 等
- 配置：2 核 4GB 内存 50GB 磁盘

**2. 安装操作系统**
- 推荐：Ubuntu 20.04 LTS

**3. 安装必要软件**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装 Git
sudo apt install -y git
```

### 4.2 应用部署

**1. 克隆项目**
```bash
cd /opt
sudo git clone <repository-url> trading-system
cd trading-system
```

**2. 配置环境**
```bash
# 创建 .env 文件
sudo cp backend/.env.example backend/.env

# 编辑配置
sudo nano backend/.env
```

**3. 启动应用**
```bash
sudo docker-compose up -d
```

**4. 配置反向代理**

创建 Nginx 配置文件 `/etc/nginx/sites-available/trading-system`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/trading-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4.3 SSL 证书配置

使用 Let's Encrypt 配置 HTTPS：
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4.4 监控和日志

**1. 查看日志**
```bash
docker-compose logs -f
```

**2. 配置日志轮转**

创建 `/etc/logrotate.d/trading-system`：
```
/var/log/trading-system/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
```

**3. 设置自动启动**

创建 systemd 服务文件 `/etc/systemd/system/trading-system.service`：
```ini
[Unit]
Description=Trading System
After=docker.service
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=/opt/trading-system
ExecStart=/usr/local/bin/docker-compose up
ExecStop=/usr/local/bin/docker-compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable trading-system
sudo systemctl start trading-system
```

---

## 故障排查

### 5.1 常见问题

**问题 1：端口被占用**
```bash
# 查看占用端口的进程
lsof -i :8000
lsof -i :8080

# 杀死进程
kill -9 <PID>
```

**问题 2：数据库连接失败**
```bash
# 检查数据库文件
ls -la backend/trading_system.db

# 重新初始化数据库
rm backend/trading_system.db
docker-compose restart backend
```

**问题 3：前端无法连接后端**
```bash
# 检查 API 配置
cat frontend-admin/src/utils/api.ts

# 检查网络连接
curl http://localhost:8000/api/health
```

**问题 4：容器启动失败**
```bash
# 查看详细日志
docker-compose logs backend
docker-compose logs frontend

# 重建镜像
docker-compose build --no-cache
```

### 5.2 日志分析

**后端日志位置**：
```bash
docker-compose logs backend
```

**前端日志位置**：
```bash
docker-compose logs frontend
```

**系统日志**：
```bash
docker-compose logs
```

### 5.3 性能诊断

**检查容器资源使用**：
```bash
docker stats
```

**检查数据库性能**：
```bash
# 进入后端容器
docker-compose exec backend bash

# 查看数据库大小
ls -lh trading_system.db
```

---

## 维护指南

### 6.1 定期备份

**1. 手动备份**
```bash
# 备份数据库
cp backend/trading_system.db backend/trading_system.db.backup

# 备份整个项目
tar -czf trading-system-backup-$(date +%Y%m%d).tar.gz /opt/trading-system
```

**2. 自动备份脚本**

创建 `/opt/backup.sh`：
```bash
#!/bin/bash

BACKUP_DIR="/opt/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
cp /opt/trading-system/backend/trading_system.db \
   $BACKUP_DIR/trading_system_$TIMESTAMP.db

# 删除 7 天前的备份
find $BACKUP_DIR -name "trading_system_*.db" -mtime +7 -delete

echo "Backup completed at $TIMESTAMP"
```

设置定时任务：
```bash
# 编辑 crontab
crontab -e

# 添加每天凌晨 2 点执行备份
0 2 * * * /opt/backup.sh
```

### 6.2 更新升级

**1. 更新代码**
```bash
cd /opt/trading-system
git pull origin main
```

**2. 重建镜像**
```bash
docker-compose build --no-cache
```

**3. 重启服务**
```bash
docker-compose down
docker-compose up -d
```

**4. 验证更新**
```bash
docker-compose ps
curl http://localhost:8000/api/health
```

### 6.3 性能优化

**1. 数据库优化**
```bash
# 进入后端容器
docker-compose exec backend bash

# 分析数据库
sqlite3 trading_system.db ".tables"
sqlite3 trading_system.db ".schema"
```

**2. 缓存优化**
- 启用浏览器缓存
- 启用 Gzip 压缩
- 使用 CDN 加速

**3. 代码优化**
- 定期代码审查
- 性能测试
- 内存泄漏检测

### 6.4 安全加固

**1. 更新依赖**
```bash
# 检查依赖漏洞
pip audit
npm audit

# 更新依赖
pip install --upgrade -r requirements.txt
npm update
```

**2. 配置防火墙**
```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

**3. 定期安全审计**
- 检查访问日志
- 监控异常活动
- 定期渗透测试

### 6.5 监控告警

**1. 系统监控**
```bash
# 监控容器资源
watch docker stats

# 监控系统资源
top
free -h
df -h
```

**2. 应用监控**
- 监控 API 响应时间
- 监控错误率
- 监控用户活跃度

**3. 告警配置**
- 高 CPU 使用率告警
- 高内存使用率告警
- 磁盘空间不足告警
- API 错误率告警

---

## 附录

### A. 常用命令速查

```bash
# Docker 相关
docker-compose up -d              # 启动服务
docker-compose down               # 停止服务
docker-compose logs -f            # 查看日志
docker-compose ps                 # 查看容器状态
docker-compose exec <service> bash # 进入容器

# 系统相关
systemctl status trading-system    # 查看服务状态
systemctl restart trading-system   # 重启服务
journalctl -u trading-system -f    # 查看服务日志

# 数据库相关
sqlite3 trading_system.db          # 进入数据库
.tables                            # 查看表
.schema                            # 查看表结构
SELECT COUNT(*) FROM users;        # 查询数据
```

### B. 故障恢复清单

- [ ] 检查服务状态
- [ ] 查看错误日志
- [ ] 检查磁盘空间
- [ ] 检查内存使用
- [ ] 检查网络连接
- [ ] 重启服务
- [ ] 验证功能
- [ ] 通知用户

### C. 参考资源

- Docker 官方文档：https://docs.docker.com/
- Docker Compose 文档：https://docs.docker.com/compose/
- Nginx 文档：https://nginx.org/en/docs/
- Ubuntu 服务器指南：https://ubuntu.com/server/docs
