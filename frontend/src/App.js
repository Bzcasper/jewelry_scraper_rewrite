import React from 'react';
import { AppProvider } from './context/AppContext';
import DataDashboard from './components/DataDashboard';
import DataTable from './components/DataTable';
import EnhancedSearch from './components/EnhancedSearch';
import SystemMonitor from './components/SystemMonitor';
import './App.css';

const App = () => {
    return (
        <AppProvider>
            <div className="App">
                <header>
                    <h1>Jewelry Scraper</h1>
                </header>
                <main>
                    <EnhancedSearch />
                    <DataDashboard />
                    <DataTable />
                    <SystemMonitor />
                </main>
            </div>
        </AppProvider>
    );
};

export default App;
