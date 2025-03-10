import { NextRequest, NextResponse } from "next/server";

import { URL } from '../api/config';

export async function POST(url: string, data: {}) {
    const res = await fetch(URL + url, 
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getToken()
        },
        body: JSON.stringify(data)
    })
    if(!res.ok) {
        return NextResponse.json({ status: false, message: "Connect fail!" })
    }
    const value = await res.json()

    return NextResponse.json({ value })
}

export async function GET(url: string) {
    const res = await fetch(URL + url, 
    {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getToken()
        }
    })
    if(!res.ok) {
        return NextResponse.json({ status: false, message: "Connect fail!" })
    }
    const value = await res.json()

    return NextResponse.json({ value })
}

// export async function getToken() {
//     const res = await fetch('/api/getToken', 
//     {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     const value = await res.json()
//     return value.value.data
// }

export async function getToken() {
    const res = await fetch(URL + '/api/get_token/', 
    {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        mode: 'cors'
    });
    if (!res.ok) {
        const message = "Connect fail!";
        return {
            status: false,
            message
        };
    }
    const value = await res.json()
    return value.data
}