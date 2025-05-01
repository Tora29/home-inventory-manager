/**
 * フィルタリングユーティリティ
 * 汎用的なフィルタリング機能と、特定のドメイン向けの拡張機能を提供します
 */

import type { Stock } from '$features/stockDataTable/model/stockModel';

// ベースとなるフィルタリング関数 -----------------------------------

/**
 * 配列の中から条件に一致するアイテムをフィルタリングする基本関数
 * @param items フィルタリング対象の配列
 * @param predicate フィルタリング条件（trueを返す要素が結果に含まれる）
 * @returns フィルタリングされた配列
 */
export function filterItems<T>(items: T[], predicate: (item: T) => boolean): T[] {
  return items.filter(predicate);
}

/**
 * キーワードによる文字列検索
 * @param items フィルタリング対象の配列
 * @param keyword 検索キーワード
 * @param getSearchString アイテムから検索対象の文字列を取得する関数
 * @returns フィルタリングされた配列
 */
export function filterByKeyword<T>(
  items: T[], 
  keyword: string,
  getSearchString: (item: T) => string | null | undefined
): T[] {
  if (!keyword) return items;
  
  const lowerKeyword = keyword.toLowerCase();
  return filterItems(items, item => {
    const searchText = getSearchString(item);
    return !!searchText && searchText.toLowerCase().includes(lowerKeyword);
  });
}

/**
 * IDによる関連アイテムのフィルタリング
 * @param items フィルタリング対象の配列
 * @param relatedId 関連するID
 * @param getRelatedId アイテムから関連IDを取得する関数
 * @returns フィルタリングされた配列
 */
export function filterByRelatedId<T>(
  items: T[],
  relatedId: number,
  getRelatedId: (item: T) => number | null | undefined
): T[] {
  return filterItems(items, item => getRelatedId(item) === relatedId);
}

/**
 * プロパティによるフィルタリング
 * @param items フィルタリング対象の配列
 * @param propValue 検索する値
 * @param getPropValue アイテムからプロパティ値を取得する関数
 * @returns フィルタリングされた配列
 */
export function filterByProperty<T, V>(
  items: T[],
  propValue: V,
  getPropValue: (item: T) => V | null | undefined
): T[] {
  return filterItems(items, item => getPropValue(item) === propValue);
}

// 在庫関連のフィルタリング関数 -----------------------------------

/**
 * 場所名による在庫フィルタリング
 * @param stocks 対象の在庫データ
 * @param locationName 場所名
 * @param locations 場所データの配列
 * @returns フィルタリングされた在庫データ
 */
export function filterStocksByLocation(
  stocks: Stock[], 
  locationName: string, 
  locations: ReadonlyArray<{ id: number; name: string }> | null | undefined
): Stock[] {
  if (!locations || !Array.isArray(locations)) return [];
  
  const locObj = locations.find(loc => loc.name === locationName);
  if (!locObj) return [];
  
  return filterByRelatedId(stocks, locObj.id, stock => stock.location_id);
}

/**
 * 商品名による在庫フィルタリング
 * @param stocks 対象の在庫データ
 * @param keyword 検索キーワード
 * @param items 商品データの配列
 * @returns フィルタリングされた在庫データ
 */
export function filterStocksByKeyword(
  stocks: Stock[], 
  keyword: string, 
  items: ReadonlyArray<{ id: number; name: string }> | null | undefined
): Stock[] {
  if (!keyword) return stocks;
  if (!items || !Array.isArray(items)) return [];

  return filterItems(stocks, stock => {
    const item = items.find(i => i.id === stock.item_id);
    return !!item?.name && item.name.toLowerCase().includes(keyword.toLowerCase());
  });
}

/**
 * カテゴリによる在庫フィルタリング
 * @param stocks 対象の在庫データ
 * @param categoryId カテゴリID
 * @param items 商品データの配列
 * @returns フィルタリングされた在庫データ
 */
export function filterStocksByCategory(
  stocks: Stock[], 
  categoryId: string, 
  items: ReadonlyArray<{ id: number; category_id?: number | null | undefined }> | null | undefined
): Stock[] {
  if (!categoryId) return stocks;
  if (!items || !Array.isArray(items)) return [];
  
  const categoryIdNum = parseInt(categoryId);
  
  return filterItems(stocks, stock => {
    const item = items.find(i => i.id === stock.item_id);
    return item?.category_id === categoryIdNum;
  });
}

/**
 * 複数のフィルターを在庫データに適用する
 * @param stocks 対象の在庫データ
 * @param filters フィルター条件
 * @param items 商品データの配列
 * @param locations 場所データの配列
 * @returns フィルタリングされた在庫データ
 */
export function applyStockFilters(
  stocks: Stock[],
  filters: {
    location?: string | null;
    keyword?: string;
    categoryId?: string;
  },
  items: ReadonlyArray<{ id: number; name: string; category_id?: number | null }> | null | undefined,
  locations: ReadonlyArray<{ id: number; name: string }> | null | undefined
): Stock[] {
  let result = [...stocks];

  // ロケーションフィルター適用
  if (filters.location) {
    result = filterStocksByLocation(result, filters.location, locations);
  }

  // カテゴリフィルター適用
  if (filters.categoryId) {
    result = filterStocksByCategory(result, filters.categoryId, items);
  }

  // 検索キーワードフィルター適用（商品名のみ）
  if (filters.keyword) {
    result = filterStocksByKeyword(result, filters.keyword, items);
  }

  return result;
} 