"use strict";
import React, { useState, MouseEvent, forwardRef } from "react";
import Button from "@/components/buttons/button";
import style from "./dropdown.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleDown } from "@fortawesome/free-solid-svg-icons";

interface DropdownProps {
	label: string | null;
	options: string[];
	onChange: (selection: string | null) => void;
	innerRef: React.RefObject<HTMLDivElement> | undefined;
	styles: React.CSSProperties | undefined;
}
const Dropdown: React.FC<DropdownProps> = ({
	label,
	options,
	innerRef,
	styles,
	onChange
}) => {
	const [isOpen, setIsOpen] = useState(false);
	const [selectedOption, setSelectedOption] = useState(label);

	const toggleDropdown = () => {
		setIsOpen(!isOpen);
	};

	const handleOptionClick = (event: MouseEvent<HTMLButtonElement>,option:string) => {
		const target = event.target as HTMLButtonElement;
		setSelectedOption(target.textContent);
		setIsOpen(false);
		console.log(option);
		onChange(option);
	};

	return (
		<div className={style.dropdown} ref={innerRef} style={styles}>
			<button className={style.dropdownToggle} onClick={toggleDropdown}>
				<span> {selectedOption} </span>
				<FontAwesomeIcon icon={faAngleDown} />
			</button>
			{isOpen && (
				<div className={style.dropdownContent}>
					<div className={style.dropdownTitle}> Choose Audience</div>
					{options.map((option: string, index: number) => (
						<button
							className={style.dropdownOptions}
							onClick={(e:MouseEvent<HTMLButtonElement>)=>{handleOptionClick(e,option)}}
							key={index}
						>
							{option}
						</button>
					))}
				</div>
			)}
		</div>
	);
};

export default Dropdown;
