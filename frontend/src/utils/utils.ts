const DOMAIN = "127.0.0.1:8000";
export const FRONTEND = "http://localhost:3000"
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

export async function navigate(suffix:string) {
  window.location.href = `${FRONTEND}${suffix}`
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

export async function saveSettings(Name: string, Github: string, PFP: string, auth: string, id:number) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
    body: JSON.stringify({ "displayName": Name, "github": Github, "profileImage": PFP})
  };
  return await fetch(API + `/users/${id}`, options);
}


export async function getUserLocalInfo(auth: string, id:number) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(API + `/users/${id}`, options);
}
