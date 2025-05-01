import type { Floor, Room } from '$features/floorViewer/model/floorModel';
import { ErrorMessages } from './errorMessages';

/**
 * SVGファイルを読み込む
 * @param url SVGファイルのURL
 * @returns SVGコンテンツ（HTML文字列）
 */
export async function loadSvg(url: string): Promise<string> {
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`Failed to load SVG: ${response.status} ${response.statusText}`);
		}
		return await response.text();
	} catch {
		throw new Error(ErrorMessages.SVG_GENERATION_ERROR);
	}
}

/**
 * JSONデータからSVGを生成する
 * @param floorPlan 間取り図データ
 * @returns SVGコンテンツ（HTML文字列）
 */
export function generateSvgFromJson(floorPlan: Floor): string {
	const { width, height, viewBox, rooms } = floorPlan;

	let svgContent = `<svg width="${width}" height="${height}" viewBox="${viewBox}" fill="none" xmlns="http://www.w3.org/2000/svg">`;

	// 各部屋の要素を生成
	rooms.forEach((room: Room) => {
		svgContent += generateRoomElement(room);
	});

	svgContent += '</svg>';
	return svgContent;
}

/**
 * 部屋要素を生成する
 * @param room 部屋データ
 * @returns SVG要素（HTML文字列）
 */
function generateRoomElement(room: Room): string {
	const { id, name, type, style } = room;

	// スタイル属性を生成
	const styleAttrs = Object.entries(style)
		.map(([key, value]) => {
			// キャメルケースをケバブケースに変換（例: strokeWidth → stroke-width）
			const attrName = key.replace(/([A-Z])/g, '-$1').toLowerCase();
			return `${attrName}="${value}"`;
		})
		.join(' ');

	// data-room属性を追加
	const dataAttr = `data-room="${name}"`;

	// 要素タイプに応じてSVG要素を生成
	if (type === 'path') {
		return `  <path d="${room.coordinates}" ${styleAttrs} ${dataAttr} id="${id}" />`;
	} else if (type === 'rect') {
		const { x = 0, y = 0, width = 0, height = 0 } = room;
		return `  <rect x="${x}" y="${y}" width="${width}" height="${height}" ${styleAttrs} ${dataAttr} id="${id}" />`;
	}

	return '';
}

/**
 * SVG内の部屋要素にクリックイベントを追加
 * @param callback クリックイベントのコールバック関数
 */
export function addRoomClickEvents(callback: (roomName: string) => void): void {
	// レンダリング後にDOM要素を取得
	setTimeout(() => {
		const roomElements = document.querySelectorAll('[data-room]');

		roomElements.forEach((element) => {
			const roomName = element.getAttribute('data-room');
			if (roomName) {
				element.addEventListener('click', () => {
					callback(roomName);
				});

				// ホバー効果を適用
				element.classList.add('room-element');
			}
		});
	}, 100);
}

/**
 * JSONファイルを読み込んでFloorオブジェクトを返す
 * @param url JSONファイルのURL
 * @returns Floorオブジェクト
 */
export async function loadFloorJson(url: string): Promise<Floor> {
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`Failed to load floor plan data: ${response.status} ${response.statusText}`);
		}
		return await response.json();
	} catch {
		throw new Error(ErrorMessages.SVG_GENERATION_ERROR);
	}
}

/**
 * 間取り図の初期化処理を一括で行う
 * @param url 間取り図JSONファイルのURL
 * @param roomClickCallback 部屋クリック時のコールバック関数
 * @returns {Promise<{svgContent: string}>} 生成されたSVG文字列
 */
export async function initializeFloor(
	url: string,
	roomClickCallback: (roomName: string) => void
): Promise<{ svgContent: string, floorPlan: Floor | null }> {
	try {
		// JSONから間取り図データを読み込む
		const floorPlan = await loadFloorJson(url);
		
		// JSONデータからSVGを生成
		const svgContent = generateSvgFromJson(floorPlan);
		
		// SVG生成後、部屋要素にクリックイベントを追加
		addRoomClickEvents(roomClickCallback);
		
		return { svgContent, floorPlan };
	} catch {
		throw new Error(ErrorMessages.SVG_GENERATION_ERROR);
	}
}
