"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./singlepost.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import { faRepeat } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-regular-svg-icons";
import { faHeart } from "@fortawesome/free-regular-svg-icons";
import React, { useEffect, useState } from "react";
import {
	navigate,
	createPost,
	getAPIEndpoint,
	getFrontend,
	getPost,
	likePost,
	// sendPostToInbox,
	// sendLikeToInbox,
} from "../utils/utils";
import { Badge, Card } from "react-bootstrap";
import Dropdown from "./dropdowns/dropdown";
import MarkdownPreview from "@uiw/react-markdown-preview";
import {
	deletePost,
	deleteComment,
	getMediaEndpoint,
	getFollowers,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { useContext } from "react";
import { PostContext } from "../utils/postcontext";
import EditPopupPanel from "./editpopuppanel";
import { get } from "http";
import { error } from "console";

export function TimeConverter(date: Date) {
	var now = new Date();
	var seconds = (now.getTime() - date.getTime()) / 1000;
	var minutes = (now.getTime() - date.getTime()) / 1000 / 60;
	var hours = (now.getTime() - date.getTime()) / 1000 / 60 / 24;
	if (seconds <= 60) {
		return <>{Math.round(seconds)}s</>;
	} else if (minutes <= 60) {
		return <>{Math.round(minutes)}m</>;
	} else if (hours <= 24) {
		return <>{Math.round(hours)}h</>;
	} else {
		const months = [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		];
		if (date.getFullYear() === now.getFullYear()) {
			return (
				<>
					{months[date.getMonth()]} {date.getDay()}
				</>
			);
		}
		return (
			<>
				{months[date.getMonth()]} {date.getDay()}, {date.getFullYear()}
			</>
		);
	}
}

type Props = {
	name: string;
	profileImage: string;
	username: string;
	userId: string;
	text: string;
	postImage: string | undefined;
	date: number;
	host: string;
	likes: number;
	comments: number;
	postId: string;
	onPostPage?: boolean;
	contentType: string;
	parentId?: string;
	author: any;
};

const SinglePost: React.FC<Props> = (props) => {
	const onClickProfile = (event: any) => {
		navigate("/profile/" + props.userId);
		event.stopPropagation();
	};
	const onClickShare = (event: any) => {
		console.log("Share Clicked");
		share();
		event.stopPropagation();
	};
	const onClickPost = (event: any) => {
		if (!props.parentId) {
			navigate("/post/" + props.postId);
		}
		event.stopPropagation();
	};

	const [popupOpen, setPopupOpen] = useState(false);
	const [post, setPost] = useState<any>(null);
	const [visibility, setVisibility] = useState<string>("");
	const [likes, setLikes] = useState<number>(props.likes);
	const share = () => {
		console.log(post);
		console.log(visibility);
		if (!(props.contentType === "text/post")) {
			if (visibility === "PUBLIC") {
				sharePost();
				console.log("shared post");
			} else {
				alert("You can only share public posts");
			}
		}
	};

	const onClickLike = (event: any) => {
		console.log("CLICKED");
		const cookies = new Cookies();
		const user = cookies.get("user");
		const auth = cookies.get("auth");
		// if (props.parentId) {
		// 	sendLikeToInbox(
		// 		user["id"],
		// 		auth["access"],
		// 		getAPIEndpoint() +
		// 			"/post/" +
		// 			props.parentId +
		// 			"/comments/" +
		// 			props.postId
		// 	);
		// } else {
		// 	sendLikeToInbox(
		// 		user["id"],
		// 		auth["access"],
		// 		getAPIEndpoint() + "/post/" + props.postId
		// 	);
		// }
		
		let author = {
			type: "author",
			id: props.author["id"],
			url: props.author["url"],
			host: props.author["host"],
			displayName: props.author["displayName"],
			github: props.author["github"],
			profileImage: props.author["profileImage"],
		};

		likePost(
			author,
			getAPIEndpoint() + "authors/"+author.id+"/posts/" + props.postId,
			auth["access"]
		);
		setLikes(likes + 1);
		event.stopPropagation();
	};

	const [user, setuser] = useState<any>(null);
	useEffect(() => {
		const cookies = new Cookies();
		const user = cookies.get("user");
		const auth = cookies.get("auth");
		setuser(user);
		getPost(auth["access"], props.postId,user.id)
			.then(async (result: any) => {
				if (result.status === 200) {
					const Data = await result.json();
					setPost(Data);
					setVisibility(Data.visibility);
				} else {
					console.log("Error getting post")
					console.log(result);
					throw new Error("Error getting post");
				}
			})
			.catch((error) => {
				console.log("failed getting post")
			});
		if (props.contentType === "text/post") {
			console.log("shared post1");
			var originalPostId = props.text;
			getPost(auth.access, originalPostId, user.id)
				.then(async (result: any) => {
					const Data = await result.json();
					setSharedPost(Data);
				})
				.catch(async (result: any) => {
					const Data = await result.json();
					console.log("shared post error");
				});
		}
	}, [props.postId, props.contentType, props.text]);

	const sharePost = () => {
		const cookies = new Cookies();
		const auth = cookies.get("auth");
		const user = cookies.get("user");
		const VisibilityMap: { [key: string]: string } = {
			Everyone: "PUBLIC",
		};
		var contentToSend: string = props.postId;
		var contentTypeF = "text/post";
		createPost(
			"",
			"",
			contentTypeF,
			contentToSend,
			VisibilityMap["Everyone"],
			auth.access,
			user.id
		)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
			})
			.catch(async (result: any) => {
				const Data = await result.json();
			});
			console.log("Post");
			console.log(post);
			console.log(post.author);
		createPost(
			"Share",
			post.description,
			post.contentType,
			post.content,
			post.visibility,
			auth.access,
			post.author.id
		)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
			})
			.catch(async (result: any) => {
				const Data = await result.json();
			});
	};

	const [sharedPost, setSharedPost] = useState<any>({});

	const onPostOptionSelect = (selection: string | null) => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		if (selection === "Delete") {
			if (props.parentId) {
				deleteComment(auth, props.parentId, props.postId, props.userId)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.status === 200) {
							setReplies(
								replies.filter((post: any) => post.id !== props.postId)
							);
							setPosts(
								posts.map((post: any) => ({ ...post, count: post.count - 1 }))
							);
						}
					})
					.catch(async (result: any) => {
						console.log(result);
					});
			} else {
				deletePost(auth, props.postId)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.status === 200) {
							console.log(posts);
							setPosts(posts.filter((post: any) => post.id !== props.postId));
							console.log(posts);
						}
					})
					.catch(async (result: any) => {
						console.log(result);
					});
			}
		} else if (selection === "Edit") {
			console.log("edit");
			setPopupOpen(true);
			document.body.style.overflow = "hidden";
		} else if (selection === "Copy Link") {
			console.log("copy link");
			navigator.clipboard.writeText(getFrontend() + "/post/" + props.postId);
		}
	};
	const date = new Date(0);
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);

	date.setUTCSeconds(props.date);
	const formattedDate = TimeConverter(date);
	return (
		<>
			{popupOpen && (
				<EditPopupPanel setPopupOpen={setPopupOpen} postId={props.postId} />
			)}
			<div
				className={style.overflow}
				onClick={onClickPost}
				style={{ cursor: props.onPostPage ? "default" : "pointer" }}
			>
				<div className={style.blockImage}>
					<img
						id="profile6"
						className={style.img}
						src={props.profileImage}
						alt={""}
						width={40}
						height={40}
						onClick={onClickProfile}
					/>
				</div>
				<div className={style.blockContent}>
					<div className={[style.topText, style.blockFlexContent].join(" ")}>
						<div className={style.topLeft} id="profile2">
							<div
								className={style.inlineBlock}
								id="profile3"
								onClick={onClickProfile}
							>
								{props.name}
							</div>
							<div
								id="profile4"
								className={[style.topUserText, style.inlineBlock].join(" ")}
								onClick={onClickProfile}
							>
								{props.username}
							</div>
							<div
								id="profile5"
								className={[style.topUserText, style.inlineBlock].join(" ")}
							>
								{" "}
								· {formattedDate}
                            </div>
                            <div id="profile99" className={[style.topUserText, style.inlineBlock].join(" ")}>
                                <Badge bg="primary">{props.host.split(".")[0].split("/").slice(-1)}</Badge>
                            </div>
						</div>
						<div className={style.separator} />
						<div>
							<Dropdown
								icon={faEllipsis}
								options={(props.userId === user?.id
									? ["Delete", "Edit"]
									: []
								).concat(["Copy Link"])}
								onChange={onPostOptionSelect}
							/>
						</div>
					</div>
					{props.contentType.includes("image") ? (
						<Card className="bg-dark text-white">
							<Card.Img src={props.text} alt="Card image" />
						</Card>
					) : (
						<></>
					)}
					{props.contentType === "text/markdown" ? (
						<MarkdownPreview
							source={props.text}
							className={style.markdownColor}
						/>
					) : (
						<></>
					)}
					{props.contentType === "text/plain" ? (
						<div className={style.topBottom}>{props.text}</div>
					) : (
						<></>
					)}
					{props.contentType === "text/post" ? (
						<Card className={style.postEmbed} id="embedPost">
							{typeof sharedPost.author === "undefined" ? (
								<div className={style.missingEmbed}>Post Not Found</div>
							) : (
									<SinglePost
										author={sharedPost.author}
									name={sharedPost.author.displayName}
									userId={sharedPost.author.id}
									profileImage={
										getMediaEndpoint() +
										sharedPost.author.profileImage.split("?")[0]
									}
									username={sharedPost.author.displayName}
									text={sharedPost.content}
									postImage={undefined}
									date={Math.floor(
										new Date(sharedPost.published).getTime() / 1000
									)}
									likes={sharedPost.likes}
									comments={sharedPost.count}
									postId={sharedPost.id}
									host={sharedPost.author.host}
									contentType={sharedPost.contentType}
								/>
							)}
						</Card>
					) : (
						<></>
					)}
					<div>
						{props.postImage && (
							<Card className="bg-dark text-white">
								<Card.Img src={props.postImage} alt="Card image" />
							</Card>
						)}
					</div>
					<div className={style.flexContainer}>
						{props.parentId ? (
							<></>
						) : (
							<>
								<div className={style.flexItem}>
									<FontAwesomeIcon icon={faComment} fixedWidth />{" "}
									{props.comments}
								</div>
								{props.contentType === "text/post" ? (
									<></>
								) : (
									<div
										className={style.flexItemShare}
										id={"sharePost" + props.postId}
										onClick={onClickShare}
									>
										<FontAwesomeIcon
											icon={faRepeat}
											fixedWidth
											id="sharePost2"
										/>{" "}
									</div>
								)}
							</>
						)}

						{! props.parentId && <div className={style.flexItemLike}>
							<FontAwesomeIcon
								icon={faHeart}
								fixedWidth
								onClick={onClickLike}
							/>{" "}
							{likes}
						</div>}
						<div className={style.flexItem2}>
							<FontAwesomeIcon icon={faArrowUpFromBracket} fixedWidth />
						</div>
					</div>
				</div>
			</div>
		</>
	);
};

export default SinglePost;
