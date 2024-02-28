"use client";
import "@fortawesome/fontawesome-svg-core/styles.css";
import style from "./singlepost.module.css";
import Image from "next/image";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import { faRepeat } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-regular-svg-icons";
import { faHeart } from "@fortawesome/free-regular-svg-icons";
import React from "react";
import { Card } from "react-bootstrap";
import Dropdown from "@/components/dropdowns/dropdown";
import { navigate } from "@/utils/utils";
import MarkdownPreview from '@uiw/react-markdown-preview';

export function TimeConverter(date: Date) {
	var now = new Date();
	var seconds = (now.getTime() - date.getTime()) / 1000;
	var minutes = (now.getTime() - date.getTime()) / 1000 / 60;
	var hours = (now.getTime() - date.getTime()) / 1000 / 60 / 24;
	if (seconds <= 60) {
		return <>{Math.round(seconds)}s</>;
	} else if (minutes <= 60) {
		return <>{Math.round(minutes)}m</>;
	} else if (hours <= 24) {
		return <>{Math.round(hours)}h</>;
	} else {
		const months = [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		];
		if (date.getFullYear() === now.getFullYear()) {
			return (
				<>
					{months[date.getMonth()]} {date.getDay()}
				</>
			);
		}
		return (
			<>
				{months[date.getMonth()]} {date.getDay()}, {date.getFullYear()}
			</>
		);
	}
}

type Props = {
	name: string;
	profileImage: string;
	username: string;
	text: string;
	postImage: string | undefined;
	date: number;
	likes: number;
	retweets: number;
	comments: number;
	postID: string;
	onPostPage?: boolean | undefined;
	contentType: string;
};

export default class SinglePost extends React.Component<Props> {
	constructor(props: Props) {
		super(props);
	}

	render() {
		const onClick = () => {
			if (!this.props.onPostPage) {
				navigate("/post/" + this.props.postID);
			}
		};

		const onPostOptionSelect = (selection: string | null) => {
			if (selection === "Delete") {
				console.log("delete");
			} else if (selection === "Edit") {
				console.log("edit");
			}
		};

		const date = new Date(0);
		date.setUTCSeconds(this.props.date);
		return (
			<div
				className={style.overflow}
				onClick={onClick}
				style={{ cursor: this.props.onPostPage ? "default" : "pointer" }}
			>
				<div className={style.blockImage}>
					<img
						className={style.img}
						src={this.props.profileImage}
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
							<div className={[style.topUserText, style.inlineBlock].join(" ")}>
								{" "}
								· {TimeConverter(date)}
							</div>
						</div>
						<div className={style.separator} />
						<div>
							<Dropdown
								icon={faEllipsis}
								options={["Delete", "Edit"]}
								onChange={onPostOptionSelect}
							/>
						</div>
                    </div>
                    {
                        this.props.contentType.includes("image") ? <Card className="bg-dark text-white">
                        <Card.Img src={this.props.text} alt="Card image" />
                    </Card> : <></>

                    }
                    {
                        this.props.contentType === "text/markdown" ? <MarkdownPreview source={this.props.text} className={style.markdownColor}/> : <></>

                    }
                    {
                        this.props.contentType === "text/plain" ? <div className={style.topBottom}>{this.props.text}</div> : <></>

                    }                    
					<div>
						{this.props.postImage && (
							<Card className="bg-dark text-white">
								<Card.Img src={this.props.postImage} alt="Card image" />
							</Card>
						)}
					</div>
					<div className={style.flexContainer}>
						<div className={style.flexItem}>
							<FontAwesomeIcon icon={faComment} fixedWidth />{" "}
							{this.props.comments}
						</div>
						<div className={style.flexItem}>
							<FontAwesomeIcon icon={faRepeat} fixedWidth />{" "}
							{this.props.retweets}
						</div>
						<div className={style.flexItem}>
							<FontAwesomeIcon icon={faHeart} fixedWidth /> {this.props.likes}
						</div>
						<div className={style.flexItem2}>
							<FontAwesomeIcon icon={faArrowUpFromBracket} fixedWidth />
						</div>
					</div>
				</div>
			</div>
		);
	}
}
