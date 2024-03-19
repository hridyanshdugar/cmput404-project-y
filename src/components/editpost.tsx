"use strict";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./editpost.module.css";
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
	EditPost,
	getMediaEndpoint,
	getPost,
	imageUploadHandler,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { Card } from "react-bootstrap";
import MDEditor from "@uiw/react-md-editor";

interface EditPostProps {
	postId: string;
	style?: React.CSSProperties;
	setPopupOpen?: React.Dispatch<React.SetStateAction<boolean>>;
}

const EditPostt: React.FC<EditPostProps> = (props) => {
	const dropdownRef = useRef<HTMLDivElement>(null);
	const horizontalLineRef = useRef<HTMLHRElement>(null);

	const [content, setcontent] = useState<string>("");
	const [visibility, setvisibility] = useState<string>("Everyone");

	const cookies = new Cookies();
	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const [markdownValue, setMarkdownValue] = useState<string | undefined>("");

	const [PFPbackground, setPFPbackground] = useState<File | null>(null);
	const [PFPbackgroundurl, setPFPbackgroundurl] = useState<string>("");

	const [postInformation, setPostInformation] = useState<any>(null);
	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		setuser(user);
		setauth(auth);
		getPost(auth, props.postId)
			.then((result) => {
				if (result.status == 200) {
					return result.json();
				} else {
					//   navigate('/');
				}
			})
			.catch((error) => {
				console.log(error);
				//   navigate('/');
			})
			.then((data) => {
				setPostInformation(data);
				console.log(data);
				setcontent(data.content);
				setMarkdownValue(data.content);
				setPFPbackgroundurl(data.content);
			});
	}, []);

	const handlePFPbackgroundf = (event: ChangeEvent<HTMLInputElement>) => {
		console.log("1start");
		if (event.target.files && event.target.files[0]) {
			const file = event.target.files[0];
			setPFPbackground(file);

			const fileReader = new FileReader();
			console.log("start");
			fileReader.onload = () => {
				setPFPbackgroundurl(fileReader.result as string);
				console.log(fileReader.result);
				console.log("bob");
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
		if (dropdownRef.current && horizontalLineRef.current) {
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
		const VisibilityMap: { [key: string]: string } = {
			Everyone: "PUBLIC",
			Unlisted: "UNLISTED",
			Friends: "FRIENDS",
		};
		var contentToSend: string = "";
		var contentTypeF: string = "";
		if (postInformation?.contentType.includes("image")) {
			contentTypeF =
				PFPbackgroundurl?.split("base64")[0]?.split("data:")[1] + "base64";
			contentToSend = PFPbackgroundurl;
		} else if (postInformation?.contentType === "text/markdown") {
			contentToSend = markdownValue!;
		} else {
			contentToSend = content;
		}
		EditPost(
			{
				content: contentToSend,
				visibility: VisibilityMap[visibility],
				contentType: postInformation?.contentType.includes("image")
					? contentTypeF
					: postInformation?.contentType,
			},
			auth.access,
			postInformation?.id
		)
			.then(async (result: any) => {
				const Data = await result.json();
				window.location.reload();
			})
			.catch(async (result: any) => {
				const Data = await result?.json();
				console.log(Data);
			});
	};
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
					{postInformation?.contentType === "text/plain" ? (
						<textarea
							value={content}
							className={style.textarea}
							placeholder="What is happening?!"
							onChange={onTextChange}
						></textarea>
					) : (
						""
					)}

					{postInformation?.contentType.includes("image") ? (
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

					{postInformation?.contentType === "text/markdown" ? (
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
				{postInformation?.contentType.includes("image") ? (
					<>
						<div className={style.flexItem}>
							<input
								onChange={handlePFPbackgroundf}
								type="file"
								id="editpostimage"
								name="PFP"
								accept="image/*"
								style={{ display: "none" }}
							/>
							<label htmlFor="editpostimage">
								<FontAwesomeIcon icon={faImage} fixedWidth />
							</label>
						</div>
					</>
				) : (
					""
				)}
				<div className={style.flexItem2}>
					<Button
						onClick={onSubmit}
						text={"Edit"}
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

export default EditPostt;
