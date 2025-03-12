<script setup>

import { ref } from 'vue'

import router from '@/router';

import {
    get_hr_list_request, 
    is_login_request,
    export_excel_request,
} from '@/api/api';

import SettlementList from '../components/SettlementList.vue';
import SettlementDetail from '../components/SettlementDetail.vue';

const user                 = ref("")
const isShowStudentDetail  = ref(false)
const isShowAddHr    = ref(false)
const isShowHrDetail = ref(false)
const HRShort        = ref()
const studentClicked       = ref()
const settlementClicked      = ref()

const hrList = ref([])
const studentNameList = ref([])

function open_student_detail(student) {
    studentClicked.value = student
    isShowStudentDetail.value = true
}

function open_settlement_detail(hr) {
    console.log(hr)
    settlementClicked.value = hr
    isShowHrDetail.value = true
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
                hrList.value = value.data
                hrList.value.forEach(e => {
                    studentNameList.value[e.pk] = e.username
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
    <!-- {{ hrList[0].fields }} -->
    <Transition>
        <div v-if="isShowHrDetail" class="container" :class="{ container_filter: isShowHrDetail }">
            <SettlementDetail :settlement="settlementClicked" @close="isShowHrDetail=false"></SettlementDetail>
        </div>
    </Transition>
    <div class="activity-container">
        <div class="activity-menu">
            <div class="activity-container-title">流水管理</div>
            <div class="add-buttons">
                <div class="add-button" @click="refresh">刷新</div>
                <!-- <div class="add-button" @click="isShowAddHr=true">添加HR</div> -->
                <!-- <div v-if="user.is_admin" class="add-button" @click="exportInformation">导出信息</div> -->
            </div>
        </div>
        <div class="split-line"></div>
        <div class="activity-list">
            <SettlementList :user="user" ref="SettlementShort" @settlement_selected="(value) => open_settlement_detail(value)"></SettlementList>
        </div>
    </div>
</div>

</template>

<style scoped>
.container {
    height: 100vh;
    width: screen;
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
</style>