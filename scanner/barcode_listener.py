#!/usr/bin/env python3
"""
バーコードスキャナーからの入力を読み取り、APIにデータを送信するスクリプト
"""
import evdev
import requests
import time
import signal
import sys
import os

# 相対インポート
from logging_setup import setup_logging
from device_utils import find_scanner, get_character_from_keycode
from config import STOCK_IN_ENDPOINT

# ロギング設定
logger = setup_logging()

# 終了フラグ
running = True

def signal_handler(sig, frame):
    """シグナルハンドラ - プログラム終了時の処理"""
    global running
    logger.info("終了シグナルを受信しました")
    running = False
    sys.exit(0)

def process_barcode(barcode):
    """
    バーコードをAPIに送信
    
    Args:
        barcode: スキャンされたバーコード文字列
    """
    if not barcode:
        logger.warning("空のバーコードをスキップします")
        return
    
    logger.info(f"バーコード処理: {barcode}")
    
    try:
        # APIにPOSTリクエスト送信
        response = requests.post(
            STOCK_IN_ENDPOINT,
            json={"barcode": barcode},
            timeout=5  # タイムアウト設定
        )
        
        # レスポンスの確認
        if response.status_code == 200:
            logger.info(f"API送信成功: {response.status_code}")
            try:
                data = response.json()
                logger.debug(f"レスポンスデータ: {data}")
            except Exception:
                logger.debug(f"レスポンスボディ: {response.text}")
        else:
            logger.error(f"API送信エラー: ステータスコード {response.status_code}")
            logger.error(f"レスポンス: {response.text}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API接続エラー: {e}")
    except Exception as e:
        logger.error(f"予期せぬエラー: {e}")

def main():
    """メイン実行関数"""
    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("バーコードリスナーを起動しています...")
    
    # スキャナーを検索
    scanner = None
    while running and scanner is None:
        scanner = find_scanner()
        if scanner is None:
            logger.warning("スキャナーが見つかりません。5秒後に再試行します")
            time.sleep(5)
    
    if not running:
        return
    
    logger.info(f"スキャナー接続: {scanner.name} ({scanner.path})")
    
    # 排他的なデバイスアクセスを取得
    try:
        scanner.grab()
        logger.info("スキャナーへの排他的アクセスを取得しました")
    except Exception as e:
        logger.error(f"スキャナーのグラブに失敗: {e}")
        return
    
    # バーコードバッファ
    barcode_buffer = ""
    last_event_time = time.time()
    timeout = 1.0  # バーコード入力のタイムアウト (秒)
    
    try:
        # イベントループ
        logger.info("スキャン待機中...")
        
        for event in scanner.read_loop():
            if not running:
                break
                
            # キーイベントのみ処理
            if event.type == evdev.ecodes.EV_KEY and event.value == 1:  # キー押下時
                current_time = time.time()
                
                # 一定時間入力がなかった場合、バッファをクリア
                if current_time - last_event_time > timeout and barcode_buffer:
                    logger.debug(f"タイムアウトによりバッファをクリア: {barcode_buffer}")
                    barcode_buffer = ""
                
                last_event_time = current_time
                
                # キー入力を処理
                key_event = evdev.categorize(event)
                
                # Enterキーが押されたらバーコード処理
                if key_event.keycode == "KEY_ENTER":
                    if barcode_buffer:
                        process_barcode(barcode_buffer)
                        barcode_buffer = ""
                else:
                    # バーコードにキー文字を追加
                    char = get_character_from_keycode(key_event.keycode)
                    if char:
                        barcode_buffer += char
                        logger.debug(f"バッファ更新: {barcode_buffer}")
    
    except Exception as e:
        logger.error(f"イベント処理中にエラーが発生: {e}")
    
    finally:
        # 終了処理
        try:
            scanner.ungrab()
            logger.info("スキャナーの排他的アクセスを解放しました")
        except Exception as e:
            logger.error(f"スキャナー解放中にエラー: {e}")

if __name__ == "__main__":
    main() 