export interface DocumentType {
  id: string;
  name: string;
  type: string;
  size: string;
  uploadedAt: string;
  page_content: string;
  file_path: string;
  metadata: {
    source: string;
    filename: string;
    type: string;
    size: string;
  };
}

export interface DocumentStatsType {
  lastQueried: string;
  totalQueries: number;
  itemsIndexed: number;
  createdAt: string;
} 