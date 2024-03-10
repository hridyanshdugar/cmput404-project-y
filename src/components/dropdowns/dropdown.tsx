"use strict";
import React, { useState, MouseEvent, forwardRef } from "react";
import style from "./dropdown.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IconDefinition, faAngleDown } from "@fortawesome/free-solid-svg-icons";

interface DropdownProps {
	label?: string | null;
	dropdownTitle?: string | null;
	icon?: IconDefinition;
	options: string[];
	onChange: (selection: string | null) => void;
	innerRef?: React.RefObject<HTMLDivElement> | undefined;
	styles?: React.CSSProperties | undefined;
}
const Dropdown: React.FC<DropdownProps> = ({
	label,
	dropdownTitle,
	icon,
	options,
	innerRef,
	styles,
	onChange,
}) => {
	const [isOpen, setIsOpen] = useState(false);
	const [selectedOption, setSelectedOption] = useState(label);

	const toggleDropdown = (event: MouseEvent<HTMLButtonElement>) => {
		event.stopPropagation();
		setIsOpen(!isOpen);
	};

	const handleOptionClick = (
		event: MouseEvent<HTMLButtonElement>,
		option: string
	) => {
		const target = event.target as HTMLButtonElement;
		setSelectedOption(target.textContent);
		setIsOpen(false);
		console.log(option);
		onChange(option);
	};

	return (
		<div className={style.dropdown} ref={innerRef} style={styles}>
			<button className={style.dropdownToggle} onClick={toggleDropdown}>
				{label && <span> {selectedOption} </span>}
				<FontAwesomeIcon icon={icon ? icon : faAngleDown} />
			</button>
			{isOpen && (
				<div className={style.dropdownContent}>
					{dropdownTitle && (
						<div className={style.dropdownTitle}> {dropdownTitle} </div>
					)}
					{options.map((option: string, index: number) => (
						<button
							className={style.dropdownOptions}
							onClick={(e: MouseEvent<HTMLButtonElement>) => {
								e.stopPropagation();
								handleOptionClick(e, option);
							}}
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
