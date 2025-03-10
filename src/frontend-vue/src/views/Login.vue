<script setup>
import {ref} from 'vue'

import router from '@/router'
import { student_login_request, logout_request } from '../api/api';

const studentId = ref();
const password  = ref();
const message   = ref();

async function student_login(){

    if (studentId.value == undefined) {
        message.value = "请输入学号";
        return;
    }
    if (password.value == undefined) {
        message.value = "请输入密码";
        return;
    }

    var value = await student_login_request(
        {
            'studentId': studentId.value, 
            'password': password.value
        }
    )

    message.value = value.message

    if (value.status == true) {
        router.push('/')
    }

}

</script>

<template>
<div></div>

<div id='main'>
    <div class="container">
        <div class="title">登录</div>
        <div class="form">
            <div class="form-item">
                <div class="form-item-label">学号</div>
                <div class="form-item-input">
                    <input type="text" placeholder="请输入学号" v-model="studentId">
                </div>
            </div>
            <div class="form-item">
                <div class="form-item-label">密码</div>
                <div class="form-item-input">
                    <input type="password" placeholder="请输入密码" v-model="password">
                </div>
            </div>
            {{ message }}
            <div class="login-button" @click="student_login">登录</div>
            <div class="login-button" @click="clinic_logout_request">登出</div>
        </div>
        <div class="navigation">
            <div class="register">申请注册</div>
            <div class="forget-password">忘记密码</div>
            <div class="admin-login">管理员登录</div>
        </div>
    </div>
</div>

</template>

<style scoped>
#main {
    height: 1000px;
    width: 100%;
    background-color: grey;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.container {
    width: 600px;
    height: 600px;
    background-color: white;
    border-radius: 20px;
    display: flex;
    justify-content: start;
    flex-direction: column;
}
.title {
    display: flex;
    justify-content: center;
}
.form {
    display: flex;
    flex-direction: column;
    
}
.form-item {
    display: flex;
    justify-content: center;
}
.login-button {
    display: flex;
    justify-content: center;
    cursor: pointer;
}
</style>