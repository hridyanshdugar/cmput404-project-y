"use client"
import { Inter } from "next/font/google";
import style from "./page.module.css";
import "./../global.css";
import SideBar from "@/components/sidebar";
import Rightbar from "@/components/rightbar";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <html lang="en">
          <body className={style.backgroundColer}>
                <SideBar/>
                {children}
                <Rightbar/>
          </body>
    </html>
  );
}