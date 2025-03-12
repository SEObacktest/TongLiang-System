<template>
  <div>
    <Header />
    <div class="container">
      <SideMenu />
      <div class="content">
        <h2>修改个人信息 {{ formData.username }}</h2>
        <FormCard>
          <!-- 原有字段 -->
          <InputField label="姓名" v-model="formData.username" placeholder="请输入姓名" />
          <InputField label="收款银行卡号" v-model="formData.bankCard" placeholder="请输入银行卡号" />
          <InputField label="开户行" v-model="formData.bank" placeholder="请输入开户行" />
          <InputField label="电话" v-model="formData.phone" type="tel" placeholder="请输入电话" />

          <!-- 新增账户持有人字段 -->
          <InputField label="账户持有人" v-model="formData.accountHolderName" placeholder="请输入账户持有人" />

          <!-- 新增字段：所在城市 -->
          <InputField label="所在城市" v-model="formData.city" placeholder="请输入所在城市" />

          <!-- 原有的出生日期输入框已删除，新增年龄输入框 -->
          <InputField label="年龄" v-model="formData.age" type="number" placeholder="请输入年龄" />

          <!-- 新增下拉菜单选择性别 -->
          <label for="genderSelect">性别：</label>
          <select id="genderSelect" v-model="formData.gender">
            <option value="">请选择性别</option>
            <option value="male">男</option>
            <option value="female">女</option>
            <option value="未注明">N/A</option>
          </select>

          <!-- 移动保存和取消按钮到选择性别下面 -->
          <SubmitButton label="保存" @click="submitForm" />
          <SubmitButton label="取消" class="cancel" @click="$router.push('/salary-form')" />
        </FormCard>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "./components/header/Header.vue";
import SideMenu from "@/components/SideMenu.vue";
import FormCard from "@/components/FormCard.vue";
import InputField from "@/components/InputField.vue";
import SubmitButton from "@/components/SubmitButton.vue";

import { is_login_request, hr_update_request } from "@/api/api";

export default {
  name: "EditUserInfo",
  components: { 
    Header, 
    SideMenu, 
    FormCard, 
    InputField, 
    SubmitButton 
  },
  data() {
    return {
      formData: {
        userId: "",
        username: "",
        phone: "",
        bankCard: "",
        bank: "",
        age: "",
        gender: "",
        city: "",
        accountHolderName: "" 
      }
    };
  },
  async created() {
    // 组件加载时，先获取用户登录状态
    await this.loadUserData();
  },
  methods: {
    async loadUserData() {
      try {
        const resp = await is_login_request();
        if (!resp.status) {
          // 未登录则跳转
          this.$router.push("/login_register");
        } else {
          // 填充表单，将所有字段都填上
          this.formData.userId = resp.data.userId || "";
          this.formData.username = resp.data.username || "";
          this.formData.phone = resp.data.phone || "";
          this.formData.bankCard = resp.data.bankCard || "";
          this.formData.bank = resp.data.bank || "";
          this.formData.accountHolderName = resp.data.accountHolderName || "";
          this.formData.city = resp.data.city || "";
          this.formData.age = resp.data.age || "";
          this.formData.gender = resp.data.gender || "";
          this.formData.idCard = resp.data.idCard || "";
          this.formData.account = resp.data.account || "";
          console.log(this.formData)
        }
      } catch (error) {
        alert("加载用户信息失败，请检查网络或重新登录");
        console.error(error);
        this.$router.push("/login_register");
      }
    },

    async submitForm() {
      try {
        // 构造 payload，确保所有字段都有值
        const payload = {
          userId: this.formData.userId,
          username: this.formData.username?.toString().trim() || "",
          phone: this.formData.phone?.toString().trim() || "",
          bankCard: this.formData.bankCard?.toString().trim() || "",
          bank: this.formData.bank?.toString().trim() || "",
          gender: this.formData.gender?.toString().trim() || "",
          city: this.formData.city?.toString().trim() || "",
          accountHolderName: this.formData.accountHolderName?.toString().trim() || "",
          idCard: (this.formData.idCard && this.formData.idCard.toString().trim()) || "",
          account: (this.formData.account && this.formData.account.toString().trim()) || "",
          age: this.formData.age.toString().trim() !== "" ? Number(this.formData.age) : 0
        };

        console.log("即将提交:", payload);
        const response = await hr_update_request(payload);
        if (response.status) {
          alert("信息已更新");
          this.$router.push("/salary-form");
        } else {
          alert("更新失败，请重试");
        }
      } catch (error) {
        alert("提交失败，请检查网络");
        console.error(error);
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
}
.cancel {
  background-color: gray;
  margin-left: 10px;
}
</style>
