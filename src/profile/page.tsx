"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import { Col, Row, Spinner } from "react-bootstrap";
import Profile from "../components/profile";
import SinglePost from "../components/singlepost";
import React, { useContext, useEffect, useState } from "react";
import { PostContext } from "../utils/postcontext";
import {
	getAPIEndpoint,
	getFrontend,
	getAuthorPosts,
	getFollowers,
	getMediaEndpoint,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { useOutletContext, useParams } from "react-router-dom";

export default function Profiles() {
	const outletObject = useOutletContext<any>();

	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useState<any>([]);
	const [userId, setUserId] = useState<any>(null);
	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const currentUrl = window.location.href;

	const id = currentUrl.split("/").pop() || '';

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		let friend = false;
		setUserId(outletObject.userId);
		setuser(user);
		setauth(auth);
		getFollowers(user.id)
			.then(async (result1: any) => {
				if (result1.ok) {
					const data = await result1.json();
					console.log("their id", id)
					data["friends"].every((currFriend : {"id" : string}) => {
						friend = currFriend.id.split("/").at(-1) === id;
						return !friend
					})
				}
				getAuthorPosts(user.host, page, size, auth, id)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log("posts before filter",Data["items"])
						if (id !== user.id) {
							if (!friend) {
								console.log("I am not friends with this user")
								Data["items"] = Data["items"].filter((item: any) => {
									return item.visibility === "PUBLIC";
								})
							} else {
								console.log("I am friends with this user")
								Data["items"] = Data["items"].filter((item: any) => {
									return item.visibility === "PUBLIC" || item.visibility === "FRIENDS";
								})
							}
						}
						console.log("filtered posts",Data["items"])
						setPosts(Data["items"]);
					})
					.catch(async (result: any) => {
						console.log("getAuthorPosts2 err",result);
					});
			})
			.catch((result1: any) => {
				console.log("getFollowers err",result1);
			})
			
	}, []);

	return (
		<>
			<div className={"main"}>
				<div className={styles.mainContentView}>
					{posts ? (
						posts.length === 0 ? (
							<>There are no posts available</>
						) : (
							posts.sort((a: { published: string; }, b: { published: string; }) => b.published.localeCompare(a.published)).map((item: any, index: any) =>
								true ? (
									<SinglePost
										post={item}
										key={index}
									/>
								) : (
									<></>
								)
							)
						)
					) : (
						<Spinner animation="border" role="status">
							<span className="visually-hidden">Loading...</span>
						</Spinner>
					)}{" "}
				</div>
			</div>
		</>
	);
}
