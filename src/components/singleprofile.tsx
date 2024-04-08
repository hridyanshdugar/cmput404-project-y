"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./singleprofile.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import { faRepeat } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-regular-svg-icons";
import { faHeart } from "@fortawesome/free-regular-svg-icons";
import React, { useEffect, useState } from "react";
import { Badge, Card } from "react-bootstrap";
import Dropdown from "./dropdowns/dropdown";
import { getFrontend, navigate } from "../utils/utils";
import MarkdownPreview from "@uiw/react-markdown-preview";
import { deletePost, deleteComment } from "../utils/utils";
import Cookies from "universal-cookie";
import { useContext } from "react";
import { PostContext } from "../utils/postcontext";
import EditPopupPanel from "./editpopuppanel";


type Props = {
	name: string;
	profileImage: string;
	username: string;
	host: string;
	userId: string;
};

const SingleProfile: React.FC<Props> = (props) => {
	const onClickF = (event: React.MouseEvent<HTMLElement>) => {
			navigate("/profile/" + props.userId.split("/").slice(-1));
    };
    
	const [user, setuser] = useState<any>(null);
	useEffect(() => {
		const cookies = new Cookies();
		const user = cookies.get("user");
		setuser(user);
	}, []);

    return (
        <>

<div
			className={style.overflow}
			onClick={onClickF}
			style={{ cursor: "default" }}
            >
                <div className={style.blockImage}>
				<img
					id="profile6"
					className={style.img}
					src={props.profileImage}
					alt={""}
					width={40}
					height={40}
				/>
			</div>
			<div className={style.blockContent}>
				<div className={[style.topText, style.blockFlexContent].join(" ")}>
					<div className={style.topLeft} id="profile2">
						<div className={style.inlineBlock} id="profile3">
							{props.name}
						</div>
						<div
							id="profile4"
							className={[style.topUserText, style.inlineBlock].join(" ")}
						>
							{props.username}
                            </div>
                            <div id="profile99" className={[style.topUserText, style.inlineBlock].join(" ")}>
                                <Badge bg="primary">{props.host.split(".")[0].split("/").slice(-1)}</Badge>
                            </div>                            
					</div>
				</div>
			</div>
		</div>        
        </>
		
	);
};

export default SingleProfile;
