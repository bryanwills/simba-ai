export interface DocumentType {
  id: string;
  name: string;
  type: string;
  size: string;
  uploadedAt: string;
}

export interface DocumentStatsType {
  lastQueried: string;
  totalQueries: number;
  itemsIndexed: number;
  createdAt: string;
} 