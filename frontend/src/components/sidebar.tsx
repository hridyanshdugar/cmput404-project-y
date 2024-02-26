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
import PopupPanel from "@/components/popuppanel";
import { useRef } from "react";

export default function SideBar() {
	const popupPanelRef = useRef<HTMLDivElement>(null);
	const onPostClick = () => {
		if (popupPanelRef.current) {
			document.body.style.overflow = "hidden"; // Bad
			popupPanelRef.current.style.display = "block";
		}
	};
	return (
		<>
			<PopupPanel innerRef={popupPanelRef} style={{ display: "none" }} />
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
						<a href="/notification">
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
						<a href="/profile">
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
						<div className={style.avatarImage}></div>
						<div className={style.myName}>
							<div>John Dowe</div>
							<div className={style.atNameText}>@beacon</div>
						</div>
						<div className={style.dotdotdoticon}>
							<FontAwesomeIcon icon={faEllipsis} inverse fixedWidth />
						</div>
					</a>
				</div>
			</nav>
		</>
	);
}
