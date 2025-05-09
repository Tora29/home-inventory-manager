import { API_BASE_URL } from '$shared/utils/apiConfigUtils';
import { handleApiError, safeApiCall } from '$shared/utils/apiErrorHandlerUtils';
import type { Item } from '$features/stockList/model/itemModel';

/**
 * すべての商品データを取得
 * @returns 商品データの配列
 */
export const load = async (skip = 0, limit = 100): Promise<Item[]> => {
  return safeApiCall(
    async () => {
      const url = `${API_BASE_URL}/items?skip=${skip}&limit=${limit}`;
      const response = await fetch(url);

      if (!response.ok) {
        await handleApiError(response);
      }

      return await response.json();
    },
    []
  );
}; 