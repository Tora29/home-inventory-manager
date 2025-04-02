import type { Category } from '../model/types';

/**
 * すべてのカテゴリを取得する
 * @returns カテゴリのリスト
 */
export const fetchCategories = async (): Promise<Category[]> => {
	try {
		const API_BASE_URL = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000/v1';
		const url = `${API_BASE_URL}/categories/`;

		const response = await fetch(url);

		if (!response.ok) {
			let errorBody = '';
			try {
				errorBody = await response.text();
			} catch (e) {
				errorBody = 'レスポンス本文を取得できません';
			}

			throw new Error(`APIエラー: ${response.status} - ${response.statusText} - ${errorBody}`);
		}

		const data = await response.json();
		return data;
	} catch (error) {
		console.error('カテゴリデータの取得に失敗しました:', error);
		throw error;
	}
};
