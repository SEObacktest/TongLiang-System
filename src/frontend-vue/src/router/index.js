import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue')
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('@/views/Admin.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue')
    },
    {
        path: '/login_register',
        name: 'login_register',
        component: () => import('@/views/Login_Register.vue')
    },
    {
        path: '/admin_login',
        name: 'admin_login',
        component: () => import('@/views/Admin_Login.vue')
    },
    {
        path: '/show-model',
        name: 'ShowModel',
        component: () => import('@/views/ShowModel.vue')
    },
    {
        path: '/admin/online_hr',
        name: 'AdminOnlineHR',
        component: () => import('@/views/admin/OnlineHR.vue')
    },
    {
        path: '/admin/interview',
        name: 'AdminInterview',
        component: () => import('@/views/admin/Interview.vue')
    },
    {
        path: '/admin/question',
        name: 'AdminQuestion',
        component: () => import('@/views/admin/Question.vue')
    },
    {
        path: '/admin/salary',
        name: 'AdminSalary',
        component: () => import('@/views/admin/Salary.vue')
    },
    {
        path: '/admin/test_module',
        name: 'AdminTestModule',
        component: () => import('@/views/admin/TestModule.vue')
    },
    {
        path: '/admin/settlement',
        name: 'AdminSettlement',
        component: () => import('@/views/admin/Settlement.vue')
    },
    { 
        path: "/salary-form", 
        name: 'SalaryForm',
        component: () => import('@/views/SalaryForm.vue')
    },
    { 
        path: "/salary-detail", 
        name: 'SalaryDetail' ,
        component: () => import('@/views/SalaryDetail.vue')
    },
    {   
        path: '/edit-salary-info', 
        name: 'EditSalaryInfo', 
        component: () => import('@/views/EditSalaryInfo.vue')
    },
    { 
        path: '/salary-transactions', 
        name: 'SalaryTransactions', 
        component: () => import('@/views/SalaryTransactions.vue')
    },
    {
        path: '/test-module',
        name: 'TestModule',
        component: () => import('@/views/JHSrc/TestModule.vue')
    },
    {
        path: '/interview-upload',
        name: 'InterviewUpload',
        component: () => import('@/views/JHSrc/InterviewUpload.vue')
    },
    {
        path: '/interview-query',
        name: 'InterviewQuery',
        component: () => import('@/views/JHSrc/InterviewQuery.vue')
    },
    {
        path: '/interview-edit',
        name: 'InterviewEdit',
        component: () => import('@/views/JHSrc/Interview_edit.vue')
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router