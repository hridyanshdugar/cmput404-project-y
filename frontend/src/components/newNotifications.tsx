import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./contentChoice.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { Card, Form, InputGroup } from "react-bootstrap";

export default function NewNotifications() {
	return (
		<>
			<div className={style.blockContent}>
				<div className={style.flexContainer}>
					<div className={style.flexItem}>New Notifications!</div>
				</div>
			</div>
		</>
	);
}
