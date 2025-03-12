import { apiClient } from '$shared/api/base';
import type {
	Transaction,
	TransactionDetail,
	TransactionCreate,
	TransactionUpdate
} from '../model/types';

/**
 * 取引一覧を取得
 */
export async function getTransactions(
	skip: number = 0,
	limit: number = 100
): Promise<TransactionDetail[]> {
	return await apiClient<TransactionDetail[]>(`/transactions/?skip=${skip}&limit=${limit}`, {
		method: 'GET'
	});
}

/**
 * 取引の詳細を取得
 */
export async function getTransaction(id: number): Promise<TransactionDetail> {
	return await apiClient<TransactionDetail>(`/transactions/${id}`, {
		method: 'GET'
	});
}

/**
 * 取引を作成
 */
export async function createTransaction(transaction: TransactionCreate): Promise<Transaction> {
	return await apiClient<Transaction>('/transactions/', {
		method: 'POST',
		body: transaction
	});
}

/**
 * 取引を更新
 */
export async function updateTransaction(
	id: number,
	transaction: TransactionUpdate
): Promise<Transaction> {
	return await apiClient<Transaction>(`/transactions/${id}`, {
		method: 'PUT',
		body: transaction
	});
}

/**
 * 取引を削除
 */
export async function deleteTransaction(id: number): Promise<void> {
	await apiClient<void>(`/transactions/${id}`, {
		method: 'DELETE'
	});
}
