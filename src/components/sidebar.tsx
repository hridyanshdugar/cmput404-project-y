"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./sidebar.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome } from "@fortawesome/free-solid-svg-icons";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { faBell } from "@fortawesome/free-solid-svg-icons";
import { faPerson } from "@fortawesome/free-solid-svg-icons";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import PopupPanel from "./popuppanel";
import Cookies from "universal-cookie";
import { useEffect, useState } from "react";
import { useRef } from "react";
import { getAPIEndpoint, getFrontend, getMediaEndpoint } from "../utils/utils";
import { Spinner } from "react-bootstrap";

export default function SideBar() {
	const [userData, setUser] = useState<any>(null);
	const [popupOpen, setPopupOpen] = useState(false);

	useEffect(() => {
		const cookies = new Cookies();
		setUser(cookies.get("user"));
	}, []);

	const onPostClick = () => {
		document.body.style.overflow = "hidden";
		setPopupOpen(true);
	};

	return (
		<>
			{popupOpen && <PopupPanel setPopupOpen={setPopupOpen} />}
			<nav className={style.sidenav}>
				<ul>
					<li>
						<a className={style.logo} href="/home">
							𝕐
						</a>
					</li>
					<li>
						<a href="/home">
							<div className={style.inline}>
								<FontAwesomeIcon icon={faHome} inverse fixedWidth />
							</div>
							<div className={[style.inline, style.inlinetitle].join(" ")}>
								Home
							</div>
						</a>
					</li>
					<li>
						<a href="/explore">
							<div className={style.inline}>
								<FontAwesomeIcon icon={faSearch} inverse fixedWidth />
							</div>
							<div className={[style.inline, style.inlinetitle].join(" ")}>
								Explore
							</div>
						</a>
					</li>
					<li>
						<a href="/notifications">
							<div className={style.inline}>
								<FontAwesomeIcon icon={faBell} inverse fixedWidth />
							</div>
							<div className={[style.inline, style.inlinetitle].join(" ")}>
								Notifications
							</div>
						</a>
					</li>
					<li>
						<a href="/message">
							<div className={style.inline}>
								<FontAwesomeIcon icon={faEnvelope} inverse fixedWidth />
							</div>
							<div className={[style.inline, style.inlinetitle].join(" ")}>
								Messages
							</div>
						</a>
					</li>
					<li>
                        <a href={"/profile/" +  (userData ? userData.id : "null")}>
							<div className={style.inline}>
								<FontAwesomeIcon icon={faPerson} inverse fixedWidth />
							</div>
							<div className={[style.inline, style.inlinetitle].join(" ")}>
								Profile
							</div>
						</a>
					</li>
					<li>
						<a className={style.post} onClick={() => onPostClick()}>
							<div className={style.postButtonBig}>
								<button>Post</button>
							</div>
							<div className={style.postButtonSmall}>
								<button>
									<FontAwesomeIcon icon={faPen} inverse fixedWidth />
								</button>
							</div>
						</a>
					</li>
				</ul>
				<div className={style.avatarBottom}>
                    <a href="/settings">
                        {
                            userData ? <>
                            
                                <img
                                    src={getMediaEndpoint() + userData?.profileImage?.split("?")[0] || ""}
                                    className={style.avatarImage}
                                    style={{ verticalAlign: "-10%" }}
                                ></img>
                                <div className={style.myName}>
                                    <div>{`${userData?.displayName}`}</div>
                                    <div className={style.atNameText}>{`${userData?.email}`}</div>
                                </div>
                                <div className={style.dotdotdoticon}>
                                    <FontAwesomeIcon icon={faEllipsis} inverse fixedWidth />
                                </div>                            
                            
                            </>
                        :     <Spinner animation="border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </Spinner>
                        }

					</a>
				</div>
			</nav>
		</>
	);
}
