import { API_BASE_URL } from '$shared/utils/apiConfig';
import type { Location } from '$features/floorViewer/model/types';
import { handleApiError, safeApiCall } from '$shared/utils/apiErrorHandler';
import { ErrorMessages } from '$shared/utils/errorMessages';

/**
 * すべての部屋を取得
 * @returns 部屋の配列
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
		{ error: ErrorMessages.GENERAL_FAILURE }
	);
};
