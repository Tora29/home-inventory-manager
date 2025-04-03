import os
import sys
from loguru import logger
from config import LOG_FILE, LOG_LEVEL, LOG_ROTATION, LOG_DIR

def setup_logging():
    """
    ロギング設定をセットアップする
    """
    # ログディレクトリがなければ作成
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # デフォルトのロガーを削除
    logger.remove()
    
    # 標準出力へのロガー
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL
    )
    
    # ファイルへのロガー
    logger.add(
        LOG_FILE,
        rotation=LOG_ROTATION,  # ローテーション期間
        retention="30 days",    # ログ保持期間
        compression="zip",      # 圧縮形式
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=LOG_LEVEL
    )
    
    logger.info(f"ログ初期化完了 (レベル: {LOG_LEVEL}, ファイル: {LOG_FILE})")
    
    return logger 