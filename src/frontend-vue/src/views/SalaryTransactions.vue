<template>
  <div>
    <NavBar />
    <div class="container">
      <SideMenu />
      <div class="content">
        <h2>报酬流水详情</h2>
        <p><strong>姓名：</strong> {{ userData.name }}</p>
        <table class="transaction-table">
          <thead>
            <tr>
              <th>结算时间</th>
              <th>报酬</th>
              <th>操作人</th>
              <th>银行卡</th>
              <th>银行</th>
              <th>身份证</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="settlement in settlements" :key="settlement.id">
              <td>{{ settlement.settlement_time }}</td>
              <td>{{ settlement.amount }}</td>
              <td>{{ settlement.hr }}</td>
              <td>{{ settlement.bankCard }}</td>
              <td>{{ settlement.bank }}</td>
              <td>{{ settlement.idCard }}</td>
            </tr>
          </tbody>
        </table>
        <button @click="$router.push('/salary-form')" class="btn">回到报酬结算主页</button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import SideMenu from "@/components/SideMenu.vue";
export default {
  components: { NavBar, SideMenu },
  data() {
    return {
      userData: {
        name: "xxx" // 这里可以改为从后端获取用户数据
      },
      settlements: [] // 存储结算流水数据
    };
  },
  mounted() {
    this.fetchTransactions();
  },
  methods: {
    async fetchTransactions() {
      try {
        const response = await fetch("/api/get_settlement_list/");
        const result = await response.json();
        if (result.status) {
          // 假设result.data是结算数据列表
          this.settlements = result.data;
        } else {
          alert("获取交易数据失败：" + result.message);
        }
      } catch (error) {
        alert("无法获取数据，请稍后重试");
      }
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
  width: 100%;
}
.transaction-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}
.transaction-table th, .transaction-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}
.transaction-table th {
  background-color: #f2f2f2;
}
.btn {
  padding: 10px 15px;
  background-color: #87CEEB;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 20px;
}
.btn:hover {
  background-color: #5DADE2;
}
</style>
