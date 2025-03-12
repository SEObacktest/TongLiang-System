<script setup>

import { ref } from 'vue'

import { formulate_time } from '../../utils/tools';

import {
    delete_student_request, 
    hr_update_request,
} from '@/api/api';   

import { URL } from '../../api/config';

const apiURL = URL + '/media/'

const props = defineProps(['settlement'])
const emit  = defineEmits(['close'])

const hr   = ref(props.settlement)
const new_hr = ref({
    'username': hr.value.username,
    'stage': hr.value.stage,
    'userId': hr.value.userId,
    'phone': hr.value.phone,
    'age': hr.value.age,
    'gender': hr.value.gender,
    'account': hr.value.account,
    'bankCard': hr.value.bankCard,
    'bank': hr.value.bank,
    'accountHolderName': hr.value.accountHolderName,
    'idCard': hr.value.idCard,
    'city': hr.value.city,
})
const hrId = ref(props.settlement.id)

const is_show_image = ref(false)
const show_image = ref('')

async function delete_hr() {
    if(!confirm('确定删除' + hr.value.username + '吗？ 包括相关的图片')) return;
    var value = await delete_student_request({'userId': hrId.value})
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
        emit('close')

    } else {
        alert(value.message)
    }
}

function refresh() {
    window.location.reload()
}
</script>

<template>
<div></div>

<div id='main'>
    <div class="show-image" v-if="is_show_image">
        <img :src="show_image" alt="image" @click="is_show_image = false">
    </div>
    <div class="navigation-bar">
        <div class="title">交易详情</div>
    </div>
    <div class="hr-information">
        <!-- {{ hr }} -->
        <div class="hr-left">
            <div class="hr-name">交易ID: {{ hr.id }}</div>
            <div class="hr-id">HR: {{ hr.hr }}</div>
            <div class="hr-phone">交易时间: {{ formulate_time(hr.settlement_time) }}</div>
            <!-- <div class="hr-score">已面个数: {{  }}</div> -->
            <!-- <div class="hr-age">年龄: {{ hr.age }}</div>
            <div class="hr-gender">性别: {{ hr.gender }}</div> -->
        </div>
        <div class="hr-right">

            <!-- <div class="hr-account">管理账号: {{ hr.account }}</div> -->
            <div class="hr-bank-card">银行卡号: {{ hr.bankCard }}</div>
            <div class="hr-bank">开户行: {{ hr.bank }}</div>
            <div class="hr-account-holder-name">开户人姓名: {{ hr.accountHolderName }}</div>
            <!-- <div class="hr-id-card">身份证号: {{ hr.idCard }}</div> -->
            <!-- <div class="hr-register-time">注册时间: {{ formulate_time(hr.date_joined) }}</div> -->
            <!-- <div class="hr-last-login">上次登录时间: {{ formulate_time(hr.last_login) }}</div> -->
        </div>
    </div>
    
    <div class="bottom-bar">
        <!-- <div v-if="isEdit" class="bottom-bar-item" id="close-button" @click="isEdit = !isEdit">返回</div> -->
        <div class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <!-- <div v-if="isEdit" class="bottom-bar-item" id="save-button" @click="hr_update();isEdit = !isEdit">保存</div> -->
        <!-- <div class="bottom-bar-item" id="edit-button" @click="isEdit = !isEdit">编辑</div> -->
        <!-- <div class="bottom-bar-item" id="delete-button" @click="delete_hr">删除记录</div> -->
    </div>
</div>

</template>

<style scoped>
#main {
    width: 500px;
    height: 300px;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 400px;
    padding: 10px;
    border-radius: 20px;
}
.show-image {
    position: absolute;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 800px;
    height: 600px;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;

}
.navigation-bar {
    display: flex;
    justify-content: center;
}
.navigation-bar .title {
    font-size: 30px;
    font-weight: bold;
    font-family: "SanJiXinWeiBeiJian-2";
}
.show-image img {
    width: 100%;
    height: 100%;
    z-index: 90;
}
.hr-information {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.hr-left {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hr-left img{
    object-fit: cover;
    object-position: center;
}
.hr-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background-color: rgb(167, 167, 211, 0.5);
    border-radius: 50%;
    cursor: pointer
}
.hr-avatar img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
}
.hr-right {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}
.hr-right input {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.hr-right select {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.bottom-bar {
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
}
.bottom-bar-item {
    cursor: pointer;
    width: 80px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 60px;
    border: 1px solid black;
    border-radius: 5px;
    transition: background-color 0.3s, transform 0.3s;
}
.bottom-bar-item:hover {
    background-color: rgb(110, 185, 208);
    transform: scale(1.2);
}
#delete-button:hover {
    background-color: red;
    transform: scale(1.2);
}
.image-list {
    display: flex;
    flex-direction: row;
}
input[type="file"]{
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
}
label{
    font-weight: bold;
    color: #6990f2;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px dashed #6990f2;
    height: 96px;
    width: 100px;
    flex-direction: column;
    cursor: pointer;
}
label > i{
    margin-bottom: 5px;
}
.images {
    position: relative;
    display: flex;
    flex-direction: row;
    cursor: pointer;
}
.images img {
    width: 100px;
    height: 100px;
}
.hr-3d-images {
    display: flex;
    flex-direction: row;
    margin-right: 10px;
    cursor: pointer;
}
.hr-3d-images .model3d {
    width: 100px;
    height: 100px;
}
.delete {
    width: 20px;
    height: 20px;
    position: absolute;
    top: 0;
    right: 0;
    cursor: pointer;
    background-color: red;
}
.delete:hover {
    background-color: blue;
}
</style>