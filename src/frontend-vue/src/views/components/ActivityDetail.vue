<script setup>

import {ref, onMounted, watch} from 'vue'

import {
    delete_activity_request, 
    post_activity_image_request, 
    get_activity_images_request,
    get_students_list_request,
    certified_activity_request,
} from '@/api/api';   

const apiURL = 'http://localhost:8000/media/'

const props = defineProps(['activity', 'user'])
const emit  = defineEmits(['close'])

const activity_type_color = ref({
    "志愿活动": "rgb(0, 195, 255)",
    "党日活动": "rgb(0, 255, 157)",
    "其他": "rgb(255, 225, 0)",
})

const activity   = ref(props.activity.fields)
const activityImageList = ref([])
const activityId = ref(props.activity.pk)

const isEdit = ref(false)

const is_show_image = ref(false)
const show_image = ref('')

const studentList = ref([])
const studentNameList = ref([])

const user = ref(props.user)

onMounted(async function() {
    refresh_activity_image()
    get_students_list()
})

async function get_students_list() {
    var value = await get_students_list_request()
    if(value.status == false) {
        alert(value.message)
    } else {
        studentList.value = value.data
        studentList.value.forEach(e => {
            studentNameList.value[e.pk] = e.fields.username
        });
    }
}

async function refresh_activity_image() {
    var value = await get_activity_images_request({'activityId': activityId.value})
    if(value.status == false) {
        alert(value.message)
    } else {
        console.log(value.data)
        activityImageList.value = value.data
    }
}

async function post_activity_image(e) {
    var file = e.target.files[0]
    var value = await post_activity_image_request(activityId.value, file)
    if (value.status == true) {
        alert(value.message)
        refresh_activity_image()
    } else {
        alert(value.message)
    }
}

function open_image(image) {

    is_show_image.value = true;
    show_image.value = image;
}

async function delete_activity() {
    if(!confirm('确定删除' + activity.value.name + '吗？ 包括相关的活动图片')) return;
    var value = await delete_activity_request({'activityId': activityId.value})
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
        emit('close')

    } else {
        alert(value.message)
    }
}

async function certified_activity(is_certified) {
    if(!confirm('确定' + (is_certified ? '合格' : '不合格') + '吗？')) return;
    var value = await certified_activity_request({
        'activityId': activityId.value,
        'passed': is_certified,
        'adminId': user.value.userId,
    })
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
    } else {
        alert(value.message)
    }
}

</script>

<template>
<div></div>

<div id='main'>
    <div class="show-image" v-if="is_show_image">
        <img :src="show_image" alt="image" @click="is_show_image = false">
    </div>
    <div class="navigation-bar">
        <div class="title">{{ activity.name }}</div>
    </div>
    <div class="activity-information">
        <div class="activity-left">
            <div class="activity-avatar"></div>
            <div class="activity-student">学生: {{ studentNameList[activity.student] }}</div>
            <div class="activity-register-time">活动提交时间: {{ activity.registerTime }}</div>
            <div class="activity-start-time">活动开始时间: {{ activity.startTime }}</div>
            <div class="activity-start-time">活动结束时间: {{ activity.startTime }}</div>
            <div class="activity-type">
                <div>活动类型: </div>
                <div class="activity-type-detail" :style="{backgroundColor: (activity_type_color[activity.type])}">{{  activity.type }}</div>
            </div>
            <div class="activity-certified">通过认证:
                <img class="activity-status" v-if="!activity.certified"  src="@img/dengdaiyanzheng.png">
                <img class="activity-status" v-else-if="activity.passed" src="@img/tongguo.png">
                <img class="activity-status" v-else src="@img/butongguo.png">
            </div>
        </div>
        <div class="activity-right">
            <div class="activity-location">活动地点: {{ activity.location }}</div>
            <div class="description">
                活动心得: 
                <div class="description-content">
                    {{ activity.description }}
                </div>
            </div>
        </div>
    </div>
    <div class="activity-images">
        <div class="title">活动图片: </div>
        <div class="image-list">
            <div class="images" v-for="(image, index) in activityImageList" :key="index">
                <div v-if="isEdit" class="delete" @click="delete_activity_image(index)"></div>
                <img :src="apiURL + image.fields.image" alt="image" @click="open_image(apiURL + image.fields.image)">
            </div>
            <div v-if="isEdit" id="box" style="display: flex; flex-direction: column;">
                <!-- 点击label后也会出现和点击button一样的效果其label中的for的值是服务元素的Id，绑定指定id的元素，点击label后会激活相应的控件  -->
                <label for="image-file"><i class="upload"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
                    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                    <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                </svg></i> <input type="file" single accept="image/*" value="" id="image-file" @change="post_activity_image">上传图片</label>
                <div id="progress"></div>
            </div>
        </div>
    </div>
    <div v-if="user.is_admin && !activity.certified" class="certified">
            <div class="check-title">是否合格(可以通过): </div>
            <div class="certified-input">
                <div class="certified-button" id="certified-yes" @click="certified_activity(true)">合格</div>
                <div class="certified-button" id="certified-no" @click="certified_activity(false)">不合格</div>
            </div>
        </div> 
    <div class="bottom-bar">
        <div class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <div class="bottom-bar-item" id="delete-button" @click="delete_activity">删除活动</div>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 600px;
    background-color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 400px;
    border-radius: 20px;
    padding-left: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
    padding-top: 10px;
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
.show-image img {
    width: 100%;
    height: 100%;
    z-index: 90;
}
.navigation-bar {
    display: flex;
    margin-bottom: 20px;
    justify-content: center;
}
.navigation-bar .title {
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 10px;
}
.activity-information {
    display: flex;
    flex-direction: row;
}
.activity-right {
    display: flex;
    flex-direction: column;
    margin-left: 100px;
}
.description-content {
    margin-top: 10px;
    margin-bottom: 10px;
    border: 1px solid black;
    border-radius: 5px;
    padding: 10px;
    height: 100px;
    overflow: auto;
}
.activity-type {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 10px;
}
.activity-type-detail {
    border: 1px solid black; 
    border-radius: 5px;
    height: 30px;
    width: 80px;
    margin-left: 10px;
    text-align: center;
    line-height: 30px;
}
.activity-certified {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 10px;
}
.activity-status {
    width: 50px;
    height: 50px;
    margin-left: 10px;
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
    margin-right: 10px;
    cursor: pointer;
}
.images img {
    width: 100px;
    height: 100px;
}
.activity-3d-images {
    display: flex;
    flex-direction: row;
    margin-right: 10px;
    cursor: pointer;
}
.activity-3d-images .model3d {
    width: 100px;
    height: 100px;
}
.check-title {
    font-size: 20px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 10px;
}
.certified-input {
    display: flex;
    justify-content: space-around;
    flex-direction: row;
}
.certified-button {
    cursor: pointer;
    width: 100px;
    height: 40px;
    border: 1px solid black;
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.5s;
}
#certified-yes {
    background-color: green;
}
#certified-no {
    background-color: red;
}
#certified-yes:hover {
    transform: scale(1.1);
}
#certified-no:hover {
    transform: scale(1.1);
}
</style>