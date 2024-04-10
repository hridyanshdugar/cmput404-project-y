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

	const [auth, setAuth] = useState<any>(null);
	const [post, setPost] = useState<any>(null);
	const [replies, setReplies] = useContext(PostContext);
	const [user, setUser] = useState<any>(null);
	const [loading, setLoading] = useState<boolean>(false);
	const { userId, postId } = useParams();

	useEffect(() => {
		const cookies = new Cookies();
		const authCookie = cookies.get("auth");
		const userCookie = cookies.get("user");
		if (!authCookie || !userCookie || !authCookie.access || !userCookie.id) {
			navigate("/");
		}
		const auth = authCookie.access;
		const user = userCookie;
		setAuth(auth);
		setUser(user);
		if (postId && userId) {
			getPost(auth, postId, userId)
				.then(async (result: any) => {
					if (result.ok) {
						const Data = await result.json();
						setPost(Data);
					} else {
						console.log("error", result);
						// navigate("/home");
					}
				})
				.catch(async (result: any) => {
					console.log("getPostFailed on post", result);
				});
			getPostComments(page, size, auth, userId, postId)
				.then(async (result: any) => {
					const d = await result.json();
					d.sort((a: { published: string; }, b: { published: string; }) => b.published.localeCompare(a.published))
					if (result.ok) {
						setReplies(d);
					}
				})
				.catch(async (result: any) => {
					console.log("getPostComments", result);
				});
			setLoading(true);
		} else {
			// navigate("/home");
		}
	}, []);

    const updateReplies = (State: any) => {
        const hi = [State].concat(replies);
        setReplies(hi);
        console.log("updatesReplies", hi);
	};

	return (
		<div className={"main"}>
			<div className={style.mainContentViewSticky}>
				<BackSelector contentType={"Post"} />
			</div>
			<div className={style.mainContentView}>
				{
					loading && post ? (
						<SinglePost
							post={post}
						/>
				) : (
					<Spinner animation="border" role="status">
						<span className="visually-hidden">Loading...</span>
					</Spinner>
				)}
				{auth && (
					<CreatePost
						updatePosts={updateReplies}
						postId={postId}
						postAuthorId={userId}
						style={{
							border: "1px solid rgb(47, 51, 54)",
							paddingBottom: "10px",
							backgroundColor: "black",
						}}
					/>
				)}
				{loading ? (
					post && replies && replies.length > 0 &&
                    replies.map((item: any, index: any) => (
						<SinglePost
						post={item}
							key={item.id}
							parentId={post.id.split("/").at(-1)}
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
