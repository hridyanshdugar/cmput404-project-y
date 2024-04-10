"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { Col, Row, Spinner } from "react-bootstrap";
import SinglePost from "../components/singlepost";
import HomeSelector from "../components/contentChoice";
import CreatePost from "../components/createpost";
import React, {
	ChangeEvent,
	MouseEvent,
	useState,
	useContext,
	useEffect,
} from "react";
import {
	getAPIEndpoint,
	getFrontend,
	getMediaEndpoint,
    getRemoteUsers,
	navigate
} from "../utils/utils";
import Cookies from "universal-cookie";
import { PostContext } from "../utils/postcontext";
import SingleProfile from "../components/singleprofile";

export default function Home() {
	const [page, setPage] = useState<number>(1);
	const [size, setSize] = useState<number>(100); // Temporary

	const [posts, setPosts] = useContext(PostContext);

	const [user, setuser] = useState<any>(null);
	const [auth, setauth] = useState<any>(null);

	useEffect(() => {
		const cookies = new Cookies();
		const authCookie = cookies.get("auth");
		const userCookie = cookies.get("user");
		if (!authCookie || !userCookie || !authCookie.access || !userCookie.id) {
			navigate("/");
		}
		const auth = authCookie.access;
		const user = userCookie;
		setuser(user);
		setauth(auth);

		fetchContent(auth);
	}, []);

	const fetchContent = (
		auth: string,
	) => {
        getRemoteUsers(auth)
            .then(async (result: any) => {
                const Data = await result.json();
                setPosts(Data);
            })
            .catch(async (result: any) => {
                const Data = await result.json();
                console.log("getRemoteUsers failed", Data);
            });
	};

	return (
		<div className={"main"}>
			<div className={styles.mainContentView}>
				{ posts ? (
					posts.length === 0 ? (
						<div>There are no profiles available</div>
					) : (
						posts.map((item: any, index: any) => (
                            <SingleProfile
                            key={index}
								name={item.displayName}
								userId={item.id}
								profileImage={
									item.profileImage?.split("?")[0]
								}
								username={item.displayName}
								host={item.host}
							/>
						))
					)
				) : (
					<Spinner animation="border" role="status">
						<span className="visually-hidden">Loading...</span>
					</Spinner>
				)}
			</div>
		</div>
	);
}
