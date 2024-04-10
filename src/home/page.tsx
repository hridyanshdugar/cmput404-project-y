"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { Col, Row, Spinner } from "react-bootstrap";
import SinglePost from "../components/singlepost";
import HomeSelector from "../components/contentChoice";
import CreatePost from "../components/createpost";
import React, {
	ChangeEvent,
	MouseEvent,
	useState,
	useContext,
	useEffect,
} from "react";
import {
	getHomePosts,
	getAPIEndpoint,
	getFrontend,
	getMediaEndpoint,
	getInbox,
	getFollowers,
	navigate
} from "../utils/utils";

import Cookies from "universal-cookie";
import { PostContext } from "../utils/postcontext";
import { error } from "console";

export default function Home() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useState<any>([]);

	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const [selectedSection, setSelectedSection] = useState<string>("forYou");

	useEffect(() => {
		const cookies = new Cookies();
		const authCookie = cookies.get("auth");
		const userCookie = cookies.get("user");
		if (!authCookie || !userCookie || !authCookie.access || !userCookie.id) {
			navigate("/");
		}
		const auth = authCookie.access;
		const user = userCookie;
		setuser(user);
		setauth(auth);

		fetchContent(user.host, page, size, auth, user.id, selectedSection);
	}, [selectedSection]);

	const fetchContent = (
		host: string,
		page: number,
		size: number,
		auth: string,
		userId: string,
		selectedSection: string
	) => {
		setPosts([])
		if (selectedSection === "forYou") {
			getHomePosts(host, page, size, auth, userId)
				.then(async (result: any) => {
					if (result.ok) {
						const Data = await result.json();
						setPosts(Data);
					} else {
						throw new Error("Error fetching posts");
					}
			})
			.catch(error => {
				console.log("getHomePosts failed", error);
			});
		}
		else {
			getInbox(user.id, auth)
			.then(async (result: any) => {
				if (result.ok) {
					const Data = await result.json();
					setPosts(Data.posts);
				} else {
					throw new Error("Error fetching inbox");
				}
			}).catch(error => {
				console.log("getInbox failed", error);
			});
			//get following users
			//get posts from following users
			//as well as posts that are friends only
		}
	};

	const updatePosts = (State: any) => {
        console.log("new post", State)
        const hi = [State].concat(posts);
		setPosts(hi);
		console.log(posts);
	};

	const handleSectionChange = (section: string) => {
		setSelectedSection(section);
	};

	return (
		<div className={"main"}>
			<div className={styles.mainContentViewSticky}>
				<HomeSelector handleSectionChange={handleSectionChange} />
			</div>
			<div className={styles.mainContentView}>
				<CreatePost
					updatePosts={updatePosts}
					style={{
						border: "1px solid rgb(47, 51, 54)",
						paddingBottom: "10px",
						backgroundColor: "black",
					}}
				/>
				{selectedSection === "following" ? (
					(
						posts.sort((a: { published: string; }, b: { published: string; }) => b.published.localeCompare(a.published)).map((item: any, index: any) => (
							<SinglePost
								post={item}
                                key={index}
							/>
						))
					)
				) : posts ? (
					posts.length === 0 ? (
						<div className={styles.noPosts}>There are no posts available</div>
					) : (
						posts.map((item: any, index: any) => (
							<SinglePost
								post={item}
								key={item.id}
							/>
						))
					)
				) : (
					<Spinner animation="border" role="status">
						<span className="visually-hidden">Loading...</span>
					</Spinner>
				)}
			</div>
		</div>
	);
}
