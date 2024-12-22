import React, { useState, useEffect } from 'react';
import DataTable from './components/DataTable';

const MyComponent = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProductsData = async () => {
            try {
                const response = await fetch('YOUR_API_ENDPOINT'); // Replace with the correct endpoint
                if (!response.ok) {
                    throw new Error('Failed to fetch products');
                }
                const data = await response.json();
                setProducts(data.products || []); // Adjust this based on the API response structure
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchProductsData();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return <DataTable products={products} />;
};

export default MyComponent;
