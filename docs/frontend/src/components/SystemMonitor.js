import React, { useEffect, useState } from 'react';
import { fetchSystemMetrics } from '../services/api';

const SystemMonitor = () => {
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

    return (
        <div>
            <h2>System Monitor</h2>
            <p>Active Scraping Jobs: {metrics.active_jobs}</p>
            <p>Success Rate: {metrics.success_rate ? (metrics.success_rate * 100).toFixed(2) : 0}%</p>
            <p>CPU Usage: {metrics.cpu_usage ? metrics.cpu_usage.toFixed(2) : 0}%</p>
            <p>Memory Usage: {metrics.memory_usage ? metrics.memory_usage.toFixed(2) : 0}%</p>
            <p>Error Rate: {metrics.error_rate ? (metrics.error_rate * 100).toFixed(2) : 0}%</p>
        </div>
    );
};

class PerformanceMonitor:
def track_metrics(self):
return {
'response_times': self._get_response_stats(),
'success_rates': self._get_success_rates(),
'resource_usage': self._get_resource_stats(),
'data_quality': self._get_quality_metrics()
}

export default SystemMonitor;
