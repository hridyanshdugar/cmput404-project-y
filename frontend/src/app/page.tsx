"use client";
import styles from "./page.module.css";
import Button from "@/components/buttons/button";
import Close from "@/components/buttons/close";
import Input from "@/components/inputs/input";
import React, { useState } from 'react';
import { redirect, useRouter } from 'next/navigation'; 
import { signup, login } from "@/utils/utils";

export default function Home() {
    redirect('/home');
}
