<template>
  <div class="side-menu">
    <ul>
      <li :class="{ active: isActive('/') }">
        <router-link to="/">首页</router-link>
      </li>
      <li :class="{ active: isActive('/test-module') }">
        <router-link to="/test-module">测试模块</router-link>
      </li>
      <li :class="{ active: isActive('/interview-management') }">
        <router-link to="/interview-management">约面管理</router-link>
      </li>

      <!-- 报酬结算 折叠菜单 -->
      <li @click="toggleSalaryMenu" class="collapsible" :class="{ active: isSalaryActive }">
        <span>报酬结算</span>
        <span class="arrow" :class="{ rotated: salaryMenuOpen }">▶</span>
      </li>
      <ul v-show="salaryMenuOpen" class="submenu">
        <li :class="{ active: isActive('/salary-form') }">
          <router-link to="/salary-form">结算信息登记与修改</router-link>
        </li>
        <li :class="{ active: isActive('/salary-detail') }">
          <router-link to="/salary-detail">结算信息查询</router-link>
        </li>
      </ul>

      <li :class="{ active: isActive('/question-bank') }">
        <router-link to="/question-bank">题库管理</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      salaryMenuOpen: false // 控制折叠展开
    };
  },
  computed: {
    isSalaryActive() {
      // 只要当前页面是 salary-form 或 salary-detail，报酬结算菜单都应该高亮
      return this.$route.path.startsWith("/salary-form") || this.$route.path.startsWith("/salary-detail");
    }
  },
  watch: {
    // 监听路由变化，确保"报酬结算"子菜单选中时不会折叠
    $route(to) {
      if (to.path.startsWith("/salary-form") || to.path.startsWith("/salary-detail")) {
        this.salaryMenuOpen = true;
      }
    }
  },
  methods: {
    toggleSalaryMenu() {
      this.salaryMenuOpen = !this.salaryMenuOpen;
    },
    isActive(path) {
      return this.$route.path === path;
    }
  }
};
</script>

<style scoped>
.side-menu {
  width: 200px;
  background-color: #f8f9fa;
  padding: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
}

/* 让默认字体变成黑色，并去掉访问后变紫色的效果 */
a {
  color: black;
  text-decoration: none; /* 去掉下划线 */
}

a:visited {
  color: black; /* 访问过后依然是黑色 */
}

li:hover {
  background-color: #e0e0e0;
}

/* 选中的菜单项 */
.active {
  background-color: #87CEEB !important; /* 浅蓝色高亮 */
  color: white;
}

/* 报酬结算父菜单 */
.collapsible {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 箭头旋转效果 */
.arrow {
  transition: transform 0.3s ease;
}

.rotated {
  transform: rotate(90deg); /* 旋转箭头 */
}

/* 子菜单样式 */
.submenu {
  padding-left: 15px;
  transition: all 0.3s ease;
}

.submenu li {
  padding: 8px;
  background: #f0f0f0;
  border-left: 3px solid #87CEEB;
}
</style>
