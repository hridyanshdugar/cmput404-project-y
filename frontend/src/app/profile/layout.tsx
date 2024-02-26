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
            <Profile/>
            {children}
        </div>
    );
  }