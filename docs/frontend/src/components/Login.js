import React, { useState, useContext } from 'react';
import { loginUser } from '../services/api';
import { AppContext } from '../context/AppContext';

const Login = () => {
    const { setState } = useContext(AppContext);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleLogin = async () => {
        try {
            const data = await loginUser(username, password);
            setState(prev => ({ ...prev, token: data.token }));
            setMessage('Login successful!');
        } catch (error) {
            setMessage('Login failed. Please check your credentials.');
        }
    };

    return (
        <div className="login">
            <h2>Login</h2>
            <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Username" 
            />
            <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                placeholder="Password" 
            />
            <button onClick={handleLogin}>Login</button>
            {message && <div className="message">{message}</div>}
        </div>
    );
};

export default Login;
