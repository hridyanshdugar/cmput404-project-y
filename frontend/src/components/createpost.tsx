"use strict";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./createpost.module.css";
import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faImage } from "@fortawesome/free-regular-svg-icons";
import React, { ChangeEvent, MouseEvent, useState, useRef } from "react";
import Dropdown from "@/components/dropdowns/dropdown";
import Button from "@/components/buttons/button";

interface CreatePostProps {
	profileImage: string;
	username: string;
	style?: React.CSSProperties;
}

const CreatePost: React.FC<CreatePostProps> = (props) => {
	const dropdownRef = useRef<HTMLDivElement>(null);
	const horizontalLineRef = useRef<HTMLHRElement>(null);

	const onTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
		event.target.style.height = "auto";
		event.target.style.height = event.target.scrollHeight + "px";
	};

	const onCreateClick = (event: MouseEvent<HTMLDivElement>) => {
		if (dropdownRef.current && horizontalLineRef.current) {
			dropdownRef.current.style.display = "flex";
			horizontalLineRef.current.style.display = "block";
		}
	};

	return (
		<div
			className={style.createPost}
			onClick={onCreateClick}
			style={props.style}
		>
			<div className={style.blockImage}>
				<Image
					className={style.img}
					src={props.profileImage}
					alt={""}
					width={40}
					height={40}
				/>
			</div>
			<div className={style.blockContent}>
				<Dropdown
					label="Everyone"
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
						onClick={() => {}}
						text="Post"
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
