import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/JhSrc/index.vue')
    },
    {
        path: '/test-module',
        name: 'TestModule',
        component: () => import('@/views/JhSrc/TestModule.vue'),
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
        path: '/admin',
        name: 'Admin',
        component: () => import('@/views/Admin.vue')
    },
    {
        path: '/show-model',
        name: 'ShowModel',
        component: () => import('@/views/ShowModel.vue')
    },
 // 你的子系统路由
    {
    path: '/jhTest',
    name: 'jhTest',
    component: () => import('@/views/JhSrc/index.vue'),
    },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;