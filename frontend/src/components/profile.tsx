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
import SideBar from "@/components/sidebar";
import Rightbar from "@/components/rightbar";


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
    activeUser: boolean;
    //posts: Array<SinglePost>;
}

export default class Profile extends React.Component<Props> {
    constructor(props: Props) {
        super(props);
    }
    render() {
      return  <div className={"main"}>
                <div className={styles.mainContentView}> 
                  <div className={styles.container}>
                    <div className={styles.titleContainer}>
                      <h1 id="profileName" className={styles.title}>{this.props.name}</h1>
                      <div className={styles.postCount}>0 posts</div>
                    </div>
                    <div id="profileBackround"><img className={styles.profileBackround} src={this.props.profileBackround} alt={''} width={500} height={500}/></div>
                    <div className={styles.pictureButtonContainer}>
                      <div id="profilePicture"><img className={styles.profilePicture} src={this.props.profileImage} alt={''} width={400} height={400}/></div>
                      <div className={styles.profileButton}>
                        <Button id="profileActionButton" variant="primary">Edit Profile</Button>
                      </div>
                    </div>
                    <header id="profileName" className={styles.title}>{this.props.name}</header>
                    <div id="username" className={styles.username}>{this.props.username}</div>
                    <text id="bio" className={styles.bio}>{this.props.bio !== "" ? this.props.bio : "No Bio"}</text>
                    <div className={styles.informationContainer}>
                      <div id="website" className={styles.website}>{this.props.website}</div>
                      <div id="dateJoined" className={styles.dateJoined}>Date Joined</div>
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
                        <li><a href={"/profile/" + this.props.username.slice(1)}>Posts</a></li>
                        <li><a href={"/profile/" + this.props.username.slice(1) + "/media"}>Media</a></li>
                        <li><a href={"/profile/" + this.props.username.slice(1) + "/likes"}>Likes</a></li>
                      </ul>
                    </nav>
                  </div>
                </div>                     
          </div>;
    }
}
