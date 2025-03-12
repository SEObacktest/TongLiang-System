<script setup>
import { ref, onMounted } from 'vue'
import router from '@/router'
import { logout_request, is_login_request } from '@/api/api'

// Removed defineProps and create reactive user data
const user = ref(null)

// Fetch login info on component mount
async function fetchUser() {
  try {
    const response = await is_login_request()
    if (response.status === true) {
      user.value = response.data
    } else {
      router.push("/login_register")
    }
  } catch (error) {
    console.error("获取登录状态出错:", error)
    router.push("/login_register")
  }
}

onMounted(() => {
  fetchUser()
})

async function logout() {
    await logout_request()
    alert('退出登录成功')
    window.location.reload()
}
</script>

<template>
  <div></div>
  <div id='main'>
      <div class="logo"></div>
      <div class="logo-title">同梁在线业务系统</div>
      <div class="user" v-if="user">
          <div class="user-avatar"></div>
          <div class="user-name">您好，{{ user.username }}</div>
          <div class="user-logout" @click="logout">退出登录</div>
      </div>
      <div class="user" v-else>
          <div class="user-login" @click="router.push('/login')">登录</div>
      </div>
  </div>
</template>

<style scoped>
#main {
    height: 100px;
    background-color: rgb(110, 185, 208);
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}
.logo {
    width: 200px;
    height: 100px;
    background-image: url('@img/logo.png');
    background-position: center;
    background-size: contain;
    background-repeat: no-repeat;
    margin-left: 100px;
}
.logo-title {
    font-size: 42px;
    margin-left: 100px;
    font-family: "清风行楷体";
    cursor: pointer;
}
.user {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-right: 200px;
}
.user-name {
    font-size: 24px;
    margin-right: 40px;
    font-family: "SanJiXinWeiBeiJian-2";
}
.user-logout {
    font-size: 20px;
    cursor: pointer;
    border: 1px solid black;
    font-family: "SanJiXinWeiBeiJian-2";
}
</style>