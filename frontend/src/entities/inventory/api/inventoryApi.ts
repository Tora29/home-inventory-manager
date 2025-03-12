import { apiClient } from '$shared/api/base';
import type { Inventory, InventoryDetail, InventoryCreate, InventoryUpdate } from '../model/types';

/**
 * 在庫一覧を取得
 */
export async function getInventories(
	skip: number = 0,
	limit: number = 100
): Promise<InventoryDetail[]> {
	return await apiClient<InventoryDetail[]>(`/inventory/?skip=${skip}&limit=${limit}`, {
		method: 'GET'
	});
}

/**
 * 在庫の詳細を取得
 */
export async function getInventory(id: number): Promise<InventoryDetail> {
	return await apiClient<InventoryDetail>(`/inventory/${id}`, {
		method: 'GET'
	});
}

/**
 * 在庫を作成
 */
export async function createInventory(inventory: InventoryCreate): Promise<Inventory> {
	return await apiClient<Inventory>('/inventory/', {
		method: 'POST',
		body: inventory
	});
}

/**
 * 在庫を更新
 */
export async function updateInventory(id: number, inventory: InventoryUpdate): Promise<Inventory> {
	return await apiClient<Inventory>(`/inventory/${id}`, {
		method: 'PUT',
		body: inventory
	});
}

/**
 * 在庫を削除
 */
export async function deleteInventory(id: number): Promise<void> {
	await apiClient<void>(`/inventory/${id}`, {
		method: 'DELETE'
	});
}
