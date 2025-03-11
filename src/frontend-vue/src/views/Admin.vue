<script setup>

import { ref, shallowRef } from 'vue'
import { defineAsyncComponent } from 'vue';

import router from '../router';

import {
    is_login_request,
} from '../api/api';

import Header         from './components/header/Header.vue';
import SideBar        from './components/SideBar.vue';  
import Footer         from './components/footer/Footer.vue';

const pageList = shallowRef([
    {
        name: '首页',
        component: defineAsyncComponent(() => import('./pages/Admin.vue'))
    },
    {
        name: '在线HR',
        component: defineAsyncComponent(() => import('./pages/OnlineHR.vue'))
    },
    {
        name: '测试模块',
        component: defineAsyncComponent(() => import('./pages/TestModule.vue'))
    },
    {
        name: '题库管理',
        component: defineAsyncComponent(() => import('./pages/Question.vue')) 
    },
    {
        name: '约面管理',
        component: defineAsyncComponent(() => import('./pages/Interview.vue'))
    },
    {
        name: '报酬管理',
        component: defineAsyncComponent(() => import('./pages/Salary.vue'))
    }
])

const user                 = ref("")

const selectedName = ref("报酬管理")

function refresh() {
    window.location.reload()
}

async function is_login() {
    var value = await is_login_request()
    if (value.status == true) {
        user.value = value.data
        // if(user.value.is_admin == true){
        //     var value = await get_students_list_request()
        //     if(value.status == false) {
        //         alert(data.message)
        //     } else {
        //         studentList.value = value.data
        //         studentList.value.forEach(e => {
        //             studentNameList.value[e.pk] = e.fields.username
        //         });
        //     }
        // }
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
<div></div>
<Header :user="user"></Header>
<div id='main'>
    
    <SideBar :user="user" @selectItem="(key) => {selectedName = key}"></SideBar>
    <div class="contain">
        <div class="body">
            <component :is="(pageList.find(e => e.name == selectedName)?.component) || 'div'"></component>
        </div>
    </div>  
</div>
<Footer></Footer>
</template>

<style scoped>
#main {
    min-height: 100vh;
    display: flex;
    flex-direction: row;
    /* 一定要先制定background在加其他限制 */
    background: url("@img/home_background.jpg");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    justify-content: center;
}
.contain {
    display: flex;
    flex: 1;
    justify-content: center;

}
.body {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
.container {
    height: 1300px;
    top: 100px;
    width: 100%;
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;

}
.container_filter {
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
    background-color: rgba(0, 0, 0, 0.3);
}


/* 下面我们会解释这些 class 是做什么的 */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}
.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>