<script setup>

import {ref, onMounted} from 'vue'

import { formulate_time } from '../../utils/tools';

import {
    delete_student_request, 
    post_user_image_request,
    get_user_image_request,
    hr_update_request,
} from '@/api/api';   

import { post_list } from '../../utils/data';

import { URL } from '../../api/config';

const apiURL = URL + '/media/'

const props = defineProps(['hr'])
const emit  = defineEmits(['close'])

const hr   = ref(props.hr)
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
const hrId = ref(props.hr.userId)

const isEdit = ref(false)
const userImage = ref([])
const is_show_image = ref(false)
const show_image = ref('')

const image = ref()
const image_url = ref()

onMounted(async function() {
    refresh_user_image()
})

async function refresh_user_image() {
    var value = await get_user_image_request({'userId': hrId.value})
    if(value.status == false) {
        alert(value.message)
    } else {
        console.log(value.data)
        userImage.value = value.data
    }
}

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

async function post_user_image() {
    var value = await post_user_image_request(hrId.value, image.value)
    if (value.status == true) {
        alert(value.message)
        refresh_user_image()
    } else {
        alert(value.message)
    }
}

function uploadImage(e) {
    if (!e.target.files[0].size) return;
    if (e.target.files[0].type.indexOf('image') === -1) {
        alert('请上传图片文件');
        return;
    } else {
        const reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        reader.onload = function(e) {
            image_url.value = e.target.result;
        };
        image.value = e.target.files[0];
    }
    post_user_image()
}

async function hr_update() {

    if (new_hr.value.username == '') {alert('姓名不能为空');return}
    if (new_hr.value.userId == '') {alert('学号不能为空');return}
    if (new_hr.value.phone == '') {alert('电话号码不能为空');return}
    if (new_hr.value.age == '') {alert('年龄不能为空');return}
    if (
        new_hr.value.username == hr.value.username &&
        new_hr.value.stage == hr.value.stage &&
        new_hr.value.userId == hr.value.userId &&
        new_hr.value.phone == hr.value.phone && 
        new_hr.value.age == hr.value.age &&
        new_hr.value.account == hr.value.account &&
        new_hr.value.accountHolderName == hr.value.accountHolderName &&
        new_hr.value.bankCard == hr.value.bankCard &&
        new_hr.value.bank == hr.value.bank &&
        new_hr.value.idCard == hr.value.idCard &&
        new_hr.value.city == hr.value.city
    ) {
        return
    }
    if (!confirm('确定修改吗？')) return
    var value = await hr_update_request(new_hr.value)
    if (value.status == true) {
        alert(value.message)
        hr.value = new_hr.value
    } else {
        alert(value.message)
    }
    refresh()
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
        <div class="title">在线HR简介</div>
    </div>
    <div class="hr-information">
        <div class="hr-left">
            <label v-if="isEdit && userImage.length != 0" class="images">
                <img :src="apiURL + userImage[0].fields.image" >
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
            <div v-else-if="userImage != ''" class="hr-avatar">
                <img :src="apiURL + userImage[0].fields.image" >
            </div>
            <label v-else for="image-file" class="hr-avatar">
                点击上传
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
        </div>
        <div v-if="isEdit" class="hr-right">
            <form>
                <div class="hr-name">姓名: <input type="text" v-model="new_hr.username"></div>
                <div class="hr-city">所在城市: <input type="text" v-model="new_hr.city"></div>
                <!-- <div class="hr-id">用户ID: <input type="text" v-model="new_hr.userId"></div> -->
                <div class="hr-phone">电话号码: <input type="text" v-model="new_hr.phone"></div>
                <div class="hr-age">年龄: <input type="text" v-model="new_hr.age"></div>
                <div class="hr-gender">性别: 
                    <select v-model="new_hr.gender">
                        <option value="男">男</option>
                        <option value="女">女</option>
                    </select>
                </div>
                <div class="hr-account">管理账号:
                    <select v-model="new_hr.account">
                        <option value="BOSS白">BOSS白</option>
                        <option value="BOSS乔">BOSS乔</option>
                    </select>
                </div>
                <div class="hr-bank-card">银行卡号: <input type="text" v-model="new_hr.bankCard"></div>
                <div class="hr-bank">开户行: <input type="text" v-model="new_hr.bank"></div>
                <div class="hr-account-holder-name">开户人姓名: <input type="text" v-model="new_hr.accountHolderName"></div>
                <div class="hr-id-card">身份证号: <input type="text" v-model="new_hr.idCard"></div>
            </form>
        </div>
        <div v-else class="hr-right">
            <div class="hr-name">姓名: {{ hr.username }}</div>
            <div class="hr-id">所在城市: {{ hr.city }}</div>
            <div class="hr-phone">电话号码: {{ hr.phone }}</div>
            <!-- <div class="hr-score">已面个数: {{  }}</div> -->
            <div class="hr-age">年龄: {{ hr.age }}</div>
            <div class="hr-gender">性别: {{ hr.gender }}</div>
            <div class="hr-account">管理账号: {{ hr.account }}</div>
            <!-- <div class="hr-bank-card">银行卡号: {{ hr.bankCard }}</div> -->
            <!-- <div class="hr-bank">开户行: {{ hr.bank }}</div> -->
            <div class="hr-account-holder-name">开户人姓名: {{ hr.accountHolderName }}</div>
            <!-- <div class="hr-id-card">身份证号: {{ hr.idCard }}</div> -->
            <!-- <div class="hr-register-time">注册时间: {{ formulate_time(hr.date_joined) }}</div> -->
            <div class="hr-last-login">上次登录时间: {{ formulate_time(hr.last_login) }}</div>
        </div>
    </div>
    
    <div class="bottom-bar">
        <div v-if="isEdit" class="bottom-bar-item" id="close-button" @click="isEdit = !isEdit">返回</div>
        <div v-else class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <div v-if="isEdit" class="bottom-bar-item" id="save-button" @click="hr_update();isEdit = !isEdit">保存</div>
        <div v-else class="bottom-bar-item" id="edit-button" @click="isEdit = !isEdit">编辑</div>
        <div class="bottom-bar-item" id="delete-button" @click="delete_hr">删除HR</div>
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
    justify-content: center;
    align-items: center;
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