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
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);
	console.log(posts, replies);
	const [auth, setAuth] = useState<any>(null);
	const [user, setUser] = useState<any>(null);
	const { postId } = useParams();

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		setAuth(auth);
		setUser(user);
		if (postId) {
			getPost(auth, postId,user.id)
				.then(async (result: any) => {
					if (result.status === 200) {
						const Data = await result.json();
						const postsArray = [];
						postsArray.push(Data);
						setPosts(postsArray);
						console.log(Data, posts, "posts");
					} else {
						navigate("/home");
					}
				})
				.catch(async (result: any) => {
					navigate("/home");
					// const Data = await result?.json();
					// console.log(Data);
				});
			getPostComments(user.host, page, size, auth, user.id, postId)
				.then(async (result: any) => {
					const Data = await result.json();
					setReplies(Data);
					console.log(Data, replies, "replies");
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
		setPosts(posts.map((post: any) => ({ ...post, count: post.count + 1 })));
	};

	return (
		<div className={"main"}>
			<div className={style.mainContentViewSticky}>
				<BackSelector contentType={"Post"} />
			</div>
			<div className={style.mainContentView}>
				{posts ? (
					posts.length > 0 ? (
						posts.map((item: any, index: any) => (
							<SinglePost
								author={item.author}
								key={index}
								name={item.author.displayName}
								userId={item.author.id}
								profileImage={
									getMediaEndpoint() + item.author.profileImage?.split("?")[0]
								}
								username={item.author.displayName}
								text={item.content}
								postImage={undefined}
								date={Math.floor(new Date(item.published).getTime() / 1000)}
								likes={item.likes}
								comments={item.count}
								postId={item.id}
                                contentType={item.contentType}
                                host={item.author.host}
							/>
						))
					) : (
						navigate("/home")
					)
				) : (
					<Spinner animation="border" role="status">
						<span className="visually-hidden">Loading...</span>
					</Spinner>
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
				{replies && posts && posts.length > 0 ? (
					replies.length > 0 &&
					replies.map((item: any, index: any) => (
						<SinglePost
							author={item.author}
							key={index}
							name={item.author.displayName}
							userId={item.author.id}
							profileImage={item.author.profileImage?.split("?")[0]}
							username={item.author.displayName}
							text={item.comment}
							postImage={undefined}
							date={Math.floor(new Date(item.published).getTime() / 1000)}
							likes={item.likes}
                            comments={item.count}
                            host={item.author.host}
							postId={item.id}
							contentType={item.contentType}
							parentId={posts[0].id}
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
