import { NextRequest, NextResponse } from "next/server";

import { URL } from '../config';

export async function POST(request: Request) {
    const res = await fetch(URL + '/api/logout/', 
    {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    const value = await res.json()

    return NextResponse.json({ value })
}
