export interface Item {
	id: number;
	barcode: number | null;
	name: string;
	category_id: number | null;
	min_threshold: number;
	created_at: string;
	updated_at: string;
}