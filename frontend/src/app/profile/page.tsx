"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { title } from 'process';

export default function Profile() {
    return (
      <>
            <div className={"main"}>
                <div className={styles.mainContentView}>  
                  <div className={styles.container}>
                    <h1 id="profileName" className={styles.title}>Profile</h1>
                    <div className={styles.postCount}>0 posts</div>
                    <div id="profileBackround">IMAGE</div>
                    <div id="profilePicture">IMAGE</div>
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
                        <li><a href="#posts">Posts</a></li>
                        <li><a href="#media">Media</a></li>
                        <li><a href="#likes">Likes</a></li>
                      </ul>
                    </nav>
                    <div id="posts" className={styles.tabContent}>POSTS PAGE</div>
                    <div id="media" className={styles.tabContent}>MEDIA PAGE</div>
                    <div id="likes" className={styles.tabContent}>LIKES PAGE</div>
                  </div>
                </div>                       
          </div>
      </>

  );
}
