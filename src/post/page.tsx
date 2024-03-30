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
	const [auth, setAuth] = useState<any>(null);
	console.log(posts, replies);
	const [user, setUser] = useState<any>(null);
	const [loading, setLoading] = useState<boolean>(false);
	const { userId, postId } = useParams();

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		setAuth(auth);
		setUser(user);
		console.log("big mac postId", postId, userId);
		if (postId && userId) {
			getPost(auth, postId, userId)
				.then(async (result: any) => {
					console.log("error burgerddd2");
					if (result.status === 200) {
						console.log("error burgerddd3", result );
						const Data = await result.json();
						console.log("error burgerddd4", Data);
						const postsArray: any[] = [];
						console.log("error burgerddd5", postsArray);
						postsArray.push(Data);
						console.log("error burgerddd6");
						setPosts(postsArray);
						console.log("error burgerddd7");
						console.log(Data, posts, "posts");
					} else {
						console.log("error burgerddd", result);
						// navigate("/home");
					}
				})
				.catch(async (result: any) => {
					// navigate("/home");
					// const Data = await result?.json();
					// console.log(Data);
				});
			getPostComments(user.host, page, size, auth, user.id, postId)
				.then(async (result: any) => {
					console.log(result, "pensi");
					const d = await result.json();
					console.log("d", d);
					setReplies(d);
					console.log(d, replies, "replies");
				})
				.catch(async (result: any) => {
					// const Data = await result.json();
					console.log(result, "result");
				});
			setLoading(true);
		} else {
			// navigate("/home");
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
				{loading ? (
					loading ? (
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
				{loading ? (
					loading &&
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
