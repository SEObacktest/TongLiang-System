'use client'
import { useState, useEffect } from 'react'

export default function Register({setUser}:{setUser: any}) {

    const [message, setMessage] = useState<string>("");
    const [studentId, setStudentId] = useState<string>("");
    const [studentPassword, setStudentPassword] = useState<string>("");
    const [adminId, setAdminId] = useState<string>("");
    const [adminPassword, setAdminPassword] = useState<string>("");
    const [studentName, setStudentName] = useState<string>("");
    const [studentPhone, setStudentPhone] = useState<string>("");
    const [adminName, setAdminName] = useState<string>("");
    const [adminPhone, setAdminPhone] = useState<string>("");

    async function StudentRegisterRequest() {

        if(studentId == "" || studentPassword == "" || studentName == "" || studentPhone == ""){
            setMessage("请填写完整信息");
            return;
        }

        const res = await fetch('/api/studentRegister', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                studentId: studentId,
                password: studentPassword,
                username: studentName,
                phone: studentPhone
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
        setMessage(data.value.message);
        // window.location.reload();
        return;
    }

    async function AdminRegisterRequest() {
        const res = await fetch('/api/adminRegister', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                adminId: adminId,
                password: adminPassword,
                username: adminName,
                phone: adminPhone
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
        window.location.reload();
        return;
    }


    return (
    <main className="flex min-h-screen flex-col items-center justify-center">
        <div className="flex justify-between h-96 w-2/5 rounded-xl border-2 border-black">
            <div className="flex flex-col items-center w-1/2">
                <h1>用户注册</h1>
                <div className="flex flex-col justify-start items-start mt-2">
                    <div className="flex m-3">
                    <label htmlFor="username">学号</label>
                    <input type="text" id="username" className="rounded-xl border-2" onChange={e => setStudentId(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="password">密码</label>
                    <input type="password" id="password" className="rounded-xl border-2" onChange={e => setStudentPassword(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="name">姓名</label>
                    <input type="text" id="name" className="rounded-xl border-2" onChange={e => setStudentName(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="phone">电话</label>
                    <input type="text" id="phone" className="rounded-xl border-2" onChange={e => setStudentPhone(e.target.value)} />
                    </div>
                </div>
                <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={StudentRegisterRequest}>注册</button>
            </div>
            <div className="flex flex-col items-center w-1/2">
                <h1>管理员注册</h1>
                <div className="flex flex-col justify-start items-start mt-2">
                    <div className="flex m-3">
                    <label htmlFor="username">账号</label>
                    <input type="text" id="username" className="rounded-xl border-2" onChange={e => setAdminId(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="password">密码</label>
                    <input type="password" id="password" className="rounded-xl border-2" onChange={e => setAdminPassword(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="name">姓名</label>
                    <input type="text" id="name" className="rounded-xl border-2" onChange={e => setAdminName(e.target.value)} />
                    </div>
                    <div className="flex m-3">
                    <label htmlFor="phone">电话</label>
                    <input type="text" id="phone" className="rounded-xl border-2" onChange={e => setAdminPhone(e.target.value)} />
                    </div>
                </div>
                <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={AdminRegisterRequest} >注册</button>
            </div>
        </div>
        {message}
        {/* <button className="bg-blue-500 rounded-xl h-8 w-20" onMouseDown={Logout}>登出</button> */}
    </main>
    );
}