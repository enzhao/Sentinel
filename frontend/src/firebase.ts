import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAIDJJ38pux2NK5FMkBpIelRHUisdcRYSA",
  authDomain: "sentinel-invest.firebaseapp.com",
  projectId: "sentinel-invest",
  storageBucket: "sentinel-invest.firebasestorage.app",
  messagingSenderId: "63684098605",
  appId: "1:63684098605:web:998e65ee205e09ddb2d6a4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);