/**
 * APIエラーを処理する関数
 * エラーメッセージを整形して例外をスロー
 */
export const handleApiError = async (response: Response): Promise<never> => {
  let errorBody = '';
  
  try {
    // JSONレスポンスに対応
    if (response.headers.get('content-type')?.includes('application/json')) {
      const json = await response.json();
      errorBody = JSON.stringify(json);
    } else {
      // テキストレスポンス
      errorBody = await response.text();
    }
  } catch {
    errorBody = 'レスポンスを取得できません';
  }

  // 詳細なエラーメッセージをスロー
  throw new Error(`APIエラー: ${response.status} - ${response.statusText} - ${errorBody}`);
};
  
/**
 * APIリクエストを安全に実行する汎用関数
 * @param requestFn API呼び出しの非同期関数
 * @param fallbackValue エラー時のフォールバック値
 * @returns API呼び出しの結果またはフォールバック値
 */
export async function safeApiCall<T>(
  requestFn: () => Promise<T>,
  fallbackValue: T,
  errorHandler?: (error: Error) => void
): Promise<T> {
  try {
    return await requestFn();
  } catch (error) {
    if (errorHandler && error instanceof Error) {
      errorHandler(error);
    }
    return fallbackValue;
  }
}
  