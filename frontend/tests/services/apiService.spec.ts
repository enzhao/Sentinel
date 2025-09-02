import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiService } from '@/services/apiService';
import { auth } from '@/plugins/firebase';

// Mock the global fetch function
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock Firebase auth. We only need to mock the parts we use.
vi.mock('@/plugins/firebase', () => ({
  auth: {
    currentUser: {
      getIdToken: vi.fn(),
    },
  },
}));

describe('apiService', () => {
  beforeEach(() => {
    // Reset mocks before each test to ensure isolation
    vi.resetAllMocks();
  });

  it('should make a GET request with correct headers', async () => {
    // Arrange
    const mockToken = 'test-token';
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue(mockToken);
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: 'success' }),
    });

    // Act
    await apiService.get('/test-endpoint');

    // Assert
    expect(mockFetch).toHaveBeenCalledOnce();
    const fetchCall = mockFetch.mock.calls[0];
    const fetchUrl = fetchCall[0];
    const fetchConfig = fetchCall[1];

    expect(fetchUrl).toContain('/test-endpoint');
    expect(fetchConfig.method).toBe('GET');
    expect(fetchConfig.headers.Authorization).toBe(`Bearer ${mockToken}`);
    expect(fetchConfig.headers['Content-Type']).toBe('application/json');
    // Idempotency-Key should not be present for GET requests
    expect(fetchConfig.headers['Idempotency-Key']).toBeUndefined();
  });

  it('should make a PUT request with body and idempotency key', async () => {
    // Arrange
    const mockToken = 'test-token';
    const requestBody = { name: 'test' };
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue(mockToken);
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: 'updated' }),
    });

    // Act
    await apiService.put('/test-endpoint', requestBody);

    // Assert
    expect(mockFetch).toHaveBeenCalledOnce();
    const fetchConfig = mockFetch.mock.calls[0][1];

    expect(fetchConfig.method).toBe('PUT');
    expect(fetchConfig.body).toBe(JSON.stringify(requestBody));
    expect(fetchConfig.headers.Authorization).toBe(`Bearer ${mockToken}`);
    expect(fetchConfig.headers['Idempotency-Key']).toBeDefined();
    expect(typeof fetchConfig.headers['Idempotency-Key']).toBe('string');
  });

  it('should throw an error if auth token is not available', async () => {
    // Arrange
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue(null);

    // Act & Assert
    await expect(apiService.get('/test-endpoint')).rejects.toThrow(
      'U_E_3101: Authentication token not found. Please log in again.'
    );
  });

  it('should throw an error on non-ok response using backend detail', async () => {
    // Arrange
    const mockToken = 'test-token';
    const errorResponse = { detail: 'Something went wrong from the backend' };
    vi.mocked(auth.currentUser?.getIdToken).mockResolvedValue(mockToken);
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve(errorResponse),
    });

    // Act & Assert
    await expect(apiService.get('/test-endpoint')).rejects.toThrow(
      errorResponse.detail
    );
  });
});