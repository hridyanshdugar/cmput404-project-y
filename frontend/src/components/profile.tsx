"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./profile.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { title } from 'process';
import React from 'react'
import SinglePost from '@/components/singlepost';
import Cookies from "universal-cookie";
import { useEffect, useState } from "react";
import { useRef } from "react";
import { API, formatDateToYYYYMMDD } from "@/utils/utils";


type Props = {
    name: string;
    username: string;
    profileImage: string;
    profileBackround: string;
    bio: string;
    website: string;
    dateJoined: string;
    followers: number;
    following: number;
    //posts: Array<SinglePost>;
}

interface State {
  userData: any;
}


export default class Profile extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
          userData: null,
        };
    }

    componentDidMount() {
      const cookies = new Cookies();
      this.setState({
        userData: cookies.get("user")
      });
    }

    render() {
      return <div className={"main"}>
                <div className={styles.mainContentView}> 
                  
                  <div className={styles.container}>
                    <div className={styles.titleContainer}>
                      <h1 id="profileName" className={styles.title}>{this.state.userData?.displayName}</h1>
                      <div className={styles.postCount}>0 posts</div>
                    </div>
                    <div id="profileBackround"><img className={styles.profileBackround} src={API + this.state.userData?.profileBackgroundImage || ''} alt={''} width={500} height={500}/></div>
                    <div className={styles.pictureButtonContainer}>
                      <div id="profilePicture"><img className={styles.profilePicture} src={API + this.state.userData?.profileImage || ''} alt={''} width={400} height={40}/></div>
                      <div className={styles.profileButton}>
                        <Button id="profileActionButton" variant="primary">Edit Profile</Button>
                      </div>
                    </div>
                    <header id="profileName" className={styles.title}>{this.state.userData?.displayName}</header>
                    <div id="username" className={styles.username}>{this.state.userData?.email}</div>
                    <text id="bio" className={styles.bio}>{this.props.bio !== "" ? this.props.bio : "No Bio"}</text>
                    <div className={styles.informationContainer}>
                      <div id="website" className={styles.website}>{this.state.userData?.url ? this.state.userData?.url : 'No known user site'}</div>
                      <div id="dateJoined" className={styles.dateJoined}>{this.state.userData?.creation_date ? `Joined on ${formatDateToYYYYMMDD(new Date(this.state.userData?.creation_date))}` : 'No Creation Date info'}</div>
                    </div>
                    <div className={styles.followersContainer}>
                      <div id="followers" className={styles.followCount}>{this.props.followers} 
                      <span style={{color: "grey"}}> Followers</span>
                      </div>
                      <div id="following" className={styles.followCount}>{this.props.following}
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
}
