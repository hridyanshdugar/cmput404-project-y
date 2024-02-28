"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Image from "next/image";
import style from "./page.module.css";
import BackSelector from "@/components/backSelector";
import CreatePost from "@/components/createpost";
import SinglePost from "@/components/singlepost";
import { getPost, API } from "@/utils/utils";
import Cookies from "universal-cookie";
import { useEffect, useState, useContext } from "react";
import { navigate } from "@/utils/utils";
import { PostContext } from "@/utils/postcontext";

export default function Home({ params }: { params: { post: string } }) {
	const [post, setPost] = useState<any>(null);
	const [replies, setReplies] = useContext(PostContext);
	const [auth, setAuth] = useState<any>(null);
	const postID = params.post;

	useEffect(() => {
		const cookies = new Cookies();
		setAuth(cookies.get("auth"));

		if (postID) {
			getPost(auth, postID)
				.then(async (result: any) => {
					const Data = await result.json();
					console.log(Data);
					setPost(Data);
				})
				.catch(async (result: any) => {
					const Data = await result.json();
					console.log(Data);
				});
		} else {
			navigate("/home");
		}
	}, []);

	const updateReplies = (State: any) => {
		setReplies((replies: any[]) => [State, ...replies]);
		console.log(replies);
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
						profileImage={API + post.author.profileImage}
						username={post.author.email}
						text={post.contentType === "text/plain" && post.content}
						postImage={
							post.contentType ===
								("image/png;base64" || "image/jpeg;base64") && post.content
						}
						date={Math.floor(new Date(post.published).getTime() / 1000)}
						likes={0}
						retweets={0}
						comments={0}
						postID={post.id}
						contentType={post.contentType}
					/>
				)}
				{auth && (
					<CreatePost
						updatePosts={updateReplies}
						reply={true}
						style={{
							border: "1px solid rgb(47, 51, 54)",
							paddingBottom: "10px",
							backgroundColor: "black",
						}}
					/>
				)}
			</div>
		</div>
	);
}
