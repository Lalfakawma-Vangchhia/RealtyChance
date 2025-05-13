import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getToken, removeToken, removeRole, getRole } from '../utils';

function Navbar() {
  const navigate = useNavigate();
  const isLoggedIn = !!getToken();
  const role = getRole();

  const handleLogout = () => {
    removeToken();
    removeRole();
    navigate('/login');
  };

  return (
    <nav style={{ background: '#fff', padding: '1rem', borderBottom: '1px solid #eee' }}>
      <Link to="/" style={{ marginRight: 16 }}>Home</Link>
      {isLoggedIn && role === 'owner' && (
        <>
          <Link to="/owner" style={{ marginRight: 16 }}>My Properties</Link>
          <Link to="/api/upload_property" style={{ marginRight: 16 }}>Upload Property</Link>
        </>
      )}
      {!isLoggedIn ? (
        <>
          <Link to="/login" style={{ marginRight: 16 }}>Login</Link>
          <Link to="/register">Register</Link>
        </>
      ) : (
        <button onClick={handleLogout} style={{ marginLeft: 16 }}>Logout</button>
      )}
    </nav>
  );
}

export default Navbar;
