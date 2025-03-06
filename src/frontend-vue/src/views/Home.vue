<script setup>

import { ref } from 'vue'

import router from '../router';

import {
    get_students_list_request, 
    is_login_request,
    export_excel_request,
} from '../api/api';

import Header         from './components/header/Header.vue';
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
    <Header :user="user"></Header>
    <Transition>
        <div v-if="isShowStudentDetail" class="container" :class="{ container_filter: isShowStudentDetail }">
            <StudentDetail :student="studentClicked" @close="isShowStudentDetail=false"></StudentDetail>
        </div>
    </Transition>
    <Transition>
        <div v-if="isShowAddActivity" class="container" :class="{ container_filter: isShowAddActivity }">
            <AddActivity :user="user" @close="isShowAddActivity=false"></AddActivity>
        </div>
    </Transition>
    <Transition>
        <div v-if="isShowActivityDetail" class="container" :class="{ container_filter: isShowActivityDetail }">
            <ActivityDetail :activity="activityClicked" :user="user" @close="isShowActivityDetail=false"></ActivityDetail>
        </div>
    </Transition>
    <div class="body">
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

        <div class="activity-container">
            <div class="activity-menu">
                <div class="activity-container-title">活动搜索列表</div>
                <div class="add-buttons">
                    <div class="add-button" @click="refresh">刷新</div>
                    <div class="add-button" @click="isShowAddActivity=true">添加活动</div>
                    <div v-if="user.is_admin" class="add-button" @click="exportInformation">导出信息</div>
                </div>
            </div>
            <div class="split-line"></div>
            <div class="activity-list">
                <ActivityShort :user="user" ref="activityShort" @activity_clicked="(value) => open_activity_detail(value)"></ActivityShort>
            </div>
        </div>

    </div>

</div>
<Footer></Footer>
</template>

<style scoped>
#main {
    min-height: 1328px;
    display: flex;
    flex-direction: column;
    /* 一定要先制定background在加其他限制 */
    background: url("@img/home_background.jpg");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}
.body {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.container {
    height: 1300px;
    top: 100px;
    width: 100%;
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;

}
.container_filter {
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
    background-color: rgba(0, 0, 0, 0.3);
}
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
.user-information {
    display: flex;
    flex-direction: column;
    background-color: rgb(255, 255, 255, 0.9);
    height: 100%;
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
/* 下面我们会解释这些 class 是做什么的 */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>