import React, { useState, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { initiateScraping } from '../services/api';

const EnhancedSearch = () => {
    const { setState } = useContext(AppContext);
    const [query, setQuery] = useState('');
    const [platform, setPlatform] = useState('ebay');
    const [maxItems, setMaxItems] = useState(100);

    const handleSearch = async () => {
        setState(prev => ({ ...prev, loading: true }));
        try {
            await initiateScraping(query, platform, maxItems);
            // Optionally, poll for scraping completion or provide feedback
            alert('Scraping started successfully.');
        } catch (error) {
            alert('Failed to start scraping.');
        } finally {
            setState(prev => ({ ...prev, loading: false }));
        }
    };

    return (
        <div>
            <h2>Enhanced Search</h2>
            <input 
                type="text" 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="Search for jewelry..." 
            />
            <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
                <option value="ebay">eBay</option>
                <option value="amazon">Amazon</option>
            </select>
            <input 
                type="number" 
                value={maxItems} 
                onChange={(e) => setMaxItems(parseInt(e.target.value))} 
                placeholder="Max Items" 
                min="1"
            />
            <button onClick={handleSearch}>Search</button>
        </div>
    );
};

export default EnhancedSearch;
