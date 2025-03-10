<script setup>

import { ref } from 'vue'

import { create_student_request } from '@/api/api';

const props = defineProps(['user'])
const emit  = defineEmits(['close'])

const student_name        = ref()
const student_phone       = ref()
// const student_birthday    = ref()
const student_description = ref()
const clinic_name         = ref(props.user.username)

const message = ref()

async function create_student() {

    if (
    student_name.value        == undefined ||
    student_phone.value       == undefined ||
    // student_birthday.value    == undefined ||
    student_description.value == undefined) {
        message.value = '患者信息请完整填写'
        return
    }

    var data = {
        'name'       : student_name.value,
        'phone'      : student_phone.value,
        'birthday'   : student_birthday.value,
        // 'description': student_description.value,
        // 'clinicName' : clinic_name.value
    }
    var value = await create_student_request(data)
    if (value.status == true) {
        message.value = value.message
        alert(value.message)
        emit('close')
    } else {
        alert(value.message)
        message.value = value.message
    }
}

</script>

<template>
<div></div>

<div id='main'>
    <div class="form">
        <div class="form-item">
            <div class="form-item-label">姓名</div>
            <div class="form-item-input">
                <input type="text" placeholder="请输入患者姓名" v-model="student_name">
            </div>
        </div>
        <div class="form-item">
            <div class="form-item-label">电话</div>
            <div class="form-item-input">
                <input type="text" placeholder="请输入患者电话" v-model="student_phone">
            </div>
        </div>
        <!-- <div class="form-item">
            <div class="form-item-label">患者生日(请严格按照XXXX-XX-XX合法的日期填入)</div>
            <div class="form-item-input">
                <input type="text" placeholder="请输入患者生日" v-model="student_birthday">
            </div>
        </div> -->
        <!-- <div class="form-item">
            <div class="form-item-label">患者简介</div>
            <div class="form-item-input">
                <input type="text" placeholder="请输入患者简介" v-model="student_description">
            </div>
        </div> -->
        {{ message }}
    </div>
    <div class="add-student-button" @click="$emit('close')">取消</div>
    <div class="add-student-button" @click="create_student">确认</div>
</div>

</template>

<style scoped>
#main {
    margin-top: 100px;
    width: 600px;
    height: 400px;
    background-color: blue;
    display: flex;
    flex-direction: column;
}
.add-student-button {
    background-color: red;
    width: 40px;
    cursor:pointer;
}
</style>