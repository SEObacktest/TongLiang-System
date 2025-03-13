<template>
  <div>
    <app-header :user="user" @logout="logout" />
    <div class="container">
      <app-sidebar :menu="currentMenu" :show-back-btn="showBackBtn" @menu-click="handleClick" @go-back="goBack" />
      <main class="main-content">
        <!-- 上传成功页面 -->
        <div v-if="uploadSuccess" class="success-container">
          <div class="success-icon">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="45" fill="#00c853" />
              <path d="M30 50 L45 65 L70 35" stroke="white" stroke-width="8" fill="none" />
            </svg>
          </div>
          <h2 class="success-title">上传成功！</h2>
          <div class="divider"></div>
          <button @click="backToHome" class="back-home-btn">回到主页</button>
        </div>

        <!-- 错误提示 -->
        <div v-else-if="errorMessage" class="error-container">
          <div class="error-icon">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="45" fill="#f44336" />
              <path d="M35 35 L65 65 M65 35 L35 65" stroke="white" stroke-width="8" fill="none" />
            </svg>
          </div>
          <h2 class="error-title">上传失败</h2>
          <p class="error-message">{{ errorMessage }}</p>
          <div class="divider"></div>
          <button @click="resetError" class="retry-btn">重试</button>
        </div>

        <!-- 上传中状态 -->
        <div v-else-if="isSubmitting" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">正在上传，请稍候...</p>
        </div>

        <!-- 上传表单 -->
        <div v-else class="upload-form">
          <div class="form-group" :class="{ 'has-error': validationErrors.candidateName }">
            <label for="candidateName">候选人姓名 <span class="required">*</span></label>
            <input type="text" id="candidateName" v-model="formData.candidateName" class="form-control">
            <small v-if="validationErrors.candidateName" class="error-text">{{ validationErrors.candidateName }}</small>
          </div>
          <div class="form-group" :class="{ 'has-error': validationErrors.position }">
            <label for="position">应聘岗位 <span class="required">*</span></label>
            <select id="position" v-model="formData.position" class="form-control">
              <option value="">请选择岗位</option>
              <option v-for="position in positions" :key="position" :value="position">{{ position }}</option>
            </select>
            <small v-if="validationErrors.position" class="error-text">{{ validationErrors.position }}</small>
          </div>
          <div class="form-group" :class="{ 'has-error': validationErrors.commuting_time }">
            <label for="commuting_time">通勤时间 <span class="required">*</span></label>
            <input type="text" id="commuting_time" v-model="formData.commuting_time" class="form-control" placeholder="例如：30分钟">
            <small v-if="validationErrors.commuting_time" class="error-text">{{ validationErrors.commuting_time }}</small>
          </div>
          <div class="form-group" :class="{ 'has-error': validationErrors.interviewDate }">
            <label for="interviewDate">预约面试日期 <span class="required">*</span></label>
            <input type="datetime-local" id="interviewDate" v-model="formData.interviewDate" class="form-control">
            <small v-if="validationErrors.interviewDate" class="error-text">{{ validationErrors.interviewDate }}</small>
          </div>
          <div class="form-group" :class="{ 'has-error': validationErrors.resume }">
            <label for="resumeUpload">上传简历 <span class="required">*</span></label>
            <input type="file" id="resumeUpload" @change="handleFileUpload" class="form-control-file">
            <small class="form-text text-muted">支持图片、PDF、Word文档格式</small>
            <small v-if="validationErrors.resume" class="error-text">{{ validationErrors.resume }}</small>
          </div>
          <div class="form-actions">
            <button type="button" @click="submitForm" class="btn-submit" :disabled="isSubmitting">提交</button>
            <button type="button" @click="resetForm" class="btn-reset" :disabled="isSubmitting">重置</button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import router from '@/router';
import { is_login_request } from '@/api/api';
import { create_interview_request } from '@/api/api';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';
// 导入axios用于API请求
import axios from 'axios';

export default {
  name: 'InterviewUpload',
  components: { AppHeader, AppSidebar },
  data() {
    return {
      mainMenu: [
        { text: '首页', href: '#', active: false, id: 'home' },
        { text: '在线剪辑', href: '#' },
        { text: '在线私域', href: '#' },
        { text: '在线HR', href: '#', id: 'online-hr' },
      ],
      hrMenu: [
        { text: '首页', href: '#', active: false, id: 'home' },
        { text: '测试模块', href: '#', id: 'test-module' },
        { text: '约面管理', href: '#', id: 'interview-management' },
        { text: '报酬结算', href: '#' },
        { text: '题库管理', href: '#' },
      ],
      interviewMenu: [
        { text: '首页', href: '#', active: false, id: 'home' },
        { text: '待约面信息上传', href: '#', active: true, id: 'interview-upload' },
        { text: '待约面信息查询', href: '#', id: 'interview-query' },
        { text: '待约面信息修改', href: '#', id: 'interview-edit' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,
      positions: ['岗位1', '岗位2', '岗位3', '岗位4', '岗位5',
                  '岗位6', '岗位7', '岗位8', '岗位9', '岗位10'],
      formData: {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate:'',
        resume: null,
      },
      uploadSuccess: false,
      isSubmitting: false,
      errorMessage: '',
      validationErrors: {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate:'',
        resume: ''
      }
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
        router.push('/');
      } else if (item.id === 'test-module') {
        router.push('/test-module');
      } else if (item.id === 'interview-management') {
        this.historyStack.push(this.interviewMenu);
        this.currentMenu = this.interviewMenu;
      } else if (item.id === 'interview-upload') {
        router.push('/interview-upload');
      } else if (item.id === 'interview-query') {
        router.push('/interview-query');
      } else if (item.id === 'interview-edit') {
        router.push('/interview-edit');
      }
    },
    goBack() {
      if (this.historyStack.length > 1) {
        this.historyStack.pop();
        this.currentMenu = this.historyStack[this.historyStack.length - 1];
      } else {
        router.push('/');
      }
    },
    async fetchUserInfo() {
      const value = await is_login_request();
      if (value.status) this.user = value.data;
      // else router.push('/login_register');
    },
    logout() {
      this.user = null;
      // router.push('/login_register');
    },
    handleFileUpload(event) {
      this.formData.resume = event.target.files[0];
      this.validationErrors.resume = ''; // 清除文件验证错误
    },
    validateForm() {
      let isValid = true;
      this.validationErrors = {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate:'',
        resume: ''
      };

      // 验证候选人姓名
      if (!this.formData.candidateName.trim()) {
        this.validationErrors.candidateName = '请输入候选人姓名';
        isValid = false;
      }

      // 验证应聘岗位
      if (!this.formData.position) {
        this.validationErrors.position = '请选择应聘岗位';
        isValid = false;
      }

      // 验证通勤时间
      if (!this.formData.commuting_time.trim()) {
        this.validationErrors.commuting_time = '请输入通勤时间';
        isValid = false;
      }
      if (!this.formData.interviewDate) {
        this.validationErrors.interviewDate = '请选择预约面试日期';
        isValid = false;
      }

      // 验证简历文件
      if (!this.formData.resume) {
        this.validationErrors.resume = '请上传简历文件';
        isValid = false;
      }

      return isValid;
    },
    async submitForm() {
      // 表单验证
      if (!this.validateForm()) {
        return;
      }

      this.isSubmitting = true;
      this.errorMessage = '';

      try {

        const data = {
          'name': this.formData.candidateName,
          'post': this.formData.position,
          'commuteTime': this.formData.commuting_time,
          'time': this.formData.interviewDate,
          'hr': this.user ? this.user.username : '未登录用户',
        };

        const value = await create_interview_request(data, this.formData.resume);

        if (value.status === true) {
          console.log('上传成功:', value.message);
          this.uploadSuccess = true;
          this.resetForm();
        } else {
          this.errorMessage = value.message || '上传失败，请稍后重试';
        }
      } catch (error) {
        console.error('上传失败:', error);
        this.errorMessage = error.response?.data?.message || '上传失败，请稍后重试';
      } finally {
        this.isSubmitting = false;
      }
    },

    resetForm() {
      this.formData = {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: null,
      };
      // 重置文件上传框
      const fileInput = document.getElementById('resumeUpload');
      if (fileInput) fileInput.value = '';

      // 重置验证错误
      this.validationErrors = {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: ''
      };
    },
    resetError() {
      this.errorMessage = '';
    },
    backToHome() {
      // 返回首页
      this.uploadSuccess = false; // 重置上传状态
      this.historyStack = [this.mainMenu];
      this.currentMenu = this.mainMenu;
      router.push('/');
    }
  },
  created() {
    this.currentMenu = this.interviewMenu;
    this.historyStack = [this.mainMenu, this.hrMenu, this.interviewMenu];
  },
  mounted() {
    this.fetchUserInfo();
  }
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
  overflow-y: auto;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.upload-form {
  max-width: 800px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.required {
  color: #f44336;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.has-error .form-control {
  border-color: #f44336;
}

.error-text {
  color: #f44336;
  font-size: 14px;
  margin-top: 5px;
  display: block;
}

.form-control-file {
  padding: 5px 0;
}

.form-text {
  font-size: 14px;
  color: #6c757d;
  margin-top: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.btn-submit, .btn-reset {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover {
  background-color: #0056b3;
}

.btn-submit:disabled {
  background-color: #b3d7ff;
  cursor: not-allowed;
}

.btn-reset {
  background-color: #6c757d;
  color: white;
}

.btn-reset:hover {
  background-color: #5a6268;
}

.btn-reset:disabled {
  background-color: #a1a8ae;
  cursor: not-allowed;
}

/* 上传成功页面样式 */
.success-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.success-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
}

.success-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.divider {
  width: 60%;
  height: 1px;
  background-color: #ddd;
  margin: 20px 0;
}

.back-home-btn {
  padding: 10px 20px;
  background-color: #00c853;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-home-btn:hover {
  background-color: #009624;
}

/* 错误页面样式 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

.error-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
}

.error-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #f44336;
}

.error-message {
  font-size: 16px;
  color: #555;
  max-width: 400px;
}

.retry-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background-color: #d32f2f;
}

/* 加载状态样式 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-text {
  font-size: 18px;
  color: #555;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>