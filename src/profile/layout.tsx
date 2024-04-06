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
					console.log(error);
					//   navigate('/');
				})
				.then((data) => {
					setUserInformation(data);
					//console.log(data);
				});

			getFollowers(userId)
				.then(async (result) => {
					if (result.status === 200) {
						const data = await result.json();
						setFollowersNumber(data.items.length);
						setFollowingNumber(data.following.length);
						setFriendsNumber(data.friends.length);
					} else {
						throw new Error("Error fetching posts");
					}
				})
				.catch((error) => {
					console.log(error);
				});
			}
			
			if (allcookies.auth && allcookies.user) {
				//!!Change to userName when added!!//
				if (userId === userIdCookie) {
					setActiveUser(true);
				}
			}
			
			if (!activeUser) {
				console.log("them: ", userId, " me: ", userIdCookie)
				checkFollowingStatus(userId, userIdCookie, allcookies.auth.access)
				.then(async (result: any) => {
					console.log(result, "status1");
					result = await result.json();
					console.log(result, "status2");
					console.log(result.complete, result.complete === true, result.complete == true, "status222");
					if (result.complete === true) {
						console.log("HIT")
						setFollowingStatus("Following");
					} else {
						setFollowingStatus("Requested");
					}
				})
				.catch((error) => {
                    console.log(error);
                    setFollowingStatus("Notfollowing");
					console.log(followingStatus, "status4");
				});
			}
		}, []);
		
		if (!userInformation) {
			return (
				<div style={{ backgroundColor: "#000" }}>
					<SideBar />
					<Rightbar />
				</div>
			);
		}
		
		//Query username
		//If username not in database, return 404 / user not found page
	return (
		<PostContextProvider>
			<div style={{ backgroundColor: "#000" }}>
				<SideBar />
				<Profile
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
				/>
				<Outlet context={{ userId: userId }} />
				<Rightbar />
			</div>
		</PostContextProvider>
	);
}
