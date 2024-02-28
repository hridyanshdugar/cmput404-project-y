"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Image from "next/image";
import styles from "./page.module.css";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { Col, Row } from "react-bootstrap";
import SinglePost from "@/components/singlepost";
import HomeSelector from "@/components/contentChoice";
import CreatePost from "@/components/createpost";
import React, {
	ChangeEvent,
	MouseEvent,
	useState,
	useContext,
	useEffect,
} from "react";
import { getHomePosts, API } from "@/utils/utils";
import Cookies from "universal-cookie";
import { PostContext } from "@/utils/postcontext";

export default function Home() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useContext(PostContext);

	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth");
		const user = cookies.get("user");
		setuser(user);
		setauth(auth);

		getHomePosts(user.host, page, size, auth, user.id)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data);

				setPosts(Data);
			})
			.catch(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
			});
	}, []);

	const updatePosts = (State: any) => {
		setPosts((posts: any[]) => [State, ...posts]);
		console.log(posts);
	};

	return (
		<div className={"main"}>
			<div className={styles.mainContentViewSticky}>
				<HomeSelector />
			</div>
			<div className={styles.mainContentView}>
				<CreatePost
					updatePosts={updatePosts}
					style={{
						border: "1px solid rgb(47, 51, 54)",
						paddingBottom: "10px",
						backgroundColor: "black",
					}}
				/>
				{posts.map((item: any, index: any) => (
                    <SinglePost
                        key={index}
						name={item.author.displayName}
						profileImage={API + item.author.profileImage}
						username={item.author.email}
						text={item.content}
						postImage={undefined}
						date={Math.floor(new Date(item.published).getTime() / 1000)}
						likes={0}
						retweets={0}
						comments={0}
						postID={item.id}
						contentType={item.contentType}
					/>
				))}
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
					date={1601508799}
					likes={35}
					retweets={3}
					comments={4}
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
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
					postID={"0"}
					contentType={"plain"}
				/>
			</div>
		</div>
	);
}
