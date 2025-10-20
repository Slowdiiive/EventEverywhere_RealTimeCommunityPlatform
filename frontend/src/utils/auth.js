import jwtDecode from "jwt-decode";

const TOKEN_KEY = process.env.VUE_APP_TOKEN_KEY;

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function getUserFromToken() {
  const token = getToken();
  if (!token) return null;

  try {
    return jwtDecode(token);
  } catch (e) {
    console.error("Invalid token", e);
    return null;
  }
}

// The following methods are generally used for checking user authentication status:

export function checkLoggedIn() {
  const user = getUserFromToken();
  return !!user;
}

export function getUserId() {
  const user = getUserFromToken();
  return user ? user.userId : null;
}
