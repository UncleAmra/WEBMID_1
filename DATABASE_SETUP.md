# 🔧 PostgreSQL 資料庫設置指南

## 問題診斷

你遇到的錯誤：
```
database "groupbuy_system" does not exist
```

這表示：
1. ❌ PostgreSQL 沒有運行
2. ❌ 資料庫 `groupbuy_system` 還沒創建
3. ❌ 連接設定可能不正確

---

## 🚀 快速解決方案（推薦）

### 方法 1：使用自動化工具（最簡單）⭐⭐⭐⭐⭐

```bash
cd ~/Desktop/groupbuy_system  # 你的專案目錄

# 執行自動設置工具
python3 setup_database.py
```

這個工具會：
- ✅ 自動檢測 PostgreSQL
- ✅ 測試各種連接配置
- ✅ 自動創建資料庫
- ✅ 驗證連接
- ✅ 自動更新 app.py 設定

---

## 📋 手動解決方案

### 步驟 1：啟動 PostgreSQL

#### 如果你用 Postgres.app（macOS）

1. 打開 **Applications** 資料夾
2. 雙擊 **Postgres.app**
3. 確認頂部菜單欄有大象圖示
4. 點擊圖示，確認顯示 "Running"

#### 如果你用 Homebrew

```bash
# 啟動 PostgreSQL
brew services start postgresql@15

# 檢查狀態
brew services list | grep postgresql
```

### 步驟 2：創建資料庫

#### 方法 A：使用終端

```bash
# 如果用 Postgres.app
/Applications/Postgres.app/Contents/Versions/latest/bin/psql postgres

# 如果用 Homebrew 或系統安裝
psql postgres

# 進入 psql 後，執行：
CREATE DATABASE groupbuy_system;

# 確認創建成功
\l

# 退出
\q
```

#### 方法 B：使用 pgAdmin（圖形介面）

1. 打開 **pgAdmin**
2. 連接到 PostgreSQL 伺服器
3. 右鍵點擊 **Databases**
4. 選擇 **Create** → **Database...**
5. **Database** 欄位輸入：`groupbuy_system`
6. 點擊 **Save**

### 步驟 3：設定 app.py

編輯 `app.py` 第 11 行：

```python
# 根據你的設定修改
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://用戶名:密碼@localhost:5432/groupbuy_system')
```

常見配置：

```python
# 配置 1: 預設設定（最常見）
DATABASE_URL = 'postgresql://postgres:thisisme10@localhost:5432/groupbuy_system'

# 配置 2: 無密碼
DATABASE_URL = 'postgresql://postgres@localhost:5432/groupbuy_system'

# 配置 3: 使用當前用戶（Postgres.app 常見）
DATABASE_URL = 'postgresql://localhost:5432/groupbuy_system'
```

### 步驟 4：測試連接

```bash
# 啟動應用
python3 app.py

# 如果看到錯誤，記下錯誤訊息
```

---

## 🔍 故障排除

### 問題 1：找不到 psql 命令

**錯誤訊息：**
```
command not found: psql
```

**解決方案：**

如果用 Postgres.app：
```bash
# 使用完整路徑
/Applications/Postgres.app/Contents/Versions/latest/bin/psql postgres
```

或添加到 PATH：
```bash
# 編輯 ~/.zshrc 或 ~/.bash_profile
echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc

# 重新載入
source ~/.zshrc
```

### 問題 2：密碼錯誤

**錯誤訊息：**
```
FATAL: password authentication failed for user "postgres"
```

**解決方案：**

嘗試不同的密碼：
```bash
# 常見密碼
postgres
thisisme10
(空密碼)
```

或重設密碼：
```bash
# 如果你是 superuser
psql postgres
ALTER USER postgres PASSWORD 'newpassword';
\q
```

### 問題 3：Port 被占用

**錯誤訊息：**
```
could not connect to server: Connection refused
Is the server running on host "localhost" and accepting TCP/IP connections on port 5432?
```

**解決方案：**

檢查 PostgreSQL 是否運行：
```bash
# macOS
ps aux | grep postgres

# 檢查 port
lsof -i :5432
```

如果沒有運行，啟動它：
```bash
# Postgres.app
打開 Postgres.app

# Homebrew
brew services start postgresql@15
```

### 問題 4：權限問題

**錯誤訊息：**
```
FATAL: role "your_username" does not exist
```

**解決方案：**

創建用戶或使用 postgres 用戶：
```bash
# 使用 postgres 用戶連接
psql -U postgres postgres

# 或創建你的用戶
psql postgres
CREATE USER your_username WITH PASSWORD 'password' CREATEDB;
\q
```

---

## ✅ 驗證清單

設置完成後，檢查以下項目：

```bash
# 1. PostgreSQL 正在運行
ps aux | grep postgres | grep -v grep

# 2. 可以連接到 postgres 資料庫
psql postgres -c "SELECT version();"

# 3. groupbuy_system 資料庫存在
psql postgres -c "\l" | grep groupbuy_system

# 4. 可以連接到 groupbuy_system
psql groupbuy_system -c "SELECT 1;"
```

全部通過？太好了！

---

## 🎯 下一步

資料庫設置完成後：

```bash
# 1. 啟動應用
python3 app.py

# 2. 在瀏覽器打開
http://localhost:5000

# 3. 初始化資料庫表（只需一次）
http://localhost:5000/init-db

# 4. 開始使用
用戶名: admin
密碼: admin123
```

---

## 📞 還是有問題？

提供以下資訊來診斷：

1. 你的作業系統：
   ```bash
   uname -a
   ```

2. PostgreSQL 版本：
   ```bash
   psql --version
   ```

3. PostgreSQL 狀態：
   ```bash
   ps aux | grep postgres
   ```

4. 具體錯誤訊息（完整）

5. 你的安裝方式：
   - [ ] Postgres.app
   - [ ] Homebrew
   - [ ] 其他

---

## 💡 小技巧

### 快速重置資料庫

```bash
# 刪除資料庫
psql postgres -c "DROP DATABASE IF EXISTS groupbuy_system;"

# 重新創建
psql postgres -c "CREATE DATABASE groupbuy_system;"

# 重新初始化
訪問 http://localhost:5000/init-db
```

### 查看資料庫內容

```bash
# 連接到資料庫
psql groupbuy_system

# 查看所有表
\dt

# 查看用戶
SELECT * FROM users;

# 查看團購
SELECT * FROM group_buying;

# 退出
\q
```

---

希望這能幫助你解決問題！🎉
