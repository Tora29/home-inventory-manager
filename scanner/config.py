import os
from dotenv import load_dotenv

# .envファイルがあれば読み込む
load_dotenv()

# APIエンドポイント設定
API_HOST = os.getenv("API_HOST", "http://localhost:8000")
STOCK_IN_ENDPOINT = f"{API_HOST}/stock/in"

# スキャナー設定
SCANNER_NAME = os.getenv("SCANNER_NAME", "NETUM")  # スキャナーのデバイス名に含まれる文字列
SCANNER_TIMEOUT = int(os.getenv("SCANNER_TIMEOUT", "5"))  # デバイス検索のタイムアウト(秒)

# ログ設定
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "barcode_listener.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_ROTATION = "1 week"  # ローテーション期間 