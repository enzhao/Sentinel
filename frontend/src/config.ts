// frontend/src/config.ts
// This file defines global configuration variables for the frontend application.

// The base URL for API requests. During development, this should be a relative
// path to trigger the Vite proxy defined in `vite.config.ts`.
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
