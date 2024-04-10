"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./profile.module.css";
import Button from "react-bootstrap/Button";
import React, {
	useEffect,
} from "react";
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

const Profile: React.FC<Props> = (props: Props) => {
	const [followStatus, setFollowStatus] = React.useState<string>("Follow");

	useEffect(() => {
		console.log(props.followingStatus, FollowStatusMap[props.followingStatus], "CHECK")
        setFollowStatus(FollowStatusMap[props.followingStatus])
	}, [props.followingStatus])
	
	const FollowStatusMap: { [key: string]: string } = {
		Following: "Unfollow",
		Notfollowing: "Follow",
		Requested: "Requested",
	};

	const following = (request: boolean) => {
		const cookies = new Cookies();
		const activeUserId = cookies.get("user").id;
		const externalUserId = props.userid;
		if (request) {
			let actor = {
				type: "author",
				id: user["host"] + "api/authors/" + user["id"],
				url: user["url"],
				host: user["host"],
				displayName: user["displayName"],
				github: user["github"],
				profileImage: user["profileImage"],
			};
			let object = {
				type: "author",
				id: props.host + "api/authors/" + props.userid,
				host: props.host,
				displayName: props.name,
				url: props.url,
				github: props.github,
				profileImage: props.profileImage,
			};
			sendUnfollow(actor, object, auth.access);
		}
		setFollowStatus("Follow");
		var div = document.getElementById("profileButton");
		div!.classList.remove(styles.profileButtonFollowed);
		div!.classList.add(styles.profileButton);
		var button = document.getElementById("profileActionButton");
		button!.innerHTML = followStatus;
	};

	const notFollowing = (request: boolean) => {
		const cookies = new Cookies();
		const activeUserId = cookies.get("user").id;
		const externalUserId = props.userid;
		if (request) {
			//API follow request !!NEEDED!!
			let actor = {
				type: "author",
				id: user["host"] + "/api/authors/" + user["id"],
				url: user["url"],
				host: user["host"],
				displayName: user["displayName"],
				github: user["github"],
				profileImage: user["profileImage"],
			};
			let object = {
				type: "author",
				id: props.host + "/api/authors/" + props.userid,
				host: props.host,
				displayName: props.name,
				url: props.url,
				github: props.github,
				profileImage: props.profileImage,
			};
			sendFollow(actor, object, auth.access);
		}
		setFollowStatus("Requested");
		var div = document.getElementById("profileButton");
		div!.classList.remove(styles.profileButton);
		div!.classList.add(styles.profileButtonFollowed);
		var button = document.getElementById("profileActionButton");
		button!.innerHTML = followStatus;
	};

	const handleButtonClick = () => {
		if (props.activeUser) {
			navigate("/settings");
		} else if (followStatus === "Follow") {
			notFollowing(true);
		} else {
			following(true);
		}
	};

	return (
		<div className={"main"}>
			<div className={styles.mainContentView}>
				<div className={styles.container}>
					<div className={styles.titleContainer}>
						<h1 id="profileName" className={styles.title}>
							{props.name}
						</h1>
					</div>
					<div id="profileBackround">
						<img
							className={styles.profileBackround}
							src={props.profileBackround?.split("?")[0]}
							alt={""}
							width={500}
							height={500}
						/>
					</div>
					<div className={styles.pictureButtonContainer}>
						<div id="profilePicture">
							<img
								className={styles.profilePicture}
								src={props.profileImage?.split("?")[0]}
								alt={""}
								width={400}
								height={400}
							/>
						</div>
						<div
							id="profileButton"
							className={
								followStatus === "Unfollow"
									? styles.profileButtonFollowed
									: styles.profileButton
							}
						>
							<Button
								id="profileActionButton"
								variant="primary"
								onClick={handleButtonClick}
							>
								{props.activeUser
									? "Edit Profile"
									: followStatus
								}
							</Button>
						</div>
					</div>
					<header id="profileName" className={styles.title}>
						{props.name}
					</header>
					<div id="username" className={styles.username}>
						{"@" + props.username}
					</div>
					<div id="profile99" className={[styles.username].join(" ")}>
							<Badge bg="primary">{props.host.split(".")[0].split("/").slice(-1)}</Badge>
						</div>   
					<text id="bio" className={styles.bio}>
						{props.bio !== "" ? props.bio : "No Bio"}
					</text>
					<div className={styles.informationContainer}>
						<div id="website" className={styles.website}>
							{props.website}
						</div>
						<div id="dateJoined" className={styles.dateJoined}>
							Date Joined
						</div>
					</div>
					<div className={styles.followersContainer}>
						<div id="followers" className={styles.followCount}>
							{props.followers}
							<span style={{ color: "grey" }}> Followers</span>
						</div>
						{props.host === getFrontend() + "/" ? <>
							<div id="following" className={styles.followCount}>
								{props.following}
								<span style={{ color: "grey" }}> Following</span>
							</div>
							<div id="friends" className={styles.followCount}>
								{props.friends}
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
								<Link to={"/profile/" + props.userid!}>Posts</Link>
							</li>
							{/* 								
							<li>
								<Link to={"/profile/" + props.userid + "/media"}>
									Media
								</Link>
							</li>
							<li>
								<Link to={"/profile/" + props.userid + "/likes"}>
									Likes
								</Link>
							</li> */}
						</ul>
					</nav>
				</div>
			</div>
		</div>
	);
}

export default Profile;