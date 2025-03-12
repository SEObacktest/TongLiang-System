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

          <!-- 新增输入框：所在城市 -->
          <InputField label="所在城市" v-model="formData.city" placeholder="请输入所在城市" />

          <!-- 新增出生日期，让用户选择 -->
          <InputField label="出生日期" v-model="formData.birthDate" type="date" />

          <!-- 新增下拉菜单选择性别 -->
          <label for="genderSelect">性别：</label>
          <select id="genderSelect" v-model="formData.gender">
            <option value="">请选择性别</option>
            <option value="male">男</option>
            <option value="female">女</option>
            <option value="未注明">N/A</option>
          </select>

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
        birthDate: "",   // 新增字段：出生年月日
        gender: "" ,      // 新增字段：性别
        city: ""
      }
    };
  },
  computed: {
    // 根据出生年月日，自动计算年龄
    computedAge() {
      if (!this.formData.birthDate) return 0; // 如果还没选日期，就返回 0 或你想给的默认值

      const birth = new Date(this.formData.birthDate);
      if (isNaN(birth.getTime())) {
        // 如果传进来的日期无效
        return 0;
      }

      // 计算“当前年份 - 出生年份”，再考虑月份/日的影响
      // 简单做法：按年度来算
      const now = new Date();
      let age = now.getFullYear() - birth.getFullYear();

      // 如果还没到生日就减一岁
      const nowMonthDay = (now.getMonth() + 1) * 100 + now.getDate();
      const birthMonthDay = (birth.getMonth() + 1) * 100 + birth.getDate();
      if (nowMonthDay < birthMonthDay) {
        age -= 1;
      }

      // 确保是一个整数
      return age < 0 ? 0 : age;
    }
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
          // 填充表单
          this.formData.userId = resp.data.userId;
          this.formData.username = resp.data.username;
          this.formData.phone = resp.data.phone;
          // 如果后端也存了 birthDate、gender，可以在这里一起赋值
        }
      } catch (error) {
        alert("加载用户信息失败，请检查网络或重新登录");
        console.error(error);
        this.$router.push("/login_register");
      }
    },

    async submitForm() {
      try {
        // 把computedAge 作为数字传给后端
        const ageNumber = Number(this.computedAge);

        // 拼接后端需要的payload
        const payload = {
          userId: this.formData.userId,
          username: this.formData.username,
          phone: this.formData.phone,
          bankCard: this.formData.bankCard,
          bank: this.formData.bank,
          // 关键点：后端要 age 是数字，不要传空字符串
          age: ageNumber,            
          gender: this.formData.gender || "",
          // 新增字段：city
          city: this.formData.city || "",
          
          // 如果后端不需要存 birthDate 原数据，就不传
          // 或者后端若也需要 birthDate，就加上
          // birthDate: this.formData.birthDate,

          // 你原本的字段
          accountHolderName: this.formData.accountHolderName || "",
          idCard: this.formData.idCard || "",
          account: this.formData.account || ""
        };

        console.log("即将提交:", payload);

        // 发请求给后端
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
