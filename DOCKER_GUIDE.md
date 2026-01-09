# Docker 部署指南

## 為什麼使用 Docker？

✅ **一鍵啟動** - 不需要手動安裝 PostgreSQL  
✅ **環境一致** - 在任何電腦上都一樣  
✅ **簡單乾淨** - 不會弄亂系統  
✅ **易於分享** - 只需要一個壓縮檔  

---

## 📋 給教授的使用說明

### 前置需求

只需要安裝 **Docker Desktop**：

- **Windows**: [下載 Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- **macOS**: [下載 Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### 方法 1：使用壓縮檔（最簡單）

```bash
# 1. 解壓縮專案
unzip groupbuy_system.zip
cd groupbuy_system

# 2. 啟動（第一次會下載所需映像，需要幾分鐘）
docker-compose up

# 3. 等待看到：
#    ✓ Database initialized successfully
#    ✓ Running on http://0.0.0.0:5000

# 4. 打開瀏覽器
open http://localhost:5000

# 5. 訪問初始化頁面（只需要一次）
open http://localhost:5000/init-db

# 6. 關閉（按 Ctrl+C，然後執行）
docker-compose down
```

### 方法 2：背景執行

```bash
# 啟動（背景執行）
docker-compose up -d

# 查看狀態
docker-compose ps

# 查看日誌
docker-compose logs -f

# 關閉
docker-compose down
```

### 方法 3：重新啟動

```bash
# 完全重置（刪除所有資料）
docker-compose down -v

# 重新啟動
docker-compose up
```

---

## 🎓 給學生的打包指南

### 步驟 1：準備檔案

確保專案包含：
```
groupbuy_system/
├── Dockerfile
├── docker-compose.yml
├── app.py
├── models.py
├── requirements.txt
├── static/
├── templates/
└── README.md
```

### 步驟 2：測試 Docker

```bash
# 測試是否能正常啟動
cd groupbuy_system
docker-compose up

# 測試網站
open http://localhost:5000

# 關閉
docker-compose down
```

### 步驟 3：打包給教授

```bash
# 方式 A：壓縮檔
cd ..
zip -r groupbuy_system_docker.zip groupbuy_system/ \
  -x "groupbuy_system/.git/*" \
  -x "groupbuy_system/__pycache__/*" \
  -x "groupbuy_system/*.pyc"

# 方式 B：上傳到 GitHub
cd groupbuy_system
git init
git add .
git commit -m "Docker version"
git remote add origin <你的 GitHub URL>
git push -u origin main
```

### 步驟 4：提供給教授的文件

創建一個 `HOW_TO_RUN.txt`：

```
=================================
團購平台 - Docker 啟動指南
Group 8
=================================

【系統需求】
- Docker Desktop（必須）
- 10 GB 硬碟空間
- 4 GB RAM

【安裝 Docker】
Windows/Mac: https://www.docker.com/products/docker-desktop
Linux: curl -fsSL https://get.docker.com | sh

【啟動步驟】
1. 解壓縮 groupbuy_system_docker.zip
2. 開啟終端機/命令提示字元
3. cd groupbuy_system
4. docker-compose up
5. 等待啟動完成（首次需要 5-10 分鐘）
6. 打開瀏覽器：http://localhost:5000
7. 首次使用請訪問：http://localhost:5000/init-db

【測試帳號】
用戶名：admin
密碼：admin123

【關閉方式】
1. 按 Ctrl+C
2. 執行：docker-compose down

【注意事項】
- 首次啟動需要下載映像，請確保網路暢通
- 如遇問題，請執行：docker-compose down -v
  然後重新啟動：docker-compose up

【問題排查】
Q: Port 5000 已被占用？
A: 修改 docker-compose.yml 的 ports 為 "8080:5000"
   然後訪問 http://localhost:8080

Q: 資料庫連接失敗？
A: 執行 docker-compose down -v 重置

【聯絡我們】
如有問題請聯絡：
- BA06110067 楊鈞淋
- 113590029 鄧玉璿
- 113590030 阿木樂

感謝您的指導！
=================================
```

---

## 🔧 進階功能

### 自動初始化資料庫

`docker-compose.yml` 已經包含自動初始化，無需手動訪問 `/init-db`

### 查看資料庫

```bash
# 進入資料庫容器
docker-compose exec db psql -U postgres -d groupbuy_system

# 查看所有表
\dt

# 查看用戶
SELECT * FROM users;

# 退出
\q
```

### 備份資料

```bash
# 備份
docker-compose exec db pg_dump -U postgres groupbuy_system > backup.sql

# 還原
docker-compose exec -T db psql -U postgres groupbuy_system < backup.sql
```

---

## ⚡ 快速啟動腳本

### Windows (start.bat)

```batch
@echo off
echo ================================
echo 團購平台啟動中...
echo ================================
docker-compose up
pause
```

### macOS/Linux (start.sh)

```bash
#!/bin/bash
echo "================================"
echo "團購平台啟動中..."
echo "================================"
docker-compose up
```

使用方式：
```bash
# macOS/Linux
chmod +x start.sh
./start.sh

# Windows
雙擊 start.bat
```

---

## 📊 Docker 方案優缺點

### 優點
✅ 一鍵啟動，無需配置  
✅ 環境完全一致  
✅ 自動處理資料庫  
✅ 易於清理（不留痕跡）  
✅ 支援所有作業系統  

### 缺點
❌ 需要安裝 Docker（約 500 MB）  
❌ 首次啟動需要下載映像（5-10 分鐘）  
❌ 需要一些硬碟空間  

### 適用場景
- ✅ 教授有技術背景
- ✅ 需要在多台電腦展示
- ✅ 想要乾淨的安裝/卸載
- ✅ 不想手動設定資料庫

---

## 🎯 推薦組合

**最佳方案：Render + Docker**

1. **主要展示**：使用 Render 部署的線上版本
   - 給教授一個永久網址
   - 隨時可以訪問

2. **備用方案**：提供 Docker 版本
   - 以防網路問題
   - 可以離線展示

這樣雙保險，萬無一失！
