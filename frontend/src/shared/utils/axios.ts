import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
	baseURL: BASE_URL,
	headers: {
		'Content-Type': 'application/json'
	},
	timeout: 10000
});

// 必要に応じてインターセプターを追加
apiClient.interceptors.request.use(
	(config) => {
		// 認証トークンの追加などの処理
		return config;
	},
	(error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
	(response) => response,
	(error) => {
		// グローバルエラーハンドリング
		return Promise.reject(error);
	}
);

export default apiClient;
