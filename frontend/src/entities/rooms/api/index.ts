import { API_BASE_URL } from '$shared/utils/apiConfig';
import type { Room } from '../model/types';

/**
 * すべての部屋を取得
 * @returns 部屋の配列
 */
export const fetchRooms = async (): Promise<Room[]> => {
	try {
		const url = `${API_BASE_URL}/rooms`;
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`API エラー: ${response.status}`);
		}

		const data = await response.json();
		return data;
	} catch (error) {
		console.error('部屋データの取得に失敗しました:', error);
		throw error;
	}
};
