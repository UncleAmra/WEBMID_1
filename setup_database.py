#!/usr/bin/env python3
"""
PostgreSQL 資料庫設置工具
自動創建 groupbuy_system 資料庫並測試連接
"""

import sys
import subprocess
import time

def print_header(text):
    """印出標題"""
    print("\n" + "="*50)
    print(text)
    print("="*50 + "\n")

def print_success(text):
    """印出成功訊息"""
    print(f"✓ {text}")

def print_error(text):
    """印出錯誤訊息"""
    print(f"✗ {text}")

def print_warning(text):
    """印出警告訊息"""
    print(f"⚠ {text}")

def check_psycopg2():
    """檢查 psycopg2 是否已安裝"""
    try:
        import psycopg2
        return True
    except ImportError:
        return False

def install_psycopg2():
    """安裝 psycopg2"""
    print("正在安裝 psycopg2...")
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "psycopg2-binary",
            "--break-system-packages"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("psycopg2 安裝完成")
        return True
    except:
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "psycopg2-binary"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success("psycopg2 安裝完成")
            return True
        except:
            print_error("無法安裝 psycopg2")
            return False

def test_postgres_connection(password="thisisme10"):
    """測試 PostgreSQL 連接"""
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    configs = [
        # 配置 1: 標準設定
        {
            "host": "localhost",
            "user": "postgres",
            "password": password,
            "port": 5432,
            "database": "postgres"
        },
        # 配置 2: 無密碼
        {
            "host": "localhost",
            "user": "postgres",
            "password": "",
            "port": 5432,
            "database": "postgres"
        },
        # 配置 3: 使用當前用戶
        {
            "host": "localhost",
            "user": subprocess.getoutput("whoami"),
            "password": "",
            "port": 5432,
            "database": "postgres"
        },
    ]
    
    for i, config in enumerate(configs, 1):
        try:
            print(f"\n嘗試配置 {i}: user={config['user']}, password={'***' if config['password'] else '(無)'}")
            conn = psycopg2.connect(**config)
            print_success("連接成功！")
            return conn, config
        except Exception as e:
            print_error(f"連接失敗: {str(e)[:50]}")
            continue
    
    return None, None

def create_database(conn, config):
    """創建資料庫"""
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        # 檢查資料庫是否已存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='groupbuy_system'")
        exists = cursor.fetchone()
        
        if exists:
            print_warning("資料庫 'groupbuy_system' 已存在")
        else:
            cursor.execute("CREATE DATABASE groupbuy_system")
            print_success("資料庫 'groupbuy_system' 創建成功")
        
        cursor.close()
        return True
        
    except Exception as e:
        print_error(f"創建資料庫失敗: {e}")
        cursor.close()
        return False

def verify_database(config):
    """驗證資料庫"""
    import psycopg2
    
    try:
        test_config = config.copy()
        test_config['database'] = 'groupbuy_system'
        
        conn = psycopg2.connect(**test_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        
        print_success("資料庫驗證成功")
        print(f"   PostgreSQL 版本: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"驗證失敗: {e}")
        return False

def generate_connection_string(config):
    """生成連接字串"""
    password = config['password'] if config['password'] else ''
    conn_str = f"postgresql://{config['user']}"
    
    if password:
        conn_str += f":{password}"
    
    conn_str += f"@{config['host']}:{config['port']}/groupbuy_system"
    
    return conn_str

def main():
    """主程式"""
    print_header("PostgreSQL 資料庫設置工具")
    
    # 步驟 1: 檢查並安裝 psycopg2
    print("步驟 1/4: 檢查依賴...")
    if not check_psycopg2():
        print_warning("psycopg2 未安裝")
        if not install_psycopg2():
            print_error("請手動安裝: pip3 install psycopg2-binary")
            return False
    else:
        print_success("psycopg2 已安裝")
    
    # 重新導入
    import psycopg2
    
    # 步驟 2: 測試連接
    print("\n步驟 2/4: 測試 PostgreSQL 連接...")
    
    # 如果用戶想自定義密碼
    print("\n請輸入 PostgreSQL 密碼（直接按 Enter 使用預設: thisisme10）")
    custom_password = input("密碼: ").strip()
    password = custom_password if custom_password else "thisisme10"
    
    conn, config = test_postgres_connection(password)
    
    if not conn:
        print_error("\n無法連接到 PostgreSQL")
        print("\n請確認：")
        print("1. PostgreSQL 是否正在運行？")
        print("   - macOS: 打開 Postgres.app 或執行 'brew services start postgresql@15'")
        print("   - Linux: sudo systemctl start postgresql")
        print("\n2. 密碼是否正確？")
        print("   - 預設密碼通常是空的或 'postgres'")
        return False
    
    # 步驟 3: 創建資料庫
    print("\n步驟 3/4: 創建資料庫...")
    if not create_database(conn, config):
        conn.close()
        return False
    
    conn.close()
    
    # 步驟 4: 驗證
    print("\n步驟 4/4: 驗證資料庫...")
    if not verify_database(config):
        return False
    
    # 完成
    print_header("設置完成！")
    
    conn_str = generate_connection_string(config)
    
    print("資料庫連接資訊：")
    print(f"  主機: {config['host']}")
    print(f"  端口: {config['port']}")
    print(f"  用戶: {config['user']}")
    print(f"  密碼: {'***' if config['password'] else '(無)'}")
    print(f"  資料庫: groupbuy_system")
    
    print(f"\n連接字串（用於 app.py）：")
    print(f"  {conn_str}")
    
    print("\n下一步：")
    print("1. 複製上面的連接字串")
    print("2. 編輯 app.py 第 11 行，替換 DATABASE_URL")
    print("3. 執行: python3 app.py")
    print("4. 訪問: http://localhost:5000/init-db")
    
    # 詢問是否自動更新 app.py
    print("\n" + "="*50)
    update = input("是否自動更新 app.py 中的 DATABASE_URL？(y/n): ").lower()
    
    if update == 'y':
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替換 DATABASE_URL
            import re
            pattern = r"DATABASE_URL = os\.environ\.get\('DATABASE_URL', '([^']+)'\)"
            replacement = f"DATABASE_URL = os.environ.get('DATABASE_URL', '{conn_str}')"
            
            new_content = re.sub(pattern, replacement, content)
            
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print_success("app.py 已更新！")
        except Exception as e:
            print_error(f"更新失敗: {e}")
            print("請手動更新 app.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(1)
    except Exception as e:
        print_error(f"發生錯誤: {e}")
        sys.exit(1)
