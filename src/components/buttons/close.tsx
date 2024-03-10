"use client";
import styles from "./close.module.css";
import React from "react";
import "../../global.css";

interface ButtonProps {
	onClick: () => void;
	text?: string;
	type?: "primary" | "secondary" | "tertiary";
	size?: "small" | "medium" | "large";
	roundness?: "very" | "moderate";
	style?: React.CSSProperties;
}

const Button: React.FC<ButtonProps> = ({
	onClick,
	text,
	type = "primary",
	size = "medium",
	roundness = "very",
	style,
}) => {
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

	return (
		<button onClick={onClick} className={`${styles.button}`} style={style}>
			<img
				src="/assets/close.png"
				style={{
					height: "30px",
					width: "30px",
					backgroundColor: "transparent",
				}}
			/>
		</button>
	);
};

export default Button;
