export interface Stock {
	id: number;
	item_id: number;
	item: {
		id: number;
		name: string;
		category?: {
			id: number;
			name: string;
		} | null;
	};
	quantity: number;
	location?: string;
	updated_at: string;
}
