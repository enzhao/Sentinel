import { initializeApp } from 'firebase/app'
import { getAuth, connectAuthEmulator } from 'firebase/auth'
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore'

// FirebaseConfig
const firebaseConfig = {
  apiKey: "AIzaSyAIDJJ38pux2NK5FMkBpIelRHUisdcRYSA",
  authDomain: "sentinel-invest.firebaseapp.com",
  projectId: "sentinel-invest",
  storageBucket: "sentinel-invest.firebasestorage.app",
  messagingSenderId: "63684098605",
  appId: "1:63684098605:web:998e65ee205e09ddb2d6a4"
};

// Initialize Firebase with the configuration
const app = initializeApp(firebaseConfig);

// Get instances of the services you need
const auth = getAuth(app);
const db = getFirestore(app);

// --- Emulator Connection Logic ---
// This Vite environment variable will be set to 'dev' by .env files
// for local development and for running tests.
if (import.meta.env.VITE_APP_ENV === 'dev') {
  console.log('Connecting frontend to Firebase Emulators...');
  
  // Point the auth and firestore services to the local emulators
  connectAuthEmulator(auth, "http://localhost:9099");
  connectFirestoreEmulator(db, 'localhost', 8080);
}
// --- End Emulator Connection Logic ---

// Export the initialized services for use throughout your app
export { auth, db };

