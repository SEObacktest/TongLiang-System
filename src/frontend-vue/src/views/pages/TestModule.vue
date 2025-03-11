<script setup>

import { ref } from 'vue'

import router from '@/router';

import {
    get_hr_list_request, 
    is_login_request,
    export_excel_request,
} from '@/api/api';

import ActivityShort  from '../components/ActivityShort.vue';

const user                 = ref("")
const isShowStudentDetail  = ref(false)
const isShowAddActivity    = ref(false)
const isShowActivityDetail = ref(false)
const activityShort        = ref()
const studentClicked       = ref()
const activityClicked      = ref()

const studentList = ref([])
const studentNameList = ref([])

const studentStage = ref({
    0: "群众",
    1: "团员",
    2: "积极分子",
    3: "发展对象",
    4: "预备党员",
    5: "党员",
})

function open_student_detail(student) {
    studentClicked.value = student
    isShowStudentDetail.value = true
}

function open_activity_detail(activity) {
    activityClicked.value = activity
    isShowActivityDetail.value = true
}

async function exportInformation() {
    if(!confirm('确定导出信息吗？')) return;
    var value = await export_excel_request({
        'studentId':'*',
    })
    if (value.status == true) {
        alert(value.message)
    } else {
        alert(value.message)
    }
    // alert("我还没做这个")
}

function refresh() {
    window.location.reload()
}

async function is_login() {
    var value = await is_login_request()
    if (value.status == true) {
        user.value = value.data
        if(user.value.is_admin == true){
            var value = await get_hr_list_request()
            if(value.status == false) {
                alert(data.message)
            } else {
                studentList.value = value.data
                studentList.value.forEach(e => {
                    studentNameList.value[e.pk] = e.fields.username
                });
            }
        }
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
    <div class="activity-container">
        <div class="activity-menu">
            <div class="activity-container-title">测试模块</div>
            <div class="add-buttons">
                <div class="add-button" @click="refresh">刷新</div>
                <div class="add-button" @click="isShowAddActivity=true">添加活动</div>
                <!-- <div v-if="user.is_admin" class="add-button" @click="exportInformation">导出信息</div> -->
            </div>
        </div>
        <div class="split-line"></div>
        <div class="activity-list">
            <ActivityShort :user="user" ref="activityShort" @activity_clicked="(value) => open_activity_detail(value)"></ActivityShort>
        </div>
    </div>
</div>

</template>

<style scoped>
.activity-container {
    width: 800px;
    /* height: 1000px; */
    display: flex;
    margin-left: 100px;
    flex-direction: column;
    /* background-color: red; */
    background-color: rgb(255, 255, 255, 0.7);
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
    border-radius: 10px;
    margin-top: 20px;
    margin-bottom: 20px;
}
.activity-menu {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}
.activity-container-title {
    font-size: 40px;
    font-weight: bold;
    margin-left: 100px;
    font-family: 'SanJiXinWeiBeiJian-2';
}
.add-buttons {
    display: flex;
    flex-direction: row;
}
.add-button {
    width: 80px;
    height: 100%;
    line-height: 40px;
    text-align: center;
    border: 1px solid black;
    border-radius: 5px;
    background-color: rgb(255, 255, 255);
    cursor: pointer;
    margin-right: 10px;
    transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.add-button:hover {
    background-color: rgb(110, 185, 208);
    transform: scale(1.1);
}
.split-line {
    width: 100%;
    height: 1px;
    background-color: rgb(0, 0, 0, 0.7);
    margin-top: 10px;
    margin-bottom: 10px;
}
.activity-list {
    width: 100%;
    height: 100%;
}
</style>