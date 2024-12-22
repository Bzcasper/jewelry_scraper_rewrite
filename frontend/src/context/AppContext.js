import React, { createContext, useReducer } from 'react';

const initialState = {
    products: [],
};

export const AppContext = createContext(initialState);

export const AppProvider = ({ children }) => {
    const [state, setState] = useReducer((state, action) => ({ ...state, ...action }), initialState);

    return (
        <AppContext.Provider value={{ state, setState }}>
            {children}
        </AppContext.Provider>
    );
};
