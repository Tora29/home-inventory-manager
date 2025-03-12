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

/**
 * アイテムの詳細を取得
 */
export async function getItem(id: number): Promise<ItemDetail> {
	return await apiClient<ItemDetail>(`/items/${id}`, {
		method: 'GET'
	});
}

/**
 * バーコードからアイテムを検索
 */
export async function getItemByBarcode(barcode: string): Promise<ItemDetail | null> {
	try {
		return await apiClient<ItemDetail>(`/items/barcode/${barcode}`, {
			method: 'GET'
		});
	} catch (error) {
		// 404の場合はnullを返す
		if (error instanceof Error && error.message.includes('404')) {
			return null;
		}
		throw error;
	}
}

/**
 * アイテムを作成
 */
export async function createItem(item: ItemCreate): Promise<Item> {
	return await apiClient<Item>('/items/', {
		method: 'POST',
		body: item
	});
}

/**
 * アイテムを更新
 */
export async function updateItem(id: number, item: ItemUpdate): Promise<Item> {
	return await apiClient<Item>(`/items/${id}`, {
		method: 'PUT',
		body: item
	});
}

/**
 * アイテムを削除
 */
export async function deleteItem(id: number): Promise<void> {
	await apiClient<void>(`/items/${id}`, {
		method: 'DELETE'
	});
}
