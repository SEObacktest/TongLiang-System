<template>
  <div>
    <app-header :user="user" @logout="logout" />
    <div class="container">
      <app-sidebar :menu="currentMenu" :show-back-btn="showBackBtn" @menu-click="handleClick" @go-back="goBack" />
      <main class="main-content">
        <!-- 首页内容可以在这里添加 -->
      </main>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import router from '@/router';
import { is_login_request } from '@/api/api';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';

export default {
  name: 'IndexPage',
  components: { AppHeader, AppSidebar },
  data() {
    return {
      mainMenu: [
        { text: '首页', href: '#', active: true, id: 'home' },
        { text: '在线剪辑', href: '#' },
        { text: '在线私域', href: '#' },
        { text: '在线HR', href: '#', id: 'online-hr' },
      ],
      hrMenu: [
        { text: '首页', href: '#', active: false, id: 'home' },
        { text: '测试模块', href: '#', id: 'test-module' },
        { text: '约面管理', href: '#' },
        { text: '报酬结算', href: '#' },
        { text: '题库管理', href: '#' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,
    };
  },
  computed: {
    showBackBtn() {
      return !this.currentMenu.some(item => item.id === 'home' && item.active);
    },
  },
  methods: {
    handleClick(item) {
      if (item.id === 'online-hr') {
        this.historyStack.push(this.hrMenu);
        this.currentMenu = this.hrMenu;
      } else if (item.id === 'home') {
        this.historyStack = [this.mainMenu];
        this.currentMenu = this.mainMenu;
      } else if (item.id === 'test-module') {
        router.push('/test-module');
      }
    },
    goBack() {
      if (this.historyStack.length > 1) {
        this.historyStack.pop();
        this.currentMenu = this.historyStack[this.historyStack.length - 1];
      }
    },
    async fetchUserInfo() {
      const value = await is_login_request();
      if (value.status === true) {
        this.user = value.data;
      } else {
        this.user = null;
        router.push('/login_register');
      }
    },
    logout() {
      this.user = null;
      router.push('/login_register');
    },
  },
  created() {
    this.currentMenu = this.mainMenu;
    this.historyStack.push(this.mainMenu);
  },
  mounted() {
    this.fetchUserInfo();
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: calc(100vh - 60px);
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: #fff;
}
</style>