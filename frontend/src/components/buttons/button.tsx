"use client";
import styles from './button.module.css'
import React from 'react';
import "@/app/global.css";

interface ButtonProps {
    onClick: () => void;
    text?: string;
    type?: "primary" | "secondary" | "tertiary";
    size?: "verySmall" | "small" | "medium" | "large";
    roundness?: "very" | "moderate";
    style?: React.CSSProperties;
  }

const Button: React.FC<ButtonProps> = ({onClick, text, type = "primary", size = "medium",roundness="very",style}) => {

    const sizeStyles = {
        verySmall: styles.verySmallButton,
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
    
    return (<button 
              className={`${styles.button} ${roundStyles[roundness]} ${sizeStyles[size]} ${typeStyles[type]}`}
              onClick={onClick}
              style={style} > {text} </button>);
};

export default Button;
