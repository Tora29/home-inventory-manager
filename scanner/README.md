# バーコードスキャナーリスナー

このモジュールはバーコードスキャナーからの入力を読み取り、API に送信するためのシステムです。

## 機能

- Bluetooth バーコードスキャナーからのバーコードを Linux `evdev` を使用して読み取り
- 読み取ったバーコードを Web サーバーの API に送信
- systemd サービスとしてバックグラウンドで実行
- 自動再接続機能と詳細なログ記録

## 必要条件

- Python 3.6 以上
- Linux サーバー (Ubuntu 推奨)
- バーコードスキャナー (NETUM Bluetooth バーコードスキャナーなど)
- 必要なパッケージ:
  - evdev (Linux デバイスイベント処理)
  - requests (HTTP 通信)
  - loguru (ログ管理)
  - python-dotenv (.env 設定ファイル読み込み)

## インストール

1. 依存パッケージをインストール:

```bash
pip install -r requirements.txt
```

2. 設定ファイルを調整:

   - `.env`ファイルを作成して環境変数を設定（オプション）
   - または`config.py`を直接編集

3. サービスとしてインストール:

```bash
cd service
sudo ./install_service.sh
```

## 設定オプション

`.env`ファイルまたは環境変数で以下の設定を変更できます:

- `API_HOST`: API サーバーの URL (デフォルト: "http://localhost:8000")
- `SCANNER_NAME`: スキャナーデバイス名の一部 (デフォルト: "NETUM")
- `SCANNER_TIMEOUT`: デバイス検索タイムアウト (デフォルト: 5 秒)
- `LOG_LEVEL`: ログレベル (デフォルト: "INFO")

## サービス管理

systemd サービスとしてインストール後:

```bash
# サービス開始
sudo systemctl start barcode-listener.service

# サービス停止
sudo systemctl stop barcode-listener.service

# サービス状態確認
sudo systemctl status barcode-listener.service

# ログ表示
sudo journalctl -u barcode-listener.service
```

## トラブルシューティング

1. スキャナーが認識されない場合:

   - `ls -l /dev/input/event*` でデバイスを確認
   - `evtest` コマンドでデバイスをテスト
   - `config.py` の `SCANNER_NAME` を調整

2. 権限エラーの場合:

   - サービスが root 権限で実行されているか確認
   - 入力デバイスへのアクセス権を確認

3. API と通信できない場合:
   - ネットワーク接続を確認
   - `curl` コマンドで API を直接テスト
   - ログを確認して詳細なエラーメッセージを確認
