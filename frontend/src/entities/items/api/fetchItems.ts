import type { Item } from '../model/types';
import { API_BASE_URL } from '$shared/utils/apiConfig';

/**
 * アイテム一覧を取得する
 * @param skip スキップする件数
 * @param limit 取得する上限件数
 * @returns アイテムのリスト
 */
export const fetchItems = async (skip: number = 0, limit: number = 100): Promise<Item[]> => {
	try {
		const url = `${API_BASE_URL}/items/?skip=${skip}&limit=${limit}`;

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
		console.error('アイテムデータの取得に失敗しました:', error);
		throw error;
	}
};
