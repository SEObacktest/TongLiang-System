'use client'
import { useState, useEffect } from 'react'

import { is_login } from './api/api'

import type {User} from '@/app/utils/interface'
import {defaultUser} from '@/app/utils/interface'

import Login from "./lib/ui/login";

export default function Home() {

  const [message, setMessage] = useState<string>("");
  const [user, setUser] = useState<User>(defaultUser);
 
  async function isLoginRequest() {
    const data:any = await is_login();
    if(data.status == false){
      setMessage(data.message);
      return;
    }
    // console.log(data);
    user.isLogin = data.statue;
    setUser(user);
    setMessage(data.message);
    return;
  }

  // isLoginRequest();

  return (
    <main>
      <div onClick={isLoginRequest}>isLogin</div>
      {user.username}
      {message}
      {
        user.isLogin ? (
            // <Dashboard user={user}/>
            <>
            </>
        ) : (
          <>
            <Login setUser={setUser}/>
            
          </>
        )
      }
      
    </main>
  );
}
