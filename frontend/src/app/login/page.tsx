'use client';
import React, { useState } from 'react';
import styles from "./page.module.css";
import closeIcon from "@/assets/close.svg"
import { login } from "@/utils/utils";
import Button from "@/components/buttons/button";
import Close from "@/components/buttons/close";
import Input from "@/components/inputs/input";
import { useRouter } from 'next/navigation'; 
import Cookies from 'universal-cookie';

export default function Home() {
  const router = useRouter();

  const [Email, setEmail] = useState<string>('');
  const [Password, setPassword] = useState<string>('');

  const handleEmail = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePassword = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };


  const handleLogin = async () => {
    login(Email,Password).then(async (result:any) => {
      const cookies = new Cookies();
      const Data = await result.json();

      cookies.set("auth",Data["auth"],{ path: '/' });
      cookies.set("user",Data["user"],{ path: '/' });

      router.replace('/home');
    }).catch(async (result: any) => {
      const Data = await result.json();
      console.log(Data);
    })
  };

  return (
    <div>
      <div style={{width: "100%", height: "100%", zIndex: 1, position: "fixed", backgroundColor: "rgba(255,255,255,0.15)", display: "flex"}}>
        <div style={{ border: "1px solid #333", backgroundColor: "#000", borderRadius: "30px", height: "80vh", width: "80vh", fontSize: "50vh", margin: "auto", display: "flex", flexDirection: "column", justifyContent: "space-between"}}>
          <div style={{marginLeft: "20px", marginRight: "50px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "space-between", height: "80%"}}>
            <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", width: "100%"}}>
              <Close onClick={()=>{router.replace('/')}}/>
              <div style={{color: "#FFF", height: "5vh", fontSize: "5vh", display: "flex"}}>𝕐</div>
              <div/>
            </div>
            <div style={{color: "#FFF", height: "5vh", fontSize: "4.5vh", display: "flex"}}>Sign in to Y</div>
            <div style={{flexDirection:"column",display:"flex"}}>
              <Input placeholder="Email" inputtype="email" onChange={handleEmail} />
              <Input placeholder="Password" inputtype="password" onChange={handlePassword} />
              <Button text="Sign In" type="tertiary" roundness="moderate" onClick={handleLogin} style={{marginBottom:"0px"}}/>
            </div>
            <div style={{flexDirection:"row",display:"flex",height:"0%"}}>
              <div style={{height: "1px", backgroundColor: "#FFF", width: "150px", marginTop:"20px"}}/>
              <span style={{color: "#FFF", height: "2vh", fontSize: "2vh", padding: "10px"}} >Or</span>
              <div style={{height: "1px", backgroundColor: "#FFF", width: "150px", marginTop:"20px"}}/>
            </div>
            <Button text="Create Account" type="secondary" roundness="moderate" onClick={() =>{router.replace('/signup')}}/>
            <div/>
          </div>
        </div>
      </div>
      <div style={{flexDirection: "row", display: "flex", fontFamily: "Arial",filter:"blur(15px)"}}>
        <div style={{color: "#FFF", height:"100vh", alignItems:"center", justifyContent:"center",display:"flex",fontSize:"50vh",margin:"auto"}}>𝕐</div>
        <div style={{margin: "auto", flexDirection: "column", display:"flex"}}>
            <span style={{color: "#FFF", fontSize:"10vh", marginBottom: "50px"}}>Happening now</span>
            <span style={{color: "#FFF", fontSize: "5vh",marginBottom: "10px"}}>Join today.</span>
            <Button text="Create Account" type="tertiary" onClick={() =>{}}/>
            <span style={{color: "#FFF", fontSize: "2vh",marginBottom: "10px",marginTop:"50px"}}>Already have an account?</span>
            <Button text="Sign In" type="secondary" onClick={() =>{}}/>
        </div>
      </div>
    </div>
    
  );
}

