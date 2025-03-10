<script setup>

import {ref} from 'vue'

import { get_students_list_request} from '../api/api';

const studentList = ref()
// const patientList = ref()

async function get_students_list() {
    studentList.value = await get_students_list_request()
}

// async function get_all_patient() {
//     patientList.value = await get_all_patient_request()
// }

</script>

<template>
<div></div>

<div id='main'>
    <div class="container" >
        <div class="student">
            <div class="get-student" @click="get_students_list">获取所有学生</div>
            <div class="student-list">
                <div class="student-item" v-for="student in studentList">
                    <div class="information" id="account-id">学号: {{ student.accountId }}</div>
                    <div class="information" id="username">姓名: {{ student.username }}</div>
                    <div class="information" id="password">密码: {{ student.password }}</div>
                    <div class="information" id="date-joined">创建时间: {{ student.date_joined }}</div>
                    <div class="information" id="last-login">最后登录时间: {{ student.last_login }}</div>
                </div>
            </div>
        </div>
    </div>
    <!-- <div class="container" >
        <div class="patient">
            <div class="get-patient" @click="get_all_patient">获取所有患者</div>
            <div class="patient-list">
                <div class="patient-item" v-for="patient in patientList">
                    <div class="information" id="name">患者姓名: {{ patient.name }}</div>
                    <div class="information" id="phone">患者电话: {{ patient.phone }}</div>
                    <div class="information" id="student">所属诊所: {{ patient.student }}</div>
                    <div class="information" id="birthday">患者生日: {{ patient.birthday }}</div>
                    <div class="information" id="description">患者简介: {{ patient.description }}</div>
                    <div class="information" id="register-time">患者创建时间: {{ patient.registerTime }}</div>
                    <div class="information" id="mouth-image-number">患者口腔图片数量: {{ patient.mouthImageNumber }}</div>
                </div>
            </div>
        </div>
    </div> -->
</div>

</template>

<style scoped>
#main {
    width: 100%;
    height: 1000px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.container {
    display: flex;
}
.student, .patient {
    margin: 20px;
    /* height: 600px; */
    width: 400px;
    background-color: beige;
    margin-left: 20px;
}
.get-student, .get-patient {
    cursor: pointer;
}
.student-item, .patient-item {
    margin: 10px;
    padding: 10px;
    border: 1px solid black;
}
</style>