# 🎓 教授電腦使用指南 - 三種方案

## 📊 方案比較表

| 方案 | 難度 | 準備時間 | 適用場景 | 推薦度 |
|------|------|----------|----------|--------|
| **方案 1: Render 線上部署** | ⭐ 極簡單 | 30 分鐘 | 隨時隨地展示 | ⭐⭐⭐⭐⭐ |
| **方案 2: Docker 容器** | ⭐⭐ 簡單 | 15 分鐘 | 離線展示 | ⭐⭐⭐⭐ |
| **方案 3: 手動安裝** | ⭐⭐⭐ 中等 | 20 分鐘 | 傳統方式 | ⭐⭐⭐ |

---

## 🏆 方案 1：Render 線上部署（最推薦）

### 給教授的說明

```
親愛的教授您好：

這是我們的團購平台專案，已部署至雲端。

🌐 訪問網址：
   https://你的應用名稱.onrender.com

📱 直接用瀏覽器打開即可，無需安裝任何軟體

⏰ 注意事項：
   - 首次訪問需等待 30 秒（免費方案限制）
   - 之後使用流暢無延遲

🔐 測試帳號：
   用戶名：admin
   密碼：admin123

📋 功能展示：
   1. 用戶註冊與登入
   2. 瀏覽團購商品
   3. 查看團購詳情
   4. 開團功能
   5. 跟團購買
   6. 訂單管理
   7. 後台管理

感謝您的指導！
```

### 部署步驟

詳見 `RENDER_DEPLOY.md`

### 優點
✅ 無需安裝  
✅ 隨時訪問  
✅ 永久網址  
✅ 自動 HTTPS  
✅ 支援手機  

---

## 🐳 方案 2：Docker 容器化（推薦備案）

### 給教授的說明

```
=================================
Docker 一鍵啟動版本
=================================

【前置需求】
僅需安裝 Docker Desktop：
https://www.docker.com/products/docker-desktop

【啟動步驟】
1. 解壓縮專案資料夾
2. 雙擊運行：
   - Windows: start.bat
   - Mac/Linux: start.sh
3. 等待啟動完成（首次約 5 分鐘）
4. 瀏覽器訪問：http://localhost:5000

【測試帳號】
用戶名：admin
密碼：admin123

【關閉方式】
按 Ctrl+C 或關閉視窗
```

### 部署步驟

詳見 `DOCKER_GUIDE.md`

### 優點
✅ 一鍵啟動  
✅ 環境一致  
✅ 易於清理  
✅ 離線可用  

---

## 💻 方案 3：傳統手動安裝

### 給教授的說明（macOS）

```
=================================
手動安裝版本（macOS）
=================================

【步驟 1】安裝 PostgreSQL
brew install postgresql@15
brew services start postgresql@15

【步驟 2】創建資料庫
psql postgres -c "CREATE DATABASE groupbuy_system;"

【步驟 3】安裝依賴
cd groupbuy_system
pip3 install -r requirements.txt --break-system-packages

【步驟 4】啟動應用
python3 app.py

【步驟 5】初始化
瀏覽器訪問：http://localhost:5000/init-db

【測試帳號】
用戶名：admin
密碼：admin123
```

### 給教授的說明（Windows）

```
=================================
手動安裝版本（Windows）
=================================

【步驟 1】安裝 PostgreSQL
1. 下載：https://www.postgresql.org/download/windows/
2. 安裝並記住密碼
3. 確保服務運行

【步驟 2】創建資料庫
1. 打開 pgAdmin
2. 右鍵 Databases → Create → Database
3. 名稱：groupbuy_system

【步驟 3】修改設定
編輯 app.py 第 11 行：
DATABASE_URL = 'postgresql://postgres:你的密碼@localhost:5432/groupbuy_system'

【步驟 4】安裝依賴
cd groupbuy_system
pip install -r requirements.txt

【步驟 5】啟動應用
python app.py

【步驟 6】初始化
瀏覽器訪問：http://localhost:5000/init-db

【測試帳號】
用戶名：admin
密碼：admin123
```

### 或使用自動化腳本

#### macOS/Linux:
```bash
chmod +x install.sh
./install.sh
```

#### Windows:
```
雙擊 install.bat
```

---

## 🎯 推薦使用策略

### 情境 1：期末報告展示
**方案**: Render 線上版本
- 提前部署好
- 給教授永久網址
- 隨時可以查看

### 情境 2：現場展示（有網路）
**方案**: Render 線上版本 + Docker 備案
- 主要用線上版本
- Docker 作為備用
- 雙重保險

### 情境 3：現場展示（無網路）
**方案**: Docker 容器
- 完全離線可用
- 環境一致
- 啟動快速

### 情境 4：需要修改代碼展示
**方案**: 手動安裝
- 可以即時修改
- 展示開發過程
- 靈活度高

---

## 📦 打包清單

### 提交給教授的檔案

```
groupbuy_system_submission/
│
├── 📄 README.md                    # 專案說明
├── 📄 HOW_TO_RUN.md               # 如何運行（重要！）
│
├── 🌐 方案 1: Render 部署
│   ├── RENDER_DEPLOY.md           # Render 部署指南
│   └── RENDER_URL.txt             # 已部署的網址
│
├── 🐳 方案 2: Docker（推薦）
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── DOCKER_GUIDE.md
│   ├── start.sh                   # Mac/Linux 啟動腳本
│   └── start.bat                  # Windows 啟動腳本
│
├── 💻 方案 3: 手動安裝
│   ├── install.sh                 # Mac/Linux 安裝腳本
│   ├── install.bat                # Windows 安裝腳本
│   └── MANUAL_INSTALL.md          # 手動安裝指南
│
├── 📁 應用程式檔案
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
└── 📋 文件
    ├── GROUP_8.pdf                # 專案報告
    ├── PRESENTATION.pdf           # 簡報
    └── DEMO_VIDEO.mp4            # 展示影片（選用）
```

---

## 📝 建議的 HOW_TO_RUN.md

```markdown
# 如何運行團購平台

## 🚀 快速開始（三選一）

### 選項 A：線上版本（最簡單）⭐⭐⭐⭐⭐

直接訪問：**https://你的應用名稱.onrender.com**

- 無需安裝任何東西
- 首次訪問等待 30 秒
- 測試帳號：admin / admin123

---

### 選項 B：Docker 版本（推薦）⭐⭐⭐⭐

1. 安裝 Docker Desktop
2. 雙擊運行啟動腳本：
   - Windows: `start.bat`
   - Mac/Linux: `start.sh`
3. 訪問：http://localhost:5000

---

### 選項 C：手動安裝 ⭐⭐⭐

#### macOS
```bash
./install.sh
```

#### Windows
```
雙擊 install.bat
```

---

## 📞 聯絡資訊

如有問題請聯絡：
- BA06110067 楊鈞淋
- 113590029 鄧玉璿  
- 113590030 阿木樂

---

## 🎓 功能展示清單

- [x] 用戶註冊與登入
- [x] 瀏覽團購列表
- [x] 團購詳情頁面
- [x] 開團功能
- [x] 跟團購買
- [x] 訂單管理
- [x] 後台管理
- [x] 響應式設計

感謝您的指導！
```

---

## ✅ 檢查清單

在提交前確認：

- [ ] Render 部署成功且可訪問
- [ ] Docker 版本測試通過
- [ ] 手動安裝腳本測試通過
- [ ] 所有文件檔案齊全
- [ ] README 說明清楚
- [ ] 測試帳號可用（admin/admin123）
- [ ] 已創建示範資料
- [ ] 截圖/影片準備好
- [ ] 報告已完成
- [ ] 簡報已完成

---

## 🎬 展示技巧

1. **提前測試**
   - 展示前一天測試所有方案
   - 確保 Render 網站正常運行
   - 準備好備用方案

2. **多重備份**
   - 線上版本（Render）
   - 本地 Docker 版本
   - USB 隨身碟備份

3. **準備說明**
   - 印出快速指南
   - 準備故障排除方案
   - 記錄所有網址和密碼

4. **時間掌控**
   - Render 首次訪問提前 1 分鐘
   - Docker 啟動需要 30 秒
   - 保留緩衝時間

---

## 💡 最佳實踐建議

### 給學生
1. **至少提前 3 天完成部署**
2. **測試所有三種方案**
3. **準備完整的文件**
4. **錄製展示影片作為備用**

### 給教授
1. **推薦使用線上版本**（最簡單）
2. **如需本地運行，推薦 Docker**（最可靠）
3. **提供完整文件供參考**

---

Good luck! 🎉
```

---

## 🎁 額外資源

### 創建示範影片
```bash
# 使用 QuickTime (Mac) 或 OBS Studio 錄製
# 內容包括：
- 登入過程
- 瀏覽團購
- 開團流程
- 跟團購買
- 查看訂單
- 後台管理
```

### 準備簡報
重點展示：
1. 系統架構圖
2. 資料庫設計
3. 主要功能截圖
4. 技術棧說明
5. 部署方式
6. 團隊分工

---

希望這份指南對你有幫助！🚀
