import React, { useEffect, useState, useContext } from 'react';
import { fetchProducts, fetchSystemMetrics } from '../services/api';
import { AppContext } from '../context/AppContext';
import ProductCard from './ProductCard';

const AdminDashboard = () => {
    const { state, setState } = useContext(AppContext);
    const [metrics, setMetrics] = useState({});
    const [users, setUsers] = useState([]); // Assuming user management is implemented

    useEffect(() => {
        const getMetrics = async () => {
            try {
                const data = await fetchSystemMetrics();
                setMetrics(data);
            } catch (error) {
                console.error('Error fetching system metrics:', error);
            }
        };
        getMetrics();
        const interval = setInterval(getMetrics, 15000); // Update every 15 seconds
        return () => clearInterval(interval);
    }, []);

    const handleUserManagement = async () => {
        // Implement user management functionalities
    };

    return (
        <div className="admin-dashboard">
            <h2>Admin Dashboard</h2>
            <div className="metrics">
                <p>Active Scraping Jobs: {metrics.active_jobs}</p>
                <p>Products Found: {metrics.products_found}</p>
                <p>CPU Usage: {metrics.cpu_usage ? metrics.cpu_usage.toFixed(2) : 0}%</p>
                <p>Memory Usage: {metrics.memory_usage ? metrics.memory_usage.toFixed(2) : 0}%</p>
                <p>Success Rate: {metrics.success_rate ? (metrics.success_rate * 100).toFixed(2) : 0}%</p>
                <p>Error Rate: {metrics.error_rate ? (metrics.error_rate * 100).toFixed(2) : 0}%</p>
            </div>
            <div className="user-management">
                <h3>User Management</h3>
                {/* Implement user management UI */}
                <button onClick={handleUserManagement}>Manage Users</button>
            </div>
            <div className="product-management">
                <h3>Product Management</h3>
                {/* Implement product management UI */}
                <div className="product-grid">
                    {state.products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
