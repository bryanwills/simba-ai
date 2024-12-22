import { config } from '@/config'

interface ApiResponse {
  message: string;
  error?: string;
}

export async function sendMessage(message: string): Promise<ApiResponse> {
  try {
    const response = await fetch(`${config.apiUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Check the content type of the response
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      return data;
    } else {
      // Handle text response
      const text = await response.text();
      return { message: text };
    }
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
} 