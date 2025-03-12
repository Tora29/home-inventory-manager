#!/bin/bash
set -e

echo "データベースマイグレーションを実行します..."
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

echo "マイグレーション完了"

# アプリケーションを起動
exec "$@" 