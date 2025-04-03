#!/bin/bash

# このスクリプトはバーコードリスナーサービスをインストールします
# sudo権限で実行する必要があります

# パスが正しいか確認
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCANNER_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="$SCRIPT_DIR/barcode-listener.service"
TARGET_SERVICE_PATH="/etc/systemd/system/barcode-listener.service"

# 権限チェック
if [ "$EUID" -ne 0 ]; then
  echo "このスクリプトはroot権限で実行する必要があります。"
  echo "sudo $0 を実行してください。"
  exit 1
fi

# サービスファイルが存在するか確認
if [ ! -f "$SERVICE_FILE" ]; then
  echo "エラー: サービスファイルが見つかりません: $SERVICE_FILE"
  exit 1
fi

echo "バーコードリスナーサービスをインストールしています..."

# サービスファイルを編集（パスを置換）
sed "s|/path/to/home-inventory-manager/scanner|$SCANNER_DIR|g" "$SERVICE_FILE" > "$TARGET_SERVICE_PATH"

# 権限設定
chmod 644 "$TARGET_SERVICE_PATH"

# 依存パッケージをインストール
echo "必要なパッケージをインストールしています..."
pip3 install -r "$SCANNER_DIR/requirements.txt"

# サービスをリロードして有効化
systemctl daemon-reload
systemctl enable barcode-listener.service
systemctl start barcode-listener.service

# ステータスを確認
echo "サービスステータス:"
systemctl status barcode-listener.service

echo "インストール完了。以下のコマンドでサービスを管理できます:"
echo "  サービス開始: sudo systemctl start barcode-listener.service"
echo "  サービス停止: sudo systemctl stop barcode-listener.service"
echo "  状態確認: sudo systemctl status barcode-listener.service"
echo "  ログ確認: sudo journalctl -u barcode-listener.service" 