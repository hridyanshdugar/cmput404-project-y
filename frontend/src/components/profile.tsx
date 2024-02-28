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
import Cookies from 'universal-cookie';
import {navigate} from '@/utils/utils';
import Link from 'next/link';


type Props = {
    userid: string;
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
        console.log(props);
    }

    //Change to reflect follow status using API if not activeUser !!NEEDED!!
    followStatus = "Follow"

    handleButtonClick = () => {
      if (this.props.activeUser) {
        navigate('/settings');
      } 
      else if (this.followStatus == "Follow"){
        //API follow request !!NEEDED!!
        const cookies = new Cookies()
        const activeUserId = cookies.get("user").id
        const externalUserId = this.props.userid
        var button = document.getElementById("profileActionButton");
        this.followStatus = "Following"
        button!.innerHTML = this.followStatus
        button!.style.backgroundColor = "black"
        button!.style.color = "white"
        button!.style.border = "1px solid white";
      }
      else {
        //API unfollow request !!NEEDED!!
        const cookies = new Cookies()
        const activeUserId = cookies.get("user").id
        const externalUserId = this.props.userid
        var button = document.getElementById("profileActionButton");
        this.followStatus = "Follow"
        button!.innerHTML = this.followStatus
        button!.style.backgroundColor = "white"
        button!.style.color = "black"
        button!.style.border = "1px solid black";
      }
    };

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
                        <Button id="profileActionButton" variant="primary" onClick={this.handleButtonClick}>{this.props.activeUser? "Edit Profile" : this.followStatus}</Button>
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
                        <li><Link href={"/profile/" + this.props.userid!}>Posts</Link></li>
                        <li><Link href={"/profile/" + this.props.userid + "/media"}>Media</Link></li>
                        <li><Link href={"/profile/" + this.props.userid + "/likes"}>Likes</Link></li>
                      </ul>
                    </nav>
                  </div>
                </div>                     
          </div>;
    }
}
