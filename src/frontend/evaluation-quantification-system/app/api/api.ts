// import { GET, POST, getToken } from "@/app/utils/tools";
import { get, post} from '@/app/api/'

export async function is_login() {
    
    let value = await get('/api/is_login/')
    console.log(value)
    return value
}

export async function student_login({studentId, studentPassword}:{studentId: string, studentPassword: string}) {

    let value = await post('/api/student_login/', {
        "studentId": studentId,
        "password": studentPassword
    })
    console.log(value)
    return value
}

// export async function isLogin() {
    
//     const data = await (await GET('/api/is_login/')).json();
//     console.log(data.value);
//     return data.value;
// }

// export async function Logout() {
//     const res = await fetch(URL + '/api/logout/', {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': await getToken()
//         },
//         mode : 'cors',
//     });
//     if (!res.ok) {
//         const message = "Connect fail!";
//         return {
//             message
//         };
//     }
//     const data = await res.json();
//     console.log(data.value)
//     return data.value;
// }

// export async function StudentLogin({studentId, studentPassword}:{studentId: string, studentPassword: string}) {
//     const data = await (await POST('/api/student_login/', {
//         studentId: studentId,
//         password: studentPassword
//     })).json();
//     console.log(data.value)
//     return data.value;
// }

// export async function AdminLogin(adminId: string, adminPassword: string) {
//     const res = await fetch(URL + '/api/admin_login/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': await getToken()
//         },
//         body: JSON.stringify({
//             adminId: adminId,
//             password: adminPassword
//         }),
//         mode : 'cors',
//     });
//     if (!res.ok) {
//         const message = "Connect fail!";
//         return {
//             message
//         };
//     }
//     const data = await res.json();
//     if(data.value.status == false){
//         const message = "Connect fail!";
//         return {
//             message
//         };
//     }
//     console.log(data.value)
//     return data.value;
// }