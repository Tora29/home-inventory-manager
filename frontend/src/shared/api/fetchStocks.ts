import { API_BASE_URL } from '$shared/utils/apiConfigUtils';
import { handleApiError, safeApiCall } from '$shared/utils/apiErrorHandlerUtils';
import type { Stock } from '$features/stockList/model/stockModel';

/**
 * すべての在庫データを取得
 * @returns 在庫データの配列
 */
export const load = async (skip = 0, limit = 100): Promise<Stock[]> => {
  return safeApiCall(
    async () => {
      const url = `${API_BASE_URL}/stocks?skip=${skip}&limit=${limit}`;
      const response = await fetch(url);

      if (!response.ok) {
        await handleApiError(response);
      }

      return await response.json();
    },
    []
  );
}; 