"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import { Col, Row, Spinner } from "react-bootstrap";
import Profile from "../components/profile";
import SinglePost from "../components/singlepost";
import React, { useContext, useEffect, useState } from "react";
import { PostContext } from "../utils/postcontext";
import {
	getAPIEndpoint,
	getFrontend,
	getAuthorPosts,
	getMediaEndpoint,
} from "../utils/utils";
import Cookies from "universal-cookie";
import { useOutletContext, useParams } from "react-router-dom";

export default function Profiles() {
	const outletObject = useOutletContext<any>();

	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useState<any>([]);

	const [userId, setUserId] = useState<any>(null);
	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	const currentUrl = window.location.href;

	const id = currentUrl.split("/").pop() || '';

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
		console.log("TESTED CHANGE");
		setUserId(outletObject.userId);
		setuser(user);
		setauth(auth);

		getAuthorPosts(user.host, page, size, auth, id)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data);
				setPosts(Data);
			})
			.catch(async (result: any) => {
				console.log(result);
			});
	}, []);

	return (
		<>
			<div className={"main"}>
				<div className={styles.mainContentView}>
					{posts ? (
						posts.length === 0 ? (
							<>There are no posts available</>
						) : (
							posts.map((item: any, index: any) =>
								true ? (
									<SinglePost
									post2={item}
										author={item.author}
										key={index}
										name={item.author.displayName}
										userId={item.author.id}
										profileImage={
											getMediaEndpoint() +
											item.author.profileImage?.split("?")[0]
										}
										username={item.author.displayName}
										text={item.content}
										postImage={undefined}
										date={Math.floor(new Date(item.published).getTime() / 1000)}
										likes={item.likes}
										comments={item.count}
                                        postId={item.id}
                                        host={item.author.host}
										contentType={item.contentType}
									/>
								) : (
									<></>
								)
							)
						)
					) : (
						<Spinner animation="border" role="status">
							<span className="visually-hidden">Loading...</span>
						</Spinner>
					)}{" "}
				</div>
			</div>
		</>
	);
}
