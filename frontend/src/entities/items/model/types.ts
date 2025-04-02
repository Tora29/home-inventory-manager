import type { Category } from '$entities/categories/model/types';

export interface Item {
	id: number;
	barcode: string | null;
	item_name: string;
	category_id: number | null;
	note: string | null;
	created_at: string;
	updated_at: string;
}

export interface ItemDetail extends Item {
	category: Category | null;
}

export interface ItemCreate {
	barcode?: string;
	item_name: string;
	category_id?: number;
	note?: string;
}

export interface ItemUpdate {
	barcode?: string;
	item_name?: string;
	category_id?: number;
	note?: string;
}
