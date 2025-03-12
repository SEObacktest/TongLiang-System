<script setup>

import {ref} from 'vue'

import { is_login_request } from '../../api/api';

import router from '../../router';

const user = ref("")

async function is_login() {
    var value = await is_login_request()
    if (value.status == true) {
        user.value = value.data
        // if(user.value.is_admin == true){
        //     var value = await get_students_list_request()
        //     if(value.status == false) {
        //         alert(data.message)
        //     } else {
        //         studentList.value = value.data
        //         studentList.value.forEach(e => {
        //             studentNameList.value[e.pk] = e.fields.username
        //         });
        //     }
        // }
    } else {
        user.value = undefined
        // router.push('/login')
        router.push('/login_register')
    }
}
is_login()

</script>

<template>
<div></div>

<div id='main'>
    <div class="container">
        <h1>欢迎使用同梁在线业务系统管理员后台</h1>
        <h2>当前用户: {{ user.username }}</h2>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 100%;
    height: 1000px;
    /* margin-top: 100px; */
    display: flex;
    justify-content: center;
}
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 100px;
    padding: 20px;
    width: 400px;
    height: 300px;
    /* 毛玻璃效果 */
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1)); 
    backdrop-filter: blur(15px) saturate(150%);
    -webkit-backdrop-filter: blur(15px) saturate(150%);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    padding: 20px;
    color: black;
        
    border-radius: 20%;
}
</style>