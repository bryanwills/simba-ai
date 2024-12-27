import { config } from '@/config'

export async function sendMessage(message: string): Promise<Response> {
  try {
    const response = await fetch(`${config.apiUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
} 