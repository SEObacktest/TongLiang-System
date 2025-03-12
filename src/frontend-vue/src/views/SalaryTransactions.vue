<template>
    <div>
      <NavBar />
      <div class="container">
        <SideMenu />
        <div class="content">
          <h2>流水详情</h2>
          <p><strong>姓名：</strong> {{ userData.name }}</p>
          <table class="transaction-table">
            <thead>
              <tr>
                <th>时间</th>
                <th>交易类型</th>
                <th>金额</th>
                <th>交易状态</th>
                <th>发起方/接收方</th>
                <th>备注</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="transaction in transactions" :key="transaction.id">
                <td>{{ transaction.date }}</td>
                <td>{{ transaction.type }}</td>
                <td>{{ transaction.amount }}</td>
                <td>{{ transaction.status }}</td>
                <td>{{ transaction.party }}</td>
                <td>{{ transaction.note }}</td>
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
        transactions: [] // 存储交易流水数据
      };
    },
    mounted() {
      this.fetchTransactions();
    },
    methods: {
      async fetchTransactions() {
        try {
          const response = await fetch("/api/salary-transactions"); // 假设后端提供 API
          const result = await response.json();
          if (result.success) {
            this.transactions = result.data;
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
  