import type { Stock } from '../model/types';
import { API_BASE_URL } from '$shared/utils/apiConfig';

/**
 * 在庫データを取得する
 * @returns 在庫のリスト
 */
export const fetchStocks = async (): Promise<Stock[]> => {
	try {
		console.log('在庫データの取得を開始します');
		const url = `${API_BASE_URL}/stocks/`;

		console.log(`APIエンドポイント: ${url}`);
		const response = await fetch(url);

		console.log(`APIレスポンス: ${response.status} ${response.statusText}`);
		if (!response.ok) {
			// エラーレスポンスの本文も取得
			let errorBody = '';
			try {
				errorBody = await response.text();
			} catch (e) {
				errorBody = 'レスポンス本文を取得できません';
			}

			throw new Error(`APIエラー: ${response.status} - ${response.statusText} - ${errorBody}`);
		}

		const data = await response.json();
		console.log(`在庫データを取得しました: ${data.length}件`);

		// デバッグ: APIレスポンスの詳細を表示
		console.log('=== APIレスポンスの詳細 ===');
		console.log('最初の項目のデータ構造:', JSON.stringify(data[0], null, 2));
		console.log(
			'カテゴリ情報を持つアイテム数:',
			data.filter((item: Stock) => item.item?.category).length
		);
		console.log(
			'カテゴリ情報がないアイテム数:',
			data.filter((item: Stock) => !item.item?.category).length
		);
		console.log('========================');

		return data;
	} catch (error) {
		console.error('在庫データの取得に失敗しました:', error);
		throw error;
	}
};
