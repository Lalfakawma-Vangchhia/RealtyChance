import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [form, setForm] = useState({ username: '', email: '', password: '', role: 'buyer' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/api/auth/register/', form);
      navigate('/login');
    } catch (err) {
      setError('Registration failed');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <select name="role" value={form.role} onChange={handleChange} style={{ width: '100%', marginBottom: 8 }}>
          <option value="buyer">Buyer</option>
          <option value="owner">Owner</option>
        </select>
        <button type="submit" style={{ width: '100%' }}>Register</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
}

export default Register;
