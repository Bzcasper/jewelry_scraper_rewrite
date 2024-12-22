// frontend/src/App.tsx
import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Provider } from 'react-redux';
import { store } from './store';
import { JewelryList } from './components/Jewelry/JewelryList';
import { ScrapingForm } from './components/Scraping/ScrapingForm';
import { AuthProvider } from './context/AuthContext';

const queryClient = new QueryClient();

export const App: React.FC = () => {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <div className=""container mx-auto px-4"">
            <h1 className=""text-3xl font-bold mb-8"">Jewelry Management</h1>
            <ScrapingForm />
            <JewelryList />
          </div>
        </AuthProvider>
      </QueryClientProvider>
    </Provider>
  );
};