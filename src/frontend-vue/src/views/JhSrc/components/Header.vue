<template>
  <header class="header">
    <div class="logo">
      <img src="@img/Qmacd.png" alt="Qmacd Logo" />
    </div>
    <div class="title">同梁在线业务系统</div>
    <div class="user-info">
      <span v-if="user && user.username">您好，{{ user.username }}</span>
      <span v-else>您好，未知用户</span>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>
  </header>
</template>

<script>
import {defineComponent} from 'vue';
import {useRouter} from 'vue-router';

export default defineComponent({
  name: 'Header',
  props: {
    user: {
      type: Object, // 接收 Home.vue 传递的 user 对象
      default: () => ({}) // 默认空对象，避免未定义时出错
    }
  },
  setup(props) {
    const router = useRouter(); // 引入 router 用于跳转

    const logout = () => {
      console.log('退出登录');
      router.push('/login_register'); // 退出登录后跳转到登录页面
    };

    return {logout};
  }
});
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #ddd;
}

.logo img {
  height: 40px;
}

.title {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #0056b3;
}
</style>
