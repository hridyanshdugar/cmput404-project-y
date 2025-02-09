"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Profile from "../components/profile";
import SideBar from "../components/sidebar";
import Rightbar from "../components/rightbar";
import Cookies from "universal-cookie";
import { useState, useEffect } from "react";
import {
	getFollowers,
	getUserLocalInfo,
	checkFollowingStatus,
} from "../utils/utils";
import { error } from "console";
import { userInfo } from "os";
import { PostContextProvider } from "../utils/postcontext";
import { Outlet, useParams } from "react-router-dom";

export default function ProfileLayout() {
	const { userId } = useParams();
	const [activeUser, setActiveUser ]= useState(false);
	const [followingStatus, setFollowingStatus] = useState<string>("Notfollowing");
	const cookies = new Cookies();
	const allcookies = cookies.getAll();
	const userIdCookie = cookies.get("user").id;

	const [userInformation, setUserInformation] = useState<any>(null);
	const [postCount, setPostCount] = useState<number>(0);
	const [followingNumber, setFollowingNumber] = useState<number>(0);
	const [followersNumber, setFollowersNumber] = useState<number>(0);
    const [friendsNumber, setFriendsNumber] = useState<number>(0);
    
	useEffect(() => {
		if (userId) {
			getUserLocalInfo(allcookies.auth.access, userId!)
				.then((result) => {
					if (result.status == 200) {
						return result.json();
					} else {
						//   navigate('/');
					}
				})
				.catch((error) => {
					console.log("getUserLocalInfo", error);
					//   navigate('/');
				})
				.then((data) => {
					setUserInformation(data);
				});

			getFollowers(userId)
				.then(async (result) => {
					if (result.ok) {
						const data = await result.json();
						setFollowersNumber(data.items.length);
						setFollowingNumber(data.following.length);
						setFriendsNumber(data.friends.length);
					} else {
						throw new Error("Error fetching posts");
					}
				})
				.catch((error) => {
					console.log("getFollowers err", error);
				});
			}
			
			if (allcookies.auth && allcookies.user) {
				//!!Change to userName when added!!//
				if (userId === userIdCookie) {
					setActiveUser(true);
				}
			}
			
			if (!activeUser) {
				checkFollowingStatus(userIdCookie, userId, allcookies.auth.access)
				.then(async (result: any) => {
					result = await result.json();
					if (result.complete === true) {
						setFollowingStatus("Following");
					} else if (result.complete === false) {	 
						setFollowingStatus("Requested");
					} else {
						setFollowingStatus("Notfollowing");
					}
				})
				.catch((error) => {
                    setFollowingStatus("Notfollowing");
				});
			}
		}, []);
		
		// if (!userInformation) {
		// 	return (
		// 		<div style={{ backgroundColor: "#000" }}>
		// 			<SideBar />
		// 			<Rightbar />
		// 		</div>
		// 	);
		// }
		
		//Query username
		//If username not in database, return 404 / user not found page
	return (
		<PostContextProvider>
			<div style={{ backgroundColor: "#000" }}>
				<SideBar />
				{ userInformation && <Profile
					userid={userId!}
					name={userInformation?.displayName}
					username={userInformation?.displayName}
					bio={userInformation?.bio ? userInformation?.bio : "No Bio"}
					website={
						userInformation?.github ? userInformation?.github : "No Website"
					}
					dateJoined={""}
					followers={followersNumber}
					following={followingNumber}
					friends={friendsNumber}
					activeUser={activeUser}
					followingStatus={followingStatus}
					profileImage={userInformation?.profileImage || ""}
					profileBackround={userInformation?.profileBackgroundImage || ""}
					url={userInformation?.url || ""}
					postCount={postCount}
					host={userInformation?.host || ""}
					github={userInformation?.github || ""}
				/>}
				<Outlet context={{ userId: userId }} />
				<Rightbar />
			</div>
		</PostContextProvider>
	);
}
