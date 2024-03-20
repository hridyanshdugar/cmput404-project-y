"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Profile from "../components/profile";
import SideBar from "../components/sidebar";
import Rightbar from "../components/rightbar";
import Cookies from "universal-cookie";
import { useState, useEffect } from "react";
import { getFollowers, getHomePosts, getUserLocalInfo, navigate } from "../utils/utils";
import { error } from "console";
import { userInfo } from "os";
import { PostContextProvider } from "../utils/postcontext";
import { Outlet, useParams } from "react-router-dom";

export default function ProfileLayout() {
	const { userId } = useParams();
	let activeUser: boolean = false;
	const [followingStatus, setFollowingStatus] = useState<boolean>(false);
	const cookies = new Cookies();
	const allcookies = cookies.getAll();
	const userIdCookie = cookies.get("user").id;
	if (allcookies.auth && allcookies.user) {
		//!!Change to userName when added!!//
		if (userId == userIdCookie) {
			activeUser = true;
		}
	}

	const [userInformation, setUserInformation] = useState<any>(null);
	const [postCount, setPostCount] = useState<number>(0);
	const [following, setFollowing] = useState<any>(null);
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

			getFollowers(cookies.get("user").email)
				.then(async (result) => {
					if (result.status === 200) {
						const Data = await result.json();
						setFollowing(Data.length);
					} else {
						throw new Error("Error fetching posts");
					}
				})
				.catch((error) => {
					console.log(error);
				});

			/*
			getHomePosts(cookies.get("user").host, 1, 100, cookies.get("auth").access, userId)
				.then(async (result: any) => {
					if (result.status === 200) {
						const Data = await result.json();
						console.log(Data);
						let temp_count = 0;
						for (var i = 0; i < Data.length; i++) {
							if (Data[i].userId == userId) {
								temp_count++;
							}
						}
						setPostCount(temp_count);
					} else {
						throw new Error("Error fetching posts");
					}
				})
				.catch((error) => {
					console.log(error);
				});*/
		}
	}, [followingStatus]);

	if (!userInformation) {
		return (
			<div style={{ backgroundColor: "#000" }}>
				<SideBar />
				<Rightbar />
			</div>
		);
	}

	// API call to check if the user is already following the other user
	// Not working as expected for some reason
	if (!activeUser) {
		getFollowers(userInformation?.email)
			.then((result) => {
				return result.json();
			})
			.catch((error) => {
				console.log(error);
			})
			.then((data) => {
				for (let followerData of data) {
					if (userIdCookie == followerData.id) {
						setFollowingStatus(true);
					}
				}
			});
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
					username={userInformation?.email}
					bio={userInformation?.bio ? userInformation?.bio : "No Bio"}
					website={
						userInformation?.github ? userInformation?.github : "No Website"
					}
					dateJoined={""}
					followers={0}
					following={following}
					activeUser={activeUser}
					followingStatus={followingStatus}
					profileImage={userInformation?.profileImage || ""}
					profileBackround={userInformation?.profileBackgroundImage || ""}
					url={userInformation?.url || ""}
					postCount={postCount}
				/>
				<Outlet context={{ userId: userId }} />
				<Rightbar />
			</div>
		</PostContextProvider>
	);
}
