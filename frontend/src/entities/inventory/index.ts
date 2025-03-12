// モデル
export type { Inventory, InventoryDetail, InventoryCreate, InventoryUpdate } from './model/types';

// API
export {
	getInventories,
	getInventory,
	createInventory,
	updateInventory,
	deleteInventory
} from './api/inventoryApi';
