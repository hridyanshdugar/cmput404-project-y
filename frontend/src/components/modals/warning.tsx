"use client";
import styles from './input.module.css'
import React from 'react';
import Close from "../../components/buttons/close";
import Button from "../../components/buttons/button";
import "../../global.css";

interface InputProps {
    onClick: () => void;
    title?: string;
    message?: string;
  }

const Warning: React.FC<InputProps> = ({onClick, title, message}) => {
    
    return (<div style={{width: "100%", height: "100%", zIndex: 2, position: "fixed", display: "flex"}}>
    <div style={{ border: "3px solid red", backgroundColor: "#000", borderRadius: "30px", height: "40vh", width: "50vh", fontSize: "50vh", margin: "auto", display: "flex", flexDirection: "column", justifyContent: "space-between"}}>
      <div style={{marginLeft: "20px", marginRight: "50px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "space-between", height: "100%"}}>
        <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between", width: "100%"}}>
          <Close onClick={onClick}/>
          <div style={{color: "#FFF", height: "5vh", fontSize: "5vh", display: "flex",marginLeft: "-20px"}}>𝕐</div>
          <div/>
        </div>
        <div style={{color: "#FFF", height: "5vh", fontSize: "3vh", display: "flex"}}>{title}</div>
        <p style={{color: "#FFF", height: "10vh", fontSize: "2vh", display: "flex", margin:"0px 20px 0 60px"}}>{message}</p>
        
        <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
          <Button text="Okay" type="secondary" roundness="moderate" size="small" onClick={onClick}/>
        </div>
        <div/>
        <div/>
      </div>
    </div>
  </div>);
};

export default Warning;
