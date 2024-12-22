import React, { useState, useContext } from 'react';
import { registerUser } from '../services/api';
import { AppContext } from '../context/AppContext';

const Register = () => {
    const { setState } = useContext(AppContext);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('user');
    const [message, setMessage] = useState('');

    const handleRegister = async () => {
        try {
            const data = await registerUser(username, password, role);
            setMessage('Registration successful! You can now log in.');
        } catch (error) {
            setMessage('Registration failed. Please try again.');
        }
    };

    return (
        <div className="register">
            <h2>Register</h2>
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
            <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="user">User</option>
                <option value="admin">Admin</option>
            </select>
            <button onClick={handleRegister}>Register</button>
            {message && <div className="message">{message}</div>}
        </div>
    );
};

export default Register;
