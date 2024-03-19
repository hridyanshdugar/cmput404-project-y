"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import { NewNotifications, NoNewNotifications } from "../components/newNotifications";
import FollowRequestNotification from "../components/FollowRequestNotification";
import { getNewFollowRequests } from "../utils/utils";
import Cookies from "universal-cookie";
import { useEffect, useState } from "react";

export default function Notifications() {
  const [requests, setRequests] = useState<any>([]); 
  const [isLoading, setIsLoading] = useState<boolean>(true);

	useEffect(() => {
		const cookies = new Cookies();
		const auth = cookies.get("auth")["access"];
		const user = cookies.get("user");
    getNewFollowRequests(user.email)
      .then((res: any) => {
        return res.json();
      }).then((data)=>{
        setRequests(data);
        setIsLoading(false);
      })
      .catch((err)=> {
        console.log(err);
      })
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
                          name={request["displayName"]} 
                          profileImage={request["profileImage"]} 
                          username={request["email"]} />
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
