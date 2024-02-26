"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./profile.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { title } from 'process';
import SinglePost from '@/components/singlepost';

export default function Profile() {
    return    <div className={"main"}>
                <div className={styles.mainContentView}> 
                  
                  <div className={styles.container}>
                    <div className={styles.titleContainer}>
                      <h1 id="profileName" className={styles.title}>Profile</h1>
                      <div className={styles.postCount}>0 posts</div>
                    </div>
                    <div id="profileBackround" className={styles.profileBackround}>IMAGE</div>
                    <div id="profilePicture" className={styles.profilePicture}>IMAGE</div>
                    <header id="profileName" className={styles.title}>Profile</header>
                    <div id="username" className={styles.username}>@Username</div>
                    <text id="bio" className={styles.bio}>Bio</text>
                    <div id="website" className={styles.website}>Website</div>
                    <div className={styles.followersContainer}>
                      <div id="followers" className={styles.followCount}>0 
                      <span style={{color: "grey"}}> Followers</span>
                      </div>
                      <div id="following" className={styles.followCount}>0  
                          <span style={{color: "grey"}}> Following</span>
                      </div>
                    </div>
                  </div>
                  <div className={styles.container}>
                    <nav className={styles.profileNav}>
                      <ul>
                        <li><a href="/profile">Posts</a></li>
                        <li><a href="/profile/media">Media</a></li>
                        <li><a href="/profile/likes">Likes</a></li>
                      </ul>
                    </nav>
                  </div>
                </div>                       
          </div>;
}
