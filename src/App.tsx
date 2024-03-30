import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import Home from './home/page';
import { RootLayout } from './layout';
import RootPage from './root/page';
import Login from './login/page';
import Signup from './signup/page';
import Settings from './settings/page';
import Post from './post/page';
import Notifications from './notifications/page';
import Profiles from './profile/page';
import ProfileLayout from './profile/layout';
import PostsMedia from './profile/media/page';
import PostsLikes from './profile/likes/page';
import Explore from './explore/page';

function App() {
    return <Routes>
        <Route path="/" element={<RootPage/>} />
        <Route element={<RootLayout/>}>
            <Route path="/home" element={<Home />} />
            <Route path="/explore" element={<Explore />} />
            <Route path="/notifications" element={ <Notifications/>} />
            <Route path="/settings" element={ <Settings/>} />            
        </Route>
        <Route path="/profile/:userId" element={<ProfileLayout/>}>
            <Route index element={<Profiles />} />
            <Route path="post/:postId" element={ <Post/>} />
            <Route path="media" element={ <PostsMedia/>} />
            <Route path="likes" element={ <PostsLikes/>} />
        </Route>
        <Route path="/login" element={ <Login/>} />
        <Route path="/signup" element={ <Signup/>} />
  </Routes>
}

export default App;
