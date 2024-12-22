// DataTable.jsx
import React, { useEffect, useState, useContext } from 'react';
import { fetchProducts } from '../services/api';
import ProductCard from './ProductCard';
import { AppContext } from '../context/AppContext';

const DataTable = () => {
    const { state, setState } = useContext(AppContext);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getProducts = async () => {
            try {
                const data = await fetchProducts();
                setState(prev => ({ ...prev, products: data }));
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch products');
                setLoading(false);
            }
        };
        getProducts();
    }, [setState]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h2>Data Table</h2>
            <div className="product-grid">
                {state.products.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export const ProductTable = ({ products }) => {
    if (!Array.isArray(products)) {
        return <div>Loading products...</div>;
    }

    return (
        <table>
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                {products.map(product => (
                    <tr key={product.id}>
                        <td>{product.name}</td>
                        <td>{product.price}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default DataTable;
