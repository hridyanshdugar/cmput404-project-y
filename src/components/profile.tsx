"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./profile.module.css";
import Button from "react-bootstrap/Button";
import React from "react";
import Cookies from "universal-cookie";
import { getFrontend, navigate, sendFollow, sendUnfollow } from "../utils/utils";
import { Link } from "react-router-dom";
import { Badge } from "react-bootstrap";

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
	friends: number;
	activeUser: boolean;
	followingStatus: string;
	url: string;
	postCount: number;
	host: string;
	github: string;
};

const cookies = new Cookies();
const user = cookies.get("user");
const auth = cookies.get("auth");

export default class Profile extends React.Component<Props> {
	followStatus: string = "Follow";
	constructor(props: Props) {
		super(props);
		console.log(props);

		//Change to reflect follow status using API if not activeUser !!NEEDED!!
		//FollowingStatus should be aquired in /profile/[profile]/layout.tsx
		console.log(this.props.followingStatus, this.FollowStatusMap[this.props.followingStatus], "CHECK")
		this.followStatus = this.FollowStatusMap[this.props.followingStatus];
	}

	FollowStatusMap: { [key: string]: string } = {
		Following: "Unfollow",
		NotFollowing: "Follow",
		Requested: "Requested",
	};

	following = (request: boolean) => {
		const cookies = new Cookies();
		const activeUserId = cookies.get("user").id;
		const externalUserId = this.props.userid;
		if (request) {
			let actor = {
				type: "author",
				id: user["id"],
				url: user["url"],
				host: user["host"],
				displayName: user["displayName"],
				github: user["github"],
				profileImage: user["profileImage"],
			};
			let object = {
				type: "author",
				id: this.props.userid,
				host: this.props.host,
				displayName: this.props.name,
				url: this.props.url,
				github: this.props.github,
				profileImage: this.props.profileImage,
			};
			sendUnfollow(actor, object, auth.access);
		}
		this.followStatus = "Follow";
		var div = document.getElementById("profileButton");
		div!.classList.remove(styles.profileButtonFollowed);
		div!.classList.add(styles.profileButton);
		var button = document.getElementById("profileActionButton");
		button!.innerHTML = this.followStatus;
	};

	notFollowing = (request: boolean) => {
		const cookies = new Cookies();
		const activeUserId = cookies.get("user").id;
		const externalUserId = this.props.userid;
		if (request) {
			//API follow request !!NEEDED!!
			let actor = {
				type: "author",
				id: user["id"],
				url: user["url"],
				host: user["host"],
				displayName: user["displayName"],
				github: user["github"],
				profileImage: user["profileImage"],
			};
			let object = {
				type: "author",
				id: this.props.userid,
				host: this.props.host,
				displayName: this.props.name,
				url: this.props.url,
				github: this.props.github,
				profileImage: this.props.profileImage,
			};
			sendFollow(actor, object, auth.access);
		}
		this.followStatus = "Requested";
		var div = document.getElementById("profileButton");
		div!.classList.remove(styles.profileButton);
		div!.classList.add(styles.profileButtonFollowed);
		var button = document.getElementById("profileActionButton");
		button!.innerHTML = this.followStatus;
	};

	handleButtonClick = () => {
		if (this.props.activeUser) {
			navigate("/settings");
		} else if (this.followStatus === "Follow") {
			this.notFollowing(true);
		} else {
			this.following(true);
		}
	};

	render() {
		return (
			<div className={"main"}>
				<div className={styles.mainContentView}>
					<div className={styles.container}>
						<div className={styles.titleContainer}>
							<h1 id="profileName" className={styles.title}>
								{this.props.name}
							</h1>
						</div>
						<div id="profileBackround">
							<img
								className={styles.profileBackround}
								src={this.props.profileBackround?.split("?")[0]}
								alt={""}
								width={500}
								height={500}
							/>
						</div>
						<div className={styles.pictureButtonContainer}>
							<div id="profilePicture">
								<img
									className={styles.profilePicture}
									src={this.props.profileImage?.split("?")[0]}
									alt={""}
									width={400}
									height={400}
								/>
							</div>
							<div
								id="profileButton"
								className={
									this.followStatus === "Unfollow"
										? styles.profileButtonFollowed
										: styles.profileButton
								}
							>
								<Button
									id="profileActionButton"
									variant="primary"
									onClick={this.handleButtonClick}
								>
									{this.props.activeUser
										? "Edit Profile"
										: this.followStatus
									}
								</Button>
							</div>
						</div>
						<header id="profileName" className={styles.title}>
							{this.props.name}
						</header>
						<div id="username" className={styles.username}>
							{"@" + this.props.username}
						</div>
						<div id="profile99" className={[styles.username].join(" ")}>
                                <Badge bg="primary">{this.props.host.split(".")[0].split("/").slice(-1)}</Badge>
                            </div>   
						<text id="bio" className={styles.bio}>
							{this.props.bio !== "" ? this.props.bio : "No Bio"}
						</text>
						<div className={styles.informationContainer}>
							<div id="website" className={styles.website}>
								{this.props.website}
							</div>
							<div id="dateJoined" className={styles.dateJoined}>
								Date Joined
							</div>
						</div>
						<div className={styles.followersContainer}>
							<div id="followers" className={styles.followCount}>
								{this.props.followers}
								<span style={{ color: "grey" }}> Followers</span>
							</div>
							{this.props.host === getFrontend() ? <>
								<div id="following" className={styles.followCount}>
									{this.props.following}
									<span style={{ color: "grey" }}> Following</span>
								</div>
								<div id="friends" className={styles.followCount}>
									{this.props.friends}
									<span style={{ color: "grey" }}> Friends</span>
								</div>								
							</> : <></>

							}

						</div>
					</div>
					<div className={styles.container}>
						<nav className={styles.profileNav}>
							<ul>
								<li>
									<Link to={"/profile/" + this.props.userid!}>Posts</Link>
								</li>
								<li>
									<Link to={"/profile/" + this.props.userid + "/media"}>
										Media
									</Link>
								</li>
								<li>
									<Link to={"/profile/" + this.props.userid + "/likes"}>
										Likes
									</Link>
								</li>
							</ul>
						</nav>
					</div>
				</div>
			</div>
		);
	}
}
