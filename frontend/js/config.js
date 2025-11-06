// API Configuration
// Update this URL after deploying to Render
const API_CONFIG = {
    // For local development
    LOCAL_API_URL: 'http://localhost:8000/api',
    
    // For production (update with your Render backend URL)
    PRODUCTION_API_URL: 'https://your-app-name.onrender.com/api',
    
    // Automatically detect environment
    getApiUrl: function() {
        // Check if running on GitHub Pages
        if (window.location.hostname.includes('github.io')) {
            return this.PRODUCTION_API_URL;
        }
        // Otherwise use local development URL
        return this.LOCAL_API_URL;
    }
};

// Export the API base URL
const API_BASE_URL = API_CONFIG.getApiUrl();