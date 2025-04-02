/**
 * API呼び出しをラップして共通エラーハンドリングを提供する
 * @param apiCall API呼び出しを行う非同期関数
 * @returns API呼び出しの結果
 */
export async function withErrorHandling<T>(apiCall: () => Promise<T>): Promise<T> {
	try {
		return await apiCall();
	} catch (error) {
		console.error('APIリクエストに失敗しました:', error);
		throw error;
	}
}

/**
 * レスポンスのステータスコードを確認する
 * @param response fetchのレスポンス
 * @param errorMessage エラー時のメッセージ
 */
export function checkResponse(response: Response, errorMessage = 'APIエラー'): void {
	if (!response.ok) {
		throw new Error(`${errorMessage}: ${response.status}`);
	}
}
