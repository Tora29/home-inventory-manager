import evdev
import time
from loguru import logger
from config import SCANNER_NAME, SCANNER_TIMEOUT

def find_scanner():
    """
    接続されているデバイスからバーコードスキャナーを検出する
    """
    start_time = time.time()
    logger.info("バーコードスキャナーの検索を開始")
    
    while time.time() - start_time < SCANNER_TIMEOUT:
        try:
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                logger.debug(f"検出されたデバイス: {device.name} ({device.path})")
                if SCANNER_NAME.lower() in device.name.lower():
                    logger.info(f"スキャナーを検出: {device.name} ({device.path})")
                    return device
            
            # 見つからなかった場合は少し待ってリトライ
            time.sleep(1)
        except Exception as e:
            logger.error(f"デバイス検索中にエラー: {e}")
            time.sleep(1)
    
    logger.warning(f"タイムアウト: {SCANNER_TIMEOUT}秒以内にスキャナーが見つかりませんでした")
    return None

def get_character_from_keycode(keycode):
    """
    evdevのキーコードから文字を抽出
    """
    # キーコードが配列の場合は最初の要素を使用
    if isinstance(keycode, list):
        keycode = keycode[0]
    
    # キーコードから文字を取得
    if keycode.startswith('KEY_'):
        key = keycode[4:]  # 'KEY_' を削除
        
        # 数字キー
        if key.isdigit():
            return key
        
        # 特殊キー
        if key == 'MINUS':
            return '-'
        elif key == 'DOT':
            return '.'
        elif key == 'SPACE':
            return ' '
        
        # アルファベット (小文字に変換)
        return key.lower()
    
    return ''
