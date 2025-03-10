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
              @click="selectPosition(position)"
              :class="{ selected: selectedPosition === position }"
              class="option-btn"
            >
              {{ position }}
            </button>
          </div>
          <div class="test-content">
            <div v-if="currentIndex >= 0 && currentIndex < questions.length" class="test-area">
              <div class="resume-container">
                <img :src="questions[currentIndex].resumeImage" alt="简历" class="resume-image" />
                <div class="resume-label">简历{{ currentIndex + 1 }}</div>
              </div>
              <div class="judgment-buttons">
                <button @click="submitAnswer(true)" class="judgment-btn correct">√</button>
                <button @click="submitAnswer(false)" class="judgment-btn incorrect">×</button>
              </div>
              <div class="navigation-buttons">
                <button v-if="currentIndex > 0" @click="goPrevious" class="nav-btn">上一题</button>
                <button v-if="currentIndex < questions.length - 1" @click="goNext" class="nav-btn">下一题</button>
                <button v-if="currentIndex === questions.length - 1" @click="submitTest" class="nav-btn submit-btn">提交</button>
              </div>
            </div>
            <div v-else class="completed">测试已完成！总得分：{{ score }}</div>
          </div>
        </div>
        <div v-else class="placeholder">请点击“测试模块”开始测试</div>
      </main>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import router from '@/router';
import { is_login_request } from '@/api/api';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';

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
        { text: '约面管理', href: '#' },
        { text: '报酬结算', href: '#' },
        { text: '题库管理', href: '#' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,
      isTestModuleActive: true,
      currentIndex: 0,
      selectedPosition: null,
      score: 0,
      positions: ['岗位1', '岗位2', '岗位3', '岗位4', '岗位5'],
      questions: [
        { resumeImage: 'path/to/resume1.jpg', correctPosition: '岗位1' },
        { resumeImage: 'path/to/resume2.jpg', correctPosition: '岗位2' },
        { resumeImage: 'path/to/resume3.jpg', correctPosition: '岗位3' },
        { resumeImage: 'path/to/resume4.jpg', correctPosition: '岗位4' },
        { resumeImage: 'path/to/resume5.jpg', correctPosition: '岗位5' },
      ],
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
        router.push('/jhTest');
      } else if (item.id === 'test-module') {
        this.isTestModuleActive = true;
      }
    },
    goBack() {
      if (this.historyStack.length > 1) {
        this.historyStack.pop();
        this.currentMenu = this.historyStack[this.historyStack.length - 1];
        this.isTestModuleActive = false;
      } else {
        router.push('/jhTest');
      }
    },
    async fetchUserInfo() {
      const value = await is_login_request();
      if (value.status) this.user = value.data;
      else router.push('/login_register');
    },
    logout() {
      this.user = null;
      router.push('/login_register');
    },
    selectPosition(position) {
      this.selectedPosition = position;
    },
    submitAnswer(isCorrect) {
      if (!this.selectedPosition) return console.log('请选择一个岗位！');
      const currentQuestion = this.questions[this.currentIndex];
      if ((isCorrect && this.selectedPosition === currentQuestion.correctPosition) ||
          (!isCorrect && this.selectedPosition !== currentQuestion.correctPosition)) {
        this.score += 10;
      }
      this.selectedPosition = null;
    },
    goPrevious() {
      if (this.currentIndex > 0) this.currentIndex--;
    },
    goNext() {
      if (this.currentIndex < this.questions.length - 1) this.currentIndex++;
    },
    submitTest() {
      this.currentIndex = -1;
    },
  },
  created() {
    this.currentMenu = this.hrMenu;
    this.historyStack.push(this.hrMenu);
  },
  mounted() {
    this.fetchUserInfo();
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
  position: absolute;
  bottom: 30px; /* 调整位置，确保在导航按钮上方 */
  left: 50%;
  transform: translateX(-50%);
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
.navigation-buttons {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
}
.nav-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
.nav-btn:hover {
  background-color: #0056b3;
}
.submit-btn {
  background-color: #28a745;
}
.submit-btn:hover {
  background-color: #218838;
}
.completed, .placeholder {
  font-size: 18px;
  color: #333;
}
.completed {
  font-weight: bold;
  font-size: 24px;
}
</style>
