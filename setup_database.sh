#!/bin/bash

echo "================================"
echo "PostgreSQL 資料庫設置工具"
echo "================================"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢測 PostgreSQL 安裝方式
check_postgres() {
    echo -e "${BLUE}正在檢查 PostgreSQL 安裝狀態...${NC}"
    echo ""
    
    # 方法 1: 檢查 Postgres.app
    if [ -d "/Applications/Postgres.app" ]; then
        echo -e "${GREEN}✓ 找到 Postgres.app${NC}"
        POSTGRES_TYPE="app"
        PSQL_PATH="/Applications/Postgres.app/Contents/Versions/latest/bin/psql"
        return 0
    fi
    
    # 方法 2: 檢查 Homebrew
    if command -v brew &> /dev/null; then
        if brew list postgresql@15 &> /dev/null 2>&1; then
            echo -e "${GREEN}✓ 找到 Homebrew PostgreSQL${NC}"
            POSTGRES_TYPE="brew"
            PSQL_PATH="psql"
            return 0
        fi
    fi
    
    # 方法 3: 檢查系統 psql
    if command -v psql &> /dev/null; then
        echo -e "${GREEN}✓ 找到系統 PostgreSQL${NC}"
        POSTGRES_TYPE="system"
        PSQL_PATH="psql"
        return 0
    fi
    
    echo -e "${RED}✗ 未找到 PostgreSQL${NC}"
    return 1
}

# 啟動 PostgreSQL
start_postgres() {
    echo ""
    echo -e "${BLUE}正在啟動 PostgreSQL...${NC}"
    
    if [ "$POSTGRES_TYPE" = "app" ]; then
        echo "請手動啟動 Postgres.app："
        echo "1. 打開 Applications 資料夾"
        echo "2. 雙擊 Postgres.app"
        echo "3. 點擊大象圖示"
        echo ""
        read -p "已啟動 Postgres.app？按 Enter 繼續..."
        
    elif [ "$POSTGRES_TYPE" = "brew" ]; then
        brew services start postgresql@15
        echo -e "${GREEN}✓ PostgreSQL 已啟動${NC}"
        sleep 2
        
    elif [ "$POSTGRES_TYPE" = "system" ]; then
        pg_ctl -D /usr/local/var/postgres start
        echo -e "${GREEN}✓ PostgreSQL 已啟動${NC}"
        sleep 2
    fi
}

# 創建資料庫
create_database() {
    echo ""
    echo -e "${BLUE}正在創建資料庫 'groupbuy_system'...${NC}"
    
    # 嘗試創建資料庫
    $PSQL_PATH postgres -c "CREATE DATABASE groupbuy_system;" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 資料庫創建成功${NC}"
    else
        echo -e "${YELLOW}⚠ 資料庫可能已存在（這是正常的）${NC}"
    fi
    
    # 確認資料庫存在
    echo ""
    echo -e "${BLUE}確認資料庫列表：${NC}"
    $PSQL_PATH postgres -c "\l" | grep groupbuy_system
}

# 測試連接
test_connection() {
    echo ""
    echo -e "${BLUE}測試資料庫連接...${NC}"
    
    $PSQL_PATH groupbuy_system -c "SELECT version();" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 資料庫連接成功！${NC}"
        return 0
    else
        echo -e "${RED}✗ 資料庫連接失敗${NC}"
        return 1
    fi
}

# 獲取連接字串
get_connection_string() {
    echo ""
    echo -e "${BLUE}資料庫連接資訊：${NC}"
    echo ""
    echo -e "${GREEN}連接字串（用於 app.py）：${NC}"
    echo "postgresql://postgres:thisisme10@localhost:5432/groupbuy_system"
    echo ""
    echo -e "${YELLOW}請確認：${NC}"
    echo "1. 用戶名：postgres"
    echo "2. 密碼：thisisme10 (如果不對請修改)"
    echo "3. Port：5432"
    echo "4. 資料庫名：groupbuy_system"
}

# 主流程
main() {
    # 檢查 PostgreSQL
    if ! check_postgres; then
        echo ""
        echo -e "${RED}請先安裝 PostgreSQL：${NC}"
        echo ""
        echo "方法 1: 下載 Postgres.app"
        echo "  https://postgresapp.com"
        echo ""
        echo "方法 2: 使用 Homebrew"
        echo "  brew install postgresql@15"
        echo ""
        exit 1
    fi
    
    # 啟動 PostgreSQL
    start_postgres
    
    # 創建資料庫
    create_database
    
    # 測試連接
    test_connection
    
    # 顯示連接資訊
    get_connection_string
    
    echo ""
    echo "================================"
    echo -e "${GREEN}資料庫設置完成！${NC}"
    echo "================================"
    echo ""
    echo "下一步："
    echo "1. 確認 app.py 中的 DATABASE_URL 設定正確"
    echo "2. 執行：python3 app.py"
    echo "3. 訪問：http://localhost:5000/init-db"
    echo ""
}

# 執行主程式
main
