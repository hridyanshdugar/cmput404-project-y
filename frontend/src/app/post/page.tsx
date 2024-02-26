"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Image from "next/image";
import style from "./page.module.css";
import BackSelector from "@/components/backSelector";
import CreatePost from "@/components/createpost";
import SinglePost from "@/components/singlepost";

export default function Home() {
	return (
		<div className={"main"}>
			<div className={style.mainContentViewSticky}>
				<BackSelector contentType={"Post"} />
			</div>
			<div className={style.mainContentView}>
				<SinglePost
					name={"Kolby"}
					profileImage={
						"https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg"
					}
					username={"@kolbyml"}
					text={
						"What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, "
					}
					postImage={undefined}
					date={1601408799}
					likes={35}
					retweets={3}
					comments={4}
					postID={0}
					onPostPage={true}
				/>
				<CreatePost
					profileImage={
						"https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg"
					}
					username={"@kolbyml"}
					reply={true}
				/>
				<SinglePost
					name={"Kolby"}
					profileImage={
						"https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg"
					}
					username={"@kolbyml"}
					text={
						"What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, "
					}
					postImage={
						"https://i0.wp.com/www.thewrap.com/wp-content/uploads/2023/06/spider-man-across-the-spider-verse-group-shot.jpg?fit=990%2C557&ssl=1"
					}
					date={1601408799}
					likes={35}
					retweets={3}
					comments={4}
					postID={0}
				/>
				<SinglePost
					name={"Kolby"}
					profileImage={
						"https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg"
					}
					username={"@kolbyml"}
					text={
						"What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, "
					}
					postImage={undefined}
					date={1601408799}
					likes={35}
					retweets={3}
					comments={4}
					postID={0}
				/>
			</div>
		</div>
	);
}
