<script setup>

import {ref, onMounted} from 'vue'

import {
    delete_student_request, 
    post_user_image_request,
    get_user_image_request,
    student_update_request,
} from '@/api/api';   

const apiURL = 'http://localhost:8000/media/'

const props = defineProps(['student'])
const emit  = defineEmits(['close'])

const student   = ref(props.student.fields)
const new_student = ref({
    'username': student.value.username,
    'stage': student.value.stage,
    'userId': student.value.userId,
    'phone': student.value.phone,
})
const studentId = ref(props.student.fields.userId)

const isEdit = ref(false)
const userImage = ref([])
const is_show_image = ref(false)
const show_image = ref('')

const image = ref()
const image_url = ref()


const student_stage = ref({
    0: "群众",
    1: "团员",
    2: "积极分子",
    3: "发展对象",
    4: "预备党员",
    5: "党员",
})

onMounted(async function() {
    refresh_user_image()
})

async function refresh_user_image() {
    var value = await get_user_image_request({'userId': studentId.value})
    if(value.status == false) {
        alert(value.message)
    } else {
        console.log(value.data)
        userImage.value = value.data
    }
}

async function delete_student() {
    if(!confirm('确定删除' + student.value.username + '吗？ 包括相关的活动和活动图片')) return;
    var value = await delete_student_request({'studentId': studentId.value})
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
        emit('close')

    } else {
        alert(value.message)
    }
}

async function post_user_image() {
    var value = await post_user_image_request(studentId.value, image.value)
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

async function student_update() {

    if (new_student.value.username == '') {
        alert('姓名不能为空')
        return
    }
    if (new_student.value.userId == '') {
        alert('学号不能为空')
        return
    }
    if (new_student.value.phone == '') {
        alert('电话号码不能为空')
        return
    }
    if (
        new_student.value.username == student.value.username &&
        new_student.value.stage == student.value.stage &&
        new_student.value.userId == student.value.userId &&
        new_student.value.phone == student.value.phone
    ) {

        return
    }
    if (!confirm('确定修改吗？')) return
    var value = await student_update_request(new_student.value)
    if (value.status == true) {
        alert(value.message)
        student.value = new_student.value
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
        <div class="title">党员简介</div>
    </div>
    <div class="student-information">
        <div class="student-left">
            <label v-if="isEdit" class="images">
                <img :src="apiURL + userImage[0].fields.image" >
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
            <div v-else-if="userImage != ''" class="student-avatar">
                <img :src="apiURL + userImage[0].fields.image" >
            </div>
            <label v-else for="image-file" class="student-avatar">
                点击上传
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
        </div>
        <div v-if="isEdit" class="student-right">
            <form>
                <div class="student-name">姓名: <input type="text" v-model="new_student.username"></div>
                <div class="student-stage">身份: 
                    <select v-model="new_student.stage">
                        <option v-for="(value, key) in student_stage" :value="key">{{ value }}</option>
                    </select>
                </div>
                <div class="student-id">学号: <input type="text" v-model="new_student.userId"></div>
                <div class="student-phone">电话号码: <input type="text" v-model="new_student.phone"></div>
            </form>
        </div>
        <div v-else class="student-right">
            <div class="student-name">姓名: {{ student.username }}</div>
            <div class="student-stage">身份: {{ student_stage[student.stage] }}</div>
            <div class="student-id">学号: {{ student.userId }}</div>
            <div class="student-phone">电话号码: {{ student.phone }}</div>
            <div class="student-score">活动个数: {{ student.score_test1 }}</div>
            <div class="student-register-time">注册时间: {{ student.date_joined }}</div>
            <div class="student-last-login">上次登录时间: {{ student.last_login }}</div>
        </div>
    </div>
    
    <div class="bottom-bar">
        <div class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <div v-if="isEdit" class="bottom-bar-item" id="save-button" @click="student_update();isEdit = !isEdit">保存</div>
        <div v-else class="bottom-bar-item" id="edit-button" @click="isEdit = !isEdit">编辑</div>
        <div class="bottom-bar-item" id="delete-button" @click="delete_student">删除党员</div>
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
.student-information {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.student-left {
    display: flex;
    justify-content: center;
    align-items: center;
}
.student-left img{
    object-fit: cover;
    object-position: center;
}
.student-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background-color: rgb(167, 167, 211, 0.5);
    border-radius: 50%;
    cursor: pointer
}
.student-avatar img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
}
.student-right {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}
.student-right input {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.student-right select {
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
.student-3d-images {
    display: flex;
    flex-direction: row;
    margin-right: 10px;
    cursor: pointer;
}
.student-3d-images .model3d {
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