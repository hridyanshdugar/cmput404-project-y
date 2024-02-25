const DOMAIN = "127.0.0.1:8000";
export const API = `http://${DOMAIN}`;

export async function login(email: string, password: string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "email": email, "password": password })
  };
  return await fetch(API + `/auth/login`, options);
}

export async function signup(email: string, password: string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "email": email, "password": password })
  };
  return await fetch(API + `/auth/signup`, options);
}