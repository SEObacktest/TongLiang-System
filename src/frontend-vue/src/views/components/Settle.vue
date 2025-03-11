<script setup>

const props = defineProps(['interviewList', 'hr'])
const emit  = defineEmits(['close'])

import { post_settlement_request } from '../../api/api';

async function settle_account() {

    const interviewList = props.interviewList
    const hr = props.hr

    if (interviewList.length == 1) {
        const result = confirm("确认为HR: " + hr.username + " 结算面试ID" + interviewList[0].id + " 100元吗？")
        if (!result) {
            return
        }
    } else {
        const result = confirm("确认为HR: " + hr.username + "结算" + interviewList.length + "个面试，总计" + interviewList.length * 100 + "元吗？")
        if (!result) {
            return
        }
    }

    let interviewIdList = []

    interviewList.forEach(interview => {
        interviewIdList.push(interview.id)
    });

    const value = await post_settlement_request({
        'interviewIdList': interviewIdList,
    })

    if (value.status == true) {
        alert(value.message)
        refresh()
    } else {
        alert(value.message)
    }

    console.log(value)
}

function refresh() {
    window.location.reload()
}

</script>

<template>
<div></div>

<div id='main'>

    <div class="information">
        <div class="title">确认结算</div>
        <div class="body">
            <div class="left">
                <div>HR: {{ hr.username }}</div>
                <div>结算面试数量: {{ interviewList.length }}</div>
                <div>结算金额: {{ interviewList.length * 100 }}元</div>
            </div>
            <div class="right">
                <div>银行卡号: {{ hr.bankCard }}</div>
                <div>开户行: {{ hr.bank }}</div>
                <div>开户人: {{ hr.accountHolderName }}</div>
            </div>
        </div>
    </div>

    <div class="button-bar">
        <div class="button" @click="emit('close')">关闭</div>
        <div class="button" id="settle"  @click="settle_account()">结算</div>
    </div>

</div>

</template>

<style scoped>
#main {
    position: absolute;
    left: 0;
    right: 0;
    margin: 0 auto;
    width: 600px;
    height: 400px;
    /* background-color: rgba(0, 0, 0, 0.5); */
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: space-around;
    background-color: white;
    border-radius: 10px;
    padding: 10px;
    z-index: 100;
}
.information {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    font-size: 18px;
}
.title {
    font-size: 24px;
    margin-bottom: 10px;
}
.body {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
}
.left {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}
.right {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}
.button-bar {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
}
.button {
    width: 80px;
    height: 30px;
    font-size: 20px;
    line-height: 30px;
    margin-right: 10px;
    text-align: center;
    cursor: pointer;
    background-color: rgb(110, 185, 208);
    border-radius: 5px;
    transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.button:hover {
    background-color: rgb(0, 195, 255);
    transform: scale(1.1);
}
#settle:hover {
    background-color: green;
}
#detail {
    font-size: 16px;
}
</style>