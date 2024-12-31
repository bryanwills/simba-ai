import { config } from '@/config';

const MAX_FILE_SIZE = 200 * 1024 * 1024; // 200MB
const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'text/plain',
  'text/markdown',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
];

interface ValidationResult {
  isValid: boolean;
  error?: string;
}

interface IngestionResponse {
  message: string;
}

export const ingestionApi = {
  validateFile: (file: File): ValidationResult => {
    if (!file) return { isValid: false, error: "No file selected" };
    
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      return { isValid: false, error: "File type not supported" };
    }

    if (file.size === 0) {
      return { isValid: false, error: "File is empty" };
    }

    if (file.size > MAX_FILE_SIZE) {
      return { isValid: false, error: "File size exceeds 200MB limit" };
    }

    return { isValid: true };
  },

  uploadDocument: async (file: File): Promise<IngestionResponse> => {
    const validation = ingestionApi.validateFile(file);
    if (!validation.isValid) {
      throw new Error(validation.error);
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

      const response = await fetch(`${config.apiUrl}/ingestion`, {
        method: 'POST',
        body: formData,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || 'Upload failed');
      }

      return response.json();
    } catch (error: any) {
      if (error.name === 'AbortError') {
        throw new Error('Upload timeout - please try again');
      }
      throw error;
    }
  },
};
