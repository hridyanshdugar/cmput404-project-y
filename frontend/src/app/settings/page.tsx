"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';

export default function Settings() {
    return (
      <>
            <div className={"main"}>
                <div className={styles.mainContentView}>  
                  <div className={styles.container}>
                    <h1 className={styles.title}>Settings</h1>
                    <header className={styles.header}>Edit Account Details:</header>
                    <form>
                        <label className={styles.form}>Name
                          <input className={styles.input} type="text" id="name" name="name" placeholder="Enter your name" required></input>
                        </label>
                        <label className={styles.form}>Username
                          <input className={styles.input} type="text" id="username" name="username" placeholder="Enter your username" required></input>
                        </label>
                        <label className={styles.form}>Bio
                          <input className={styles.input} type="text" id="bio" name="bio" placeholder="Enter your bio"></input>
                        </label>
                        <label className={styles.form}>Website
                          <input className={styles.input} type="text" id="website" name="website" placeholder="Enter your website"></input>
                        </label>

                        <input className={styles.submit} type="submit" value="Save"></input>
                    </form>
                  </div> 
                </div>                       
          </div>
      </>

  );
}
