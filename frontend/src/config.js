// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Debug: Log the API URL being used
console.log('🔧 API_URL configured as:', API_URL);
console.log('🔧 VITE_API_URL env var:', import.meta.env.VITE_API_URL);

export default {
  API_URL
};
