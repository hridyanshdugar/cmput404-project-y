import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./contentChoice.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { Button, Card, Form, InputGroup } from "react-bootstrap";

export default function HomeSelector({handleSectionChange} : {handleSectionChange: (section: string) => void}) {
	return (
		<>
			<div className={style.blockContent}>
				<div className={style.flexContainer}>
					<Button onClick={() => handleSectionChange("forYou")} className={style.flexItem}><span>For you</span></Button>
					<Button onClick={() => handleSectionChange("following")} className={style.flexItem}><span>Following</span></Button>
				</div>
			</div>
		</>
	);
}
