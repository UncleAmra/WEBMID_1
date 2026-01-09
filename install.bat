@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================
echo 團購平台自動安裝程式
echo Group 8
echo ================================
echo.

REM 檢查 Python
echo 步驟 1/4: 檢查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 請先安裝 Python 3.8+
    echo 下載: https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [成功] Python %PYTHON_VERSION% 已安裝
echo.

REM 檢查 PostgreSQL
echo 步驟 2/4: 檢查 PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] PostgreSQL 未安裝或不在 PATH 中
    echo.
    echo 請手動完成以下步驟：
    echo 1. 下載 PostgreSQL: https://www.postgresql.org/download/windows/
    echo 2. 安裝時記住密碼（預設: postgres）
    echo 3. 確保 PostgreSQL 服務正在運行
    echo 4. 使用 pgAdmin 創建資料庫 'groupbuy_system'
    echo.
    set /p SKIP_DB="已完成 PostgreSQL 設置？(y/n): "
    if /i "!SKIP_DB!" neq "y" (
        echo 請完成 PostgreSQL 設置後重新執行
        pause
        exit /b 1
    )
) else (
    for /f "tokens=3" %%i in ('psql --version 2^>^&1') do set PG_VERSION=%%i
    echo [成功] PostgreSQL !PG_VERSION! 已安裝
)
echo.

REM 安裝 Python 依賴
echo 步驟 3/4: 安裝 Python 依賴...
if exist requirements.txt (
    pip install -r requirements.txt
    echo [成功] Python 依賴安裝完成
) else (
    echo [錯誤] 找不到 requirements.txt
    pause
    exit /b 1
)
echo.

REM 配置提示
echo 步驟 4/4: 配置檢查...
echo.
echo 請確認 app.py 中的資料庫連接設定：
echo   DATABASE_URL = 'postgresql://postgres:你的密碼@localhost:5432/groupbuy_system'
echo.
set /p DB_READY="資料庫已創建且設定正確？(y/n): "
if /i "!DB_READY!" neq "y" (
    echo.
    echo 請完成以下步驟：
    echo 1. 打開 pgAdmin
    echo 2. 右鍵 Databases → Create → Database
    echo 3. 名稱輸入: groupbuy_system
    echo 4. 檢查 app.py 的 DATABASE_URL 設定
    echo.
    pause
    exit /b 1
)
echo.

REM 啟動應用
echo ================================
echo [成功] 安裝完成！
echo ================================
echo.
echo 現在將啟動應用...
echo.
echo 請在瀏覽器中訪問：
echo   http://localhost:5000
echo.
echo 首次使用請訪問：
echo   http://localhost:5000/init-db
echo.
echo 測試帳號：
echo   用戶名: admin
echo   密碼: admin123
echo.
echo 按 Ctrl+C 停止應用
echo ================================
echo.
pause

REM 啟動應用
python app.py
