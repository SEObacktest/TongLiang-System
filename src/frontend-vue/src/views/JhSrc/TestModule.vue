<template>
  <div>
    <app-header :user="user" @logout="logout" />
    <div class="container">
      <app-sidebar :menu="currentMenu" :show-back-btn="showBackBtn" @menu-click="handleClick" @go-back="goBack" />
      <main class="main-content">
        <div v-if="isTestModuleActive" class="test-layout">
          <div class="options-column">
            <button
              v-for="position in positions"
              :key="position"
              @click="showPositionStandard(position)"
              :class="{ selected: selectedPosition === position }"
              class="option-btn"
            >
              {{ position }}
            </button>
          </div>
          <div class="test-content">
            <div v-if="currentIndex >= 0 && currentIndex < questions.length" class="test-area">
              <!-- 添加: 显示当前题目的岗位信息 -->
              <div class="question-info">
                <span class="question-number">题目 {{ currentIndex + 1 }}/{{ questions.length }}</span>
                <span class="position-label">岗位: {{ questions[currentIndex].post }}</span>
              </div>
              <div class="resume-container">
                <img :src="url + questions[currentIndex].file_url" alt="简历" class="resume-image" />
                <div class="resume-label">简历{{ currentIndex + 1 }}</div>
              </div>
              <div class="judgment-buttons">
                <button @click="submitAnswer(true)" class="judgment-btn correct">√</button>
                <button @click="submitAnswer(false)" class="judgment-btn incorrect">×</button>
              </div>
              <!-- 完全移除导航按钮区域 -->

            </div>
            <div v-else-if="testSubmitted" class="completed">测试已完成！总得分：{{ score }}</div>
            <div v-else class="loading">正在加载题目...</div>
          </div>
        </div>
      </main>
    </div>

    <!-- 岗位标准弹窗 -->
    <div v-if="showStandardModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>{{ currentPositionStandard.title }}</h3>
        <p>{{ currentPositionStandard.content }}</p>
        <button @click="closeModal" class="modal-close-btn">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import router from '@/router';
import { is_login_request } from '@/api/api';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';
import axios from 'axios';

export default {
  name: 'TestModule',
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
        { text: '测试模块', href: '#', active: true, id: 'test-module' },
        { text: '约面管理', href: '#', id: 'interview-management' },
        { text: '报酬结算', href: '#' },
        { text: '题库管理', href: '#' },
      ],
      interviewMenu: [
        { text: '首页', href: '#', active: false, id: 'home' },
        { text: '待约面信息上传', href: '#', id: 'interview-upload' },
        { text: '待约面信息查询', href: '#', id: 'interview-query' },
        { text: '待约面信息修改', href: '#', id: 'interview-edit' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,
      isTestModuleActive: true,
      currentIndex: 0,
      selectedPosition: null,
      score: 0,
      url: 'http://192.168.3.215:8000',
      positions: ['岗位1', '岗位2', '岗位3', '岗位4', '岗位5',
                  '岗位6', '岗位7', '岗位8', '岗位9', '岗位10'],
      questions: [],
      // 记录用户的答案
      userAnswers: [],
      testSubmitted: false,
      // 岗位标准弹窗相关数据
      showStandardModal: false,
      currentPositionStandard: {
        title: '',
        content: ''
      },
      // 岗位标准内容
      positionStandards: {
        '岗位1': '略',
        '岗位2': '略',
        '岗位3': '略',
        '岗位4': '略',
        '岗位5': '略',
        '岗位6': '略',
        '岗位7': '略',
        '岗位8': '略',
        '岗位9': '略',
        '岗位10': '略',
      }
    };
  },
  computed: {
    showBackBtn() {
      return !this.currentMenu.some(item => item.id === 'home' && item.active);
    },
  },
  methods: {
    // 删除不需要的isAnswered方法
    handleClick(item) {
      if (item.id === 'online-hr') {
        this.historyStack.push(this.hrMenu);
        this.currentMenu = this.hrMenu;
      } else if (item.id === 'home') {
        this.historyStack = [this.mainMenu];
        this.currentMenu = this.mainMenu;
        router.push('/');
      } else if (item.id === 'test-module') {
        this.isTestModuleActive = true;
        // 当进入测试模块时，从后端获取题目
        this.fetchTestQuestions();
      } else if (item.id === 'interview-management') {
        // 添加约面管理相关功能
        this.historyStack.push(this.interviewMenu);
        this.currentMenu = this.interviewMenu;
        this.isTestModuleActive = false; // 隐藏测试模块内容
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
        // 如果返回到了HR菜单，需要重新显示测试模块
        if (this.currentMenu === this.hrMenu) {
          this.isTestModuleActive = true;
        } else {
          this.isTestModuleActive = false;
        }
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
      router.push('/login_register');
    },

    // 显示岗位标准弹窗
    showPositionStandard(position) {
      this.currentPositionStandard = {
        title: `${position}评判标准`,
        content: this.positionStandards[position]
      };
      this.showStandardModal = true;
    },

    closeModal() {
      this.showStandardModal = false;
    },

    // 提交答案并自动切换到下一题
    submitAnswer(isCorrect) {
      // 记录用户的答案 - 确保questionId是字符串类型
      this.userAnswers.push({
        questionId: String(this.questions[this.currentIndex].id),
        answer: isCorrect
      });

      // 自动进入下一题
      if (this.currentIndex < this.questions.length - 1) {
        this.currentIndex++;
      } else {
        // 如果是最后一题，自动提交答案
        this.submitTest();
      }
    },

    // 提交测试答案到后端
    async submitTest() {
      try {
        this.isSubmitting = true;
        // 修改: 确保使用正确的API端点
        const response = await axios.post('http://192.168.3.215:8000/api/post_exam_result/', this.userAnswers);
        if (response.data.status) {
          this.score = response.data.data;
          this.testSubmitted = true;
          this.currentIndex = -1; // 隐藏题目显示区域
          alert(`测试已完成，您的得分是：${this.score}`);
        } else {
          alert(`提交失败：${response.data.message}`);
        }
      } catch (error) {
        console.error('提交答案失败:', error);
        alert('提交答案失败，请稍后重试！');
      }
      finally {
    // 添加: 无论成功还是失败，都结束加载状态
        this.isSubmitting = false;
      }
    },

    // 从后端获取题目
    async fetchTestQuestions() {
      try {
        const response = await axios.get('http://192.168.3.215:8000/api/get_exam_question_list/');
        if (response.data.status) {
          this.questions = response.data.data;
          // 重置测试状态
          this.currentIndex = 0;
          this.userAnswers = [];
          this.score = 0;
          this.testSubmitted = false;
          this.selectedPosition = null;
        } else {
          alert(`获取题目失败：${response.data.data}`);
        }
      } catch (error) {
        console.error('获取题目失败:', error);
        alert('获取题目失败，请稍后重试！');
      }
    }
  },
  created() {
    this.currentMenu = this.hrMenu;
    this.historyStack.push(this.hrMenu);
  },
  mounted() {
    this.fetchUserInfo();
    // 进入页面时自动获取题目
    this.fetchTestQuestions();
  },
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
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  position: relative;
}

.test-layout {
  display: flex;
  width: 100%;
  max-width: 1000px;
}

.options-column {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-right: 20px;
}

.option-btn {
  padding: 10px 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  width: 120px;
}

.option-btn.selected {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.test-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: calc(100vh - 100px);
  padding-bottom: 100px;
}

.test-area {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

/* 添加: 题目信息样式 */
.question-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
}

.question-number {
  font-weight: bold;
}

.position-label {
  color: #007bff;
  font-weight: bold;
}

.resume-container {
  position: relative;
  margin-bottom: 20px;
}

.resume-image {
  max-width: 600px;
  max-height: 800px;
  display: block;
  margin: 0 auto;
}

.resume-label {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
}

.judgment-buttons {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  /* 调整判断按钮位置，由于没有导航按钮 */
  position: relative;
  padding-bottom: 20px;
}

.judgment-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  width: 60px;
}

.judgment-btn.correct {
  background-color: #28a745;
  color: white;
}

.judgment-btn.incorrect {
  background-color: #dc3545;
  color: white;
}

.judgment-btn:hover {
  opacity: 0.9;
}

/* 删除不再需要的导航按钮样式 */

.completed, .placeholder, .loading {
  font-size: 18px;
  color: #333;
}

.completed {
  font-weight: bold;
  font-size: 24px;
}

/* 加载提示样式 */
.loading {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 添加: 加载中状态下的按钮样式 */
.loading-buttons {
  margin-top: 30px;
}

.judgment-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 80%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-close-btn {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.modal-close-btn:hover {
  background-color: #0056b3;
}
</style>