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

import { URL } from '../../api/config';

const apiURL = URL

const props = defineProps(['interview'])
const emit  = defineEmits(['close'])

const interview   = ref(props.interview)
const new_interview = ref({
    'id': interview.value.id,
    'name': interview.value.name,
    'hr': interview.value.hr,
    'commuteTime': interview.value.commuteTime,
    'interview_time': interview.value.interview_time,
    'isAgreed': interview.value.isAgreed == true ? '1' : '0',
    'isArrived': interview.value.isArrived == true ? '1' : '0',
    'post': interview.value.post,
})
const hrId = ref(props.interviewuserId)

const isEdit = ref(false)
const userImage = ref([])
const is_show_image = ref(false)
const show_image = ref('')

const image = ref()
const image_url = ref()

const hr_list = ref([])

// onMounted(async function() {
//     refresh_curriculumVitae_image()
// })

// async function refresh_curriculumVitae_image() {
//     var value = await get_curriculumVitae_image_request({'userId': hrId.value})
//     if(value.status == false) {
//         alert(value.message)
//     } else {
//         console.log(value.data)
//         userImage.value = value.data
//     }
// }

async function delete_interview() {
    if(!confirm('确定删除题目' + interview.value.id + '吗？ 包括相关的图片')) return;
    var value = await delete_interview_request({'interviewId': interview.value.id})
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
        emit('close')

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

async function interview_update() {
    if (
        new_interview.value.name == interview.value.name &&
        new_interview.value.post == interview.value.post &&
        new_interview.value.hr == interview.value.hr &&
        new_interview.value.commuteTime == interview.value.commuteTime &&
        new_interview.value.interview_time == interview.value.interview_time &&
        new_interview.value.isAgreed == interview.value.isAgreed &&
        new_interview.value.isArrived == interview.value.isArrived
    ) {
        return
    }
    if (!confirm('确定修改吗？')) return
    var value = await interview_update_request(new_interview.value)
    if (value.status == true) {
        alert(value.message)
        interview.value = new_interview.value
        refresh()
    } else {
        alert(value.message)
    }
    isEdit = !isEdit
    refresh()
}

function refresh() {
    window.location.reload()
}
async function getHRList() {
    var value = await get_hr_list_request()
    if(value.status == false) {
        alert(data.message)
    } else {
        hr_list.value = value.data
    }
}
getHRList()
</script>

<template>
<div></div>

<div id='main'>
    <div class="show-image" v-if="is_show_image">
        <img :src="show_image" alt="image" @click="is_show_image = false">
    </div>
    <div class="navigation-bar">
        <div class="title">约面信息</div>
    </div>
    <div class="interview-information">
        <div class="interview-image">
            <label v-if="isEdit && interview.file_url != null" class="images">
                <img :src="apiURL + interview.file_url" >
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
            <div v-else-if="interview.file_url != null" class="interview-avatar">
                <img :src="apiURL + interview.file_url" >
            </div>
            <label v-else for="image-file" class="interview-avatar">
                点击上传
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
        </div>
        <div v-if="isEdit" class="interview-right">
            <form>
                <div class="interview-id">面试者姓名: <input type="text" v-model="new_interview.name"></div>
                <div class="interview-post">岗位: 
                    <select v-model="new_interview.post">
                        <option v-for="post_type in post_list">
                            {{ post_type }}
                        </option>
                    </select>
                </div>
                <div class="interview-answer">HR:
                    <select v-model="new_interview.hr">
                        <option v-for="hr in hr_list">
                            {{ hr.username }}
                        </option>
                    </select>
                </div>
                <div class="interview-num-test">通勤时间(分钟/M): <input type="number" v-model="new_interview.commuteTime"></div>
                <div class="interview-num-test">约面时间: <input type="datetime-local" v-model="new_interview.interview_time"></div>
                <div class="interview-num-test">是否通过面试:
                    <select v-model="new_interview.isAgreed">
                        <option value="1">是</option>
                        <option value="0">否</option>
                    </select>
                </div>
                <div class="interview-num-test">是否到场面试过:
                    <select v-model="new_interview.isArrived">
                        <option value="1">是</option>
                        <option value="0">否</option>
                    </select>
                </div>

            </form>
        </div>
        <div v-else class="interview-right">
            <div class="interview-id">面试者姓名: {{ interview.name }}</div>
            <div class="interview-post">岗位: {{ interview.post }}</div>
            <div class="interview-num-test">HR: {{ interview.hr }}</div>
            <div class="interview-num-test">通勤时间(分钟/M): {{ interview.commuteTime }}</div>
            <div class="interview-num-test">约面时间: {{ interview.interview_time }}</div>
            <div class="interview-time">创建时间: {{ formulate_time(interview.create_time) }}</div>
            <div class="interview-num-test">是否通过面试:</div>
            <div v-if="interview.isAgreed == true" class="interview-state">
                <img src="@img/tongguo.png" alt="通过">
            </div>
            <div v-else class="interview-state">
                <img src="@img/butongguo.png" alt="错误">
            </div>
            <div class="interview-pass-rate">是否面试过:</div>
            <div v-if="interview.isArrived == true" class="interview-state">
                <img src="@img/tongguo.png" alt="通过">
            </div>
            <div v-else class="interview-state">
                <img src="@img/butongguo.png" alt="错误">
            </div>
            <div class="interview-settlement">是否结算</div>
            <div v-if="interview.settlement == true" class="interview-state">
                <img src="@img/tongguo.png" alt="通过">
            </div>
            <div v-else class="interview-state">
                <img src="@img/butongguo.png" alt="错误">
            </div>
        </div>
    </div>
    
    <div class="bottom-bar">
        <div v-if="isEdit" class="bottom-bar-item" id="close-button" @click="isEdit = !isEdit">返回</div>
        <div v-else class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <div v-if="isEdit" class="bottom-bar-item" id="save-button" @click="interview_update()">保存</div>
        <div v-else class="bottom-bar-item" id="edit-button" @click="isEdit = !isEdit">编辑</div>
        <div class="bottom-bar-item" id="delete-button" @click="delete_interview">删除约面</div>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 500px;
    height: 400px;
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
.interview-information {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.interview-image {
    display: flex;
    justify-content: center;
    align-items: center;
}
.interview-image img{
    object-fit: cover;
    object-position: center;
}
.interview-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background-color: rgb(167, 167, 211, 0.5);
    cursor: pointer
}
.interview-avatar img {
    width: 200px;
    height: 320px;
}
.interview-right {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}
.interview-right input {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.interview-right select {
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
.interview-state img{
    width: 30px;
    height: 30px;
}
.interview-3d-images {
    display: flex;
    flex-direction: row;
    margin-right: 10px;
    cursor: pointer;
}
.interview-3d-images .model3d {
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