"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import { NewNotifications, NoNewNotifications } from "../components/newNotifications";
import FollowRequestNotification from "../components/FollowRequestNotification";
import { getInbox, navigate } from "../utils/utils";
import Cookies from "universal-cookie";
import { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";

export default function Notifications() {
  const [requests, setRequests] = useState<any>(null); 
  const [auth, setAuth] = useState<string>("");

	useEffect(() => {
		const cookies = new Cookies();
    const authCookie = cookies.get("auth");
		const userCookie = cookies.get("user");
		if (!authCookie || !userCookie || !authCookie.access || !userCookie.id) {
			navigate("/");
		}
		const auth = authCookie.access;
		const user = userCookie;
    setAuth(auth);
    
    getInbox(user.id, auth)
    .then(async (result: any) => {
      if (result.status === 200) {
        const Data = await result.json();
        console.log("Inbox");
        console.log(Data);
        setRequests(Data["followRequest"]);
        console.log("requests (male chicken)", requests)
      } else {
        throw new Error("Error fetching inbox");
      }
    }).catch(error => {
      console.log(error);
    });    
	}, []);

    return (
            <div className={"main"}>   
              <div className={styles.mainContentViewSticky}>
                  <NewNotifications />
              </div>
              <div className={styles.mainContentView}>
                { requests ? 
                    ( requests.length == 0 ? 
                      (<NoNewNotifications />) : 
                      (
                        requests.map((request: any, index: any) => (
                            <FollowRequestNotification 
                            key={index}
                            auth={auth}
                          actor={request["actor"]} 
                          object={request["object"]} />
                        ))
                      )
                    )
                :
                (					<Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>)
                }
                {/* <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} /> */}
              </div>
            </div>
  );
}
