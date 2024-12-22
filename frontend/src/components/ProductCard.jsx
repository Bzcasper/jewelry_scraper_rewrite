import React from 'react';
import PropTypes from 'prop-types';

const ProductCard = ({ product }) => (
    <div className="product-card">
        <h3>{product.name}</h3>
        <p>Price: ${product.price}</p>
    </div>
);

ProductCard.propTypes = {
    product: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        price: PropTypes.number.isRequired,
    }).isRequired,
};

export default ProductCard;
