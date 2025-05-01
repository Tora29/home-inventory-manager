import { 
  fetchItems,
  fetchLocations,
  fetchStocks, 
  fetchCategories 
} from "$features/stockDataTable/api/stockDataTableApi";
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
  const items = await fetchItems(0, 25)
  const locations = await fetchLocations()
  const stocks = await fetchStocks()
  const categories = await fetchCategories()
  return { items, locations, stocks, categories }
};
