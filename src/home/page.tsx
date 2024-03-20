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
} from "../utils/utils";
import Cookies from "universal-cookie";
import { PostContext } from "../utils/postcontext";

export default function Home() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useContext(PostContext);

	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const [selectedSection, setSelectedSection] = useState<string>("forYou");

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
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
		if (selectedSection === "forYou") {
			getHomePosts(host, page, size, auth, userId)
				.then(async (result: any) => {
					const Data = await result.json();
					console.log(Data);

				setPosts(Data);
				console.log(posts);
			})
			.catch(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
			});
		}
		else {
			//get following users
			//get posts from following users
			//as well as posts that are friends only
		}
	};

	const updatePosts = (State: any) => {
		setPosts((posts: any[]) => [State, ...posts]);
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
					<div className={styles.noPosts}>Following</div>
				) : posts ? (
					posts.length === 0 ? (
						<div className={styles.noPosts}>There are no posts available</div>
					) : (
						posts.map((item: any, index: any) => (
							<SinglePost
								key={index}
								name={item.author.displayName}
								userId={item.author.id}
								profileImage={
									getMediaEndpoint() + item.author.profileImage?.split("?")[0]
								}
								username={item.author.email}
								text={item.content}
								postImage={undefined}
								date={Math.floor(new Date(item.published).getTime() / 1000)}
								likes={0}
								retweets={0}
								comments={item.count}
								postId={item.id}
								contentType={item.contentType}
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
