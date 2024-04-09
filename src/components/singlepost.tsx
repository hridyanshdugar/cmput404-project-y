"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./singlepost.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis, faHeart as faHeartSolid } from "@fortawesome/free-solid-svg-icons";
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
		navigate("/profile/" + post.author.id.split("/").at(-1));
		event.stopPropagation();
	};
	const onClickShare = (event: any) => {
		console.log("Share Clicked");
		share();
		event.stopPropagation();
	};
	const onClickPost = (event: any) => {
		if (!props.parentId) {
			navigate("/profile/"+post.author.id.split("/").at(-1)+"/post/" + post.source.split("/").slice(-1)[0]);
		}
		event.stopPropagation();
	};


	const [post, setPost] = useState<any>(props.post);
	const [sharedPost, setSharedPost] = useState<any>({});
	const [popupOpen, setPopupOpen] = useState(false);
	const [likes, setLikes] = useState<number>(-2);
	const [likable, setLikable] = useState<boolean>(true);
	const share = () => {
		if (post.origin === post.source) {
			if (post.visibility === "PUBLIC") {
				const cookies = new Cookies();
				const auth = cookies.get("auth");
				const user = cookies.get("user");
				createSharedPost(
					post.title,
					post.description,
					post.contentType,
					post.content,
					post.visibility,
					auth.access,
					user.id,
					post.origin
				).then(async (result: any) => {
					if (result.ok) {
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
		if (likable) {
			console.log("likable");
			const cookies = new Cookies();
			const user = cookies.get("user");
			const auth = cookies.get("auth");
			console.log("THING", post.author)
			let author = {
				type: "author",
				id: post.author["id"],
				url: post.author["url"],
				host: post.author["host"],
				displayName: post.author["displayName"],
				github: post.author["github"],
				profileImage: post.author["profileImage"],
			};
	
			likePost(
				author,
				getAPIEndpoint() + "/authors/"+author.id.split("/").at(-1)+"/posts/" + (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0],
				auth["access"]
			)
			.then(async (result: any) => {
				console.log(result, "sent like");
				const d = await result.json();
				if (result.ok) {
					console.log("d", d);
					setLikes(likes + 1);
					setLikable(false);
				}
			})
			.catch(async (result: any) => {
				console.log("like failed");
			});
		}
		event.stopPropagation();
	};

	const [user, setuser] = useState<any>(null);
	useEffect(() => {
		const cookies = new Cookies();
		const user = cookies.get("user");
		const auth = cookies.get("auth");
        setuser(user);
        if (post.origin !== post.source && !props.embedParentId) {
			//Get shared post information
			console.log("shared post1", post.origin.split("/").slice(-1)[0], post.origin.split("/").slice(-3)[0]);
			getPost(auth["access"], post.origin.split("/").slice(-1)[0], post.origin.split("/").slice(-3)[0])
				.then(async (result: any) => {
					const Data = await result.json();
					if (result.ok) {
						console.log("shared post", Data)
						setSharedPost(Data);
					} else {
						console.log("shared post error", result);
						throw new Error("Error fetching shared post");
					}
				}).catch(async (result: any) => { 
					console.log("shared post error", result);
				});
        }
        if (post.author.host.split(".")[0].split("/").slice(-1) !== getAPIEndpoint().split(".")[0].split("/").slice(-1)) {
            getPost(auth["access"], (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0], (post.type === "post" ? post.source : post.id).split("/").slice(-3)[0])
            .then(async (result: any) => {
                console.log("error burgerddd2");
                if (result.ok) {
                    console.log("error burgerddd3", result );
                    const Data = await result.json();
                    console.log("error burgerddd4", Data);
                    setPost(Data);
                    console.log("error burgerddd7");
                } else {
                    console.log("error burgerddd not ok", result);
                    // navigate("/home");
                }
            })
            .catch(async (result: any) => {
                // navigate("/home");
                // const Data = await result?.json();
                // console.log(Data);
            });
        }
        getLikePost(post.author.id.split("/").at(-1), (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0], auth["access"])
        		.then(async (result: any) => {
						const Data = await result.json();
						console.log("like post", Data)
						Data.items.every((dataLike : {"author" : {"id" : string}}) => {
							console.log("like author id", dataLike.author.id.split("/").at(-1))
							if (dataLike.author.id.split("/").at(-1) === user?.id) {
								console.log("already liked this")
								setLikable(false);
							}
							return likable
						});
            			setLikes(Data.items.length);
            		})
            		.catch(async (result: any) => {
            			console.log("shared post error", result);
            		});
	}, [post.id, post.contentType, post.content]);

	const onPostOptionSelect = (selection: string | null) => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		if (selection === "Delete") {
			if (props.parentId) {
				deleteComment(auth, props.parentId, (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0], post.author.id.split("/").at(-1))
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.ok) {
							setReplies(
								replies.filter((post: any) => (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0] !== (post.type === "post" ? post.source : post.id).split("/").slice(-3)[0])
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
				deletePost(auth, (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0], post.author.id.split("/").at(-1))
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data);

						if (result.ok) {
							console.log(posts);
							setPosts(posts.filter((post: any) => (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0] !== (post.type === "post" ? post.source : post.id).split("/").slice(-3)[0]));
							console.log(posts);
						}
					})
					.catch(async (result: any) => {
						console.log("not ok")
						console.log(result);
					});
			}
		} else if (selection === "Edit") {
			console.log("edit");
			setPopupOpen(true);
			document.body.style.overflow = "hidden";
		} else if (selection === "Copy Link") {
			console.log("copy link");
			navigator.clipboard.writeText(getFrontend() + "/post/" + (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0]);
		}
	};
	const date = new Date(0);
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);

	date.setUTCSeconds(Math.floor(new Date(post.published).getTime() / 1000));
	const formattedDate = TimeConverter(date);
	return (
		<>
			{popupOpen && (
				<EditPopupPanel setPopupOpen={setPopupOpen} postId={(post.type === "post" ? post.source : post.id).split("/").slice(-1)[0]} />
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
						src={getMediaEndpoint() + post.author.profileImage?.split("?")[0]}
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
								{post.author.displayName}
							</div>
							<div
								id="profile5"
								className={[style.topUserText, style.inlineBlock].join(" ")}
							>
								{" "}
								· {formattedDate}
                            </div>
                            <div id="profile99" className={[style.topUserText, style.inlineBlock].join(" ")}>
                                <Badge bg="primary">{post.author.host.split(".")[0].split("/").slice(-1)}</Badge>
                            </div>
						</div>
                        <div className={style.separator} />
                        {props.embedParentId ? <></> : <>
                            <div>
                                <Dropdown
                                    icon={faEllipsis}
                                    options={(post.author.id.split("/").at(-1) === user?.id && !props.parentId
                                        ? ["Delete", "Edit"]
                                        : []
                                    ).concat(["Copy Link"])}
                                    onChange={onPostOptionSelect}
                                />
                            </div>                        
                        </>}
					</div>
                    {!props.parentId && post.origin !== post.source && !props.embedParentId ? <>
						<Card className={style.postEmbed} id="embedPost">
							{typeof sharedPost.author === "undefined" ? (
								<div className={style.missingEmbed}>Post Not Found</div>
							) : (
									<SinglePost
										post={sharedPost}
										embedParentId={(post.type === "post" ? post.source : post.id).split("/").slice(-1)[0]}
									/>
							)}
						</Card>
                    </> : <>
						{post.contentType.includes("image") ? (
							<Card className="bg-dark text-white">
								<Card.Img src={props.parentId ? post.comment : post.content} alt="Card image" />
							</Card>
						) : (
							<></>
						)}
						{post.contentType === "text/markdown" ? (
							<MarkdownPreview
								source={props.parentId ? post.comment : post.content}
								className={style.markdownColor}
							/>
						) : (
							<></>
						)}
						{post.contentType === "text/plain" ? (
							<div className={style.topBottom}>{props.parentId ? post.comment : post.content}</div>
						) : (
							<></>
						)}					
					
                    </>}
                    {props.embedParentId ? <></> : <>
                    <div className={style.flexContainer}>
						{props.parentId ? (
							<></>
						) : (
							<>
								<div className={style.flexItem}>
									<FontAwesomeIcon icon={faComment} fixedWidth />{" "}
									{post.count}
								</div>
								{post.origin !== post.source  && !props.embedParentId ? (
									<div
                                    className={style.flexItemShare}
                                    id={"sharePost" + (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0]}
                                    onClick={onClickShare}
                                >
                                </div>
								) : (
									<div
										className={style.flexItemShare}
										id={"sharePost" + (post.type === "post" ? post.source : post.id).split("/").slice(-1)[0]}
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
								icon={likable ? faHeart : faHeartSolid}
								fixedWidth
								onClick={onClickLike}
							/>{" "}
							{likes}
						</div>}
						<div className={style.flexItem2}>
							<FontAwesomeIcon icon={faArrowUpFromBracket} fixedWidth />
						</div>
					</div>
                </>}
                </div> 
			</div>
		</>
	);
};

export default SinglePost;
