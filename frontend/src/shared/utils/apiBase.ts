import axios from 'axios';
import { API_BASE_URL } from './apiConfig';

// Axiosインスタンスを作成
const axiosInstance = axios.create({
	baseURL: API_BASE_URL,
	headers: {
		'Content-Type': 'application/json'
	},
	timeout: 15000
});

// リクエストインターセプター
axiosInstance.interceptors.request.use(
	(config) => {
		console.log(`APIリクエスト: ${config.method?.toUpperCase()} ${config.url}`);
		return config;
	},
	(error) => {
		console.error('リクエストエラー:', error);
		return Promise.reject(error);
	}
);

// レスポンスインターセプター
axiosInstance.interceptors.response.use(
	(response) => {
		return response.data;
	},
	(error) => {
		console.error('APIエラー:', error);
		return Promise.reject(error);
	}
);

// 型付きのAPIクライアントを提供
export const apiClient = async <T>(
	url: string,
	options: { method: string; data?: any } = { method: 'GET' }
): Promise<T> => {
	const { method, data } = options;

	try {
		if (method === 'GET') {
			const response = await axiosInstance.get(url);
			return response.data;
		} else if (method === 'POST') {
			const response = await axiosInstance.post(url, data);
			return response.data;
		} else if (method === 'PUT') {
			const response = await axiosInstance.put(url, data);
			return response.data;
		} else if (method === 'DELETE') {
			const response = await axiosInstance.delete(url);
			return response.data;
		}
		throw new Error(`未サポートのHTTPメソッド: ${method}`);
	} catch (error) {
		console.error('APIリクエストエラー:', error);
		throw error;
	}
};
