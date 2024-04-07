"use strict";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./createpost.module.css";
import { faImage } from "@fortawesome/free-regular-svg-icons";
import React, {
	ChangeEvent,
	MouseEvent,
	useState,
	useRef,
	useEffect,
} from "react";
import Dropdown from "./dropdowns/dropdown";
import Button from "./buttons/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMarkdown } from "@fortawesome/free-brands-svg-icons";
import { faFileLines } from "@fortawesome/free-regular-svg-icons";
import {
	createComment,
	createPost,
	getAPIEndpoint,
	getFrontend,
	getMediaEndpoint,
	imageUploadHandler,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { Card } from "react-bootstrap";
import MDEditor from "@uiw/react-md-editor";

interface CreatePostProps {
	style?: React.CSSProperties;
	postId?: string | undefined;
	postAuthorId ?: string | undefined;
	setPopupOpen?: React.Dispatch<React.SetStateAction<boolean>>;
	updatePosts: (State: any) => void;
}

const CreatePost: React.FC<CreatePostProps> = (props) => {
	const dropdownRef = useRef<HTMLDivElement>(null);
	const horizontalLineRef = useRef<HTMLHRElement>(null);

	const [contentType, setcontentType] = useState<string>("text/plain");
	const [contentTypeMinimal, setcontentTypeMinimal] = useState<string>("plain");
	const [title, settitle] = useState<string>("");
	const [description, setdescription] = useState<string>("");
	const [content, setcontent] = useState<string>("");
	const [visibility, setvisibility] = useState<string>("Everyone");

	const cookies = new Cookies();
	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const [markdownValue, setMarkdownValue] = useState<string | undefined>("");

	const [PFPbackground, setPFPbackground] = useState<File | null>(null);
	const [PFPbackgroundurl, setPFPbackgroundurl] = useState<string>("");

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		setuser(user);
		setauth(auth);
	}, []);

	const handlePFPbackground = (event: ChangeEvent<HTMLInputElement>) => {
		if (event.target.files && event.target.files[0]) {
			const file = event.target.files[0];
			setPFPbackground(file);

			const fileReader = new FileReader();
			fileReader.onload = () => {
				setPFPbackgroundurl(fileReader.result as string);
				console.log(fileReader.result);
			};
			fileReader.readAsDataURL(file);
		}
	};

	const onTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
		event.target.style.height = "auto";
		event.target.style.height = event.target.scrollHeight + "px";
		setcontent(event.target.value);
	};

	const handleVisibilityChange = (newSelection: string | null) => {
		console.log(newSelection);
		setvisibility(newSelection || "Everyone");
	};

	const onCreateClick = (event: MouseEvent<HTMLDivElement>) => {
		if (dropdownRef.current && horizontalLineRef.current && !props.postId) {
			dropdownRef.current.style.display = "flex";
			horizontalLineRef.current.style.display = "block";
		}
	};

	const handlePaste = async (event: React.ClipboardEvent<HTMLDivElement>) => {
		const clipboardData = event.clipboardData;
		if (clipboardData.files.length === 1) {
			const myfile = clipboardData.files[0] as File;
			const response = await imageUploadHandler(myfile, auth);
			const data = await response.json();
			let url = getMediaEndpoint() + data.image;
			url = url?.split("?")[0];
			event.preventDefault();
			if (url) {
				document.execCommand("insertText", false, `![${url}](${url})\n`);
			} else {
				document.execCommand(
					"insertText",
					false,
					"ERROR Image has not been stored on server"
				);
			}
		}
	};

	const onSubmit = () => {
		if (content !== "" || /^\s*$/.test(content)) {
			const VisibilityMap: { [key: string]: string } = {
				Everyone: "PUBLIC",
				Unlisted: "UNLISTED",
				Friends: "FRIENDS",
			};
			var contentToSend: string = "";
			if (contentTypeMinimal === "picture") {
				var contentTypeF =
					PFPbackgroundurl?.split("base64")[0]?.split("data:")[1] + "base64";
				contentToSend = PFPbackgroundurl;
			} else if (contentTypeMinimal === "markdown") {
				var contentTypeF = "text/markdown";
				contentToSend = markdownValue!;
			} else {
				var contentTypeF = "text/plain";
				contentToSend = content;
			}
			console.log(props.postId, "id");
			if (props.postId && props.postAuthorId) {
				let author = {
					type: "author",
					id: user["id"],
					url: user["url"],
					host: user["host"],
					displayName: user["displayName"],
					github: user["github"],
					profileImage: user["profileImage"],
				};
				console.log("author", author)
				createComment(contentTypeF, contentToSend, auth, author, props.postId, props.postAuthorId)
					.then(async (result: any) => {
						const Data = await result.json();
						console.log(Data, "check data")
						console.log(Data[0], "check data")
						
						if (Data[0] === '{"Title":"Done"}') {
							console.log("HIT")
							console.log("prro")
							if (props.setPopupOpen) {
								props.setPopupOpen(false);
							}
							if (contentTypeMinimal === "plain") {
								setcontent("");
							} else if (contentTypeMinimal === "markdown") {
								setMarkdownValue("");
							} else if (contentTypeMinimal === "picture") {
								setPFPbackgroundurl("");
							}
							console.log("big boss");
							window.location.reload();
						}
						
					})
					.catch(async (result: any) => {
						const Data = await result.json();
						console.log(Data);
					});
			} else {
				createPost(
					title,
					description,
					contentTypeF,
					contentToSend,
					VisibilityMap[visibility],
					auth,
					user.id
				)
					.then(async (result: any) => {
						const Data = await result.json();
						props.updatePosts(Data);
						if (props.setPopupOpen) {
							props.setPopupOpen(false);
						}
						if (contentTypeMinimal === "plain") {
							setcontent("");
						} else if (contentTypeMinimal === "markdown") {
							setMarkdownValue("");
						} else if (contentTypeMinimal === "picture") {
							setPFPbackgroundurl("");
						}
					})
					.catch(async (result: any) => {
						const Data = await result.json();
						console.log(Data);
					});
			}
		} else {
			alert("Cannot post empty post");
		}
	};

	console.log(contentTypeMinimal);
	// src={`${pfp ? getAPIEndpoint() + pfp : ''}`}
	return (
		<div style={props.style}>
			<div className={style.createPost} onClick={onCreateClick}>
				<div className={style.blockImage}>
					<img
						className={style.img}
						src={`${
							user ? getMediaEndpoint() + user.profileImage?.split("?")[0] : ""
						}`}
						style={{ width: "40px", height: "40px" }}
					/>
				</div>
				<div className={style.blockContent}>
					{contentTypeMinimal === "plain" ? (
						<textarea
							value={content}
							className={style.textarea}
							placeholder="What is happening?!"
							onChange={onTextChange}
						></textarea>
					) : (
						""
					)}

					{contentTypeMinimal === "picture" ? (
						<>
							{PFPbackgroundurl && (
								<Card
									className="bg-dark text-white"
									style={{ marginTop: "30px" }}
								>
									<Card.Img src={PFPbackgroundurl} alt="Card image" />
								</Card>
							)}
						</>
					) : (
						""
					)}

					{contentTypeMinimal === "markdown" ? (
						<MDEditor
							value={markdownValue}
							onChange={setMarkdownValue}
							onPaste={handlePaste}
							className={style.markdownColor}
						/>
					) : (
						""
					)}
				</div>
			</div>
			<Dropdown
				label="Everyone"
				dropdownTitle="Choose Audience"
				onChange={handleVisibilityChange}
				options={["Everyone", "Friends", "Unlisted"]}
				innerRef={dropdownRef}
				styles={{ display: "none" }}
			/>
			<hr
				className={style.horizontalLine}
				ref={horizontalLineRef}
				style={{ display: "none" }}
			></hr>
			<div className={style.flexContainer}>
				<div className={style.flexItem}>
					<FontAwesomeIcon
						icon={faFileLines}
						fixedWidth
						className={contentTypeMinimal === "plain" ? style.selectItem : ""}
						onClick={() => {
							setcontentTypeMinimal("plain");
						}}
					/>
				</div>
				<div className={style.flexItem}>
					<FontAwesomeIcon
						icon={faMarkdown}
						fixedWidth
						className={
							contentTypeMinimal === "markdown" ? style.selectItem : ""
						}
						onClick={() => {
							setcontentTypeMinimal("markdown");
						}}
					/>
				</div>
				<div className={style.flexItem}>
					<input
						onChange={handlePFPbackground}
						type="file"
						id="createpostimage"
						name="PFP"
						accept="image/*"
						style={{ display: "none" }}
					/>
					<label
						onClick={() => {
							setcontentTypeMinimal("picture");
						}}
						htmlFor="createpostimage"
					>
						<FontAwesomeIcon
							icon={faImage}
							fixedWidth
							className={
								contentTypeMinimal === "picture" ? style.selectItem : ""
							}
						/>
					</label>
				</div>
				<div className={style.flexItem2}>
					<Button
						onClick={onSubmit}
						text={props.postId ? "Reply" : "Post"}
						type="tertiary"
						size="small"
						roundness="very"
						style={{
							fontSize: "1.1rem",
							height: "45px",
							width: "85px",
							fontWeight: "bold",
						}}
					/>
				</div>
			</div>
		</div>
	);
};

export default CreatePost;
