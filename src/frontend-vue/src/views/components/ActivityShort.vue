<script setup>

import { onMounted, watch } from 'vue';
import {ref} from 'vue'

import {get_students_list_request, get_activities_list_request} from "@/api/api.js";

const props = defineProps(['user'])
const emit  = defineEmits(['activity_clicked'])

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
const activity_type_color = ref({
    "志愿活动": "rgb(0, 195, 255)",
    "党日活动": "rgb(0, 255, 157)",
    "其他": "rgb(255, 225, 0)",
})

const studentList = ref([])
const studentNameList = ref([])

async function refresh_activities_list(user) {
    if(!user.is_admin) {
        studentId.value = user.userId
    } else {
        var value = await get_students_list_request()
        if(value.status == false) {
            alert(data.message)
        } else {
            studentList.value = value.data
            studentList.value.forEach(e => {
                studentNameList.value[e.pk] = e.fields.username
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
function activity_click(activity) {
    // console.log("用户点击了" + activity.name)
    emit('activity_clicked', activity)
}


async function refresh_activities_list_all(user) {
    if(!user.is_admin) {
        studentId.value = user.userId
    } else {
        var value = await get_students_list_request()
        if(value.status == false) {
            alert(data.message)
        } else {
            studentList.value = value.data
            studentList.value.forEach(e => {
                studentNameList.value[e.pk] = e.fields.username
            });
        }
    }

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
        <div class="check-activity">
            <div v-if="user.is_admin" class="check-activity-item">
                <div class="check-activity-item-label">学号</div>
                <div class="check-activity-item-input">
                    <input type="text" placeholder="请输入学号" v-model="studentId">
                </div>
            </div>
            <div v-if="user.is_admin" class="check-activity-item">
                <div class="check-activity-item-label">负责人(审核人)</div>
                <div class="check-activity-item-input">
                    <input type="text" placeholder="请输入学号" v-model="adminId">
                </div>
            </div>
            <div class="check-activity-item">
                <div class="check-activity-item-label">开始时间</div>
                <div class="check-activity-item-input">
                    <input type="date" placeholder="请输入开始时间" v-model="startTime">
                </div>
            </div>
            <div class="check-activity-item">
                <div class="check-activity-item-label">结束时间</div>
                <div class="check-activity-item-input">
                    <input type="date" placeholder="请输入结束时间" v-model="endTime">
                </div>
            </div>
            <div class="check-activity-item">
                <div class="check-activity-item-label">是否认证</div>
                <div class="check-activity-item-input">
                    <!-- <input style="cursor: pointer;width: 20px;" type="checkbox" placeholder="请输入是否认证" v-model="certified"> -->
                    <input type="text" list="yes_no_all" placeholder="请输入是否认证" v-model="certified">
                </div>
            </div>
            <div class="check-activity-item">
                <div class="check-activity-item-label">是否通过</div>
                <div class="check-activity-item-input">
                    <!-- <input style="cursor: pointer;width: 20px;" type="checkbox" placeholder="请输入是否通过" v-model="passed"> -->
                    <input type="text" list="yes_no_all" placeholder="请输入是否通过" v-model="passed">

                </div>
            </div>
        </div>
        <div class="search" @click="refresh_activities_list(props.user)">查询</div>
    </div>
    <div class="activity-list">
        <div class="activity" v-for="activity in activity_list">
            <div class="activity-information">
                <div class="activity-left">
                    <div class="activity-name">{{ activity.fields.name }}</div>
                    <div v-if="user.is_admin" class="activity-student">{{ studentNameList[activity.fields.student] }}</div>
                    <div v-else class="activity-student">{{ user.username }}</div>
                    <div class="activity-type">
                        <div>活动类型: </div>
                        <div class="activity-type-detail" :style="{backgroundColor: (activity_type_color[activity.fields.type])}">{{  activity.fields.type }}</div>
                    </div>
                    <div class="activity-certified">通过认证:
                        <img class="activity-status" v-if="!activity.fields.certified"  src="@img/dengdaiyanzheng.png">
                        <img class="activity-status" v-else-if="activity.fields.passed" src="@img/tongguo.png">
                        <img class="activity-status" v-else src="@img/butongguo.png">
                    </div>
                </div>
                <div class="activity-right">
                    <div class="activity-time">活动时间: {{  activity.fields.startTime }} 至 {{  activity.fields.endTime }}</div>
                    <div class="activity-location">活动地点: {{  activity.fields.location }}</div>
                    <div class="activity-description">活动内容: {{  activity.fields.description }}</div>
                    <div class="activity-detail" @click="activity_click(activity)">查看详情</div>
                </div>
            </div>
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
    height: 90%;
    width: 100%;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    overflow: auto;
}
.activity {
    background-color: rgba(255, 255, 255, 0.8);
    border: 1px solid black;
    border-radius: 20px;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 20px;
    padding-top: 20px;
    padding-bottom: 20px;
    padding-left: 20px;
}
.activity-information {
    display: flex;
    justify-content: center;
    flex-direction: row;
}

.activity-name {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}
.activity-student {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
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
.activity-right {
    display: flex;
    justify-content: start;
    flex-direction: column;
    margin: 40px;
}
.activity-time {
    margin-top: -40px;
    margin-bottom: 10px;
}
.activity-location {
    margin-bottom: 10px;
}
.activity-description {
    margin-bottom: 10px;
}
.activity-detail {
    cursor: pointer;
    margin-top: 10px;
    width: 80px;
    height: 30px;
    border: 1px solid black;
    border-radius: 5px;
    align-items: center;
    justify-content: center;
    display: flex;
    transition: transform 0.3s ease, background-color 0.3s; /* 平滑过渡 */
}
.activity-detail:hover {
    background-color: rgb(110, 185, 208);
    transform: scale(1.1);
}
</style>