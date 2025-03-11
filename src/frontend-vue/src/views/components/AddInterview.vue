<script setup>

import { ref } from 'vue'

import { 
    create_interview_request,
    post_activity_image_request,
    get_hr_list_request,
 } from '@/api/api';

import { post_list } from '../../utils/data';

const props = defineProps(['user'])
const emit  = defineEmits(['close'])

const interview_name        = ref()
const interview_post        = ref()
const inetrvew_commute_time = ref()
const interview_hr          = ref()
const interview_time        = ref()
const student_name          = ref(props.user.username)

const hr_list     = ref([])
const hr_username = ref()


const image     = ref()
const image_url = ref()

const is_show_image = ref(false)
const show_image    = ref('')

const message = ref()

async function create_activity() {

    if (
    interview_name.value        == undefined ||
    interview_post.value        == undefined ||
    inetrvew_commute_time.value == undefined ||
    interview_time.value        == undefined ||
    interview_hr.value          == undefined ||
    image.value    == null) {
        message.value = '请完整填写题目'
        return
    }

    console.log(props.user.userId)
    console.log(student_name.value)
    console.log(interview_name.value)
    console.log(interview_post.value)


    var data = {
        'name'       : interview_name.value,
        'post'       : interview_post.value,
        'commuteTime': inetrvew_commute_time.value,
        'time'       : interview_time.value,
        'hr'         : interview_hr.value,
    }
    var value = await create_interview_request(data, image.value)
    if (value.status == true) {
        message.value = value.message
        // await post_activity_image(value.data.activityId)
        alert(value.message)
        window.location.reload()
        emit('close')
    } else {
        alert(value.message)
        message.value = value.message
    }
}

function delete_image(imageId) {
    if (!confirm('确定删除这张图片吗？')) return;
    image.value = null;
    image_url.value = null;
}

function open_image(image) {

    is_show_image.value = true;
    show_image.value = image;
}

async function post_activity_image(activity_id) {
    for (let i = 0; i < image.value.length; i++) {
        var value = await post_activity_image_request(activity_id, image.value[i])
        if (value.status == false) {
            alert(value.message)
            return;
        }
    }
}

function uploadImage(e) {
    if (!e.target.files[0].size) return;
    const reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function(e) {
        image_url.value = e.target.result;
    };
    image.value = e.target.files[0];
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
    <div class="title">添加约面</div>
    <div class="show-image" v-if="is_show_image">
        <img :src="show_image" alt="image" @click="is_show_image = false">
    </div>
    <div class="add-activity" v-else>
        <div class="form">
            <div class="form-left">
                <div class="question-images">
                    <div class="image-list">
                        <div v-if="image != null" class="images">
                            <span class="delete" @click="delete_image(index)"></span>
                            <img :src="image_url" alt="image" @click="open_image(image)">
                        </div>
                        <div v-else id="box">
                            <!-- 点击label后也会出现和点击button一样的效果其label中的for的值是服务元素的Id，绑定指定id的元素，点击label后会激活相应的控件  -->
                            <label class="box-label" for="image-file">
                                <i class="upload"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">
                                    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                                    <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                                </svg></i>
                            <input type="file" single accept=".pdf, .doc, .docx, .rtf, .txt, image/*" value="" id="image-file" @change="uploadImage($event)">上传简历
                            </label>
                        <!-- </svg></i> <input type="file" single accept="image/*" value="" id="image-file">上传图片</label> -->
                            <div id="progress"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="form-right">
                <div class="form-item">
                    <div class="form-item-label">姓名</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入姓名" v-model="interview_name">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">面试岗位</div>
                    <div class="form-item-input">
                        <!-- {{ interview_post }} -->
                        <select name="postType" id="post-type" v-model="interview_post">
                            <option v-for="post_type in post_list">
                                {{ post_type }}
                            </option>
                        </select>
                        <!-- <input type="text" placeholder="请选择活动类型" v-model="interview_post"> -->
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">HR</div>
                    <div class="form-item-input">
                        <select name="hr" id="hr" v-model="interview_hr">
                            <option v-for="hr in hr_list">
                                {{ hr.username }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">通勤时间(分钟/M)</div>
                    <div class="form-item-input">
                        <input type="number" placeholder="请输入通勤时间" v-model="inetrvew_commute_time">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">面试时间</div>
                    <div class="form-item-input">
                        <input type="datetime-local" placeholder="请输入面试时间" v-model="interview_time">
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="message">
        {{ message }}
    </div>
    <div class="buttons">
        <div class="add-activity-button" @click="$emit('close')">取消</div>
        <div class="add-activity-button" @click="create_activity">确认</div>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 600px;
    background-color: white;
    display: flex;
    flex-direction: column;
    margin-bottom: 400px;
    border-radius: 20px;
    padding: 10px;
    padding-left: 30px;
    padding-right: 30px;
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
}
.title{
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
    text-align: center;
    font-family: "SanJiXinWeiBeiJian-2";
}
.add-activity {
    border: 1px solid black;
    border-radius: 10px;
    padding: 10px;
}
.form {
    display: flex;
    flex-direction: row;
    justify-content: space-around;

}
.form-item {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: start;
    margin-bottom: 10px;
}
.form-item-label {
    margin-right: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.form-item-input {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.form-item-input input {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
}
.form-item-input select {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
}
.form-item-input textarea {
    margin-top: 10px;
    border: 1px solid black;
    border-radius: 5px;
    width: 300px;
    font-size: 14px;
}
#activity-content {
    height: 100px;
    word-wrap: break-word;
}
#form-description {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: start;
    margin-bottom: 10px;
}
.question-images {
    display: flex;
    justify-content: center;
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
    width: 200px;
    height: 300px;
}
.delete {
    position: absolute;
    top: 5px;
    right: 5px;
    background: red;
    color: white;
    font-size: 14px;
    cursor: pointer;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition-duration: 0.3s;
}
.delete:hover {
    background: red;
    transform: scale(1.1);
    transition-duration: 0.3s;
}
#box {
    display: flex; 
    flex-direction: column;
}
.box-label {
    width: 200px;
    height: 280px;
}
.buttons {
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
}
.add-activity-button {
    cursor: pointer;
    width: 80px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 60px;
    border: 1px solid black;
    border-radius: 5px;
    transition: background-color 0.5s, transform 0.5s;
}
.add-activity-button:hover {
    background-color: #6990f2;
    transform: scale(1.1);
}
.message {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 30px;
    color: red;
    font-size: 14px;
    font-weight: bold;
}
</style>