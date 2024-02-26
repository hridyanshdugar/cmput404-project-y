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
                    <div id="profileBackround"><Image className={styles.profileBackround} src={'https://i0.wp.com/www.thewrap.com/wp-content/uploads/2023/06/spider-man-across-the-spider-verse-group-shot.jpg?fit=990%2C557&ssl=1'} alt={''} width={500} height={500}/></div>
                    <div className={styles.pictureButtonContainer}>
                      <div id="profilePicture"><Image className={styles.profilePicture} src={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} alt={''} width={400} height={40}/></div>
                      <div className={styles.profileButton}>
                        <Button id="profileActionButton" variant="primary">Edit Profile</Button>
                      </div>
                    </div>
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
