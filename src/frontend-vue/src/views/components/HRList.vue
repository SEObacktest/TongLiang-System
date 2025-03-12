<script setup>

import { onMounted, watch } from 'vue';
import {ref} from 'vue'

import { formulate_time } from '../../utils/tools';

import {get_hr_list_request, get_activities_list_request} from "@/api/api.js";

const props = defineProps(['user'])
const emit  = defineEmits(['hr_selected'])

watch(
    () => props.user,
    (newVal, oldVal) => {
        refresh_activities_list_all(newVal)
    }
)

// onMounted(() => {
//     refresh_activities_list(props.user)
//     console.log("before mount" + props.user)
// })

const activity_list = ref([])

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

const hrList = ref([])
const hrNameList = ref([])

async function refresh_activities_list(user) {
    if(!user.is_admin) {
        studentId.value = user.userId
    } else {
        var value = await get_hr_list_request()
        if(value.status == false) {
            alert(data.message)
        } else {
            hrList.value = value.data
            hrList.value.forEach(e => {
                hrNameList.value[e.pk] = e.fields.username
            });
        }

    }

    activity_list.value = await get_activities_list_request({
       "studentId": studentId.value,
       "startTime": startTime.value,
       "endTime"  : endTime.value,
       "certified": certified.value,
       "passed"   : passed.value,
       "adminId"  : adminId.value,
    })
    if(activity_list.value.status == false) {
        alert(activity_list.value.message)
    } else {
        activity_list.value = activity_list.value.data
    }
}
function hr_click(hr) {
    console.log("用户点击了" + hr)
    emit('hr_selected', hr)
}


async function refresh_activities_list_all(user) {
    if(!user.is_admin) {
        studentId.value = user.userId
    } else {
        var value = await get_hr_list_request()
        if(value.status == false) {
            alert(data.message)
        } else {
            hrList.value = value.data
            hrList.value.forEach(e => {
                hrNameList.value[e.pk] = e.username
            });
        }
    }
    // console.log("studentId: " + studentId.value)
    // console.log("startTime: " + startTime.value)
    // console.log("endTime: " + endTime.value)
    // console.log("certified: " + certified.value)
    // console.log("passed: " + passed.value)
    // console.log("adminId: " + adminId.value)
    activity_list.value = await get_activities_list_request({
       "studentId": studentId.value,
       "startTime": '*',
       "endTime"  : '*',
       "certified": '*',
       "passed"   : '*',
       "adminId"  : '*',
    })
    if(activity_list.value.status == false) {
        alert(activity_list.value.message)
    } else {
        activity_list.value = activity_list.value.data
    }
}

/*
    <script setup> 使用这个语法糖的组件是默认关闭的，不会向外暴露任何在<script setup>中声明的属性或者方法。如果想让外部组件能访问到，就要使用defineExpose编译器宏
    defineExpose不需要引入，直接调用即可
*/
defineExpose({
    refresh_activities_list
})

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
            <div class="hr-title">姓名</div>
            <div class="hr-title">已面个数</div>
            <div class="hr-title">管理账号</div>
            <div class="hr-title">最后登录时间</div>
            <div class="hr-title">操作</div>
        </div>
        <div class="activity" v-for="hr in hrList">
            <!-- {{ hr }} -->
            <div class="hr-content">{{ hr.username }}</div>
            <div class="hr-content">{{ hr.interviewCount }}</div>
            <div class="hr-content">{{  hr.account }}</div>
            <div class="hr-content">{{  formulate_time(hr.last_login) }}</div>
            <div class="hr-content-botton" @click="hr_click(hr)">查看详情</div>
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