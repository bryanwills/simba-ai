import { config } from '@/config';
import { SimbaDoc } from '@/types/document';

const MAX_FILE_SIZE = 200 * 1024 * 1024; // 200MB
const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'text/plain',
  'text/markdown',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',  // .xls
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  // .xlsx
  'application/vnd.ms-powerpoint',  // .ppt
  'application/vnd.openxmlformats-officedocument.presentationml.presentation'  // .pptx
];

class IngestionApi {
  private baseUrl = config.apiUrl;

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Accept': 'application/json',
        ...options.headers,
      }
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || 'Request failed');
    }

    return response.json();
  }

  async uploadDocuments(
    files: File[], 
  ): Promise<SimbaDoc[]> {
    // Validate all files
    for (const file of files) {
      if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        throw new Error(`File type not supported for ${file.name}`);
      }
      if (file.size === 0 || file.size > MAX_FILE_SIZE) {
        throw new Error(`Invalid file size for ${file.name}`);
      }
    }

    const formData = new FormData();
    // Add each file to formData with the same field name
    files.forEach(file => {
      formData.append('files', file);
    });


    return this.request('/ingestion', {
      method: 'POST',
      body: formData,
    });
  }

  // Helper method for single file upload
  async uploadDocument(
    file: File, 
  ): Promise<SimbaDoc[]> {
    return this.uploadDocuments([file]);
  }

  async getDocuments(): Promise<SimbaDoc[]> {
    const response = await this.request<Record<string, SimbaDoc>>('/ingestion');
    
    if (!response || Object.keys(response).length === 0) {
      return [];
    }
    
    return Object.values(response);
  }

  async getDocument(id: string): Promise<SimbaDoc> {
    return this.request(`/ingestion/${id}`);
  }

  async deleteDocument(id: string): Promise<void> {
    const isConfirmed = window.confirm('Are you sure you want to delete this document?');
    if (!isConfirmed) {
      throw new Error('Delete cancelled by user');
    }

    await this.request('/ingestion', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify([id])
    });
  }

  async deleteDocumentWithoutConfirmation(id: string): Promise<void> {
    await this.request('/ingestion', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify([id])
    });
  }

  async updateDocument(id: string, document: SimbaDoc): Promise<SimbaDoc> {
    return this.request(`/ingestion/update_document?doc_id=${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(document)
    });
  }

  async getLoaders(): Promise<string[]> {
    const response = await this.request<{ loaders: string[] }>('/loaders');
    return response.loaders;
  }

  /**
   * @deprecated Use parsingApi.getParsers() instead
   * This method is kept for backward compatibility
   */
  async getParsers(): Promise<string[]> {
    console.warn('IngestionApi.getParsers is deprecated. Use parsingApi.getParsers instead.');
    
    try {
      const response = await this.request<{ parsers: string[] | string }>('/parsers');
      
      // Handle string response (backward compatibility)
      if (typeof response.parsers === 'string') {
        return [response.parsers];
      }
      
      // Handle array response
      if (Array.isArray(response.parsers)) {
        return response.parsers;
      }
      
      console.warn('Unexpected parsers response format:', response);
      return ['docling']; // Default fallback
    } catch (error) {
      console.error('Error fetching parsers:', error);
      return ['docling']; // Default fallback on error
    }
  }

  async getUploadDirectory(): Promise<string> {
    const response = await this.request<{ path: string }>('/upload-directory');
    return response.path;
  }

  /**
   * @deprecated Use parsingApi.startParsing() instead
   * This method is kept for backward compatibility
   */
  async startParsing(documentId: string, parser: string): Promise<{ task_id?: string } | SimbaDoc> {
    console.warn('IngestionApi.startParsing is deprecated. Use parsingApi.startParsing instead.');
    
    // For Mistral OCR, always use synchronous processing
    const sync = parser === 'mistral_ocr' ? true : false;
    
    console.log(`Starting parsing for ${documentId} using ${parser} (sync: ${sync})`);
    
    const response = await this.request<{ task_id?: string } | SimbaDoc>('/parse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        document_id: documentId,
        parser: parser,
        sync: sync
      })
    });
    
    // The response could be either a task_id (for docling) or a SimbaDoc (for Mistral OCR)
    console.log('Parse response:', response);
    return response;
  }

  /**
   * @deprecated Use parsingApi.getParseStatus() instead
   * This method is kept for backward compatibility
   */
  async getParseStatus(taskId: string): Promise<{
    status: string;
    result?: {
      status: 'success' | 'error';
      document_id?: string;
      error?: string;
    };
  }> {
    console.warn('IngestionApi.getParseStatus is deprecated. Use parsingApi.getParseStatus instead.');
    return this.request(`/parsing/tasks/${taskId}`);
  }
}

// Export a single instance
export const ingestionApi = new IngestionApi();
