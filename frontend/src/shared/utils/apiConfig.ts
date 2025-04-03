/**
 * API設定の共通モジュール
 */

// 本番環境かどうかを判定
export const isProduction = import.meta.env.PUBLIC_ENV === 'production';

// API基本URL
export const API_BASE_URL = 'http://localhost:8000/v1';
