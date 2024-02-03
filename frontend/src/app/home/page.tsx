"use client"
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import styles from "./page.module.css";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

export default function Home() {
  return (
      <div className={"main"}>
          <div className={styles.flexSpaceBetween}>
              <div className={styles.mainContentView}>
                  hi
              </div>
              <div className={styles.trending}>
                  bob
              </div>
          </div>
    </div>
  );
}
