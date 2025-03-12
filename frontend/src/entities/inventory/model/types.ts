import type { Item } from '$entities/items';

export interface Inventory {
	id: number;
	item_id: number;
	quantity: number;
	location: string | null;
	expiry_date: string | null;
	created_at: string;
	updated_at: string;
}

export interface InventoryDetail extends Inventory {
	item: Item;
}

export interface InventoryCreate {
	item_id: number;
	quantity: number;
	location?: string;
	expiry_date?: string;
}

export interface InventoryUpdate {
	quantity?: number;
	location?: string;
	expiry_date?: string;
}
