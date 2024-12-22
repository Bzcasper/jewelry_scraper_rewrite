// Example test for DataDashboard component
import React from 'react';
import { render, screen } from '@testing-library/react';
import DataDashboard from '../../../frontend/src/components/DataDashboard';

test('renders DataDashboard component', () => {
    render(<DataDashboard />);
    const heading = screen.getByText(/Data Dashboard/i);
    expect(heading).toBeInTheDocument();
});

// Add more tests for other frontend components
