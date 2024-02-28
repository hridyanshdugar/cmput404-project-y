"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row, Spinner } from 'react-bootstrap';
import { useRouter } from 'next/router';
import Profile from "@/components/profile";
import SinglePost from '@/components/singlepost';
import React, { useContext, useEffect, useState } from 'react';
import { PostContext } from '@/utils/postcontext';
import { getAPIEndpoint, getHomePosts } from '@/utils/utils';
import Cookies from 'universal-cookie';

export default function Posts({ params }: { params: { profile: string } }) {

    const username = params.profile;


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
				console.log(result);
			});
	}, []);

    return (
        <>
            <div className={"main"}>
                <div className={styles.mainContentView}> 
                    {posts ? posts.length === 0 ? <>There are no posts avaliable</> : posts.map((item: any, index: any) => (
                    item.author.id === username ?
                    <SinglePost
                        key={index}
                        name={item.author.displayName}
                        userId={item.author.id}
						profileImage={getAPIEndpoint() + item.author.profileImage}
						username={item.author.email}
						text={item.content}
						postImage={undefined}
						date={Math.floor(new Date(item.published).getTime() / 1000)}
						likes={0}
						retweets={0}
						comments={0}
						postID={item.id}
						contentType={item.contentType}
					/> : <></>
				)) : <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>}                </div>                        
          </div>
      </>

  );
}
