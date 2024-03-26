import { json } from "stream/consumers";
import Cookie from "universal-cookie";

export function getFrontend() {
    if (process.env.NODE_ENV === "production") {
        return window.location.origin;
    } else {
        return `http://localhost:3000`;
    }
}

export function getMediaEndpoint() {
    if (process.env.NODE_ENV === "production") {
        return '';
    } else {
        return `http://127.0.0.1:8000`;
    }
}

export function getAPIEndpoint() {
    if (process.env.NODE_ENV === "production") {
        return window.location.origin + `/api`;
    } else {
        return `http://127.0.0.1:8000/api`;
    }
}

export async function login(email: string, password: string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "email": email, "password": password })
  };
  return await fetch(getAPIEndpoint() + `/auth/login`, options);
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
  window.location.href = `${getFrontend()}${suffix}`
}

export async function signup(email: string, password: string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "email": email, "password": password })
  };
  return await fetch(getAPIEndpoint() + `/auth/signup`, options);
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
  return await fetch(getAPIEndpoint() + `/users/${id}`, options);
}


export async function getUserLocalInfo(auth: string, id:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(getAPIEndpoint() + `/users/all/${id}`, options);
}

export async function createPost(title:string, description:string, contentType:string, content:string, visibility:string , auth: string, id:string) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
    body: JSON.stringify({ "title": title, "description": description, "contentType": contentType, "content": content, "author": id, "visibility": visibility })
  };
  return await fetch(getAPIEndpoint() + `/posts/`, options);
}

export async function getRemoteUsers(auth: string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
  };
  return await fetch(getAPIEndpoint() + `/users/all`, options);
}

export async function EditPost(payload: any, auth: string, id:string) {
  const options: RequestInit = {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
    body: JSON.stringify(payload)
  };
    console.log("hi p: ", payload, auth, id)
  return await fetch(getAPIEndpoint() + `/posts/${id}`, options);
}

export async function createComment(contentType:string, comment:string, auth: string, id:string, postId:string,) {
  const options: RequestInit = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
    body: JSON.stringify({ "comment": comment, "contentType": contentType, "author": id, "post":postId })
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}/comments/`, options);
}

export async function likePost(auth: string, id:string, postId:string) {
  const options: RequestInit = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/posts/${postId}/likes`, options);
}

export async function getHomePosts(host: string, page:number, size: number , auth: string, id:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(getAPIEndpoint() + `/posts/?page=${page}&size=${size}&host=${host}&id=${id}`, options);
}

export async function getPostComments(host: string, page:number, size: number , auth: string, id:string, postId:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}/comments/?page=${page}&size=${size}&host=${host}&id=${id}`, options);
}

export async function getPost(auth: string, postId:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}`, options);
}

export async function getComment(auth: string, postId:string, commentId:string) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    }
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}/comments/${commentId}`, options);
}

export async function imageUploadHandler(image: File, auth: string) {
    const formData = new FormData();

    formData.append('image', image);

    const options: RequestInit = {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${auth}`,
        },
        body: formData
    };
    return await fetch(getAPIEndpoint() + `/images/`, options);
}
    
export async function deletePost(auth: string, postId:string) {
  const options: RequestInit = {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}`, options);
}

export async function deleteComment(auth: string, postId:string, commentId:string) {
  const options: RequestInit = {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`,
    },
  };
  return await fetch(getAPIEndpoint() + `/posts/${postId}/comments/${commentId}`, options);
}

export async function getNewFollowRequests(id: string){
    const options: RequestInit = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };
  return await fetch(getAPIEndpoint() + `/followers/${id}/requests/`, options)
}

export async function processFollowRequest(id:any, followerId:any, action:any) {
  const options: RequestInit = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    }
  };
  if (action === "accept"){
    await fetch(getAPIEndpoint() + `/authors/all/${id}/followers/${followerId}/`, options).then((res) => {
      console.log(res);
    }).catch((err) => {
      console.log(err);
    });
  }
  else{
    await fetch(getAPIEndpoint() + `/followers/all/${id}/decline/${followerId}/`, options).then((res) => {
      console.log(res);
    }).catch((err) => {
      console.log(err);
    });
  }
}



export async function sendFollowRequest(id:any, auth:any, actor:any, object:any) {
  const options: RequestInit = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`},
    body: JSON.stringify({
      type: "Follow",
      summary: "Follow request",
      actor: actor,
      object : object
    })
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/inbox/`, options)
}

export async function sendUnfollow(id:any, followerId:any) {
  const options: RequestInit = {
    method: 'DELETE',
    headers: {
        'Content-Type': 'application/json'
    }
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/followers/${followerId}/`, options);
}

export async function getFollowers(id:any) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/followers/`, options)
}

export async function checkFollowingStatus(id:any, followerId:any){
  const options: RequestInit = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
  };
  return await fetch(getAPIEndpoint() + `/authors/all/${id}/followers/${followerId}/`, options);
}

export async function sendPostToInbox(id:any, auth:any, post:any, author:any) {
  const options: RequestInit = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`},
    body: JSON.stringify({
      type: "post",
      id: id,
      post: post,
      author: author
    })
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/inbox/`, options)
}

export async function sendLikeToInbox(id:any, auth:any, post:any) {
  const options: RequestInit = {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`},
    body: JSON.stringify({
      type: "liked",
      id: id,
      object: post,
    })
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/inbox/`, options)
}

export async function getInbox(id:any, auth:any) {
  const options: RequestInit = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth}`
    }
  };
  return await fetch(getAPIEndpoint() + `/authors/${id}/inbox/`, options)
}