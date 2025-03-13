<!-- 用于用户界面的报酬详情 -->
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
              <td>应收报酬 (待发工资，根据面试数据与发薪日计算)</td>
              <td>{{ formattedAmountDue }}</td>
            </tr>
            <tr>
              <td>已收报酬 (累计结算金额)</td>
              <td>{{ formattedAmountReceived }}</td>
            </tr>
            <tr>
              <td>未结算线下面试数量：</td>
              <td>{{ unsettledCount }}</td>
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
import { user_info_request, get_salary_info_request } from "@/api/api"; 

export default {
  components: { Header, SideMenu },
  data() {
    return {
      salaryData: {
        name: "",
        amount_due: "",
        amount_received: "",
        next_payment_date: ""
      },
      unsettledCount: 0
    };
  },
  async mounted() {
    // 在页面挂载时，调用 user_info_request
    try {
      const respUser = await user_info_request();
      // 后端返回 { status: true/false, data: {...}, message: "..." }
      if (respUser.status) {
        this.salaryData.name = respUser.data.username || "";
        //this.salaryData.next_payment_date = resp.data.payDay || "";
        this.salaryData.next_payment_date = respUser.data.payDay 
          ? new Date(respUser.data.payDay).toISOString().split('T')[0] 
          : "";
        console.log(respUser.data.payDay)
      } else {
        console.warn("获取用户信息失败:", respUser.message);
        this.$router.push("/login_register");
      }
    } catch (error) {
      console.error("请求 user_info 失败:", error);
    }

    // 新增：调用获取未结算面试数的接口
    try {
      const respSalary = await get_salary_info_request();
      if (respSalary.status) {
        this.salaryData.amount_due = respSalary.data.amount_due || "";
        this.salaryData.amount_received = respSalary.data.amount_received || "";
        this.unsettledCount = respSalary.data.unsettled_interviews || 0;
      } else {
        console.warn("获取报酬信息失败:", respSalary.message);
      }
    } catch (error) {
      console.error("请求报酬信息时出错:", error);
    }
  },
  computed: {
    formattedAmountDue() {
      return this.salaryData.amount_due !== "" ? `￥${this.salaryData.amount_due}` : "N/A";
    },
    formattedAmountReceived() {
      return this.salaryData.amount_received !== "" ? `￥${this.salaryData.amount_received}` : "N/A";
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
