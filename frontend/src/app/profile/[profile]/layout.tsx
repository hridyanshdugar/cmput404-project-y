"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { title } from 'process';
import Profile from "@/components/profile";
import SideBar from "@/components/sidebar";
import Rightbar from "@/components/rightbar";
import Cookies from 'universal-cookie';
import { useState, useEffect } from 'react';
import { getUserLocalInfo, navigate, API} from '@/utils/utils';
import { error } from 'console';
import { userInfo } from 'os';


export default function ProfileLayout({
    children,
    params,
  }: {
    children: React.ReactNode;
    params: { profile: string };
  }) {

    const userId = params.profile;
    let activeUser: boolean = false;

    const cookies = new Cookies()
    const allcookies = cookies.getAll()
    if (allcookies.auth && allcookies.user) {
        //!!Change to userName when added!!//
        const userIdCookie = cookies.get("user").id
        if (userId == userIdCookie) {
            activeUser = true;
        }
    }

    const [userInformation, setUserInformation] = useState<any>(null);
    
    useEffect(() => {

      getUserLocalInfo(allcookies.auth, userId).then((result) => {
          if (result.status == 200) {
              return result.json();
          }
          else {
              navigate('/');
          }
      }).catch((error) => {
          console.log(error);
          navigate('/');
      }).then((data) => {
          setUserInformation(data);
          //console.log(data);
      });
    }, []);

    if (!userInformation) {
      return (<div>
        <SideBar/>
        <Rightbar/>
        </div>);
    }

    console.log(userInformation);


    //Query username
    //If username not in database, return 404 / user not found page

    return (
        <div>
            <SideBar/>
            <Profile 
            userid={userId}
            name={userInformation?.displayName} 
            username={'@' + userInformation?.email} 
            bio={userInformation?.bio? userInformation?.bio : 'No Bio'}
            website={userInformation?.github? userInformation?.github : 'No Website'} 
            dateJoined={''} 
            followers={0} 
            following={0} 
            activeUser={activeUser} 
            profileImage={userInformation?.profileImage || ""} 
            profileBackround={userInformation?.profileBackgroundImage || ""}/>
            {children}
            <Rightbar/>
        </div>
    );
  }