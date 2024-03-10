"use strict";

import React, { useState, useContext } from "react";
import style from "./popuppanel.module.css";
import Close from "./buttons/close";
import CreatePost from "./createpost";
import { PostContext } from "../utils/postcontext";

interface PopupPanelProps {
	setPopupOpen: React.Dispatch<React.SetStateAction<boolean>>;
	style?: React.CSSProperties;
}

const PopupPanel: React.FC<PopupPanelProps> = (props) => {
	const [posts, setPosts] = useContext(PostContext);
	const onClose = () => {
		document.body.style.overflow = "auto"; // Bad
		props.setPopupOpen(false);
	};
	const updatePosts = (State: any) => {
		setPosts((posts: any[]) => [State, ...posts]);
		console.log(posts);
	};
	return (
		<div className={style.overlay} style={props.style}>
			<div className={style.main}>
				<Close onClick={onClose} style={{ marginTop: 0 }} />
				<div className={style.paddedContainer}>
					<CreatePost
						updatePosts={updatePosts}
						style={{ borderBottom: "none" }}
						setPopupOpen={props.setPopupOpen}
					/>
				</div>
			</div>
		</div>
	);
};

export default PopupPanel;
