<script setup>

import { ref } from 'vue'

import { 
    hr_register_request,
} from '@/api/api';

const props = defineProps(['user'])
const emit  = defineEmits(['close'])

const hr_userId    = ref()
const hr_name      = ref()
const hr_age       = ref()
const hr_gender    = ref()
const hr_account   = ref()
const hr_phone     = ref()
const hr_bank      = ref()
const hr_bankCard      = ref()
const hr_accountHolderName = ref()
const hr_idCard    = ref()
const hr_password  = ref()

const student_name = ref(props.user.username)
//     userId = models.CharField(max_length=20, unique=True)
// phone = models.CharField(max_length=20)
//     isAdmin = models.BooleanField(default=False)
//     bankCard = models.CharField(max_length=30, default="")
//     bank = models.CharField(max_length=30, default="")
//     accountHolderName = models.CharField(max_length=30, default="")
//     idCard = models.CharField(max_length=30, default="")
//     age = models.IntegerField(default=0)
//     gender = models.CharField(max_length=10, default="")
//     account = models.CharField(max_length=30, default="")

const image_list = ref([])
const image_url_list = ref([])

const is_show_image = ref(false)
const show_image = ref('')

const message = ref()

async function create_hr() {

    if (
    hr_name.value        == undefined ||
    hr_age.value  == undefined ||
    hr_gender.value    == undefined ||
    hr_account.value        == undefined ||
    hr_phone.value    == undefined ||
    hr_bank.value == undefined ||
    hr_bankCard.value == undefined ||
    hr_accountHolderName.value == undefined ||
    hr_idCard.value == undefined ||
    hr_password.value == undefined ||
    hr_userId.value == undefined) {
        message.value = '活动信息请完整填写'
        return
    }

    console.log(props.user.userId)
    console.log(student_name.value)
    console.log(hr_bank.value)
    console.log(hr_age.value)
    console.log(hr_gender.value)
    console.log(hr_phone.value)
    console.log(hr_account.value)


    var data = {
        'name'             : hr_name.value,
        'userId'           : hr_userId.value,
        'password'         : hr_password.value,
        'phone'            : hr_phone.value,
        'age'              : hr_age.value,
        'gender'           : hr_gender.value,
        'account'          : hr_account.value,
        'bank'             : hr_bank.value,
        'bankCard'         : hr_bankCard.value,
        'accountHolderName': hr_accountHolderName.value,
        'idCard'           : hr_idCard.value,
    }
    var value = await hr_register_request(data)
    if (value.status == true) {
        message.value = value.message
        // await post_hr_image(value.data.activityId)
        alert(value.message)
        window.location.reload()
        emit('close')
    } else {
        alert(value.message)
        message.value = value.message
    }
}

async function delete_image(imageId) {
    if(!confirm('确定删除这张图片吗？')) return;
    image_list.value.splice(imageId, 1)
    image_url_list.value.splice(imageId, 1)
}

</script>

<template>
<div></div>

<div id='main'>
    <div class="title">添加HR</div>
    <div class="show-image" v-if="is_show_image">
        <img :src="show_image" alt="image" @click="is_show_image = false">
    </div>
    <div class="add-activity" v-else>
        <div class="form">
            <div class="form-left">
                <div class="form-item">
                    <div class="form-item-label">用户ID</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入用户ID" v-model="hr_userId">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">密码</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入密码" v-model="hr_password">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">姓名</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入姓名" v-model="hr_name">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">电话</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入开户人姓名" v-model="hr_phone">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">年龄</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入年龄" v-model="hr_age">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">性别</div>
                    <div class="form-item-input">
                        <select name="activityType" id="activity-type" v-model="hr_gender">
                            <option value="男">男</option>
                            <option value="女">女</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="form-right">
                <div class="form-item">
                    <div class="form-item-label">管理账号</div>
                    <div class="form-item-input">
                        <select name="activityType" id="activity-type" v-model="hr_account">
                            <option value="BOSS白">BOSS白</option>
                            <option value="BOSS乔">BOSS乔</option>
                        </select>
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">开户行</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入开户行" v-model="hr_bank">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">银行账号</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入银行账号" v-model="hr_bankCard">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">开户人姓名</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入开户人姓名" v-model="hr_accountHolderName">
                    </div>
                </div>
                <div class="form-item">
                    <div class="form-item-label">身份证号</div>
                    <div class="form-item-input">
                        <input type="text" placeholder="请输入身份证号" v-model="hr_idCard">
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
        <div class="add-activity-button" @click="create_hr">确认</div>
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
#box {
    display: flex; 
    flex-direction: column;
}
.message {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    color: red;
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
    cursor: pointer;
}
</style>