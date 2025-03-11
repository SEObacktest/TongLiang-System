<script setup>

import {ref, onMounted} from 'vue'

import { formulate_time } from '../../utils/tools';

import {
    delete_interview_request, 
    post_curriculumVitae_image_request,
    get_curriculumVitae_image_request,
    interview_update_request,
    get_hr_list_request,
} from '@/api/api';   

import { post_list } from '../../utils/data';

import Settle from './Settle.vue';

import { URL } from '../../api/config';

const apiURL = URL

const props = defineProps(['salary'])
const emit  = defineEmits(['close'])

const salary   = ref(props.salary)

const showInterview = ref(false)
const showSettle = ref(false)
const specificInterview = ref()

const selectedInterviewList = ref([])

function open_interview_detail(interview) {
    showInterview.value = true
    specificInterview.value = interview
}

function open_settle_detail() {
    showSettle.value = true
}

function settle_account(value) {
    selectedInterviewList.value = []
    selectedInterviewList.value.push(value)
    showSettle.value = true
}

function settle_account_list(value) {
    selectedInterviewList.value = []
    for (let i = 0; i < value.length; i++) {
        selectedInterviewList.value.push(value[i])
    }
    console.log(selectedInterviewList.value)
    showSettle.value = true
}

</script>

<template>
<div></div>

<div id='main'>

    <Settle v-if="showSettle" :interviewList="selectedInterviewList" :hr="salary.hr" @close="showSettle=false"></Settle>

    <div v-if="showInterview" class="interview-detail">
        <div class="information">
            <div class="curriculum-vitae">
                <img :src="apiURL + specificInterview.file_url " alt="简历">
            </div>
            <div class="detail">
                <div>约面ID: {{ specificInterview.id }}</div>
                <div>姓名: {{ specificInterview.name }}</div>
                <div>HR: {{ specificInterview.hr }}</div>
                <div>岗位: {{ specificInterview.post }}</div>
                <div>通勤时间(分钟/M): {{ specificInterview.commuteTime }}</div>
                <div>创建时间: {{ formulate_time(specificInterview.create_time) }}</div>
                <div>面试时间: {{ formulate_time(specificInterview.interview_time) }}</div>
                <div v-if="specificInterview.isAgreed == true" class="interview-state">
                    <img src="@img/tongguo.png" alt="通过">
                </div>
                <div v-else class="interview-state">
                    <img src="@img/butongguo.png" alt="错误">
                </div>
                <div class="interview-pass-rate">是否面试过:</div>
                <div v-if="specificInterview.isArrived == true" class="interview-state">
                    <img src="@img/tongguo.png" alt="通过">
                </div>
                <div v-else class="interview-state">
                    <img src="@img/butongguo.png" alt="错误">
                </div>
            </div>
        </div>
        <div class="button-bar">
            <div class="button" @click="showInterview=false">关闭</div>
            <div class="button" id="settle"  @click="settle_account(specificInterview)">结算</div>
        </div>
    </div>

    <div class="title">
        <div class="header">HR {{ salary.hr.username }}的待结算明细</div>
        <div class="sum">合计: {{ salary.salaryInformation.price }}元</div>
    </div>
    <!-- {{ salary }} -->
      <!-- {{ salary.interviewList[0].file_url }} -->
    <div class="container">
        <div class="container-item" id="header">
            <div >面试ID</div>
            <div >面试者姓名</div>
            <div >岗位</div>
            <div >创建时间</div>
            <div >详情</div>
        </div>
        <div v-for="item in salary.interviewList"
            class="container-item"
            id="item">
            <div>{{ item.id }}</div>
            <div>{{ item.name }}</div>
            <div>{{ item.post }}</div>
            <div>{{ formulate_time(item.create_time) }}</div>
            <div @click="open_interview_detail(item)" class="button" id="detail">查看详情</div>
        </div>
    </div>
    <div class="button-bar">
        <div class="button" @click="$emit('close')">关闭</div>
        <div class="button" id="settle"  @click="settle_account_list(salary.interviewList)">结算</div>
    </div>

</div>

</template>

<style scoped>
#main {
    width: 700px;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 200px;
    padding: 10px;
    border-radius: 20px;
}
.interview-detail {
    position: absolute;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 600px;
    height: 400px;
    /* background-color: rgba(0, 0, 0, 0.5); */
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: space-around;
    background-color: white;
    border-radius: 10px;
    padding: 10px;
}
.information {
    width: 100%;
    display: flex;
    justify-content: space-around;
}
.curriculum-vitae {
    width: 200px;
    height: 300px;
    border: 1px solid black;
    border-radius: 10px;
    overflow: hidden;
}
.curriculum-vitae img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.detail {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}
.interview-state img{
    width: 30px;
    height: 30px;
}
.button-bar {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
    margin-top: 10px;
}
.title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-around;
    font-family: "SanJiXinWeiBeiJian-2";
}
.sum {
    color: red;
}
.container {
    min-height: 320px;
    display: flex;
    flex-direction: column;
    border: 1px solid black;
    border-radius: 10px;
    padding: 10px;
    overflow-y: auto;
}
.container-item {
    margin-top: 10px;
    padding-bottom: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    border-bottom: 1px solid black;
}
.container-item div {
    flex: 1;
    text-align: center;
}
.container #header {
    font-weight: bold;
    font-size: 18px;
}
.button {
    width: 80px;
    height: 30px;
    font-size: 20px;
    line-height: 30px;
    margin-right: 10px;
    text-align: center;
    cursor: pointer;
    background-color: rgb(110, 185, 208);
    border-radius: 5px;
    transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.button:hover {
    background-color: rgb(0, 195, 255);
    transform: scale(1.1);
}
#settle:hover {
    background-color: green;
}
#detail {
    font-size: 16px;
}
</style>