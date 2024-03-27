"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import { NewNotifications, NoNewNotifications } from "../components/newNotifications";
import FollowRequestNotification from "../components/FollowRequestNotification";
import { getInbox } from "../utils/utils";
import Cookies from "universal-cookie";
import { useEffect, useState } from "react";

export default function Notifications() {
  const [requests, setRequests] = useState<any>([]); 
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [auth, setAuth] = useState<string>("");

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
    setAuth(auth);
    const user = cookies.get("user");
    
    getInbox(user.id, auth)
    .then(async (result: any) => {
      if (result.status === 200) {
        const Data = await result.json();
        console.log("Inbox");
        console.log(Data);
        setRequests(Data["requests"]);
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
                {! isLoading ? 
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
                (<></>)
                }
                {/* <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} /> */}
              </div>
            </div>
  );
}
