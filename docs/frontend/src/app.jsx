// src/App.jsx

import React from 'react';
import { AppProvider } from './context/AppContext';
import MyDataComponent from './views/MyDataComponent';

const App = () => (
    <AppProvider>
        <div className="app-container">
            <MyDataComponent />
        </div>
    </AppProvider>
);

export default App;
