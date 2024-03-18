"use client";
import styles from "./close.module.css";
import React from "react";
import "../../global.css";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
interface ButtonProps {
	onClick: () => void;
	style?: React.CSSProperties;
}

const Button: React.FC<ButtonProps> = ({
	onClick,
	style,
}) => {

	return (
		<button onClick={onClick} className={styles.button} style={style}>
			<FontAwesomeIcon icon={faX} style={{ height: "15px", width: "15px" }} />
		</button>
	);
};

export default Button;
