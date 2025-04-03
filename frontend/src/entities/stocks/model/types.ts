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

// バーコードスキャン入力モデル
export interface BarcodeStockIn {
	barcode: string;
	location?: string;
	quantity?: number;
}

// バーコードスキャンレスポンスモデル
export interface StockInResponse {
	success: boolean;
	message: string;
	stock?: Stock;
	item_name?: string;
}

// WebSocketからの通知モデル
export interface StockNotification {
	type: 'stock_in';
	data: {
		item_id: number;
		item_name: string;
		barcode: string;
		location: string;
		quantity: number;
		total_quantity: number;
		category_id: number | null;
		category_name: string | null;
	};
}

// スキャンされた商品の履歴アイテム
export interface ScannedItem {
	id: string; // ユニークID（クライアントサイドで生成）
	timestamp: Date;
	barcode: string;
	item_name: string;
	location: string;
	quantity: number;
	isNew: boolean; // 新規商品か既存商品か
	category_id?: number | null;
	category_name?: string | null;
}
