// Utility functions for auth and API
export function getToken() {
  return localStorage.getItem('token');
}

export function setToken(token) {
  localStorage.setItem('token', token);
}

export function removeToken() {
  localStorage.removeItem('token');
}

export function getRole() {
  return localStorage.getItem('role');
}

export function setRole(role) {
  localStorage.setItem('role', role);
}

export function removeRole() {
  localStorage.removeItem('role');
}
