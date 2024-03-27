"use client";
import styles from './input.module.css'
import React from 'react';
import "../../global.css";

interface InputProps {
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    text?: string;
    inputtype?: "text" | "displayName" | "password";
    placeholder?: string;
    type?: "primary" | "secondary" | "tertiary";
    size?: "small" | "medium" | "large";
    roundness?: "very" | "moderate";
    style?: React.CSSProperties;
  }

const Button: React.FC<InputProps> = ({onChange, text, placeholder,inputtype = "text", type = "primary", size = "medium",roundness="moderate",style}) => {

    const sizeStyles = {
        small: styles.smallButton,
        medium: styles.mediumButton,
        large: styles.largeButton,
      };
    
    const roundStyles = {
        very: styles.very,
        moderate: styles.moderate,
      };
    
    const typeStyles = {
        primary: styles.primary,
        secondary: styles.secondary,
        tertiary: styles.tertiary,
      };
    
    return (<input
      type={inputtype}
      placeholder={placeholder}
      value={text}
      onChange={onChange}
      style={{
        padding: "10px",
        fontSize: "2vh",
        color: "#FFF",
        backgroundColor: "#333",
        border: "1px solid #333",
        borderRadius: "5px",
        width: "480px", // Adjust width as needed
        outline: "none",
        marginBottom:"20px"
      }}
    ></input>);
};

export default Button;
