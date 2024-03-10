import "./global.css";
import SideBar from "./components/sidebar";
import Rightbar from "./components/rightbar";
import { PostContextProvider } from "./utils/postcontext";
import { Outlet } from "react-router-dom";

export function RootLayout() {
	return (
		<html lang="en">
			<body style={{backgroundColor: "#000"}}>
				<PostContextProvider>
					<SideBar />
					<Outlet/>
					<Rightbar />
				</PostContextProvider>
			</body>
		</html>
	);
}
