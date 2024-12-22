import React, { useEffect, useState } from 'react';
import { fetchSystemMetrics } from '../services/api';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const DataDashboard = () => {
    const [metrics, setMetrics] = useState({});

    useEffect(() => {
        const getMetrics = async () => {
            const data = await fetchSystemMetrics();
            setMetrics(data);
        };
        getMetrics();
        const interval = setInterval(getMetrics, 15000); // Update every 15 seconds
        return () => clearInterval(interval);
    }, []);

    const lineData = {
        labels: metrics.timestamps || [],
        datasets: [
            {
                label: 'CPU Usage',
                data: metrics.cpu_usage || [],
                borderColor: 'rgba(75,192,192,1)',
                fill: false,
            },
            {
                label: 'Memory Usage',
                data: metrics.memory_usage || [],
                borderColor: 'rgba(153,102,255,1)',
                fill: false,
            },
        ],
    };

    const barData = {
        labels: ['Success Rate', 'Error Rate'],
        datasets: [
            {
                label: 'Metrics',
                data: [
                    metrics.success_rate ? metrics.success_rate * 100 : 0,
                    metrics.error_rate ? metrics.error_rate * 100 : 0
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ],
            },
        ],
    };

    return (
        <div>
            <h2>Data Dashboard</h2>
            <div>
                <Line data={lineData} />
            </div>
            <div>
                <Bar data={barData} />
            </div>
        </div>
    );
};

export default DataDashboard;
