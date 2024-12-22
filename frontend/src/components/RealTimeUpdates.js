import React, { useEffect, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import io from 'socket.io-client';

const socket = io(process.env.REACT_APP_SOCKET_URL || 'http://localhost:8000');

const RealTimeUpdates = () => {
    const { setState } = useContext(AppContext);

    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        socket.on('new_product', (product) => {
            setState(prev => ({ 
                ...prev, 
                products: [product, ...prev.products] 
            }));
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
        });

        return () => {
            socket.off('connect');
            socket.off('new_product');
            socket.off('disconnect');
        };
    }, [setState]);

    return null; // This component does not render anything
};

export default RealTimeUpdates;
