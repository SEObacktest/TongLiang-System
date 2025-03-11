<script setup>

import {ref, onMounted, watch} from 'vue'

import router from '../../router';

const emit = defineEmits(['selectItem']);

const sendData = (name) => {
  emit('selectItem', name);
};

const props = defineProps(['user'])

const level1style = ref({
    backgroundColor: 'rgb(135, 203, 223)',
    solid: 'None',
    height: '40px',
})

const selectedStyle = ref({
    backgroundColor: 'rgb(255, 195, 255)',
})

const list = ref([])

function getList() {
    if (props.user.is_admin) {
        list.value = [
            {name: '首页', level: 0, group: 0, selected: true, path: '/admin'},
            // {name: '在线剪辑', level: 0, group: 1, selected: false, path: '/student'},
            // {name: '在线私域', level: 0, group: 2, selected: false, path: '/activity'},
            {name: '在线HR', level: 0, group: 3, selected: false, path: '/admin/online_hr'},
            {name: '测试模块', level: 1, group: 3, selected: false, path: '/admin/test_module'},
            {name: '题库管理', level: 1, group: 3, selected: false, path: '/admin/question'},
            {name: '约面管理', level: 1, group: 3, selected: false, path: '/admin/interview'},
            {name: '报酬管理', level: 1, group: 3, selected: false, path: '/admin/salary'},
        ]
    } else {
        list.value = [
            {name: '首页', level: 0, group: 0, selected: true, path: '/'},
        ]
    }
    selectItem(router.currentRoute.value.path)
}

function selectItem(path) {
    // console.log(path)
    const item = list.value.find(item => item.path === path)

    // console.log(item.name)
    sendData(item.name)
    list.value.forEach((item, i) => {
        if (item.path == path) {
            item.selected = true
        } else {
            item.selected = false
        }
    })    

    if (item.level == 1) {
        list.value.forEach((item1, i) => {
            if (item1.level == 0 && item1.group == item.group) {
                item1.selected = true;
            }
        })
    }
    router.push(item.path)

}

function selectedItemGroup(list) {
    for (let i = 0; i < list.length; i++) {
        if (list[i].selected) {
            return list[i].group
        }
    }
}

// getList()
// onMounted(async function() {
//     getList()
// })

// 监听 props.user，当它变更时，重新获取列表
watch(() => props.user, (newUser) => {
    if (newUser) {
        getList()
    }
}, { immediate: true })  // `immediate: true` 让 watch 立即执行一次

</script>

<template>
<div></div>

<div id='main'>
    {{ router.path }}
    <div v-for="(item, index) in list" :key="index" >
        <div v-if="(item.selected && item.level == 0)" 
        class="container" 
        :style="[selectedStyle]"
        @click="selectItem(item.path)">
            <div class="title">
                {{ item.name }}
            </div>
            <img class="arrow-icon" style="transform: rotate(0deg);" src="@icons/xiangxia.svg" alt="">
        </div>
        <div v-else-if="(item.selected && item.level == 1)" 
        class="container" 
        :style="[level1style, selectedStyle]"
        @click="selectItem(item.path)">
            <div class="title">
                {{ item.name }}
            </div>
        </div>
        <div v-else-if="(item.level == 0)" 
        class="container"
        @click="selectItem(item.path)">
            <div class="title">
                {{ item.name }}
            </div>
            <img class="arrow-icon" src="@icons/xiangxia.svg" alt="">
        </div>
        <div v-else-if="(item.group == selectedItemGroup(list))" class="container" 
        :style="[level1style]"
        @click="selectItem(item.path)">
            <div class="title">
                {{ item.name }}
            </div>
        </div>
    </div>
</div>

</template>

<style scoped>
#main {
    width: 162px;
    height: screen;
    background-color: rgb(110, 185, 208);
    display: flex;
    flex-direction: column;
}
.container {
    width: 160px;
    height: 50px;
    background-color: rgb(36, 187, 233);
    border: 1px solid rgb(0, 0, 0);

    display: flex;
    flex-direction: row;
    align-items: center;
    cursor: pointer;
}  
.title {
    width: 120px;
    font-size: 16px;
    margin-left: 20px;
    /* font-family: "SanJiXinWeiBeiJian-2"; */
    cursor: pointer;
}
.arrow-icon {
    width: 20px;
    height: 20px;
    margin-right: 10px;
    cursor: pointer;
    transform: rotate(270deg);
}
</style>