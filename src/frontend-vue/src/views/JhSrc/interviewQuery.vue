<template>
  <div>
    <app-header :user="user" @logout="logout" />
    <div class="container">
      <app-sidebar :menu="currentMenu" :show-back-btn="showBackBtn" @menu-click="handleClick" @go-back="goBack" />
      <main class="main-content">
        <div class="interview-query">
          <!-- 日历视图，默认显示 -->
          <div v-if="!selectedDate" class="calendar-container">
            <div class="calendar-header">
              <button @click="prevMonth" class="nav-btn">&lt;</button>
              <h2>{{ currentYear }} / {{ currentMonth }}</h2>
              <button @click="nextMonth" class="nav-btn">&gt;</button>
            </div>

            <div class="weekdays">
              <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
            </div>

            <div class="days">
              <div
                v-for="day in calendarDays"
                :key="day.date"
                :class="['day', { 'current-month': day.currentMonth, 'other-month': !day.currentMonth, 'has-interviews': hasInterviews(day) }]"
                @click="selectDate(day)"
              >
                <div class="day-number">{{ day.dayNumber }}</div>
                <div v-if="hasInterviews(day)" class="interview-indicator"></div>
              </div>
            </div>
          </div>

          <!-- 选择日期后显示的面试时间表 -->
          <div v-else class="schedule-container">
            <div class="schedule-header">
              <button @click="backToCalendar" class="back-btn">返回日历</button>
              <h2>{{ formatSelectedDate }} 面试安排</h2>
            </div>

            <table class="schedule-table">
              <thead>
                <tr>
                  <th>可约面试时间</th>
                  <th>{{ getDayOfWeek }}</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(timeSlot, index) in timeSlots" :key="index">
                  <!-- 时间段：显示面试者姓名、面试时间和应聘岗位 -->
                  <tr>
                    <td class="time-slot">{{ timeSlot.time }}</td>
                    <td>
                      <div v-for="(interview, idx) in timeSlot.interviews" :key="idx">
                        <!-- 显示面试者姓名(name)、面试时间(interview_time)和应聘岗位(post) -->
                        {{ interview.name }} - {{ interview.interview_time }} - {{ interview.post }}
                      </div>
                    </td>
                  </tr>
                  <!-- 简历截图：显示面试者简历链接 -->
                  <tr>
                    <td>简历截图</td>
                    <td>
                      <div v-for="(interview, idx) in timeSlot.interviews" :key="idx">
                        <!-- 使用file_url字段提供简历链接 -->
                        <a :href="interview.file_url" target="_blank">查看简历</a>
                      </div>
                    </td>
                  </tr>
                  <!-- 来源：显示上传此面试信息的HR -->
                  <tr>
                    <td>来源</td>
                    <td>
                      <div v-for="(interview, idx) in timeSlot.interviews" :key="idx">
                        <!-- 显示HR信息(hr)，表示此面试信息由哪个HR上传 -->
                        {{ interview.hr }}
                      </div>
                    </td>
                  </tr>
                  <!-- 是否参加面试：显示候选人是否确认参加面试 -->
                  <tr class="last-row">
                    <td>是否参加面试</td>
                    <td>
                      <div v-for="(interview, idx) in timeSlot.interviews" :key="idx">
                        <!-- 使用isAgreed字段判断候选人是否同意参加面试 -->
                        {{ interview.isAgreed ? '已确认' : '未确认' }}
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import router from '@/router';
import { is_login_request } from '@/api/api';
import AppHeader from '@/views/JhSrc/components/Header.vue';
import AppSidebar from '@/views/JhSrc/components/Sidebar.vue';
import axios from 'axios';

export default defineComponent({
  name: 'InterviewQuery',
  components: { AppHeader, AppSidebar },
  data() {
    return {
      // 菜单相关
      mainMenu: [
        { text: '首页', href: '#', active: true, id: 'home' },
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
        { text: '待约面信息查询', href: '#', id: 'interview-query', active: true },
        { text: '待约面信息修改', href: '#', id: 'interview-edit' },
      ],
      currentMenu: [],
      historyStack: [],
      user: null,

      // 日历相关
      currentDate: new Date(),
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth() + 1,
      selectedDate: null,
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],

      // 面试数据
      allInterviews: [],
      dateInterviewMap: {}, // 日期到面试的映射

      // 面试时间段（每半小时一个，从10:00到18:00）
      timeSlots: [
        { time: '10:00-10:30', interviews: [] },
        { time: '10:30-11:00', interviews: [] },
        { time: '11:00-11:30', interviews: [] },
        { time: '11:30-12:00', interviews: [] },
        { time: '12:00-12:30', interviews: [] },
        { time: '12:30-13:00', interviews: [] },
        { time: '13:00-13:30', interviews: [] },
        { time: '13:30-14:00', interviews: [] },
        { time: '14:00-14:30', interviews: [] },
        { time: '14:30-15:00', interviews: [] },
        { time: '15:00-15:30', interviews: [] },
        { time: '15:30-16:00', interviews: [] },
        { time: '16:00-16:30', interviews: [] },
        { time: '16:30-17:00', interviews: [] },
        { time: '17:00-17:30', interviews: [] },
        { time: '17:30-18:00', interviews: [] },
      ]
    };
  },
  computed: {
    showBackBtn() {
      return !this.currentMenu.some(item => item.id === 'home' && item.active);
    },
    formatSelectedDate() {
      if (!this.selectedDate) return '';

      const year = this.selectedDate.getFullYear();
      const month = this.selectedDate.getMonth() + 1;
      const day = this.selectedDate.getDate();

      return `${year}年${month}月${day}日`;
    },
    getDayOfWeek() {
      if (!this.selectedDate) return '';

      const weekDay = this.selectedDate.getDay();
      return `周${this.weekdays[weekDay]}`;
    },
    calendarDays() {
      const year = this.currentYear;
      const month = this.currentMonth;

      // 获取当月的第一天
      const firstDay = new Date(year, month - 1, 1);
      // 获取当月的最后一天
      const lastDay = new Date(year, month, 0);

      const daysInMonth = lastDay.getDate();
      const firstDayWeekday = firstDay.getDay();

      // 上个月需要显示的天数
      const prevMonthDays = firstDayWeekday;
      // 获取上个月的最后一天
      const prevMonthLastDay = new Date(year, month - 1, 0).getDate();

      const calendarDays = [];

      // 添加上个月的日期
      for (let i = prevMonthDays - 1; i >= 0; i--) {
        const dayNumber = prevMonthLastDay - i;
        const prevMonth = month - 1 === 0 ? 12 : month - 1;
        const prevYear = month - 1 === 0 ? year - 1 : year;
        const dateKey = `${prevYear}-${prevMonth}-${dayNumber}`;

        calendarDays.push({
          date: new Date(prevYear, prevMonth - 1, dayNumber),
          dayNumber,
          currentMonth: false,
          dateKey
        });
      }

      // 添加当月的日期
      for (let i = 1; i <= daysInMonth; i++) {
        const dateKey = `${year}-${month}-${i}`;

        calendarDays.push({
          date: new Date(year, month - 1, i),
          dayNumber: i,
          currentMonth: true,
          dateKey
        });
      }

      // 计算需要添加的下个月的日期数量
      const remainingDays = 42 - calendarDays.length; // 6行7列 = 42

      // 添加下个月的日期
      for (let i = 1; i <= remainingDays; i++) {
        const nextMonth = month + 1 === 13 ? 1 : month + 1;
        const nextYear = month + 1 === 13 ? year + 1 : year;
        const dateKey = `${nextYear}-${nextMonth}-${i}`;

        calendarDays.push({
          date: new Date(nextYear, nextMonth - 1, i),
          dayNumber: i,
          currentMonth: false,
          dateKey
        });
      }

      return calendarDays;
    }
  },
  methods: {
    // 菜单管理相关方法
    handleClick(item) {
      if (item.id === 'online-hr') {
        this.historyStack.push(this.hrMenu);
        this.currentMenu = this.hrMenu;
      } else if (item.id === 'home') {
        this.historyStack = [this.mainMenu];
        this.currentMenu = this.mainMenu;
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
      }
    },
    async fetchUserInfo() {
      try {
        const value = await is_login_request();
        if (value.status === true) {
          this.user = value.data;
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    logout() {
      this.user = null;
      router.push('/login_register');
    },

    // 获取面试数据

    // - name:
    // - post:
    // - hr:
    // - interview_time:
    // - file_url:
    // - isAgreed:
    async fetchInterviewList() {
      try {
        const response = await axios.get('http://localhost:8000/api/get_interview_list/');
        if (response.data.status === true) {
          this.allInterviews = response.data.data;
          this.processInterviewData();
        } else {
          console.error('获取面试列表失败:', response.data.data);
        }
      } catch (error) {
        console.error('获取面试列表请求失败:', error);
      }
    },


    processInterviewData() {
      this.dateInterviewMap = {};

      this.allInterviews.forEach(interview => {
        // 提取面试时间中的年月日信息用于分组
        const interviewTime = new Date(interview.interview_time);
        const year = interviewTime.getFullYear();
        const month = interviewTime.getMonth() + 1;
        const day = interviewTime.getDate();

        // 创建日期键用于存储
        const dateKey = `${year}-${month}-${day}`;

        // 确保日期映射对象中有该日期的数组
        if (!this.dateInterviewMap[dateKey]) {
          this.dateInterviewMap[dateKey] = [];
        }

        // 将面试信息添加到对应日期
        this.dateInterviewMap[dateKey].push(interview);
      });
    },

    // 检查日期是否有面试
    hasInterviews(day) {
      const dateKey = day.dateKey;
      return this.dateInterviewMap[dateKey] && this.dateInterviewMap[dateKey].length > 0;
    },

    // 日历功能相关方法
    prevMonth() {
      if (this.currentMonth === 1) {
        this.currentYear--;
        this.currentMonth = 12;
      } else {
        this.currentMonth--;
      }
    },
    nextMonth() {
      if (this.currentMonth === 12) {
        this.currentYear++;
        this.currentMonth = 1;
      } else {
        this.currentMonth++;
      }
    },
    selectDate(day) {
      this.selectedDate = new Date(day.date);
      this.loadInterviewData(this.selectedDate);
    },
    backToCalendar() {
      this.selectedDate = null;
    },

    // 根据选择的日期加载面试数据
    // 此方法会将指定日期的面试信息按时间段组织到timeSlots中
    loadInterviewData(date) {
      // 重置所有时间段数据
      this.timeSlots = this.timeSlots.map(slot => {
        return {
          ...slot,
          interviews: []
        };
      });

      // 构建日期键以从映射中获取数据
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      const dateKey = `${year}-${month}-${day}`;

      // 获取选定日期的所有面试
      const dayInterviews = this.dateInterviewMap[dateKey] || [];

      dayInterviews.forEach(interview => {
        // 从interview对象中获取的字段:
        // - interview.name：
        // - interview.post：
        // - interview.hr：
        // - interview.interview_time：
        // - interview.file_url：
        // - interview.isAgreed：

        const interviewTime = new Date(interview.interview_time);
        const hours = interviewTime.getHours();
        const minutes = interviewTime.getMinutes();

        // 找到对应的时间段
        for (let i = 0; i < this.timeSlots.length; i++) {
          const slot = this.timeSlots[i];
          const [startTime, endTime] = slot.time.split('-');

          const [startHour, startMinute] = startTime.split(':').map(Number);
          const [endHour, endMinute] = endTime.split(':').map(Number);

          // 检查面试时间是否在当前时间段内
          if ((hours > startHour || (hours === startHour && minutes >= startMinute)) &&
              (hours < endHour || (hours === endHour && minutes < endMinute))) {
            // 将面试信息添加到对应时间段
            this.timeSlots[i].interviews.push(interview);
            break;
          }
        }
      });
    }
  },
  created() {
    console.log('InterviewQuery 组件已创建');
    // 初始化菜单状态
    this.currentMenu = this.interviewMenu;
    this.historyStack = [this.mainMenu, this.hrMenu, this.interviewMenu];
  },
  mounted() {
    console.log('InterviewQuery 组件已挂载');
    // 获取用户信息
    this.fetchUserInfo();
    // 获取面试列表数据
    this.fetchInterviewList();
  }
});
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
}

.interview-query {
  width: 100%;
  height: 100%;
}

.calendar-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h2 {
  font-size: 24px;
  font-weight: bold;
}

.nav-btn {
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 18px;
  cursor: pointer;
}

.nav-btn:hover {
  background: #e0e0e0;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.weekday {
  padding: 10px;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-gap: 5px;
}

.day {
  border: 1px solid #e0e0e0;
  height: 80px;
  padding: 5px;
  text-align: center;
  cursor: pointer;
  position: relative;
}

.day:hover {
  background-color: #f8f8f8;
}

.current-month {
  background-color: #fff;
}

.other-month {
  background-color: #f5f5f5;
  color: #aaa;
}

.day-number {
  font-size: 1.5em;
  font-weight: bold;
}

.today {
  background-color: #e6f7ff;
}

/* 有面试的日期样式 */
.has-interviews {
  position: relative;
}

.interview-indicator {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 8px;
  height: 8px;
  background-color: #1890ff;
  border-radius: 50%;
}

/* 面试时间表样式 */
.schedule-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
}

.schedule-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
  padding-bottom: 10px;
}

.schedule-header h2 {
  margin-left: 20px;
  font-size: 20px;
}

.back-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.back-btn:hover {
  background-color: #0056b3;
}

.schedule-table {
  width: 100%;
  border-collapse: collapse;
}

.schedule-table th,
.schedule-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  height: 40px;
}

.schedule-table th {
  background-color: #f2f2f2;
  position: sticky;
  top: 0;
  z-index: 5;
}

/* 时间段样式 */
.time-slot {
  font-weight: bold;
  color: #1890ff;
}

/* 最后一行添加底部边距 */
.last-row {
  border-bottom: 2px solid #ddd;
}

/* 第一列的宽度 */
.schedule-table th:first-child,
.schedule-table td:first-child {
  width: 25%;
}

/* 第二列的宽度 */
.schedule-table th:last-child,
.schedule-table td:last-child {
  width: 75%;
}

/* 滚动条样式 */
.schedule-container {
  overflow-y: auto;
  max-height: calc(100vh - 120px);
}

/* 日期选择器行高 */
.calendar-header {
  margin-bottom: 15px;
}

/* 时间段表格布局 */
.schedule-table {
  margin-top: 15px;
}

/* 表格边框 */
.schedule-table,
.schedule-table th,
.schedule-table td {
  border: 1px solid #ddd;
}

/* 内容间距 */
.schedule-container {
  padding: 15px;
}
</style>