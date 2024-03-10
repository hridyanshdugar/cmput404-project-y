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
import { getHomePosts, getAPIEndpoint } from "../utils/utils";
import Cookies from "universal-cookie";
import { PostContext } from "../utils/postcontext";

export default function Home() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useContext(PostContext);

	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth");
		const user = cookies.get("user");
		setuser(user);
		setauth(auth);

		getHomePosts(user.host, page, size, auth, user.id)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data);

				setPosts(Data);
			})
			.catch(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
			});
	}, []);

	const updatePosts = (State: any) => {
		setPosts((posts: any[]) => [State, ...posts]);
		console.log(posts);
	};

	return (
		<div className={"main"}>
			<div className={styles.mainContentViewSticky}>
				<HomeSelector />
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
				{posts ? posts.length === 0 ? <div className={styles.noPosts}>There are no posts available</div>: posts.map((item: any, index: any) => (
                    <SinglePost
                        key={index}
                        name={item.author.displayName}
                        userId={item.author.id}
						profileImage={getAPIEndpoint() + item.author.profileImage}
						username={item.author.email}
						text={item.content}
						postImage={undefined}
						date={Math.floor(new Date(item.published).getTime() / 1000)}
						likes={0}
						retweets={0}
						comments={0}
						postID={item.id}
						contentType={item.contentType}
					/>
				)) : <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>}
			</div>
		</div>
	);
}
