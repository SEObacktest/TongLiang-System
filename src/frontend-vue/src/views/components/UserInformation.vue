<script setup>


import { ref } from 'vue'

import router from '../router';

import {
    get_students_list_request, 
    is_login_request,
    export_excel_request,
} from '../api/api';

import Header         from './components/header/Header.vue';
import SideBar        from './components/SideBar.vue';  
import AddActivity    from './components/AddActivity.vue';
import ActivityShort  from './components/ActivityShort.vue';
import StudentDetail  from './components/StudentDetail.vue';
import ActivityDetail from './components/ActivityDetail.vue';
import Footer         from './components/footer/Footer.vue';

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
            var value = await get_students_list_request()
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
    <div class="user-information">
        <div class="student-information">
            <div class="title">个人信息</div>
            <div class="split-line"></div>
            <div class="admin" v-if="user.is_admin">管理员</div>
            <div class="admin" v-else-if="user.isTeacher">教师</div>
            <div class="normal-info"><img src="@img/xingming.png" class="little_icon">
                {{ user.username }}
                <!-- <div class="profile" @click="open_student_detail(user)">编辑信息</div> -->
            </div>
            <div class="normal-info"><img src="@img/wxbzhanghu.png" class="little_icon"> {{ user.userId }}</div>
            <div class="normal-info"><img src="@img/dianhua.png" class="little_icon"> {{ user.phone }}</div>
            <div class="normal-info"><img src="@img/shenfenxinxi.png" class="little_icon"> {{ studentStage[user.stage] }}</div>
            <div>活动个数: {{ user.score_test1 }}</div>
        </div>
        <div v-if="user.is_admin" class="admin-information">
            <div class="split-line"></div>
            <div class="title">学生党员列表</div>
            <div class="student-list">
                <div class="student-item" v-for="student in studentList" @click="open_student_detail(student)">
                    {{ student.fields.username }}
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<style scoped>
.user-information {
    display: flex;
    flex-direction: column;
    background-color: rgb(255, 255, 255, 0.9);
    height: 500px;
    border-radius: 20px;
    margin-top: 20px;
}
.student-information {
    width: 200px;
    /* height: 100px; */
}
.user-information .title {
    font-size: 26px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
    text-align: center;
    font-family: "SanJiXinWeiBeiJian-2";
}
.student-information .admin {
    border: 1px solid black;
    border-radius: 5px;
    width: 60px;
    text-align: center;
    background-color: rgb(110, 185, 208);
    margin-left: 5px;
    margin-bottom: 10px;
}
.student-information .normal-info {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: 5px;
    margin-bottom: 10px;
}
.student-information .little_icon {
    width: 20px;
    height: 20px;
    margin-right: 5px;
}
.student-information .profile {
    border: 1px solid black;
    border-radius: 5px;
    padding: 2px;
    cursor: pointer;
    margin-left: 10px;
    background-color: rgb(110, 185, 208);
    transition: background-color 0.3s, transform 0.3s;
}
.student-information .profile:hover {
    background-color: rgb(59, 208, 188);
    transform: scale(1.1);
}
.admin-information {
    display: flex;
    flex-direction: column;
}
.student-list {
    display: flex;
    justify-content: center;
    overflow-y: auto;
    flex-flow: wrap;
    min-height: 100px;
    padding-bottom: 20px;
    width: 200px;
}
.student-item {
    cursor: pointer;
    background-color: rgb(59, 208, 188);
    margin-top: 10px;
    width: 70px;
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    text-align: center;
    font-size: 20px;
    margin-right: 10px;
    margin-left: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s, background-color 0.3s; /* 平滑过渡 */
}
.student-item:hover {
    background-color: rgb(110, 185, 208);
    transform: scale(1.2);
}
</style>