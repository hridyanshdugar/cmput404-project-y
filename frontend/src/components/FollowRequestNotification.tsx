"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./singlepost.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import React from "react";
import Button from "./buttons/button";
import { processFollowRequest } from "@/utils/utils";
import Cookies from "universal-cookie";
import { getAPIEndpoint } from "@/utils/utils";

type Props = {
	name: string;
	profileImage: string;
	username: string;
};

const cookies = new Cookies();
const user = cookies.get("user");

export default class FollowRequestNotification extends React.Component<Props> {
	constructor(props: Props) {
		super(props);
	}

	render() {
		return (
			<div
				className={style.overflow}
			>
				<div className={style.blockImage}>
					<img
						className={style.img}
						src={getAPIEndpoint() + "/media/" + this.props.profileImage || ""}
						alt={""}
						width={40}
						height={40}
					/>
				</div>
				<div className={style.blockContent}>
					<div className={[style.topText, style.blockFlexContent].join(" ")}>
						<div className={style.topLeft}>
							<div className={style.inlineBlock}>{this.props.name}</div>
							<div className={[style.topUserText, style.inlineBlock].join(" ")}>
								{this.props.username}
							</div>
						</div>
						<div className={style.separator} />
						<div className={style.topRight}>
							<Button text="✓" type="primary" size="verySmall" roundness="very" onClick={() => processFollowRequest(user["email"], this.props.username, "accept")} style={{}}/>
							<Button text="⨉" type="primary" size="verySmall" roundness="very" onClick={() => processFollowRequest(user["email"], this.props.username, "decline")} style={{marginLeft:"10px"}}/>
					</div>
					</div>
					<div className={[style.topBottom].join(" ")}>
						Sent you a Follow Request!
					</div>
				</div>
			</div>
		);
	}
}
