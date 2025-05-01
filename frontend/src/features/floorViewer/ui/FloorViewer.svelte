<script lang="ts">
    import { onMount } from 'svelte';

    import { initializeFloor } from '$shared/utils/jsonToSvgUtils';
    import type { Floor } from '$features/floorViewer/model/floorModel';

    interface FloorViewerProps {
        jsonUrl?: string;
        onRoomClick: (roomName: string | null) => void;
        selectedLocation: string | null;
    }

    let { jsonUrl = '/floorPlan.json', onRoomClick, selectedLocation }: FloorViewerProps = $props();

    let svgContent = $state('');
    let floorPlan = $state<Floor | null>(null);

    // 部屋クリック時の処理をコンポーネント内部に実装
    function handleRoomClick(roomName: string) {
        // 同じ部屋が選択された場合は選択解除
        if (selectedLocation === roomName) {
            onRoomClick(null);
        } else {
            onRoomClick(roomName);
        }
    }

    onMount(async () => {
        // 共通関数を使用して間取り図を初期化
        try {
            const floorPlanData = await initializeFloor(jsonUrl, handleRoomClick);
            svgContent = floorPlanData.svgContent;
            floorPlan = floorPlanData.floorPlan;
        } catch (error) {
            console.error('間取り図の初期化に失敗しました', error);
        }
    });
</script>

<div class="floor-viewer-container">
    {@html svgContent}
</div>

<style>
    .floor-viewer-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    :global(.room-element) {
        cursor: pointer;
        transition: fill 0.2s ease-in-out;
    }

    :global(.room-element:hover) {
        fill: #a8a8a8 !important;
    }
</style>