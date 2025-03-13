<template>
  <div>
    <!-- Changed NavBar to Header -->
    <Header />
    <div class="container">
      <SideMenu />
      <div class="content">
        <h2>个人信息</h2>
        <FormCard>
          <p><strong>姓名：</strong> {{ userData.username || "N/A" }}</p>
          <p><strong>收款银行卡号：</strong> {{ userData.bankCard || "N/A" }}</p>
          <p><strong>开户行：</strong> {{ userData.bank || "N/A" }}</p>
          <p><strong>电话：</strong> {{ userData.phone || "N/A" }}</p>
          <p><strong>所在城市：</strong> {{ userData.city || "N/A" }}</p>
          <p><strong>年龄：</strong> {{ userData.age || "N/A" }}</p>
          <p><strong>性别：</strong> {{ userData.gender || "N/A" }}</p>
          
          <SubmitButton label="修改" @click="editInfo" />
        </FormCard>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/header/Header.vue";  // replaced header import
import SideMenu from "@/components/SideMenu.vue";
import FormCard from "@/components/FormCard.vue";
import SubmitButton from "@/components/SubmitButton.vue";

import { user_info_request } from "@/api/api";

export default {
  name: "UserInfo",
  components: {
    Header,            // replaced NavBar with Header
    SideMenu,
    FormCard,
    SubmitButton
  },
  data() {
    return {
      userData: {
        // 用于显示在页面上
        username: "",
        bankCard: "",
        bank: "",
        phone: "",
        city: "",
        age: "",
        gender: ""
      }
    };
  },
  async created() {
    // 组件加载时就去获取用户信息
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await user_info_request();
        // 后端返回形如 { status: true/false, data: {...}, message: "xxx" }
        if (response.status) {
          // 将后端 data 中的字段映射到 userData
          // 注意后端返回的键名：username, bankCard, bank, phone ...
          this.userData.username = response.data.username || "";
          this.userData.bankCard = response.data.bankCard || "";
          this.userData.bank = response.data.bank || "";
          this.userData.phone = response.data.phone || "";
          this.userData.city = response.data.city || "";
          this.userData.age = response.data.age || "";
          // 修改gender字段的显示规则
          if (response.data.gender === 'male') {
            this.userData.gender = '男';
          } else if (response.data.gender === 'female') {
            this.userData.gender = '女';
          } else {
            this.userData.gender = 'N/A';
          }
        } else {
          // 未登录或其他错误时，可以跳转到登录
          console.warn("获取用户信息失败:", response.message);
          this.$router.push("/login_register");
        }
      } catch (error) {
        console.error("获取用户信息时出错:", error);
        this.$router.push("/login_register");
      }
    },
    editInfo() {
      // 点击“修改”按钮，把 userData 作为路由的 query 传给编辑页面
      this.$router.push({
        path: "/edit-salary-info",
        query: this.userData
      });
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
}
.content {
  padding: 20px;
}
</style>
