// frontend/src/services/apiService.ts
// This service provides a generic wrapper around the native fetch API.
// It centralizes logic for authentication, headers, and error handling.

import { auth } from '@/plugins/firebase';
import { API_BASE_URL } from '@/config';

/**
 * A generic fetch wrapper that handles authentication and common headers.
 * It also handles JSON parsing and basic error handling.
 * @param method - The HTTP method (GET, POST, PUT, DELETE, PATCH).
 * @param endpoint - The API endpoint (e.g., '/users/me/settings').
 * @param body - The request body for POST, PUT, PATCH requests.
 * @returns The JSON response from the API.
 */
async function apiRequest<T>(method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE', endpoint: string, body?: unknown): Promise<T> {
  const token = await auth.currentUser?.getIdToken();
  if (!token) {
    // U_E_3101: Authorization header is missing.
    throw new Error('U_E_3101: Authentication token not found. Please log in again.');
  }

  const headers: HeadersInit = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    method,
    headers,
  };

  if (body) {
    config.body = JSON.stringify(body);
  }

  // Add idempotency key for all state-changing requests.
  // Reference: product_spec.md#10.1
  if (method !== 'GET') {
    (config.headers as Record<string, string>)['Idempotency-Key'] = crypto.randomUUID();
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
  const responseData = await response.json();

  if (!response.ok) {
    // Use the detailed error message from the backend if available.
    const errorMessage = responseData.detail || `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }

  return responseData as T;
}

export const apiService = {
  get: <T>(endpoint: string) => apiRequest<T>('GET', endpoint),
  post: <T>(endpoint: string, body: unknown) => apiRequest<T>('POST', endpoint, body),
  put: <T>(endpoint: string, body: unknown) => apiRequest<T>('PUT', endpoint, body),
  patch: <T>(endpoint: string, body: unknown) => apiRequest<T>('PATCH', endpoint, body),
  delete: <T>(endpoint: string) => apiRequest<T>('DELETE', endpoint),
};