import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./contentChoice.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { Button, Card, Form, InputGroup } from "react-bootstrap";
import { useState } from "react";

export default function HomeSelector({ handleSectionChange }: { handleSectionChange: (section: string) => void }) {
    const [page, setPage] = useState<boolean>(true);

    function helper(state: string) {
		setPage(state === "forYou")
        handleSectionChange(state)
    }
	return (
		<>
			<div className={style.blockContent}>
				<div className={style.flexContainer}>
					<Button onClick={() => helper("forYou")} className={ page ? [style.flexItem, style.boby].join(" ") : style.flexItem}><span>For you</span></Button>
					<Button onClick={() => helper("following")} className={ page ? style.flexItem : [style.flexItem, style.boby].join(" ")}><span>Following</span></Button>
				</div>
			</div>
		</>
	);
}
