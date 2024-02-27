"use strict";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./createpost.module.css";
import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faImage } from "@fortawesome/free-regular-svg-icons";
import React, { ChangeEvent, MouseEvent, useState, useRef, useEffect } from "react";
import Dropdown from "@/components/dropdowns/dropdown";
import Button from "@/components/buttons/button";
import { createPost, API, getHomePosts } from "@/utils/utils"
import Cookies from 'universal-cookie';

interface CreatePostProps {
	style?: React.CSSProperties;
	reply?: boolean | undefined;
	updatePosts: (State: any) => void;
}

const CreatePost: React.FC<CreatePostProps> = (props) => {
	const dropdownRef = useRef<HTMLDivElement>(null);
	const horizontalLineRef = useRef<HTMLHRElement>(null);

	const [contentType, setcontentType] = useState<string>('text/plain');
	const [title, settitle] = useState<string>('');
	const [description, setdescription] = useState<string>('');
	const [content, setcontent] = useState<string>('');
	const [visibility, setvisibility] = useState<string>("Everyone");

	const cookies = new Cookies();
	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth");
		const user = cookies.get("user");
		setuser(user);
		setauth(auth);
	  }, []);


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
		if (dropdownRef.current && horizontalLineRef.current && !props.reply) {
			dropdownRef.current.style.display = "flex";
			horizontalLineRef.current.style.display = "block";
		}
	};

	const onSubmit = () => {
		const VisibilityMap: { [key: string]: string } = {
			"Everyone": "PUBLIC", 
			"Friends":"FRIENDS", 
			"Unlisted": "UNLISTED"
		};
		createPost(title,description,contentType,content,VisibilityMap[visibility],auth,user.id).then(async (result:any) => {
			const Data = await result.json();
			console.log(Data);
			if (VisibilityMap[visibility] == "PUBLIC") {
				props.updatePosts(Data);
			};
		}).catch(async (result: any) => {
			const Data = await result.json();
			console.log(Data);
			
		})
	};
	// src={`${pfp ? API + pfp : ''}`}
	return (
		<div
			className={style.createPost}
			onClick={onCreateClick}
			style={props.style}
		>
			<div className={style.blockImage}>
				<img
					className={style.img}
					src={`${user ? API + user.profileImage : ''}`}
					style={{ width:"40px", height: "40px" }}
				/>
			</div>
			<div className={style.blockContent}>
				<Dropdown
					label="Everyone"
					onChange={handleVisibilityChange}
					options={["Everyone", "Friends", "Unlisted"]}
					innerRef={dropdownRef}
					styles={{ display: "none" }}
				/>
				<textarea
					className={style.textarea}
					placeholder="What is happening?!"
					onChange={onTextChange}
				></textarea>
				<hr
					className={style.horizontalLine}
					ref={horizontalLineRef}
					style={{ display: "none" }}
				></hr>
				<div className={style.bottomBar}>
					<div className={style.iconBar}>
						<FontAwesomeIcon icon={faImage} />
					</div>
					<Button
						onClick={onSubmit}
						text={props.reply ? "Reply" : "Post"}
						type="tertiary"
						size="small"
						roundness="very"
						style={{ fontSize: "1.5vh" }}
					/>
				</div>
			</div>
		</div>
	);
};

export default CreatePost;
