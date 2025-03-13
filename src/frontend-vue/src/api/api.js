import {get, post, post_with_file, post_file, post_get_excel} from '@/api/index.js'

// 登录
//////////////////////////////////////////////////
export async function is_login_request() {
    
    let value = await get('/api/is_login/')
    console.log(value)
    return value
}

export async function logout_request() {

    let value = await get('/api/logout/')
    console.log(value)
    return value
}

export async function admin_login_request(data) {

    let value = await post('/api/admin_login/', data)
    console.log(value)
    return value
}

export async function student_login_request(data) {

    let value = await post('/api/student_login/', data)
    console.log(value)
    return value
}
// 注册
//////////////////////////////////////////////////
export async function admin_register_request(data) {

    let value = await post('/api/admin_register/', data)
    console.log(value)
    return value

}

export async function hr_register_request(data) {

    let value = await post('/api/hr_register/', data)
    console.log(value)
    return value

}

// 删除
//////////////////////////////////////////////////

export async function delete_student_request(data) {

    let value = await post('/api/delete_student/', data)
    console.log(value)
    return value

}

// 在线HR
//////////////////////////////////////////////////

export async function get_hr_list_request() {

    let value = await get('/api/get_hr_list/')
    console.log(value)
    // var number = value.number
    // value = JSON.parse(value.clinics)
    // var clinics = []
    // for (var i = 0; i < number; i++) {
    //     clinics.push(value[i].fields)
    // }
    return value

}

export async function hr_update_request(data) {

    let value = await post('/api/hr_update/', data)
    console.log(value)
    return value

}

// 题库管理
//////////////////////////////////////////////////

export async function get_question_list_request() {

    let value = await get('/api/get_question_list/')
    console.log(value)
    return value

}

export async function question_update_request(data) {

    let value = await post('/api/question_update/', data)
    console.log(value)
    return value

}

export async function create_question_request(data, file) {

    // 1️⃣ 创建 FormData
    const formData = new FormData();

    // 2️⃣ 添加 JSON 数据（转换为 Blob）
    const jsonData = data
    formData.append("json", new Blob([JSON.stringify(jsonData)], { type: "application/json" }));

    // 3️⃣ 添加文件（多文件上传）
    // for (let i = 0; i < image.value.length; i++) {
    //     formData.append("file", image.value[i]); // "images" 是后端接收的字段名
    // }
    formData.append("file", file);

    let value = await post_with_file('/api/create_question/', formData)
    console.log(value)
    return value

}

export async function delete_question_request(data) {

    let value = await post('/api/delete_question/', data)
    console.log(value)
    return value

}

export async function post_question_image_request(questionId, image) {
    
    console.log(questionId)
    console.log(image)
    let formData = new FormData()
    formData.append('questionId', questionId)
    formData.append('image', image)

    let value = await post_file('/api/post_question_image/', formData)
    console.log(value)
    return value

}

// 面试管理
//////////////////////////////////////////////////

export async function get_interview_list_request() {

    let value = await get('/api/get_interview_list/')
    console.log(value)
    return value

}

export async function interview_update_request(data) {

    let value = await post('/api/interview_update/', data)
    console.log(value)
    return value

}

export async function create_interview_request(data, file) {

    // 1️⃣ 创建 FormData
    const formData = new FormData();

    // 2️⃣ 添加 JSON 数据（转换为 Blob）
    const jsonData = data
    formData.append("json", new Blob([JSON.stringify(jsonData)], { type: "application/json" }));

    // 3️⃣ 添加文件（多文件上传）
    // for (let i = 0; i < image.value.length; i++) {
    //     formData.append("file", image.value[i]); // "images" 是后端接收的字段名
    // }
    formData.append("file", file);

    let value = await post_with_file('/api/create_interview/', formData)
    console.log(value)
    return value

}

export async function delete_interview_request(data) {

    let value = await post('/api/delete_interview/', data)
    console.log(value)
    return value

}

// 报酬管理
//////////////////////////////////////////////////

export async function get_salary_list_request() {
    
    let value = await get('/api/get_salary_list/')
    console.log(value)
    return value

}

export async function post_settlement_request(data) {
    
    let value = await post('/api/post_settlement/', data)
    console.log(value)
    return value
    
}

export async function post_settle_all_request(data) {
    
    let value = await post('/api/post_settle_all/', data)
    console.log(value)
    return value
    
}

// 流水管理
//////////////////////////////////////////////////

export async function get_settlement_list_request() {

    let value = await get('/api/get_settlement_list/')
    console.log(value)
    return value
    
}

// 活动管理（已废弃）
//////////////////////////////////////////////////

export async function create_activity_request(data) {

    let value = await post('/api/create_activity/', data)
    console.log(value)
    return value

}

export async function get_activities_list_request(data) {
    
    let value = await post('/api/get_activities_list/', data)
    console.log(value)
    return value
    
}

export async function delete_activity_request(data) {
    
    let value = await post('/api/delete_activity/', data)
    console.log(value)
    return value
    
}

export async function get_activity_information_request(data) {
    
    let value = await post('/api/get_activity_information/', data)

    console.log(value)
    var valueJson = JSON.parse(value.patient)
    let imageListId = value.imageListId
    var imageList = []
    
    for (let i = 0; i < imageListId.length; i++) {
        var imageUrl = await get_activity_images_request({"imageId": imageListId[i]})
        imageList.push(String('/media/' + imageUrl))
        
    }
    valueJson = valueJson[0].fields
    valueJson.imageList = imageList
    return valueJson
    
}

export async function certified_activity_request(data) {
    
    let value = await post('/api/check_activity/', data)
    console.log(value)
    return value
    
}

// 图片工具
//////////////////////////////////////////////////

export async function post_user_image_request(userId, image) {

    console.log(userId)
    console.log(image)
    let formData = new FormData()
    formData.append('userId', userId)
    formData.append('image', image)

    let value = await post_file('/api/post_user_image/', formData)
    console.log(value)
    return value

}

export async function post_curriculumVitae_image_request(interviewId, image) {

    console.log(interviewId)
    console.log(image)
    let formData = new FormData()
    formData.append('interviewId', interviewId)
    formData.append('image', image)

    let value = await post_file('/api/post_curriculumVitae_image/', formData)
    console.log(value)
    return value

}

export async function delete_activity_image_request(data) {
    
    let value = await post('/api/delete_activity_image/', data)
    console.log(value)
    return value
    
}

export async function post_activity_image_request(activityId, image) {

    console.log(activityId)
    console.log(image)
    let formData = new FormData()
    formData.append('activityId', activityId)
    formData.append('image', image)

    let value = await post_file('/api/post_activity_image/', formData)
    console.log(value)
    return value

}


// export async function post_patient_3d_request(patientId, file) {

//     let formData = new FormData()
//     formData.append('patientId', patientId)
//     formData.append('file', file)

//     let value = await post_file('/api/post_patient_3d/', formData)
//     console.log(value)
//     return value

// }

// export async function delete_patient_3d_request(data) {
    
//     let value = await post('/api/delete_patient_3d/', data)
//     console.log(value)
//     return value
    
// }

// export async function get_patient_3d_request(data) {
    
//     let value = await post('/api/get_patient_3d/', data)
//     console.log(value)
//     for (let i = 0; i < value.data.length; i++) {
//         value.data[i] = String('/media/' + value.data[i])
//     }
//     return value.data
    
// }

/*
    data: '[{"model": "server.patientimage", "pk": 1, "fields": {"patient": 3, "image": "activity_image/test_q43DaGb.jpeg", "uploadTime": "2023-04-11T13:31:12.338Z"}}]'
    message: '获取图片成功'
    status: true
*/
export async function get_activity_images_request(data) {

    let value = await post('/api/get_activity_images/', data)
    console.log(value)
    // let imageData = JSON.parse(value.data)
    return value

}

export async function get_user_image_request(data) {

    let value = await post('/api/get_user_image/', data)
    console.log(value)
    // let imageData = JSON.parse(value.data)
    return value

}

export async function get_curriculumVitae_image_request(data) {

    let value = await post('/api/get_curriculumVitae_image/', data)
    console.log(value)
    // let imageData = JSON.parse(value.data)
    return value

}

export async function export_excel_request(data) {
        
        let value = await post_get_excel('/api/export_excel/', data)
        console.log(value)
        return value
}

/*
    get_clinic_patient_request()返回格式：
    返回一个列表，列表中每个元素是一个字典，字典中包含了患者的所有信息
    [
        {
            id: "1",
            username: "xxx",
            phone: "xxx",
            birthday: "xxxx-xx-xx",
            clinic: x,
            description: "xxx",
            activityImageNumber: x,
            registerTime: "xxxx-xx-xxTxx:xx:xx.xxxx",
        }
    ]
*/
// export async function get_clinic_patient_request(data) {

//     var value = await post('/api/get_clinic_patient/', data)
//     console.log(value)
//     var number = value.number
//     value = JSON.parse(value.patients)
//     var patients = []
//     for (var i = 0; i < number; i++) {
//         patients.push(value[i].fields)
//         value[i].fields['id'] = value[i].pk
//     }
//     console.log(patients)
//     return patients
// }

/*
    get_all_patient_request()返回格式：
    返回一个列表，列表中每个元素是一个字典，字典中包含了患者的所有信息
    [
        {
            birthday: "2002-11-13"
            clinic: 1
            description: "123"
            activityImageNumber: 0
            name: "test"
            phone: "123456"
            registerTime: "2023-04-06T16:17:04.608Z"
        }
    ]
*/
// export async function get_all_patient_request() {
    
//     let value = await get('/api/get_all_patient/')
//     console.log(value)
//     var number = value.number
//     value = JSON.parse(value.patients)
//     var patients = []
//     for (var i = 0; i < number; i++) {
//         patients.push(value[i].fields)
//     }
//     console.log(patients)
//     return patients
// }

//得到用户信息
export async function user_info_request(data){

    let value = await get('/api/user_info/', data)
    console.log(value)
    return value
}

//
export async function get_salary_info_request() {

    let value = await get('/api/get_salary_info/')
    console.log(value)
    return value

}