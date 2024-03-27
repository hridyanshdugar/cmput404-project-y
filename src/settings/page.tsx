"use client";
import React, { useState, useEffect, ChangeEvent } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import styles from "./page.module.css";
import Button from "../components/buttons/button";
import Card from "react-bootstrap/Card";
import { Col, Row } from "react-bootstrap";
import {
	saveSettings,
	getUserLocalInfo,
	navigate,
	updateCookies,
	getAPIEndpoint,
	createPost,
} from "../utils/utils";
import Cookies from "universal-cookie";

export default function Settings() {
	const cookies = new Cookies();
	const [WarningData, setWarningData] = useState<any>(null);

	const [Name, setName] = useState<string>("");
	const [Github, setGithub] = useState<string>("");

	const [PFP, setPFP] = useState<File | null>(null);
	const [PFPurl, setPFPurl] = useState<string | null>(null);

	const [PFPbackground, setPFPbackground] = useState<File | null>(null);
	const [PFPbackgroundurl, setPFPbackgroundurl] = useState<string | null>(null);

	useEffect(() => {
		const auth = cookies.get("auth")["access"];
		const id = cookies.get("user")["id"];
		getUserLocalInfo(auth, id)
			.then(async (result: any) => {
				const Data = await result.json();
				console.log(Data, Data?.displayName);

				setName(Data?.displayName || "");
				setGithub(Data?.github || "");
				setPFPurl(Data?.profileImage ? Data?.profileImage : "");
				setPFPbackgroundurl(
					Data?.profileBackgroundImage ? Data?.profileBackgroundImage : ""
				);
			})
			.catch(async (result: any) => {
				const Data = await result?.json();
				console.log(Data);
				setWarningData({ title: Data?.title, message: Data?.message });
			});
	}, []);

	const handleName = (event: React.ChangeEvent<HTMLInputElement>) => {
		setName(event.target.value);
	};
	const handleGithub = (event: React.ChangeEvent<HTMLInputElement>) => {
		setGithub(event.target.value);
	};

	const handlePFP = (event: ChangeEvent<HTMLInputElement>) => {
		if (event.target.files && event.target.files[0]) {
			const file = event.target.files[0];
			setPFP(file);

			const fileReader = new FileReader();
			fileReader.onload = () => {
				setPFPurl(fileReader.result as string);
			};
			fileReader.readAsDataURL(file);
		}
	};

	const handlePFPbackground = (event: ChangeEvent<HTMLInputElement>) => {
		if (event.target.files && event.target.files[0]) {
			const file = event.target.files[0];
			setPFPbackground(file);

			const fileReader = new FileReader();
			fileReader.onload = () => {
				setPFPbackgroundurl(fileReader.result as string);
			};
			fileReader.readAsDataURL(file);
		}
	};

	const handleSave = async (e: React.MouseEvent<HTMLElement>) => {
		e.preventDefault();
		const auth = cookies.get("auth")["access"];
		const id = cookies.get("user")["id"];
		saveSettings(Name, Github, PFP, PFPbackground, auth, id)
			.then(async (result: any) => {
				const Data = await result.json();
				updateCookies({
					displayName: Data["displayName"],
					github: Data["github"],
					profileImage: Data["profileImage"],
					profileBackgroundImage: Data["profileBackgroundImage"],
				});

				setName(Data?.displayName || "");
				setGithub(Data?.github || "");
				setPFPurl(Data?.profileImage || "");
				setPFPbackgroundurl(Data?.profileBackgroundImage || "");

				navigate("/home");
			})
			.catch(async (result: any) => {
				const Data = await result?.json();
				console.log(Data);
				setWarningData({ title: Data?.title, message: Data?.message });
			});
	};

	const githubActivityPost = () => {
		const auth = cookies.get("auth")["access"];
		const id = cookies.get("user")["id"];
		getUserLocalInfo(auth, id)
			.then(async (result: any) => {
				const Data = await result.json();
				try {
					const githubUsername = Data?.github;
					const githubActivity = await fetch(
						`https://api.github.com/users/${githubUsername}/events`
					);
					if (githubActivity.status === 200) {
						const githubActivityData = await githubActivity.json();
						githubActivityData.forEach((event: any) => {
							console.log(event);
							createPost(
								"",
								"text/plain",
								`${event.type} by ${event.actor.display_login} on ${event.repo.name} at ${event.created_at}`,
								"PUBLIC",
								auth,
								id
							);
						});
					}
				} catch {}
			})
			.catch(async (result: any) => {
				const Data = await result?.json();
				console.log(Data);
			});
	};
	return (
		<>
			<div className={"main"}>
				<div className={styles.mainContentView}>
					<div className={styles.container}>
						<h1 className={styles.title}>Settings</h1>
						<Button
							onClick={githubActivityPost}
							text="Post Recent Github Activity"
							type="tertiary"
						/>
						<header className={styles.header}>Edit Account Details:</header>
						<form>
							<label className={styles.form}>
								Name
								<input
									className={styles.input}
									value={Name}
									onChange={handleName}
									type="text"
									id="name"
									name="name"
									placeholder="Enter your name"
									required
								></input>
							</label>
							<label className={styles.form}>
								Github
								<input
									className={styles.input}
									value={Github}
									onChange={handleGithub}
									type="text"
									id="github"
									name="github"
									placeholder="Enter your github"
									required
								></input>
							</label>
							<label className={styles.form}>
								Profile Banner
								<img
									src={PFPbackgroundurl || ""}
									alt="No Banner Provided"
									style={{
										width: "90%",
										height: "auto",
										aspectRatio: "4",
										margin: "5%",
										backgroundColor: "#CCC",
										borderRadius: "10px",
									}}
								/>
								<input
									className={styles.input}
									onChange={handlePFPbackground}
									type="file"
									id="PFP"
									name="PFP"
									accept="image/*"
								></input>
							</label>
							<label className={styles.form} style={{ width: "45%" }}>
								Profile Picture
								<img
									src={PFPurl || ""}
									style={{
										width: "90%",
										height: "auto",
										aspectRatio: "1",
										margin: "5%",
										backgroundColor: "#CCC",
										borderRadius: "10px",
									}}
								/>
								<input
									className={styles.input}
									onChange={handlePFP}
									type="file"
									id="PFP"
									name="PFP"
									accept="image/*"
								></input>
							</label>

							<input
								className={styles.submit}
								onClick={handleSave}
								type="submit"
								value="Save"
							></input>
						</form>
					</div>
				</div>
			</div>
		</>
	);
}
