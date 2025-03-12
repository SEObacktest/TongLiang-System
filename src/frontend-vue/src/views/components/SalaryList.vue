<script setup>

import { onMounted, watch } from 'vue';
import {ref} from 'vue'

import { formulate_time } from '../../utils/tools';

import {
    get_hr_list_request, 
    get_salary_list_request,
} from "@/api/api.js";

const props = defineProps(['user'])
const emit  = defineEmits(['salary_selected'])

watch(
    () => props.user,
    (newVal, oldVal) => {
        refresh_salary_list_all(newVal)
    }
)

// onMounted(() => {
//     refresh_activities_list(props.user)
//     console.log("before mount" + props.user)
// })

const salary_list = ref([])

const adminId   = ref('')
const studentId = ref('')
const startTime = ref('')
const endTime   = ref('')
const certified = ref('')
const passed    = ref('')
// const activity_type_color = ref({
//     "志愿活动": "rgb(0, 195, 255)",
//     "党日活动": "rgb(0, 255, 157)",
//     "其他": "rgb(255, 225, 0)",
// })

const salaryList = ref([])
const hrNameList = ref([])
const unsettlementList = ref([])

async function refresh_activities_list(user) {

    salary_list.value = await get_salary_list_request({
       "studentId": studentId.value,
       "startTime": startTime.value,
       "endTime"  : endTime.value,
       "certified": certified.value,
       "passed"   : passed.value,
       "adminId"  : adminId.value,
    })
    if(salary_list.value.status == false) {
        alert(salary_list.value.message)
    } else {
        salary_list.value = salary_list.value.data
    }
}
function salary_click(salary) {
    console.log("用户点击了" + salary)
    emit('salary_selected', salary)
}


async function refresh_salary_list_all(user) {

    salary_list.value = await get_salary_list_request({
       "studentId": studentId.value,
       "startTime": '*',
       "endTime"  : '*',
       "certified": '*',
       "passed"   : '*',
       "adminId"  : '*',
    })
    if(salary_list.value.status == false) {
        alert(salary_list.value.message)
    } else {
        salary_list.value = salary_list.value.data
    }
}

/*
    <script setup> 使用这个语法糖的组件是默认关闭的，不会向外暴露任何在<script setup>中声明的属性或者方法。如果想让外部组件能访问到，就要使用defineExpose编译器宏
    defineExpose不需要引入，直接调用即可
*/
defineExpose({
    refresh_activities_list
})  
refresh_activities_list(props.user)
</script>

<template>
<div></div>
<div id='main'>
    <div class="head">
        <!-- <div class="check-activity">
            <div v-if="user.is_admin" class="check-activity-item">
                <div class="check-activity-item-label">手机号</div>
                <div class="check-activity-item-input">
                    <input type="text" placeholder="请输入手机号" v-model="studentId">
                </div>
            </div>
            <div v-if="user.is_admin" class="check-activity-item">
                <div class="check-activity-item-label">姓名</div>
                <div class="check-activity-item-input">
                    <input type="text" placeholder="请输入姓名" v-model="adminId">
                </div>
            </div>
            <div class="check-activity-item">
                <div class="check-activity-item-label">加入时间</div>
                <div class="check-activity-item-input">
                    <input type="date" placeholder="请输入加入时间" v-model="startTime">
                </div>
            </div>
        </div>
        <div class="search" @click="refresh_activities_list(props.user)">查询</div> -->
    </div>
    <div class="activity-list">
        <div class="hr-header">
            <div class="hr-title">HR</div>
            <div class="hr-title">待结算次数</div>
            <div class="hr-title">待结算金额</div>
            <div class="hr-title">结算状态</div>
            <!-- <div class="hr-title">最后结算时间</div> -->
            <div class="hr-title">操作</div>
        </div>
        <!-- {{ salary_list }} -->
        <div class="activity" v-for="salary in salary_list">
            <!-- {{ hr }} -->
            <div class="hr-content">{{ salary.hr.username }}</div>
            <div class="hr-content">{{ salary.salaryInformation.num }}</div>
            <div class="hr-content">{{ salary.salaryInformation.price }}</div>
            <div class="hr-content">
                <img v-if="salary.settlement == 'true'" src="@img/tongguo.png" alt="通过">
                <img v-else src="@img/dengdaiyanzheng.png" alt="等待">
            </div>
            <!-- <div class="hr-content">{{  formulate_time(salary.create_time) }}</div> -->
            <div class="hr-content-botton" @click="salary_click(salary)">查看详情</div>
        </div>
    </div>
</div>
<datalist id="yes_no_all">
    <option value="True"></option>
    <option value="False"></option>
    <option value="*"></option>
</datalist>
</template>

<style scoped>
#main {
    height: 100%;
    padding-left: 20px;
    padding-right: 20px;
}
.head {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
input {
    width: 100%;
    height: 22px;
    border-radius: 5px;
    border: 1px solid gray;
}
.check-activity {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    flex-direction: row;
}
.check-activity-item {
    display: flex;
    margin-bottom: 10px;
}
.check-activity-item-label {
    margin-right: 0px;
}
.check-activity-item-input{
    display: flex;
    align-items: center;
    min-width: 80px;
    margin-right: 10px;
}
.check-activity-item-input input{
    background-color: rgba(255, 255, 255, 0.8);
}
.search {
    cursor: pointer;
    margin-right: 20px;
    width: 100px;
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    align-items: center;
    justify-content: center;
    display: flex;
    transition: transform 0.3s ease, background-color 0.3s; /* 平滑过渡 */
}
.search:hover {
    background-color: rgb(110, 185, 208);
    transform: scale(1.1);
}
.activity-list {
    height: 80vh;
    overflow-y: auto;
    border: 1px solid #ccc;
    width: 100%;
    display: flex;
    flex-direction: column;
    overflow: auto;
}
.hr-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.hr-title {
    width: 100px;
    font-size: 16px;
    font-weight: bold;
    text-align: center;
}
.activity {
    background-color: rgba(255, 255, 255, 0.8);
    border: 1px solid black;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 4px;
}
.hr-content {
    width: 100px;
    font-size: 16px;
    text-align: center;
}
.hr-content img {
    width: 30px;
    height: 30px;
}
.hr-content-botton {
    width: 80px;
    height: 30px;
    font-size: 16px;
    line-height: 30px;
    margin-right: 10px;
    text-align: center;
    cursor: pointer;
    background-color: rgb(110, 185, 208);
    border-radius: 5px;
    transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.hr-content-botton:hover {
    background-color: rgb(0, 195, 255);
    transform: scale(1.1);
}
</style>