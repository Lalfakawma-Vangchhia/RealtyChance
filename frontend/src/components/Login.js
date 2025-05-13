import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { setToken, setRole } from '../utils';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await axios.post('/api/auth/login/', {
        username,
        password,
      });
      setToken(res.data.access);
      setRole(res.data.role);
      navigate('/');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <button type="submit" style={{ width: '100%' }}>Login</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
}

export default Login;
