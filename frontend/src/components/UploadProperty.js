import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { getToken } from '../utils';

function UploadProperty() {
  const [form, setForm] = useState({
    title: '',
    description: '',
    price: '',
    address: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await axios.post('/api/properties/', form, {
        headers: { Authorization: `Bearer ${getToken()}` },
      });
      navigate('/owner');
    } catch (err) {
      setError('Failed to upload property');
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: '2rem auto' }}>
      <h2>Upload Property</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="title"
          placeholder="Title"
          value={form.title}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          name="address"
          placeholder="Address"
          value={form.address}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <input
          name="price"
          type="number"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <textarea
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          required
          style={{ width: '100%', marginBottom: 8 }}
        />
        <button type="submit">Upload</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
}

export default UploadProperty;
