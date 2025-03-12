<script setup>

import { ref } from 'vue'

import router from '../router';

import {
    // get_students_list_request, 
    is_login_request,
    export_excel_request,
} from '../api/api';

import Header         from './components/header/Header.vue';
import SideBar        from './components/SideBar.vue';  
// import AddActivity    from './components/AddActivity.vue';
// import ActivityShort  from './components/ActivityShort.vue';
// import StudentDetail  from './components/HRDetail.vue';
// import ActivityDetail from './components/ActivityDetail.vue';
import Footer         from './components/footer/Footer.vue';
import SideMenu from "@/components/SideMenu.vue";


const user                 = ref("")
const isShowStudentDetail  = ref(false)
const isShowAddActivity    = ref(false)
const isShowActivityDetail = ref(false)
const activityShort        = ref()
const studentClicked       = ref()
const activityClicked      = ref()

const studentList = ref([])
const studentNameList = ref([])

const studentStage = ref({
    0: "群众",
    1: "团员",
    2: "积极分子",
    3: "发展对象",
    4: "预备党员",
    5: "党员",
})

function open_student_detail(student) {
    studentClicked.value = student
    isShowStudentDetail.value = true
}

function open_activity_detail(activity) {
    activityClicked.value = activity
    isShowActivityDetail.value = true
}

async function exportInformation() {
    if(!confirm('确定导出信息吗？')) return;
    var value = await export_excel_request({
        'studentId':'*',
    })
    if (value.status == true) {
        alert(value.message)
    } else {
        alert(value.message)
    }
    // alert("我还没做这个")
}

function refresh() {
    window.location.reload()
}

async function is_login() {
    var value = await is_login_request()
    if (value.status == true) {
        user.value = value.data
        if(user.value.is_admin == true){

            router.push('/admin')
            // var value = await get_students_list_request()
            // if(value.status == false) {
            //     alert(data.message)
            // } else {
            //     studentList.value = value.data
            //     studentList.value.forEach(e => {
            //         studentNameList.value[e.pk] = e.fields.username
            //     });
            // }
        }
    } else {
        user.value = undefined
        // alert("请先登录，若无反应请刷新界面")
        // router.push('/login')
        router.push('/login_register')
    }
}
is_login()
</script>

<template>
  <div id="main">
    <!-- 保留 Header 组件 -->
    <Header :user="user" />
    <div class="body">
      <!-- 保留 SideMenu 组件 -->
      <SideMenu />
      <!-- 新增简单欢迎信息 -->
      <div class="welcome-container">
        <h1>欢迎使用，请在侧边栏选择你想要的功能</h1>
      </div>
    </div>
  </div>
</template>

<style scoped>
#main {
  display: flex;
  flex-direction: column;
}
.body {
  display: flex;
}
.welcome-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>