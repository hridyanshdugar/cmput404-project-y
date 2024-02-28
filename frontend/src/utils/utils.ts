import Cookie from "universal-cookie";

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

export function formatDateToYYYYMMDD(date: Date): string {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();

  const formattedMonth = month < 10 ? `0${month}` : month.toString();
  const formattedDay = day < 10 ? `0${day}` : day.toString();

  return `${year}-${formattedMonth}-${formattedDay}`;
}

export async function updateCookies(data:any) {
  const cookies = new Cookie();
  const user = cookies.get("user");
  Object.entries(data).forEach(([key, value]) => {
    user[key] = value;
  });
  cookies.set("user",user,{ path: '/' });
}

export async function navigate(suffix:string) {
  window.location.href = `${FRONTEND}${suffix}`
}

export async function signup(email: string, password: string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "email": email, "password": password })
  };
  return await fetch(API + `/auth/signup`, options);
}

export async function saveSettings(Name: string, Github: string, PFP: File | null, PFPbackground: File | null, auth: string, id:string) {
  const formData = new FormData();

  formData.append('displayName', Name);
  formData.append('github', Github);
  if (PFP) {
    formData.append('profileImage', PFP);
  }
  if (PFPbackground) {
    formData.append('profileBackgroundImage', PFPbackground);
  }

  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${auth}`,
    },
    body: formData
  };
  return await fetch(API + `/users/${id}`, options);
}


export async function getUserLocalInfo(auth: string, id:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(API + `/users/${id}`, options);
}

export async function createPost(title:string, description:string,contentType:string, content:string, visibility:string , auth: string, id:string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
    body: JSON.stringify({ "title": title, "description": description, "contentType": contentType, "content": content, "author": id, "visibility": visibility })
  };
  return await fetch(API + `/posts/`, options);
}

export async function getHomePosts(host: string, page:number, size: number , auth: string, id:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(API + `/posts/?page=${page}&size=${size}&host=${host}&id=${id}`, options);
}

export async function getPost(auth: string, postId:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(API + `/posts/${postId}`, options);
}