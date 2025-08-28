// frontend/tests/plugins/firebase.spec.ts
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

// Mock the entire Firebase SDK modules. This must be done at the top level,
// before any other imports, to ensure the mocks are used.
vi.mock('firebase/app', () => ({
  initializeApp: vi.fn(() => ({})), // Returns a mock app object
}));

vi.mock('firebase/auth', () => ({
  getAuth: vi.fn(() => ({})), // Returns a mock auth object
  connectAuthEmulator: vi.fn(),
}));

vi.mock('firebase/firestore', () => ({
  getFirestore: vi.fn(() => ({})), // Returns a mock db object
  connectFirestoreEmulator: vi.fn(),
}));

// Now, we can import the mocked functions to make assertions on them.
import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';

describe('plugins/firebase.ts', () => {
  const mockFirebaseConfig = {
    apiKey: 'test-api-key',
    authDomain: 'test-auth-domain',
    projectId: 'test-project-id',
    storageBucket: 'test-storage-bucket',
    messagingSenderId: 'test-sender-id',
    appId: 'test-app-id',
    measurementId: 'test-measurement-id',
  };

  beforeEach(() => {
    // Reset modules to re-evaluate firebase.ts on each import
    vi.resetModules();
    // Clear mock history between tests
    vi.clearAllMocks();
  });

  afterEach(() => {
    // Clean up any environment variables stubbed in the tests
    vi.unstubAllEnvs();
  });

  it('should initialize Firebase with environment variables and not use emulators', async () => {
    // Arrange: Stub all the necessary environment variables for a production-like setup
    vi.stubEnv('VITE_FIREBASE_API_KEY', mockFirebaseConfig.apiKey);
    vi.stubEnv('VITE_FIREBASE_AUTH_DOMAIN', mockFirebaseConfig.authDomain);
    vi.stubEnv('VITE_FIREBASE_PROJECT_ID', mockFirebaseConfig.projectId);
    vi.stubEnv('VITE_FIREBASE_STORAGE_BUCKET', mockFirebaseConfig.storageBucket);
    vi.stubEnv('VITE_FIREBASE_MESSAGING_SENDER_ID', mockFirebaseConfig.messagingSenderId);
    vi.stubEnv('VITE_FIREBASE_APP_ID', mockFirebaseConfig.appId);
    vi.stubEnv('VITE_FIREBASE_MEASUREMENT_ID', mockFirebaseConfig.measurementId);
    vi.stubEnv('VITE_USE_EMULATORS', 'false');

    // Act: Dynamically import the module to trigger initialization
    await import('@/plugins/firebase');

    // Assert: Check that Firebase was initialized with the correct config
    expect(initializeApp).toHaveBeenCalledWith(mockFirebaseConfig);
    expect(getAuth).toHaveBeenCalled();
    expect(getFirestore).toHaveBeenCalled();
    expect(connectAuthEmulator).not.toHaveBeenCalled();
    expect(connectFirestoreEmulator).not.toHaveBeenCalled();
  });

  it('should connect to Auth and Firestore emulators when VITE_USE_EMULATORS is true', async () => {
    // Arrange
    const authHost = 'localhost:9099';
    const firestoreHost = 'localhost:8080';
    vi.stubEnv('VITE_USE_EMULATORS', 'true');
    vi.stubEnv('VITE_FIREBASE_AUTH_EMULATOR_HOST', authHost);
    vi.stubEnv('VITE_FIRESTORE_EMULATOR_HOST', firestoreHost);

    // Act
    await import('@/plugins/firebase');

    // Assert
    expect(initializeApp).toHaveBeenCalled(); // Should still initialize the app
    expect(connectAuthEmulator).toHaveBeenCalledTimes(1);
    expect(connectAuthEmulator).toHaveBeenCalledWith(expect.anything(), `http://${authHost}`);

    expect(connectFirestoreEmulator).toHaveBeenCalledTimes(1);
    expect(connectFirestoreEmulator).toHaveBeenCalledWith(expect.anything(), 'localhost', 8080);
  });
});