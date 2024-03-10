"use client";
import styles from "./page.module.css";
import Button from "../components/buttons/button";
import Close from "../components/buttons/close";
import Input from "../components/inputs/input";
import React, { useState } from 'react';
import { signup, login, navigate } from "../utils/utils";
import WarningModal from "../components/modals/warning";
import Cookies from 'universal-cookie';

export default function Signup() {
  const [WarningData, setWarningData] = useState<any>(null);

  const [Email, setEmail] = useState<string>('');
  const [Password, setPassword] = useState<string>('');
  const [PasswordVerify, setPasswordVerify] = useState<string>('');

  const handleEmail = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePassword = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handlePasswordVerify = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordVerify(event.target.value);
  };

  const handleSignUp = async () => {
    if (Password != PasswordVerify) {
      setWarningData({title: "Password fields Must Match", message: "Please re-enter your password"});
    } else {
      signup(Email,Password).then(async (result:any) => {
        
        const cookies = new Cookies();
        const Data = await result.json();

        cookies.set("auth",Data["auth"],{ path: '/' });
        cookies.set("user",Data["user"],{ path: '/' });

        navigate('/home')
      }).catch(async (result: any) => {
        const Data = await result.json();
        console.log(Data);
      })
    }
  };

  const removeAlert = () => {
    setWarningData(null);
  };

  return (
    <div>
      {WarningData !== null ? <WarningModal onClick={removeAlert} title={WarningData.title} message={WarningData.message}/> : null}


<div style={{width: "100%", height: "100%", zIndex: 1, position: "fixed", backgroundColor: "rgba(255,255,255,0.15)", display: "flex",filter:`blur(${WarningData !== null ? 10 : 0}px)`}}>
        <div style={{ border: "1px solid #333", backgroundColor: "#000", borderRadius: "30px", height: "80vh", width: "80vh", fontSize: "50vh", margin: "auto", display: "flex", flexDirection: "column", justifyContent: "space-between"}}>
          <div style={{marginLeft: "20px", marginRight: "50px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "space-between", height: "100%"}}>
            <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", width: "100%"}}>
              <Close onClick={()=>{navigate('/')}}/>
              <div style={{color: "#FFF", height: "5vh", fontSize: "5vh", display: "flex"}}>𝕐</div>
              <div/>
            </div>
            <div style={{color: "#FFF", height: "5vh", fontSize: "4.5vh", display: "flex"}}>Create your account</div>
            <div style={{flexDirection:"column",display:"flex", width: "60%"}}>
              <Input placeholder="Email" inputtype="email" onChange={handleEmail} />
              <Input placeholder="Password" inputtype="password" onChange={handlePassword} />
              <Input placeholder="Verify Password" inputtype="password" onChange={handlePasswordVerify} />
            </div>
            
            <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
              <Button text="Create Account" type="tertiary" roundness="moderate" onClick={handleSignUp} style={{marginBottom:"20px"}}/>
              <Button text="Forgot Password?" type="secondary" roundness="moderate" onClick={() =>{}}/>
            </div>

            <div/>
            <div/>
          </div>
        </div>
      </div>
      <div style={{flexDirection: "row", display: "flex", fontFamily: "Chirp", backgroundColor:"#000",filter:"blur(15px)"}}>
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
