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
	createSharedPost,
    getLikePost,
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
	post: any;
	onPostPage?: boolean;
	parentId?: string;
	embedParentId?: string;
};

const SinglePost: React.FC<Props> = (props) => {
	const onClickProfile = (event: any) => {
		navigate("/profile/" + props.post.author.id);
		event.stopPropagation();
	};
	const onClickShare = (event: any) => {
		console.log("Share Clicked");
		share();
		event.stopPropagation();
	};
	const onClickPost = (event: any) => {
		if (!props.parentId) {
			navigate("/profile/"+props.post.author.id+"/post/" + props.post.id);
		}
		event.stopPropagation();
	};

	const [sharedPost, setSharedPost] = useState<any>({});
	const [popupOpen, setPopupOpen] = useState(false);
	const [likes, setLikes] = useState<number>(-2);
	const share = () => {
		if (props.post.origin === props.post.source) {
			if (props.post.visibility === "PUBLIC") {
				const cookies = new Cookies();
				const auth = cookies.get("auth");
				const user = cookies.get("user");
				createSharedPost(
					props.post.title,
					props.post.description,
					props.post.contentType,
					props.post.content,
					props.post.visibility,
					auth.access,
					user.id,
					props.post.origin
				).then(async (result: any) => {
					if (result.status === 200) {
						window.location.reload();
					} else {throw new Error("Error sharing post")}
				}).catch(async (result: any) => {
					console.log("create shared post error", result);
				});
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
		console.log("THING", props.post.author)
		let author = {
			type: "author",
			id: props.post.author["id"],
			url: props.post.author["url"],
			host: props.post.author["host"],
			displayName: props.post.author["displayName"],
			github: props.post.author["github"],
			profileImage: props.post.author["profileImage"],
		};

		likePost(
			author,
			getAPIEndpoint() + "authors/"+author.id+"/posts/" + props.post.id,
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
        getLikePost(props.post.author.id, props.post.id, auth["access"])
        		.then(async (result: any) => {
                    const Data = await result.json();
                    console.log("shared post", Data)
            			setLikes(Data.items.length);
            		})
            		.catch(async (result: any) => {
            			console.log("shared post error", result);
            		});
		if (props.post.origin !== props.post.source) {
			//Get shared post information
			console.log("shared post1", props.post.source.split("/").slice(-1)[0], props.post.source.split("/").slice(-3)[0]);
			getPost(auth["access"], props.post.source.split("/").slice(-1)[0], props.post.source.split("/").slice(-3)[0])
				.then(async (result: any) => {
					if (result.status !== 200) {
						console.log("shared post error", result);
						throw new Error("Error fetching shared post");
					} else {
					const Data = await result.json();
					console.log("shared post", Data)
					setSharedPost(Data);
					}
				}).catch(async (result: any) => { 
					console.log("shared post error", result);
				});
		}
	}, [props.post.id, props.post.contentType, props.post.content]);

	const onPostOptionSelect = (selection: string | null) => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		if (selection === "Delete") {
			if (props.parentId) {
				deleteComment(auth, props.parentId, props.post.id, props.post.author.id)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.status === 200) {
							setReplies(
								replies.filter((post: any) => post.id !== props.post.id)
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
				deletePost(auth, props.post.id)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.status === 200) {
							console.log(posts);
							setPosts(posts.filter((post: any) => post.id !== props.post.id));
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
			navigator.clipboard.writeText(getFrontend() + "/post/" + props.post.id);
		}
	};
	const date = new Date(0);
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);

	date.setUTCSeconds(Math.floor(new Date(props.post.published).getTime() / 1000));
	const formattedDate = TimeConverter(date);
	return (
		<>
			{popupOpen && (
				<EditPopupPanel setPopupOpen={setPopupOpen} postId={props.post.id} />
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
						src={getMediaEndpoint() + props.post.author.profileImage?.split("?")[0]}
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
								{props.post.author.displayName}
							</div>
							<div
								id="profile5"
								className={[style.topUserText, style.inlineBlock].join(" ")}
							>
								{" "}
								· {formattedDate}
                            </div>
                            <div id="profile99" className={[style.topUserText, style.inlineBlock].join(" ")}>
                                <Badge bg="primary">{props.post.host.split(".")[0].split("/").slice(-1)}</Badge>
                            </div>
						</div>
						<div className={style.separator} />
						<div>
							<Dropdown
								icon={faEllipsis}
								options={(props.post.author.id === user?.id
									? ["Delete", "Edit"]
									: []
								).concat(["Copy Link"])}
								onChange={onPostOptionSelect}
							/>
						</div>
					</div>
					{props.post.origin !== props.post.source ? <>
						<Card className={style.postEmbed} id="embedPost">
							{typeof sharedPost.author === "undefined" ? (
								<div className={style.missingEmbed}>Post Not Found</div>
							) : (
									<SinglePost
										post={sharedPost}
										embedParentId={props.post.id}
									/>
							)}
						</Card>
					</> : <>
						{props.post.contentType.includes("image") ? (
							<Card className="bg-dark text-white">
								<Card.Img src={props.post.content} alt="Card image" />
							</Card>
						) : (
							<></>
						)}
						{props.post.contentType === "text/markdown" ? (
							<MarkdownPreview
								source={props.post.content}
								className={style.markdownColor}
							/>
						) : (
							<></>
						)}
						{props.post.contentType === "text/plain" ? (
							<div className={style.topBottom}>{props.post.content}</div>
						) : (
							<></>
						)}					
					
					</>}
					<div className={style.flexContainer}>
						{props.parentId ? (
							<></>
						) : (
							<>
								<div className={style.flexItem}>
									<FontAwesomeIcon icon={faComment} fixedWidth />{" "}
									{props.post.count}
								</div>
								{props.post.contentType === "text/post" ? (
									<></>
								) : (
									<div
										className={style.flexItemShare}
										id={"sharePost" + props.post.id}
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
