import { API_BASE_URL } from '$shared/utils/apiConfigUtils';
import { handleApiError, safeApiCall } from '$shared/utils/apiErrorHandlerUtils';
import type { Location } from '$features/stockList/model/locationModel';

/**
 * すべての保管場所データを取得
 * @returns 保管場所データの配列
 */
export const load = async (): Promise<Location[]> => {
  return safeApiCall(
    async () => {
      const url = `${API_BASE_URL}/locations`;
      const response = await fetch(url);

      if (!response.ok) {
        await handleApiError(response);
      }

      return await response.json();
    },
    []
  );
}; 