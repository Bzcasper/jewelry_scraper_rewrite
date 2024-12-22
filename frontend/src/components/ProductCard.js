import React from 'react';

const ProductCard = ({ product }) => {
    return (
        <div className="product-card">
            {product.image_url && <img src={product.image_url} alt={product.name} />}
            <h3>{product.name}</h3>
            <p>Price: </p>
            <p>Platform: {product.platform}</p>
            <p>Category: {product.category}</p>
            <p>Condition: {product.condition}</p>
            {product.product_url && 
                <a href={product.product_url} target="_blank" rel="noopener noreferrer">View Product</a>
            }
        </div>
    );
};

export default ProductCard;
