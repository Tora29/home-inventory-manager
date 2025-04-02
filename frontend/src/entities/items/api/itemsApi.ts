import { apiClient } from '$shared/api/base';
import type { Item, ItemDetail, ItemCreate, ItemUpdate } from '../model/types';

/**
 * アイテム一覧を取得
 */
export async function getItems(skip: number = 0, limit: number = 100): Promise<Item[]> {
	return await apiClient<Item[]>(`/items/?skip=${skip}&limit=${limit}`, {
		method: 'GET'
	});
}

