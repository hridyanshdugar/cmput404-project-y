"use strict";

import React, { useState, useContext } from "react";
import style from "./popuppanel.module.css";
import Close from "./buttons/close";
import { PostContext } from "../utils/postcontext";
import EditPostt from "./editpost";

interface PopupPanelProps {
	setPopupOpen: React.Dispatch<React.SetStateAction<boolean>>;
    style?: React.CSSProperties;
    postId: string;
}

const EditPopupPanel: React.FC<PopupPanelProps> = (props) => {
	const onClose = () => {
		document.body.style.overflow = "auto"; // Bad
		props.setPopupOpen(false);
	};
	return (
		<div className={style.overlay} style={props.style}>
			<div className={style.main}>
				<Close onClick={onClose} style={{ marginTop: 0 }} />
				<div className={style.paddedContainer}>
					<EditPostt
                        style={{ borderBottom: "none" }}
                        setPopupOpen={props.setPopupOpen}
                        postId={props.postId} />
				</div>
			</div>
		</div>
	);
};

export default EditPopupPanel;
