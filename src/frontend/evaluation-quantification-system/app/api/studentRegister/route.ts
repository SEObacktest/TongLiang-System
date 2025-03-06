import { NextRequest, NextResponse } from "next/server";

import { URL } from '../config';

export async function POST(request: Request, data: {}) {
    const body = await request.json()
    const res = await fetch(URL + '/api/student_register/', 
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
    const value = await res.json()

    return NextResponse.json({ value })
}


