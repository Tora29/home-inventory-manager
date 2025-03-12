type RequestOptions = {
	method: 'GET' | 'POST' | 'PUT' | 'DELETE';
	headers?: Record<string, string>;
	body?: any;
};

/**
 * 基本的なAPI通信用のクライアント
 * @param endpoint - APIエンドポイントのパス
 * @param options - リクエストオプション
 * @returns レスポンスデータ
 */
export async function apiClient<T>(endpoint: string, options: RequestOptions): Promise<T> {
	const baseUrl = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000/v1';
	const url = `${baseUrl}${endpoint}`;

	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		Accept: 'application/json',
		...options.headers
	};

	const config: RequestInit = {
		method: options.method,
		headers,
		credentials: 'include'
	};

	if (options.body) {
		config.body = JSON.stringify(options.body);
	}

	try {
		const response = await fetch(url, config);

		// JSONレスポンスを解析
		const data = await response.json();

		// エラーハンドリング
		if (!response.ok) {
			throw new Error(data.detail || 'APIリクエストが失敗しました');
		}

		return data as T;
	} catch (error) {
		console.error('API error:', error);
		throw error;
	}
}
