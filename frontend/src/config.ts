const FALLBACK_API_BASE_URL = "http://localhost:8000";

/**
 * Base URL for API requests. This value should be configured through
 * Vite environment variables (see frontend/.env.example).
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ?? FALLBACK_API_BASE_URL;
