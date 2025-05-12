/**
 * API設定の共通モジュール
 */

// 本番環境かどうかを判定
export const isProduction = import.meta.env.PUBLIC_ENV === 'production';

// 環境変数のPUBLIC_API_BASE_URLのみを使用する
export const API_BASE_URL = import.meta.env.DEV 
  ? 'http://localhost:8000/v1'
  : import.meta.env.PUBLIC_API_BASE_URL;
