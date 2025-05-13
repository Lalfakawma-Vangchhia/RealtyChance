import React, { useEffect, useState } from 'react';
import axios from 'axios';

function PropertyList() {
  const [properties, setProperties] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    axios.get('/api/properties/')
      .then(res => setProperties(res.data))
      .catch(() => setProperties([]));
  }, []);

  const filtered = properties.filter(p =>
    p.title.toLowerCase().includes(filter.toLowerCase()) ||
    p.address.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto' }}>
      <h2>Browse Properties</h2>
      <input
        type="text"
        placeholder="Filter by title or address"
        value={filter}
        onChange={e => setFilter(e.target.value)}
        style={{ width: '100%', marginBottom: 16 }}
      />
      <div>
        {filtered.length === 0 ? (
          <div>No properties found.</div>
        ) : (
          filtered.map(p => (
            <div key={p.id} style={{ background: '#fff', marginBottom: 16, padding: 16, borderRadius: 8, boxShadow: '0 2px 8px #eee' }}>
              <h3>{p.title}</h3>
              <div>{p.address}</div>
              <div>${p.price}</div>
              <div>Owner: {p.owner}</div>
              <div>{p.description}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default PropertyList;
