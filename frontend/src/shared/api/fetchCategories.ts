import { API_BASE_URL } from '$shared/utils/apiConfigUtils';
import { handleApiError, safeApiCall } from '$shared/utils/apiErrorHandlerUtils';
import type { Category } from '$features/stockList/model/categoryModel';

/**
 * すべてのカテゴリデータを取得
 * @returns カテゴリデータの配列
 */
export const load = async (): Promise<Category[]> => {
  return safeApiCall(
    async () => {
      const url = `${API_BASE_URL}/categories`;
      const response = await fetch(url);

      if (!response.ok) {
        await handleApiError(response);
      }

      return await response.json();
    },
    []
  );
}; 