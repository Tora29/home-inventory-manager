export interface Room {
  id: string;
  name: string;
  type: 'path' | 'rect';
  coordinates: string;
  style: {
    fill: string;
    stroke?: string;
    strokeWidth?: number;
  };
  width?: number;
  height?: number;
  x?: number;
  y?: number;
}

export interface Floor {
  width: number;
  height: number;
  viewBox: string;
  rooms: Room[];
} 