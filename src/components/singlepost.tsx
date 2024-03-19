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
import { Card } from "react-bootstrap";
import Dropdown from "./dropdowns/dropdown";
import { getFrontend, navigate } from "../utils/utils";
import MarkdownPreview from "@uiw/react-markdown-preview";
import { deletePost, deleteComment } from "../utils/utils";
import Cookies from "universal-cookie";
import { useContext } from "react";
import { PostContext } from "../utils/postcontext";
import EditPopupPanel from "./editpopuppanel";

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
	likes: number;
	retweets: number;
	comments: number;
	postId: string;
	onPostPage?: boolean;
	contentType: string;
	parentId?: string;
};

const SinglePost: React.FC<Props> = (props) => {
	const onClickF = (event: React.MouseEvent<HTMLElement>) => {
		let id = event.target as any;
		id = id.id;
		console.log(id);
		if (id.includes("profile")) {
			navigate("/profile/" + props.userId);
		} else {
			if (!props.onPostPage && typeof props.parentId === "undefined") {
				navigate("/post/" + props.postId);
			}
		}
    };
    
	const [user, setuser] = useState<any>(null);
	useEffect(() => {
		const cookies = new Cookies();
		const user = cookies.get("user");
		setuser(user);
	}, []);

    const [popupOpen, setPopupOpen] = useState(false);
	const onPostOptionSelect = (selection: string | null) => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		if (selection === "Delete") {
			if (props.parentId) {
				deleteComment(auth, props.parentId, props.postId)
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
            navigator.clipboard.writeText(getFrontend() + "/post/" + props.postId)
		}
	};

	const date = new Date(0);
	const [posts, setPosts, replies, setReplies] = useContext(PostContext);
    date.setUTCSeconds(props.date);
    return (
        <>
        {popupOpen && <EditPopupPanel setPopupOpen={setPopupOpen} postId={props.postId} />}

<div
			className={style.overflow}
			onClick={onClickF}
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
				/>
			</div>
			<div className={style.blockContent}>
				<div className={[style.topText, style.blockFlexContent].join(" ")}>
					<div className={style.topLeft} id="profile2">
						<div className={style.inlineBlock} id="profile3">
							{props.name}
						</div>
						<div
							id="profile4"
							className={[style.topUserText, style.inlineBlock].join(" ")}
						>
							{props.username}
						</div>
						<div
							id="profile5"
							className={[style.topUserText, style.inlineBlock].join(" ")}
						>
							{" "}
							· {TimeConverter(date)}
						</div>
					</div>
					<div className={style.separator} />
					<div>
						<Dropdown
							icon={faEllipsis}
							options={( props.userId === user?.id ? ["Delete", "Edit"] : []).concat([
                                "Copy Link",
                              ])}
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
				<div>
					{props.postImage && (
						<Card className="bg-dark text-white">
							<Card.Img src={props.postImage} alt="Card image" />
						</Card>
					)}
				</div>
				<div className={style.flexContainer}>
					<div className={style.flexItem}>
						<FontAwesomeIcon icon={faComment} fixedWidth /> {props.comments}
					</div>
					<div className={style.flexItem}>
						<FontAwesomeIcon icon={faRepeat} fixedWidth /> {props.retweets}
					</div>
					<div className={style.flexItem}>
						<FontAwesomeIcon icon={faHeart} fixedWidth /> {props.likes}
					</div>
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
