/**
 * バーコードスキャナからの入力を監視する関数
 * @param callback バーコード読み取り時に呼ばれるコールバック関数
 * @param options 設定オプション
 * @returns クリーンアップ用のunsubscribe関数
 */
export function listenForBarcodeScans(
  callback: (barcode: string) => void,
  options: {
    /** Enter以外の終端文字を使う場合に指定 */
    terminationKey?: string;
    /** バーコード入力のタイムアウト時間（ミリ秒） */
    timeout?: number;
  } = {}
): () => void {
  const { 
    terminationKey = 'Enter',
    timeout = 50 
  } = options;

  let buffer = '';
  let lastInputTime = 0;

  // キー入力イベントハンドラ
  const handleKeyDown = (event: KeyboardEvent) => {
    // まずはここにログ！
    console.log('🔍 scan-util keydown:', { 
      key: event.key, 
      code: event.code, 
      time: Date.now() - lastInputTime 
    });

    const now = Date.now();
    if (event.key === terminationKey) {
      if (buffer) {
        console.log('🔍 scan-util 完了:', buffer);
        callback(buffer);
        buffer = '';
      }
      event.preventDefault();
      return;
    }

    if (now - lastInputTime > timeout && buffer) {
      console.log('🔍 scan-util タイムアウトでバッファクリア');
      buffer = '';
    }

    if (event.key.length === 1) {
      buffer += event.key;
      lastInputTime = now;
      console.log('🔍 scan-util バッファ更新:', buffer);
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}