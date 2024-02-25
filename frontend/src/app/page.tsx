"use client";
import styles from "./page.module.css";
import Button from "@/components/buttons/button";
import Close from "@/components/buttons/close";
import Input from "@/components/inputs/input";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; 
import { signup, login } from "@/utils/utils";

export default function Home() {
  const router = useRouter();

  return (
    <div>



      <div style={{flexDirection: "row", display: "flex", fontFamily: "Chirp", backgroundColor:"#000"}}>
        <div style={{color: "#FFF", height:"100vh", alignItems:"center", justifyContent:"center",display:"flex",fontSize:"50vh",margin:"auto"}}>𝕐</div>
          <div style={{margin: "auto", flexDirection: "column", display:"flex"}}>
            <span style={{color: "#FFF", fontSize:"10vh", marginBottom: "50px"}}>Happening now</span>
            <span style={{color: "#FFF", fontSize: "5vh",marginBottom: "10px"}}>Join today.</span>
            <Button text="Create Account" type="tertiary" onClick={() =>{router.push('/signup')}}/>
            <span style={{color: "#FFF", fontSize: "2vh",marginBottom: "10px",marginTop:"50px"}}>Already have an account?</span>
            <Button text="Sign In" type="secondary" onClick={() =>{router.push('/login')}}/>
        </div>
      </div>
    </div>
    
  );
}
