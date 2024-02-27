"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import SinglePost from '@/components/singlepost';

export default function Posts() {
    return (
      <>
            <div className={"main"}>
                <div className={styles.mainContentView}> 
                    MEDIA PAGE
                </div>                        
          </div>
      </>

  );
}
