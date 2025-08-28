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

// Connect to Firebase Emulators if VITE_USE_EMULATORS is true
if (import.meta.env.VITE_USE_EMULATORS === 'true') {
  if (import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST) {
    connectAuthEmulator(auth, `http://${import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST}`);
    console.log(`Connected to Firebase Auth emulator at http://${import.meta.env.VITE_FIREBASE_AUTH_EMULATOR_HOST}`);
  }
  if (import.meta.env.VITE_FIRESTORE_EMULATOR_HOST) {
    connectFirestoreEmulator(db, import.meta.env.VITE_FIRESTORE_EMULATOR_HOST.split(':')[0], parseInt(import.meta.env.VITE_FIRESTORE_EMULATOR_HOST.split(':')[1]));
    console.log(`Connected to Firebase Firestore emulator at http://${import.meta.env.VITE_FIRESTORE_EMULATOR_HOST}`);
  }
}
