import type { Item } from '$entities/items';

export enum TransactionType {
	IN = 'IN',
	OUT = 'OUT'
}

export interface Transaction {
	id: number;
	item_id: number;
	quantity: number;
	transaction_type: TransactionType;
	transaction_date: string;
	note: string | null;
	created_at: string;
	updated_at: string;
}

export interface TransactionDetail extends Transaction {
	item: Item;
}

export interface TransactionCreate {
	item_id: number;
	quantity: number;
	transaction_type: TransactionType;
	transaction_date?: string;
	note?: string;
}

export interface TransactionUpdate {
	quantity?: number;
	transaction_type?: TransactionType;
	transaction_date?: string;
	note?: string;
}
