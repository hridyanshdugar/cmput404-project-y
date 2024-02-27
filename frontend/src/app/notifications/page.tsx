"use client";
import "bootstrap/dist/css/bootstrap.min.css";
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import NewNotifications from "@/components/newNotifications";
import FollowRequestNotification from "@/components/FollowRequestNotification";
export default function Notifications() {
    return (
            <div className={"main"}>   
              <div className={styles.mainContentViewSticky}>
                  <NewNotifications />
              </div>
              <div className={styles.mainContentView}>
                  <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} />
                  <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} />
                  <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} />
                  <FollowRequestNotification name={'Kolby'} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} username={'@kolbyml'} />
              
              </div>
            </div>
  );
}
