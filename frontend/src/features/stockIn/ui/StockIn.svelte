<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  
  import DataTable, { type Column, type DataItem } from '$shared/components/DataTable.svelte';
  import Button from '$shared/components/Button.svelte';
  import DropdownSelect from '$shared/components/DropdownSelect.svelte';
  import { listenForBarcodeScans } from '$shared/utils/barcodeScannerUtils';
  
  // 商品アイテムの型定義
  interface StockItem {
    barcode: string;
    productName: string;
    location: string;
    quantity: number;
    category: string;
    isRegistered: boolean;
  }
  
  // 選択肢のオプション
  const locationOptions = [
    { value: '冷蔵庫', label: '冷蔵庫' },
    { value: '冷凍庫', label: '冷凍庫' },
    { value: '食品棚', label: '食品棚' },
    { value: 'その他', label: 'その他' }
  ];
  
  const quantityOptions = Array.from({ length: 10 }, (_, i) => {
    const num = (i + 1).toString();
    return { value: num, label: num };
  });
  
  const categoryOptions = [
    { value: '野菜', label: '野菜' },
    { value: '肉', label: '肉' },
    { value: '魚', label: '魚' },
    { value: '調味料', label: '調味料' },
    { value: '飲料', label: '飲料' },
    { value: 'その他', label: 'その他' }
  ];
  
  // 商品データストア
  const stockItems = writable<StockItem[]>([]);
  
  // スキャン状態
  let isScanning = $state(false);
  let lastScannedBarcode = $state('');
  let barcodeInput = $state('');
  
  // 商品DBから商品名を取得する模擬関数
  // 実際の実装では、APIから取得する
  function getProductNameFromDB(barcode: string): string {
    // ここではダミーデータを返す
    const dummyProducts: Record<string, string> = {
      '4901234567890': 'サンプル商品1',
      '4902345678901': 'サンプル商品2',
      '4903456789012': 'サンプル商品3'
    };
    
    return dummyProducts[barcode] || '';
  }
  
  // バーコードスキャン時の処理
  function handleBarcodeScanned(barcode: string) {
    console.log('バーコード処理実行:', barcode);
    if (!barcode) return;
    
    // スキャン中フラグを立てる
    isScanning = true;
    lastScannedBarcode = barcode;
    
    // DBから商品名を取得
    const productName = getProductNameFromDB(barcode);
    
    // 新しい商品を追加
    stockItems.update(items => [
      ...items, 
      {
        barcode: barcode,
        productName: productName,
        location: '',
        quantity: 1,
        category: '',
        isRegistered: false
      }
    ]);
    
    // スキャンフラグをリセット（視覚フィードバック用）
    setTimeout(() => {
      isScanning = false;
    }, 1000);
  }
  
  // キーダウンイベントハンドラ
  function handleKeydown(event: KeyboardEvent) {
    console.log('キーダウン検知:', event.key, 'バーコード入力値:', barcodeInput);
    if (event.key === 'Enter' && barcodeInput) {
      console.log('Enterキー検知！バーコード処理実行:', barcodeInput);
      // Enterキーが押されたらバーコード処理を実行
      handleBarcodeScanned(barcodeInput);
      // 入力をクリア
      barcodeInput = '';
      event.preventDefault();
    }
  }
  
  // 入荷ボタン処理
  function handleRegister(index: number) {
    stockItems.update(items => {
      const updatedItems = [...items];
      updatedItems[index].isRegistered = true;
      return updatedItems;
    });
  }
  
  // 取消ボタン処理
  function handleCancel(index: number) {
    stockItems.update(items => items.filter((_, i) => i !== index));
  }
  
  // 確定ボタン処理
  function handleConfirm() {
    // 入荷状態の商品のみ抽出
    stockItems.update(items => {
      console.log('登録対象商品:', items.filter(item => item.isRegistered));
      // DBに登録する処理を実装（今回は省略）
      // 登録済み商品を除外
      return items.filter(item => !item.isRegistered);
    });
  }
  
  // コンポーネントマウント時の処理
  let inputElement: HTMLInputElement;
  
  // フォーカスを強制的に維持する関数
  function forceFocus() {
    // ログを削除
    if (document.activeElement !== inputElement) {
      inputElement?.focus();
    }
  }
  
  // バーコードスキャン検知の設定
  onMount(() => {
    // 初回フォーカス
    forceFocus();
    
    // フォーカスチェックの間隔を長く (3秒ごと)
    const intervalId = setInterval(forceFocus, 3000);
    
    // クリック時にフォーカスを戻す
    const clickHandler = () => {
      setTimeout(forceFocus, 100);
    };
    window.addEventListener('click', clickHandler);
    
    // キーボード入力のイベントハンドラを最適化
    const keydownHandler = (event: KeyboardEvent) => {
      // 入力フィールドにフォーカスがない場合のみフォーカスを設定
      if (document.activeElement !== inputElement) {
        forceFocus();
      }
    };
    window.addEventListener('keydown', keydownHandler);
    
    // コンポーネント解除時にリスナー解除
    return () => {
      clearInterval(intervalId);
      window.removeEventListener('click', clickHandler);
      window.removeEventListener('keydown', keydownHandler);
    };
  });
  
  // 項目変更ハンドラー
  function handleLocationChange(index: number, value: string) {
    stockItems.update(items => {
      const updatedItems = [...items];
      updatedItems[index].location = value;
      return updatedItems;
    });
  }
  
  function handleQuantityChange(index: number, value: string) {
    stockItems.update(items => {
      const updatedItems = [...items];
      updatedItems[index].quantity = parseInt(value);
      return updatedItems;
    });
  }
  
  function handleCategoryChange(index: number, value: string) {
    stockItems.update(items => {
      const updatedItems = [...items];
      updatedItems[index].category = value;
      return updatedItems;
    });
  }
  
  function handleProductNameChange(index: number, event: Event) {
    const value = (event.target as HTMLInputElement).value;
    stockItems.update(items => {
      const updatedItems = [...items];
      updatedItems[index].productName = value;
      return updatedItems;
    });
  }
  
  // DataTableのカラム定義
  const columns: Column[] = [
    {
      header: 'バーコード',
      key: 'barcode'
    },
    {
      header: '商品名',
      key: 'productName',
      formatter: (value, item) => {
        return {
          component: 'input',
          props: {
            type: 'text',
            value,
            class: 'input input-bordered w-full max-w-xs',
            oninput: (e: Event) => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleProductNameChange(index, e);
              }
            }
          }
        };
      }
    },
    {
      header: '保管場所',
      key: 'location',
      formatter: (value, item) => {
        return {
          component: DropdownSelect,
          props: {
            options: locationOptions,
            value,
            onChange: (newValue: string) => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleLocationChange(index, newValue);
              }
            },
            placeholder: '選択してください',
            label: ''
          }
        };
      }
    },
    {
      header: '数量',
      key: 'quantity',
      formatter: (value, item) => {
        return {
          component: DropdownSelect,
          props: {
            options: quantityOptions,
            value: value.toString(),
            onChange: (newValue: string) => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleQuantityChange(index, newValue);
              }
            },
            placeholder: '選択してください',
            label: ''
          }
        };
      }
    },
    {
      header: 'カテゴリ',
      key: 'category',
      formatter: (value, item) => {
        return {
          component: DropdownSelect,
          props: {
            options: categoryOptions,
            value,
            onChange: (newValue: string) => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleCategoryChange(index, newValue);
              }
            },
            placeholder: '選択してください',
            label: ''
          }
        };
      }
    },
    {
      header: '入荷',
      key: 'isRegistered',
      formatter: (value, item) => {
        return {
          component: Button,
          props: {
            color: 'success',
            disabled: value,
            children: '入荷',
            onclick: () => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleRegister(index);
              }
            }
          }
        };
      }
    },
    {
      header: '取消',
      key: 'isRegistered',
      formatter: (_, item) => {
        return {
          component: Button,
          props: {
            color: 'error',
            children: '取消',
            onclick: () => {
              const index = $stockItems.findIndex(i => i === item);
              if (index !== -1) {
                handleCancel(index);
              }
            }
          }
        };
      }
    }
  ];
  
  // 行のカスタムクラスを取得する関数
  function getRowClass(item: DataItem): string {
    return (item as StockItem).isRegistered ? 'bg-green-100' : '';
  }
</script>

<div class="p-4">
  <h1 class="text-2xl font-bold mb-6">入荷管理</h1>
  
  <!-- バーコードスキャン状態表示 -->
  <div class={`alert ${isScanning ? 'alert-success' : 'alert-info'} mb-4`}>
    <div>
      {#if isScanning}
        <span class="font-bold">バーコード読み取り完了！ [{lastScannedBarcode}]</span>
      {:else}
        <span class="font-bold">バーコードスキャン待機中...</span>
      {/if}
    </div>
  </div>
  
  <!-- 商品一覧テーブル -->
  <div class="mb-4">
    <DataTable 
      data={$stockItems} 
      {columns} 
      getRowClass={getRowClass}
      hoverEffect={false}
      emptyMessage="商品データがありません。バーコードをスキャンしてください。"
    />
  </div>
  
  <!-- 確定ボタン -->
  <div class="flex justify-end">
    <Button
      color="primary"
      disabled={!$stockItems.some(item => item.isRegistered)}
      children="確定"
      onclick={handleConfirm}
    />
  </div>
  
  <!-- 非表示の入力フィールド -->
  <input
    type="text"
    bind:this={inputElement}
    bind:value={barcodeInput}
    on:keydown={handleKeydown}
    class="fixed top-0 left-0 opacity-0 pointer-events-none"
    autocomplete="off"
  />
</div>
