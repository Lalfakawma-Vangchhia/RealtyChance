import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import PropertyList from './components/PropertyList';
import OwnerDashboard from './components/OwnerDashboard';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<PropertyList />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/owner" element={<OwnerDashboard />} />
        <Route path="/api/upload_property" element={<UploadProperty />} />
      </Routes>
    </Router>
  );
}

export default App;
