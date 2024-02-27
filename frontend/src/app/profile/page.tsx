"use client";
import styles from "./page.module.css";
import Button from "@/components/buttons/button";
import Close from "@/components/buttons/close";
import Input from "@/components/inputs/input";
import React, { useState } from 'react';
import {navigate } from "@/utils/utils";
import Cookies from 'universal-cookie';
import exp from "constants";

export default function Profile() {
  const cookie = new Cookies();
  const allcookies = cookie.getAll();
  if (allcookies.auth && allcookies.user) {
    const userName = cookie.get("user").email
    console.log(userName)
    //!!Change to userName.username once implemented
    navigate('/profile/' + userName);
  }
  else {
    navigate('/');
  }
}