# 團購平台 Group Buying Platform

## 專案簡介
這是一個功能完整的團購網站平台，使用 Flask 和 PostgreSQL 建構，前端採用 SB Admin 2 模板。

### 主要功能
- **用戶系統**：註冊、登入、權限管理
- **瀏覽團購**：查看所有進行中的團購活動
- **團購詳情**：查看商品資訊、進度、參與成員
- **開團功能**：創建新的團購活動
- **跟團功能**：加入喜歡的團購
- **訂單管理**：查看個人訂單歷史
- **後台管理**：管理所有團購活動（管理員/團長）

## 系統架構
```
使用者 → Frontend (HTML/CSS/JS + Bootstrap)
         ↓
      Backend (Flask / API)
         ↓
      Database (PostgreSQL)
```

### 資料庫設計
- **Users** - 用戶資訊
- **Products** - 商品資訊
- **GroupBuying** - 團購活動
- **Orders** - 訂單記錄

## 安裝與設置

### 1. 安裝依賴
```bash
pip3 install -r requirements.txt --break-system-packages
```

### 2. 設置資料庫
確保 PostgreSQL 已安裝並運行：
```bash
# 創建資料庫
psql -U postgres
CREATE DATABASE groupbuy_system;
\q
```

### 3. 修改資料庫連接
編輯 `app.py` 第 11 行，修改為你的資料庫連接：
```python
DATABASE_URL = 'postgresql://使用者:密碼@localhost:5432/groupbuy_system'
```

### 4. 初始化資料庫
訪問以下網址初始化資料庫（創建表格和測試數據）：
```
http://localhost:5000/init-db
```

預設管理員帳號：
- 用戶名：`admin`
- 密碼：`admin123`

### 5. 運行應用
```bash
python3 app.py
```

訪問：http://localhost:5000

## 路由說明

### 公開路由
- `/` - 首頁（重定向到瀏覽頁面）
- `/register` - 用戶註冊
- `/login` - 用戶登入
- `/browse` - 瀏覽團購列表

### 需要登入
- `/group/<id>` - 團購詳情
- `/create_group` - 開團
- `/join_group/<id>` - 跟團
- `/my-orders` - 我的訂單
- `/admin` - 後台管理（自己的團購）
- `/logout` - 登出

### 管理員功能
- `/admin/delete_group/<id>` - 刪除團購
- `/admin/close_group/<id>` - 關閉團購

## 技術棧
- **後端**：Flask 3.0
- **資料庫**：PostgreSQL + Flask-SQLAlchemy
- **前端**：SB Admin 2 (Bootstrap 4)
- **認證**：Session + Werkzeug (密碼加密)

## 部署到 Render

### 1. 準備檔案
確保專案包含：
- `requirements.txt`
- `app.py`
- `models.py`
- `.gitignore`

### 2. Push 到 GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <你的GitHub倉庫>
git push -u origin main
```

### 3. 在 Render 創建服務

#### 創建 PostgreSQL 資料庫
1. 登入 Render
2. 點擊 "New +" → "PostgreSQL"
3. 填寫資訊並創建
4. 複製 "Internal Database URL"

#### 創建 Web Service
1. 點擊 "New +" → "Web Service"
2. 連接你的 GitHub 倉庫
3. 設定：
   - **Name**: groupbuy-platform
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**:
     - `DATABASE_URL` = <你的 PostgreSQL URL>
     - `SECRET_KEY` = <隨機生成的密鑰>

4. 點擊 "Create Web Service"

### 4. 初始化資料庫
部署完成後，訪問：
```
https://你的應用名稱.onrender.com/init-db
```

## 使用提示

### 團長功能
- 可以創建團購
- 管理自己的團購
- 查看參與成員

### 一般用戶
- 瀏覽所有團購
- 加入喜歡的團購
- 查看訂單歷史

### 管理員
- 查看所有團購
- 管理所有團購活動
- 刪除不當內容

## 未來功能
- [ ] 付款功能整合
- [ ] 商品圖片上傳
- [ ] Email 通知
- [ ] 訂單評價系統
- [ ] 聊天功能
- [ ] 數據分析儀表板

## 團隊成員
- Group 8
- BA06110067 楊鈞淋
- 113590029 鄧玉璿
- 113590030 阿木樂

## 授權
MIT License
