"use client"
import React, { useState,useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Col, Row } from 'react-bootstrap';
import { saveSettings, getUserLocalInfo, navigate } from "@/utils/utils";
import Cookies from 'universal-cookie';

export default function Home() {
  const cookies = new Cookies();
  const [WarningData, setWarningData] = useState<any>(null);

  const [Name, setName] = useState<string>('');
  const [Github, setGithub] = useState<string>('');
  const [PFP, setPFP] = useState<string>('');

  useEffect(() => {
    const auth = cookies.get("auth")["access"];
    const id = cookies.get("user")["id"];
    getUserLocalInfo(auth, id).then(async (result:any) => {
      const Data = await result.json();
      console.log(Data,Data?.displayName);

      setName(Data?.displayName || '');
      setGithub(Data?.github || '');
      setPFP(Data?.profileImage || '');
    }).catch(async (result: any) => {
      const Data = await result.json();
      console.log(Data);
      setWarningData({title: Data?.title, message: Data?.message});
    })
  }, []);

  const handleName = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value);
  };
  const handleGithub = (event: React.ChangeEvent<HTMLInputElement>) => {
    setGithub(event.target.value);
  };
  const handlePFP = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPFP(event.target.value);
  };

  const handleSave = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    const auth = cookies.get("auth")["access"];
    const id = cookies.get("user")["id"];
    saveSettings(Name,Github,PFP,auth,id).then(async (result:any) => {
      console.log("Ran");
      navigate('/home');
    }).catch(async (result: any) => {
      const Data = await result.json();
      console.log(Data);
      setWarningData({title: Data?.title, message: Data?.message});
    })
  };

    return (
      <>
            <div className={"main"}>
                <div className={styles.mainContentView}>  
                  <div className={styles.container}>
                    <h1 className={styles.title}>Settings</h1>
                    <header className={styles.header}>Edit Account Details:</header>
                    <form>
                        <label className={styles.form}>Name
                          <input className={styles.input} value={Name} onChange={handleName} type="text" id="name" name="name" placeholder="Enter your name" required></input>
                        </label>
                        <label className={styles.form}>Github
                          <input className={styles.input} value={Github} onChange={handleGithub} type="text" id="github" name="github" placeholder="Enter your github" required></input>
                        </label>
                        <label className={styles.form}>PFP
                          <input className={styles.input} value={PFP} onChange={handlePFP} type="text" id="PFP" name="PFP" placeholder="Enter your PFP"></input>
                        </label>

                        <input className={styles.submit} onClick={handleSave} type="submit" value="Save"></input>
                    </form>
                  </div> 
                </div>                       
          </div>
      </>

  );
}
