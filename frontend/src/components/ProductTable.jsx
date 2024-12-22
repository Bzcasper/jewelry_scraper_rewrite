import React from 'react';
import PropTypes from 'prop-types';

const ProductTable = ({ products }) => {
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

ProductTable.propTypes = {
    products: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired,
            name: PropTypes.string.isRequired,
            price: PropTypes.number.isRequired,
        })
    ).isRequired,
};

export default ProductTable;
