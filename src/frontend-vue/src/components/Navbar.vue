   <template>
    <nav class="navbar">
      <div class="logo">Qmacd</div>
      <div class="title">同梁在线业务系统</div>
      <div class="user-section">
        <!-- 显示后端返回的 username -->
        <span>您好，{{ username }}</span>
        <button @click="logout" class="logout-button">退出登录</button>
      </div>
    </nav>
  </template>
  
  <script>
  import { is_login_request, logout_request } from "@/api/api";
  
  export default {
    name: "SideBar",
    data() {
      return {
        username: "加载中..."
      };
    },
    async created() {
      // 组件创建时检查登录状态
      try {
        const response = await is_login_request();
        if (response.status === true) {
          // 用户已登录，设置用户名
          this.username = response.data.username;
        } else {
          // 未登录，跳转到登录/注册界面
          this.$router.push("/login_register");
        }
      } catch (error) {
        console.error("检查登录状态时出错：", error);
        this.$router.push("/login_register");
      }
    },
    methods: {
      async logout() {
        try {
          // 调后端的logout API，清除服务器端会话
          const response = await logout_request();
          console.log("退出登录返回结果：", response);
        } catch (error) {
          console.error("退出登录出错：", error);
        } finally {
          // 不管后端是否成功登出，都移除本地 token、跳转到首页或登录页
          localStorage.removeItem("token");
          this.$router.push("/login_register");
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #fff;
    border-bottom: 1px solid #ddd;
  }
  
  .logout-button {
    padding: 5px 10px;
    background-color: #007bff;
    border: none;
    color: white;
    font-size: 14px;
    cursor: pointer;
    border-radius: 4px;
  }
  </style>
  