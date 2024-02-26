"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { title } from 'process';
import Profile from "@/components/profile";


export default function ProfileLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (
        <div>
            <Profile name={'John Dowe'} username={'@beacon'} bio={'bio'} website={'website'} dateJoined={''} followers={0} following={0} profileImage={'https://image.spreadshirtmedia.com/image-server/v1/products/T1459A839PA3861PT28D1031336018W5625H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/gamer-sticker.jpg'} profileBackround={"https://i0.wp.com/www.thewrap.com/wp-content/uploads/2023/06/spider-man-across-the-spider-verse-group-shot.jpg?fit=990%2C557&ssl=1"}/>
            {children}
        </div>
    );
  }