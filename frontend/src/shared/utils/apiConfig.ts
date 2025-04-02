/**
 * API設定の共通モジュール
 */

// 本番環境かどうかを判定
export const isProduction = import.meta.env.PUBLIC_ENV === 'production';

// API基本URL - 本番環境では相対パスを使用
export const API_BASE_URL = isProduction ? '/v1' : 'http://localhost:8000/v1';
