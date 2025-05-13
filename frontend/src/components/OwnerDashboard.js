import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { getToken } from '../utils';

function OwnerDashboard() {
  const [properties, setProperties] = useState([]);

  React.useEffect(() => {
    axios.get('/api/properties/', {
      headers: { Authorization: `Bearer ${getToken()}` },
    }).then(res => {
      // Only show properties where the owner matches the logged-in user
      setProperties(res.data.filter(p => p.owner === localStorage.getItem('username')));
    });
  }, []);

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto' }}>
      <h2>My Properties</h2>
      <div>
        {properties.length === 0 ? (
          <div>No properties yet.</div>
        ) : (
          properties.map(p => (
            <div key={p.id} style={{ background: '#fff', marginBottom: 16, padding: 16, borderRadius: 8, boxShadow: '0 2px 8px #eee' }}>
              <h3>{p.title}</h3>
              <div>{p.address}</div>
              <div>${p.price}</div>
              <div>{p.description}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default OwnerDashboard;
