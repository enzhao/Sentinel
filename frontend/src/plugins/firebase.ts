// frontend/src/plugins/firebase.ts
// This file contains the Firebase client-side configuration and initialization.
// It dynamically connects to Firebase Emulators during development.
// References: GEMINI.md (Firebase configuration)

import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';

// Sentinel web app's Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
export const auth = getAuth(app);
export const db = getFirestore(app);

// Connect to Firebase Emulators if VITE_USE_EMULATORS is explicitly set to 'true'.
// Using String() and toLowerCase() makes the check more robust against minor
// variations like `true` (boolean) or `"TRUE"`.
if (String(import.meta.env.VITE_USE_EMULATORS).toLowerCase() === 'true') {
  if (import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST) {
    connectAuthEmulator(auth, `http://${import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST}`);
    console.log(`Connected to Firebase Auth emulator at http://${import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST}`);
  }
  if (import.meta.env.VITE_FIRESTORE_EMULATOR_HOST) {
    const firestoreHost = import.meta.env.VITE_FIRESTORE_EMULATOR_HOST;
    const [host, portStr] = firestoreHost.split(':');
    const port = parseInt(portStr, 10);

    // Add a check to ensure the host and port are valid before connecting.
    // This prevents cryptic errors if the env var is malformed.
    if (!host || isNaN(port)) {
      console.error(`Invalid VITE_FIRESTORE_EMULATOR_HOST format: "${firestoreHost}". Expected "host:port".`);
    } else {
      connectFirestoreEmulator(db, host, port);
      console.log(`Connected to Firebase Firestore emulator at http://${firestoreHost}`);
    }
  }
}
