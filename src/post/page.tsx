"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import style from "./page.module.css";
import BackSelector from "../components/backSelector";
import CreatePost from "../components/createpost";
import SinglePost from "../components/singlepost";
import {
	getPost,
	getAPIEndpoint,
	getFrontend,
	getMediaEndpoint,
	getPostComments,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { useEffect, useState, useContext } from "react";
import { navigate } from "../utils/utils";
import { PostContext } from "../utils/postcontext";
import { useParams } from "react-router-dom";
import { Spinner } from "react-bootstrap";

export default function Post() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100);
	const [post, setPost] = useState<any>(null);
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);
	const [auth, setAuth] = useState<any>(null);
	const [user, setUser] = useState<any>(null);
	const { postId } = useParams();

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth");
		const user = cookies.get("user");
		setAuth(auth);
		setUser(user);
		if (postId) {
			getPost(auth, postId)
				.then(async (result: any) => {
					const Data = await result.json();
					console.log(Data);
					setPost(Data);
				})
				.catch(async (result: any) => {
					// const Data = await result?.json();
					// console.log(Data);
				});
			getPostComments(user.host, page, size, auth, user.id, postId)
				.then(async (result: any) => {
					const Data = await result.json();

					setReplies(Data);
				})
				.catch(async (result: any) => {
					// const Data = await result.json();
					console.log(result, "result");
				});
		} else {
			navigate("/home");
		}
	}, []);

	const updateReplies = (State: any) => {
		setReplies((replies: any[]) => [State, ...replies]);
		console.log(replies, "reply", State);
	};

	return (
		<div className={"main"}>
			<div className={style.mainContentViewSticky}>
				<BackSelector contentType={"Post"} />
			</div>
			<div className={style.mainContentView}>
				{post && (
					<SinglePost
						name={post.author.displayName}
						userId={post.author.id}
						profileImage={
							getMediaEndpoint() + post.author.profileImage.split("?")[0]
						}
						username={post.author.email}
						text={post.content}
						postImage={undefined}
						date={Math.floor(new Date(post.published).getTime() / 1000)}
						likes={0}
						retweets={0}
						comments={0}
						postId={post.id}
						contentType={post.contentType}
					/>
				)}
				{auth && (
					<CreatePost
						updatePosts={updateReplies}
						postId={postId}
						style={{
							border: "1px solid rgb(47, 51, 54)",
							paddingBottom: "10px",
							backgroundColor: "black",
						}}
					/>
				)}
				{replies && post ? (
					replies.length !== 0 &&
					replies.map((item: any, index: any) => (
						<SinglePost
							key={index}
							name={item.author.displayName}
							userId={item.author.id}
							profileImage={item.author.profileImage.split("?")[0]}
							username={item.author.email}
							text={item.comment}
							postImage={undefined}
							date={Math.floor(new Date(item.published).getTime() / 1000)}
							likes={0}
							retweets={0}
							comments={0}
							postId={item.id}
							contentType={item.contentType}
							parentId={post.id}
						/>
					))
				) : (
					<Spinner animation="border" role="status">
						<span className="visually-hidden">Loading...</span>
					</Spinner>
				)}
			</div>
		</div>
	);
}
