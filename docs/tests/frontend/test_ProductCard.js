// Example test for ProductCard component
import React from 'react';
import { render, screen } from '@testing-library/react';
import ProductCard from '../../../frontend/src/components/ProductCard';

test('renders ProductCard component', () => {
    const product = {
        id: 1,
        name: 'Test Necklace',
        price: 199.99,
        platform: 'eBay',
        category: 'Necklaces',
        condition: 'New',
        image_url: 'http://example.com/image.jpg',
        product_url: 'http://example.com/product',
        date_scraped: '2023-01-01T00:00:00',
        image_path: '/images/product1.jpg',
        material_details: '{"material": "Silver"}',
        market_value: 219.99,
        similar_products: '[]'
    };

    render(<ProductCard product={product} />);
    const nameElement = screen.getByText(/Test Necklace/i);
    expect(nameElement).toBeInTheDocument();

    const priceElement = screen.getByText(/\.99/i);
    expect(priceElement).toBeInTheDocument();

    const platformElement = screen.getByText(/eBay/i);
    expect(platformElement).toBeInTheDocument();

    const categoryElement = screen.getByText(/Necklaces/i);
    expect(categoryElement).toBeInTheDocument();

    const conditionElement = screen.getByText(/New/i);
    expect(conditionElement).toBeInTheDocument();

    const imageElement = screen.getByAltText(/Test Necklace/i);
    expect(imageElement).toBeInTheDocument();

    const linkElement = screen.getByText(/View Product/i);
    expect(linkElement).toBeInTheDocument();
});
