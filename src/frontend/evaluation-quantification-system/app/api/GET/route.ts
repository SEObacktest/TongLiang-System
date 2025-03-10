import { NextRequest, NextResponse } from "next/server";

import { getToken } from "@/app/utils/tools";

import { URL } from '../config';

export async function POST(request: Request, url: string) {
    const res = await fetch(URL + url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': await getToken()
        }
    })
    const value = await res.json()
    return NextResponse.json({ value })
}


