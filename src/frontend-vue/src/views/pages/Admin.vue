<script setup>

import {ref} from 'vue'

import { is_login_request } from '../../api/api';

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
        // alert("请先登录，若无反应请刷新界面")
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
        <h1>欢迎使用在线HR系统</h1>
        <h2>当前用户: {{ user.username }}</h2>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 100%;
    height: 1000px;
    margin-top: 100px;
    display: flex;
    justify-content: center;
}
</style>