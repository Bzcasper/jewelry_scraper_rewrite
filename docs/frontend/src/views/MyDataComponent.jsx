import React, { useContext, useEffect } from 'react';
import DataTable from '../components/DataTable';
import { AppContext } from '../context/AppContext';
import { fetchProducts } from '../services/api';

const MyDataComponent = () => {
    const { setState } = useContext(AppContext);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchProducts();
                setState({ products: data });
            } catch (err) {
                console.error('Failed to fetch products:', err);
            }
        };

        fetchData();
    }, [setState]);

    return <DataTable />;
};

export default MyDataComponent;
