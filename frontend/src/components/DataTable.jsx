import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';
import ProductCard from './ProductCard';

const DataTable = () => {
    const { state } = useContext(AppContext);

    if (!Array.isArray(state.products)) {
        return <div>Loading products...</div>;
    }

    return (
        <div className="product-grid">
            {state.products.map((product) => (
                <ProductCard key={product.id} product={product} />
            ))}
        </div>
    );
};

export default DataTable;
