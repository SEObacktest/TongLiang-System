'use client'
import { useState, useEffect } from 'react'

import { URL } from '@/app/api/config'

import { student_login } from '@/app/api/api'

import type {User} from '@/app/utils/interface'
import {defaultUser} from '@/app/utils/interface'

export default function Login({setUser}:{setUser: any}) {

    const [message, setMessage] = useState<string>("");
    const [studentId, setStudentId] = useState<string>("");
    const [studentPassword, setStudentPassword] = useState<string>("");
    const [adminId, setAdminId] = useState<string>("");
    const [adminPassword, setAdminPassword] = useState<string>("");

    var user: User = defaultUser;

    async function Logout() {
        const res = await fetch(URL + '/api/logout/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            mode : 'no-cors',
        });
        console.log(res);
        if (!res.ok) {
            setMessage("Connect fail!");
            return;
        }
        const data = await res.json();
        console.log(data.value)
        setMessage(data.value.message);
        return;
    }

    async function StudentLoginRequest() {
        const data:any = await student_login({studentId, studentPassword});
        if(data.status == false){
            setMessage(data.message);
            return;
        }
        user.isLogin = true;
        user.student = true;
        user.userId = data.data.studentId;
        user.phone = data.data.phone;
        user.username = data.data.username;
        setUser(user);
        console.log(user);
        setMessage(data.message);
        // window.location.reload();
        return;
    }

    async function AdminLoginRequest() {
        const res = await fetch('/api/adminLogin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                adminId: adminId,
                password: adminPassword
            })
        });
        if (!res.ok) {
            setMessage("Connect fail!");
            return;
        }
        const data = await res.json();
        if(data.value.status == false){
            setMessage(data.value.message);
            return;
        }
        console.log(data.value)
        user.isLogin = true;
        user.admin = true;
        user.userId = data.value.data.adminId;
        user.phone = data.value.data.phone;
        user.username = data.value.data.username;
        setUser(user);
        setMessage(data.value.message);
        window.location.reload();
        return;
    }

    function Register() {
        window.location.href = '/register';
    }

    return (
    <main className="flex min-h-screen flex-col items-center justify-center">
        <div className="flex flex-col items-center justify-center h-96 w-2/5 rounded-xl border-2 border-black">
            <div className="flex h-full w-full justify-between">
                <div className="flex flex-col items-center w-1/2">
                    <h1>用户登录</h1>
                    <div className="flex flex-col justify-start items-start mt-2">
                        <div className="flex m-3">
                        <label htmlFor="username">学号</label>
                        <input type="text" id="username" className="rounded-xl border-2" onChange={e => setStudentId(e.target.value)} />
                        </div>
                        <div className="flex m-3">
                        <label htmlFor="password">密码</label>
                        <input type="password" id="password" className="rounded-xl border-2" onChange={e => setStudentPassword(e.target.value)} />
                        </div>
                    </div>
                    <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={StudentLoginRequest}>登录</button>
                </div>
                <div className="flex flex-col items-center w-1/2">
                    <h1>管理员登录</h1>
                    <div className="flex flex-col justify-start items-start mt-2">
                        <div className="flex m-3">
                        <label htmlFor="username">账号</label>
                        <input type="text" id="username" className="rounded-xl border-2" onChange={e => setAdminId(e.target.value)} />
                        </div>
                        <div className="flex m-3">
                        <label htmlFor="password">密码</label>
                        <input type="password" id="password" className="rounded-xl border-2" onChange={e => setAdminPassword(e.target.value)} />
                        </div>
                    </div>
                    <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={AdminLoginRequest} >登录</button>
                </div>
            </div>
        {message}
        <div className="cursor-pointer" onMouseDown={Register}>注册</div>
        </div>
        <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={Logout}>登出</button>
    </main>
    );
}