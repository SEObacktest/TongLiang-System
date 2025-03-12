<template>
  <div>
    <Header />
    <div class="container">
      <SideMenu />
      <div class="content">
        <h2>报酬详情</h2>
        <p><strong>姓名：</strong> {{ salaryData.name || "未提供" }}</p>
        <table class="salary-table">
          <tbody>
            <tr>
              <td>应收报酬</td>
              <td>{{ salaryData.amount_due || "N/A" }}</td>
            </tr>
            <tr>
              <td>已收报酬</td>
              <td>{{ salaryData.amount_received || "N/A" }}</td>
            </tr>
            <tr>
              <td>下次发放时间</td>
              <!-- 这里显示 payDay -->
              <td>{{ salaryData.next_payment_date || "N/A" }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="viewTransactionDetails" class="btn">点击查看流水详情</button>
        <button @click="$router.push('/salary-form')" class="btn back">回到报酬结算主页</button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/header/Header.vue";
import SideMenu from "@/components/SideMenu.vue";
import { user_info_request } from "@/api/api"; 
// 记得把 user_info_request 引入

export default {
  components: { Header, SideMenu },
  data() {
    return {
      salaryData: {
        name: "",
        amount_due: "",
        amount_received: "",
        next_payment_date: ""
      }
    };
  },
  async mounted() {
    // 在页面挂载时，调用 user_info_request
    try {
      const resp = await user_info_request();
      // 后端返回 { status: true/false, data: {...}, message: "..." }
      if (resp.status) {
        this.salaryData.name = resp.data.username || "";
        this.salaryData.next_payment_date = resp.data.payDay || "";
        console.log(resp.data.payDay)
      } else {
        console.warn("获取用户信息失败:", resp.message);
        this.$router.push("/login_register");
      }
    } catch (error) {
      console.error("请求 user_info 失败:", error);
      // this.$router.push("/login_register");
    }
  },
  methods: {
    viewTransactionDetails() {
      this.$router.push("/salary-transactions");
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
.salary-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}
.salary-table td {
  padding: 10px;
  border: 1px solid #ddd;
}
.btn {
  padding: 10px 15px;
  background-color: #87CEEB;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 10px;
}
.back {
  background-color: gray;
}
</style>
