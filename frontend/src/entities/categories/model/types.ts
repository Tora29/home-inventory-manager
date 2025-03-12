export interface Category {
	id: number;
	category_name: string;
	created_at: string;
	updated_at: string;
}

export interface CategoryCreate {
	category_name: string;
}
