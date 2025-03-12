import { apiClient } from '../../../shared/api/base';
import type { Category, CategoryCreate } from '../model/types';

/**
 * カテゴリ一覧を取得
 */
export async function getCategories(): Promise<Category[]> {
	return await apiClient<Category[]>('/categories/', {
		method: 'GET'
	});
}

/**
 * カテゴリを取得
 */
export async function getCategory(id: number): Promise<Category> {
	return await apiClient<Category>(`/categories/${id}`, {
		method: 'GET'
	});
}

/**
 * カテゴリを作成
 */
export async function createCategory(category: CategoryCreate): Promise<Category> {
	return await apiClient<Category>('/categories/', {
		method: 'POST',
		body: category
	});
}

/**
 * カテゴリを更新
 */
export async function updateCategory(id: number, category: CategoryCreate): Promise<Category> {
	return await apiClient<Category>(`/categories/${id}`, {
		method: 'PUT',
		body: category
	});
}

/**
 * カテゴリを削除
 */
export async function deleteCategory(id: number): Promise<void> {
	await apiClient<void>(`/categories/${id}`, {
		method: 'DELETE'
	});
}
