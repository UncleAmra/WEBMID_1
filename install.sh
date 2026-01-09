#!/bin/bash

# 團購平台自動安裝腳本
# 支援 macOS 和 Linux

set -e

echo "================================"
echo "團購平台自動安裝程式"
echo "Group 8"
echo "================================"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 檢測作業系統
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "${GREEN}檢測到作業系統: ${MACHINE}${NC}"
echo ""

# 函數：檢查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 函數：安裝 PostgreSQL
install_postgres() {
    echo -e "${YELLOW}正在安裝 PostgreSQL...${NC}"
    
    if [ "$MACHINE" = "Mac" ]; then
        if command_exists brew; then
            brew install postgresql@15
            brew services start postgresql@15
        else
            echo -e "${RED}請先安裝 Homebrew: https://brew.sh${NC}"
            exit 1
        fi
    elif [ "$MACHINE" = "Linux" ]; then
        sudo apt-get update
        sudo apt-get install -y postgresql postgresql-contrib
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
    fi
    
    echo -e "${GREEN}✓ PostgreSQL 安裝完成${NC}"
}

# 函數：創建資料庫
create_database() {
    echo -e "${YELLOW}正在創建資料庫...${NC}"
    
    if [ "$MACHINE" = "Mac" ]; then
        psql postgres -c "CREATE DATABASE groupbuy_system;" 2>/dev/null || echo "資料庫可能已存在"
    elif [ "$MACHINE" = "Linux" ]; then
        sudo -u postgres psql -c "CREATE DATABASE groupbuy_system;" 2>/dev/null || echo "資料庫可能已存在"
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
    fi
    
    echo -e "${GREEN}✓ 資料庫創建完成${NC}"
}

# 步驟 1: 檢查 Python
echo -e "${YELLOW}步驟 1/5: 檢查 Python...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python ${PYTHON_VERSION} 已安裝${NC}"
else
    echo -e "${RED}✗ 請先安裝 Python 3.8+${NC}"
    exit 1
fi
echo ""

# 步驟 2: 檢查 PostgreSQL
echo -e "${YELLOW}步驟 2/5: 檢查 PostgreSQL...${NC}"
if command_exists psql; then
    POSTGRES_VERSION=$(psql --version | cut -d' ' -f3)
    echo -e "${GREEN}✓ PostgreSQL ${POSTGRES_VERSION} 已安裝${NC}"
else
    echo -e "${YELLOW}PostgreSQL 未安裝${NC}"
    read -p "是否要自動安裝 PostgreSQL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_postgres
    else
        echo -e "${RED}請手動安裝 PostgreSQL 後再次執行此腳本${NC}"
        exit 1
    fi
fi
echo ""

# 步驟 3: 安裝 Python 依賴
echo -e "${YELLOW}步驟 3/5: 安裝 Python 依賴...${NC}"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
    echo -e "${GREEN}✓ Python 依賴安裝完成${NC}"
else
    echo -e "${RED}✗ 找不到 requirements.txt${NC}"
    exit 1
fi
echo ""

# 步驟 4: 創建資料庫
echo -e "${YELLOW}步驟 4/5: 設置資料庫...${NC}"
create_database
echo ""

# 步驟 5: 啟動應用
echo -e "${YELLOW}步驟 5/5: 啟動應用...${NC}"
echo ""
echo "================================"
echo -e "${GREEN}安裝完成！${NC}"
echo "================================"
echo ""
echo "現在將啟動應用..."
echo ""
echo "請在瀏覽器中訪問："
echo -e "${GREEN}http://localhost:5000${NC}"
echo ""
echo "首次使用請訪問："
echo -e "${GREEN}http://localhost:5000/init-db${NC}"
echo ""
echo "測試帳號："
echo "  用戶名: admin"
echo "  密碼: admin123"
echo ""
echo "按 Ctrl+C 停止應用"
echo ""
echo "================================"
echo ""

# 等待用戶確認
read -p "按 Enter 開始啟動..." -r
echo ""

# 啟動應用
python3 app.py
