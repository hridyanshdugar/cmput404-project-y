"use strict";

import React, { useState, MouseEvent, forwardRef } from "react";
import style from "./popuppanel.module.css";
import Close from "@/components/buttons/close";
import CreatePost from "@/components/createpost";

interface PopupPanelProps {
	innerRef: React.RefObject<HTMLDivElement>;
	style: React.CSSProperties;
}
const PopupPanel: React.FC<PopupPanelProps> = (props) => {
	const onClose = () => {
		if (props.innerRef.current) {
			document.body.style.overflow = "auto"; // Bad
			props.innerRef.current.style.display = "none";
		}
	};
	return (
		<div className={style.overlay} ref={props.innerRef} style={props.style}>
			<div className={style.main}>
				<Close onClick={onClose} style={{ marginTop: 0 }} />
				<div className={style.paddedContainer}>
					<CreatePost
						profileImage={
							"https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg"
						}
						username={"@kolbyml"}
						style={{ borderBottom: "none" }}
					/>
				</div>
			</div>
		</div>
	);
};

export default PopupPanel;
