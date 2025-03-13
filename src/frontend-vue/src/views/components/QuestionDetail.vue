<script setup>

import {ref, onMounted} from 'vue'

import { formulate_time } from '../../utils/tools';

import {
    delete_question_request, 
    post_question_image_request,
    question_update_request,
} from '@/api/api';   

import { main_problem } from '../../utils/data';

import { URL } from '../../api/config';

const apiURL = URL

const props = defineProps(['question'])
const emit  = defineEmits(['close'])

const question   = ref(props.question)
const new_question = ref({
    'id': question.value.id,
    // 'post': question.value.post,
    'qualified': question.value.qualified == true ? '1' : '0',
    'mainProblem': question.value.main_problem,
    'problemDescription': question.value.problem_description,
})

const isEdit = ref(false)
const is_show_image = ref(false)
const show_image = ref('')

const image = ref()
const image_url = ref()

async function delete_question() {
    if(!confirm('确定删除题目' + question.value.id + '吗？ 包括相关的图片')) return;
    var value = await delete_question_request({'questionId': question.value.id})
    if (value.status == true) {
        alert(value.message)
        window.location.reload()
        emit('close')

    } else {
        alert(value.message)
    }
}

async function post_question_image() {
    var value = await post_question_image_request(question.value.id, image.value)
    if (value.status == true) {
        alert(value.message)
        refresh()
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
    post_question_image()
}

async function question_update() {
    if (
        // new_question.value.post == question.value.post &&
        new_question.value.qualified == question.value.qualified
        && new_question.value.mainProblem == question.value.main_problem
        && new_question.value.problemDescription == question.value.problem_description
    ) {
        return
    }
    if (!confirm('确定修改吗？')) return
    var value = await question_update_request(new_question.value)
    if (value.status == true) {
        alert(value.message)
        question.value = new_question.value
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
        <div class="title">题目</div>
    </div>
    <div class="question-information">
        <div class="question-image">
            <label v-if="isEdit && question.file_url != null" class="images">
                <img :src="apiURL + question.file_url" >
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
            <div v-else-if="question.file_url != ''" class="question-avatar">
                <img :src="apiURL + question.file_url" >
            </div>
            <label v-else for="image-file" class="question-avatar">
                点击上传
                <input type="file" single accept="image/*" value="" id="image-file" @change="uploadImage($event)">
            </label>
        </div>
        <div v-if="isEdit" class="question-right">
            <form>
                <!-- <div class="question-post">岗位: 
                    <select v-model="new_question.post">
                        <option v-for="post_type in post_list">
                            {{ post_type }}
                        </option>
                    </select>
                </div> -->
                <div class="question-qualified">答案:
                    <select v-model="new_question.qualified">
                        <option value="1">True</option>
                        <option value="0">False</option>
                    </select>
                </div>
                <div class="question-main-problem">主要问题:
                    <select v-model="new_question.mainProblem">
                        <option v-for="problem in main_problem">
                            {{ problem }}
                        </option>
                    </select>
                </div>
                <div class="question-problem-detail">
                    <div>问题详情:</div>
                    <textarea type="text" v-model="new_question.problemDescription"></textarea>
                </div>
            </form>
        </div>
        <div v-else class="question-right">
            <div class="question-id">题目ID: {{ question.id }}</div>
            <!-- <div class="question-post">岗位: {{ question.post }}</div> -->
            <div class="question-time">创建时间: {{ formulate_time(question.create_time) }}</div>
            <div class="question-num-test">测试次数: {{ question.num_test }}</div>
            <div class="question-pass-rate">通过率: {{ question.pass_rate }}</div>
            <div class="question-pass-num">通过次数: {{ question.pass_time }}</div>
            <div class="question-qualified">答案:</div>
            <div v-if="question.qualified == true">
                <img src="@img/tongguo.png" alt="通过">
            </div>
            <div v-else>
                <img src="@img/butongguo.png" alt="错误">
            </div>
            <div v-if="question.main_problem" class="question-main-problem">主要问题: {{ question.main_problem }}</div>
            <div v-if="question.problem_description" class="question-problem-detail">
                <div>问题详情:</div>
                <div>{{ question.problem_description }}</div>
            </div>
        </div>
    </div>
    
    <div class="bottom-bar">
        <div v-if="isEdit" class="bottom-bar-item" id="close-button" @click="isEdit = !isEdit">返回</div>
        <div v-else class="bottom-bar-item" id="close-button" @click="$emit('close')">退出</div>
        <div v-if="isEdit" class="bottom-bar-item" id="save-button" @click="question_update();isEdit = !isEdit">保存</div>
        <div v-else class="bottom-bar-item" id="edit-button" @click="isEdit = !isEdit">编辑</div>
        <div class="bottom-bar-item" id="delete-button" @click="delete_question">删除题目</div>
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
.question-information {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.question-image {
    display: flex;
    justify-content: center;
    align-items: center;
}
.question-image img{
    object-fit: cover;
    object-position: center;
}
.question-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background-color: rgb(167, 167, 211, 0.5);
    cursor: pointer
}
.question-avatar img {
    width: 200px;
    height: 320px;
}
.question-right {
    display: flex;
    flex-direction: column;
    margin-left: 20px;
}
.question-right input {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.question-right select {
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    font-size: 14px;
    margin-bottom: 5px;
}
.question-right img{
    width: 30px;
    height: 30px;
}
.question-right textarea {
    width: 300px;
    height: 100px;
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
.question-3d-images {
    display: flex;
    flex-direction: row;
    margin-right: 10px;
    cursor: pointer;
}
.question-3d-images .model3d {
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