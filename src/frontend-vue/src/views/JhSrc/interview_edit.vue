<template>
  <div>
    <app-header :user="user" @logout="logout" />
    <div class="container">
      <app-sidebar :menu="currentMenu" :show-back-btn="showBackBtn" @menu-click="handleClick" @go-back="goBack" />
      <main class="main-content">
        <!-- 待约面信息修改页面 -->
        <div class="interview-edit">
          <!-- 查询区域 -->
          <div class="search-container">
            <input type="text" v-model="searchKeyword" placeholder="输入候选人姓名查询" class="search-input">
            <button @click="searchInterviews" class="search-btn">查询</button>
            <button @click="resetSearch" class="reset-btn">重置</button>
          </div>

          <!-- 数据表格 -->
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>操作</th>
                  <th>候选人姓名</th>
                  <th>所属岗位</th>
                  <th>通勤时间</th>
                  <th>简历</th>
                  <th>约面状态</th>
                  <th>是否到面</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in displayInterviews" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td class="operation-cell">
                    <!-- 备注：添加编辑和删除图标 -->
                    <button @click="editInterview(item)" class="edit-btn" title="编辑">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </button>
                    <button @click="deleteInterview(item, index)" class="delete-btn" title="删除">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                      </svg>
                    </button>
                  </td>
                  <td>{{ item.candidateName }}</td>
                  <td>{{ item.position }}</td>
                  <td>{{ item.commuting_time }}</td>
                  <td>
                    <a v-if="item.resumeUrl" :href="item.resumeUrl" target="_blank" class="resume-link">查看简历</a>
                    <span v-else>未上传</span>
                  </td>
                  <td>{{ item.interviewStatus }}</td>
                  <td>{{ item.attended ? '是' : '否' }}</td>
                </tr>
                <tr v-if="displayInterviews.length === 0">
                  <td colspan="8" class="no-data">暂无数据</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 编辑弹窗 -->
          <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-container">
              <div class="modal-header">
                <h3>修改候选人信息</h3>
                <button @click="closeModal" class="close-btn">&times;</button>
              </div>
              <div class="modal-body">
                <!-- 备注：编辑表单，允许修改除了约面状态和是否到面外的所有信息 -->
                <div class="form-group" :class="{ 'has-error': validationErrors.candidateName }">
                  <label for="editCandidateName">候选人姓名 <span class="required">*</span></label>
                  <input type="text" id="editCandidateName" v-model="editForm.candidateName" class="form-control">
                  <small v-if="validationErrors.candidateName" class="error-text">{{ validationErrors.candidateName }}</small>
                </div>
                <div class="form-group" :class="{ 'has-error': validationErrors.position }">
                  <label for="editPosition">应聘岗位 <span class="required">*</span></label>
                  <select id="editPosition" v-model="editForm.position" class="form-control">
                    <option value="">请选择岗位</option>
                    <option v-for="position in positions" :key="position" :value="position">{{ position }}</option>
                  </select>
                  <small v-if="validationErrors.position" class="error-text">{{ validationErrors.position }}</small>
                </div>
                <div class="form-group" :class="{ 'has-error': validationErrors.commuting_time }">
                  <label for="editCommutingTime">通勤时间 <span class="required">*</span></label>
                  <input type="text" id="editCommutingTime" v-model="editForm.commuting_time" class="form-control" placeholder="例如：30分钟">
                  <small v-if="validationErrors.commuting_time" class="error-text">{{ validationErrors.commuting_time }}</small>
                </div>
                <div class="form-group" :class="{ 'has-error': validationErrors.interviewDate }">
                  <label for="editInterviewDate">预约面试日期 <span class="required">*</span></label>
                  <input type="date" id="editInterviewDate" v-model="editForm.interviewDate" class="form-control">
                  <small v-if="validationErrors.interviewDate" class="error-text">{{ validationErrors.interviewDate }}</small>
                </div>
                <div class="form-group" :class="{ 'has-error': validationErrors.resume }">
                  <label for="editResumeUpload">上传简历</label>
                  <input type="file" id="editResumeUpload" @change="handleFileUpload" class="form-control-file">
                  <small class="form-text text-muted">支持图片、PDF、Word文档格式。如不修改，则保留原简历</small>
                  <small v-if="validationErrors.resume" class="error-text">{{ validationErrors.resume }}</small>
                </div>

                <!-- 只显示但不允许修改的字段 -->
                <div class="form-group readonly">
                  <label>约面状态</label>
                  <input type="text" v-model="editForm.interviewStatus" class="form-control" readonly>
                  <small class="form-text text-muted">约面状态由管理员修改</small>
                </div>
                <div class="form-group readonly">
                  <label>是否到面</label>
                  <input type="text" :value="editForm.attended ? '是' : '否'" class="form-control" readonly>
                  <small class="form-text text-muted">是否到面由管理员修改</small>
                </div>
              </div>
              <div class="modal-footer">
                <button @click="saveEdit" class="save-btn" :disabled="isSubmitting">保存</button>
                <button @click="closeModal" class="cancel-btn">取消</button>
              </div>
            </div>
          </div>

          <!-- 删除确认弹窗 -->
          <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-container delete-modal">
              <div class="modal-header">
                <h3>确认删除</h3>
                <button @click="closeDeleteModal" class="close-btn">&times;</button>
              </div>
              <div class="modal-body">
                <p>确定要删除候选人"{{ deleteCandidate.candidateName }}"的全部信息吗？</p>
                <p class="warning-text">此操作不可恢复！</p>
              </div>
              <div class="modal-footer">
                <button @click="confirmDelete" class="delete-confirm-btn" :disabled="isSubmitting">确认删除</button>
                <button @click="closeDeleteModal" class="cancel-btn">取消</button>
              </div>
            </div>
          </div>

          <!-- 加载中遮罩 -->
          <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
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
// 导入axios用于API请求
import axios from 'axios';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';

export default {
  name: 'InterviewsEdit',
  components: { AppHeader, AppSidebar },
  data() {
    return {
      // 导航菜单相关
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
        { text: '待约面信息上传', href: '#', id: 'interview-upload' },
        { text: '待约面信息查询', href: '#', id: 'interview-query' },
        { text: '待约面信息修改', href: '#', active: true, id: 'interview-edit' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,

      // 页面数据相关
      positions: ['岗位1', '岗位2', '岗位3', '岗位4', '岗位5',
                  '岗位6', '岗位7', '岗位8', '岗位9', '岗位10'],
      interviews: [], // 所有面试数据
      displayInterviews: [], // 筛选后显示的数据
      searchKeyword: '', // 搜索关键词

      // 编辑相关
      showEditModal: false,
      editForm: {
        id: null,
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: null,
        interviewStatus: '',
        attended: false,
      },
      originalEditForm: null, // 保存原始数据用于比较

      // 删除相关
      showDeleteModal: false,
      deleteCandidate: {
        id: null,
        candidateName: '',
        index: -1
      },

      // 状态相关
      isLoading: false,
      isSubmitting: false,
      validationErrors: {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
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
    // 导航和菜单处理
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
    },
    logout() {
      this.user = null;
      router.push('/login_register');
    },

    // 数据获取和处理
    async fetchInterviews() {
      this.isLoading = true;
      try {
        // 实际项目中应替换为真实的API调用
        const response = await axios.get('http://localhost:3001/api/interview-upload');
        this.interviews = response.data;

        // 模拟数据，实际项目中应替换为真实的API返回数据
        setTimeout(() => {
          this.interviews = [
            {
              id: 1,
              candidateName: 'A',
              position: '岗位1',
              commuting_time: '30分钟',
              interviewDate: '2025-03-10',
              resumeUrl: '#',
              interviewStatus: '已上传',
              attended: true
            },
            {
              id: 2,
              candidateName: 'B',
              position: '岗位2',
              commuting_time: '60分钟',
              interviewDate: '2025-03-15',
              resumeUrl: '#',
              interviewStatus: '已上传',
              attended: false
            }
          ];
          this.displayInterviews = [...this.interviews];
          this.isLoading = false;
        }, 500);
      } catch (error) {
        console.error('获取面试信息失败:', error);
        this.isLoading = false;
      }
    },
    searchInterviews() {
      if (!this.searchKeyword.trim()) {
        this.displayInterviews = [...this.interviews];
        return;
      }

      const keyword = this.searchKeyword.toLowerCase().trim();
      this.displayInterviews = this.interviews.filter(item =>
        item.candidateName.toLowerCase().includes(keyword)
      );
    },
    resetSearch() {
      this.searchKeyword = '';
      this.displayInterviews = [...this.interviews];
    },

    // 编辑相关
    editInterview(item) {
      // 备注：打开编辑弹窗，填充数据
      this.editForm = {
        id: item.id,
        candidateName: item.candidateName,
        position: item.position,
        commuting_time: item.commuting_time,
        interviewDate: item.interviewDate,
        resume: null, // 不自动填充文件输入框
        interviewStatus: item.interviewStatus,
        attended: item.attended
      };

      // 保存原始数据用于比较
      this.originalEditForm = { ...this.editForm };

      // 重置验证错误
      this.validationErrors = {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: ''
      };

      this.showEditModal = true;
    },
    closeModal() {
      this.showEditModal = false;
      this.editForm = {
        id: null,
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: null,
        interviewStatus: '',
        attended: false
      };
    },
    handleFileUpload(event) {
      this.editForm.resume = event.target.files[0];
      this.validationErrors.resume = ''; // 清除文件验证错误
    },
    validateForm() {
      let isValid = true;
      this.validationErrors = {
        candidateName: '',
        position: '',
        commuting_time: '',
        interviewDate: '',
        resume: ''
      };

      // 验证候选人姓名
      if (!this.editForm.candidateName.trim()) {
        this.validationErrors.candidateName = '请输入候选人姓名';
        isValid = false;
      }

      // 验证应聘岗位
      if (!this.editForm.position) {
        this.validationErrors.position = '请选择应聘岗位';
        isValid = false;
      }

      // 验证通勤时间
      if (!this.editForm.commuting_time.trim()) {
        this.validationErrors.commuting_time = '请输入通勤时间';
        isValid = false;
      }

      // 验证面试日期
      if (!this.editForm.interviewDate) {
        this.validationErrors.interviewDate = '请选择预约面试日期';
        isValid = false;
      }

      return isValid;
    },
    async saveEdit() {
      // 表单验证
      if (!this.validateForm()) {
        return;
      }

      this.isSubmitting = true;

      try {
        // 创建FormData实例用于上传文件
        const formData = new FormData();
        formData.append('id', this.editForm.id);
        formData.append('candidateName', this.editForm.candidateName);
        formData.append('position', this.editForm.position);
        formData.append('commuting_time', this.editForm.commuting_time);
        formData.append('interviewDate', this.editForm.interviewDate);

        // 如果选择了新简历才上传
        if (this.editForm.resume) {
          formData.append('resume', this.editForm.resume);
        }

        // 备注：在实际应用中，这里应该发送HTTP请求保存数据
        // const response = await axios.put(`/api/interviews/${this.editForm.id}`, formData, {
        //   headers: {
        //     'Content-Type': 'multipart/form-data'
        //   }
        // });

        // 模拟API调用
        setTimeout(() => {
          // 更新本地数据
          const index = this.interviews.findIndex(item => item.id === this.editForm.id);
          if (index !== -1) {
            // 更新面试信息
            this.interviews[index] = {
              ...this.interviews[index],
              candidateName: this.editForm.candidateName,
              position: this.editForm.position,
              commuting_time: this.editForm.commuting_time,
              interviewDate: this.editForm.interviewDate,
              // 如果上传了新简历，则使用新的URL
              resumeUrl: this.editForm.resume ? URL.createObjectURL(this.editForm.resume) : this.interviews[index].resumeUrl
            };

            // 更新显示的数据
            this.displayInterviews = [...this.interviews];
          }

          // 关闭弹窗
          this.showEditModal = false;
          this.isSubmitting = false;

          // 清空表单
          this.editForm = {
            id: null,
            candidateName: '',
            position: '',
            commuting_time: '',
            interviewDate: '',
            resume: null,
            interviewStatus: '',
            attended: false
          };

          alert('修改成功');
        }, 1000);
      } catch (error) {
        console.error('更新失败:', error);
        alert('更新失败: ' + (error.response?.data?.message || '请稍后重试'));
        this.isSubmitting = false;
      }
    },

    // 删除相关
    deleteInterview(item, index) {
      // 备注：准备删除并显示确认弹窗
      this.deleteCandidate = {
        id: item.id,
        candidateName: item.candidateName,
        index: index
      };
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.deleteCandidate = {
        id: null,
        candidateName: '',
        index: -1
      };
    },
    async confirmDelete() {
      this.isSubmitting = true;

      try {
        // 备注：在实际应用中，这里应该发送HTTP请求删除数据
        // await axios.delete(`/api/interviews/${this.deleteCandidate.id}`);

        // 模拟API调用
        setTimeout(() => {
          // 从数据中移除
          if (this.deleteCandidate.index !== -1) {
            this.interviews = this.interviews.filter(item => item.id !== this.deleteCandidate.id);
            this.displayInterviews = [...this.interviews];
          }

          // 关闭弹窗
          this.showDeleteModal = false;
          this.isSubmitting = false;

          alert('删除成功');
        }, 1000);
      } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败: ' + (error.response?.data?.message || '请稍后重试'));
        this.isSubmitting = false;
      }
    }
  },
  created() {
    this.currentMenu = this.interviewMenu;
    this.historyStack = [this.mainMenu, this.hrMenu, this.interviewMenu];
  },
  mounted() {
    this.fetchUserInfo();
    this.fetchInterviews();
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

/* 搜索区域样式 */
.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex-grow: 1;
  max-width: 300px;
}

.search-btn, .reset-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn {
  background-color: #007bff;
  color: white;
}

.reset-btn {
  background-color: #6c757d;
  color: white;
}

/* 表格样式 */
.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.data-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.data-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.data-table tr:hover {
  background-color: #f0f0f0;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #777;
}

/* 操作按钮样式 */
.operation-cell {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.edit-btn, .delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 4px;
}

.edit-btn {
  color: #007bff;
}

.edit-btn:hover {
  background-color: rgba(0, 123, 255, 0.1);
}

.delete-btn {
  color: #dc3545;
}

.delete-btn:hover {
  background-color: rgba(220, 53, 69, 0.1);
}

.resume-link {
  color: #007bff;
  text-decoration: none;
}

.resume-link:hover {
  text-decoration: underline;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.delete-modal {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #777;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  border-top: 1px solid #ddd;
  gap: 10px;
}

.save-btn, .cancel-btn, .delete-confirm-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background-color: #007bff;
  color: white;
}

.save-btn:disabled {
  background-color: #b3d7ff;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.delete-confirm-btn {
  background-color: #dc3545;
  color: white;
}

.delete-confirm-btn:disabled {
  background-color: #f5c6cb;
  cursor: not-allowed;
}

.warning-text {
  color: #dc3545;
  font-weight: bold;
}

/* 表单样式 */
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

.form-control-file {
  padding: 5px 0;
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

.form-text {
  font-size: 14px;
  color: #6c757d;
  margin-top: 5px;
}

.readonly .form-control {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

/* 加载状态样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1100;
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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>