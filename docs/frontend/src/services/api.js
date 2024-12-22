// src/services/api.js

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL; // Replace with your API base URL

// Fetch products from the API
export const fetchProducts = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/products`);
        return response.data;
    } catch (error) {
        console.error('Error fetching products:', error);
        throw error; // Rethrow the error after logging
    }
};

// Initiate scraping with specific parameters
export const initiateScraping = async (query, platform, maxItems) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/scrape`, {
            query,
            platform,
            max_items: maxItems,
        });
        return response.data;
    } catch (error) {
        console.error('Error initiating scraping:', error);
        throw error;
    }
};

// Fetch system metrics from the API
export const fetchSystemMetrics = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/metrics`);
        return response.data;
    } catch (error) {
        console.error('Error fetching system metrics:', error);
        throw error;
    }
};
