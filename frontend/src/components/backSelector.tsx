"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./backSelector.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { Card, Form, InputGroup } from "react-bootstrap";

interface BackSelectorProps {
	contentType: string;
}
const BackSelector: React.FC<BackSelectorProps> = (props) => {
	const onBackClick = () => {
		window.history.back();
	};
	return (
		<>
			<div className={style.blockContent}>
				<div className={style.flexContainer}>
					<FontAwesomeIcon
						icon={faArrowLeft}
						onClick={onBackClick}
						className={style.icon}
					/>
					<div>{props.contentType}</div>
				</div>
			</div>
		</>
	);
};

export default BackSelector;
