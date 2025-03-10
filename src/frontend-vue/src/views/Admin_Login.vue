<script setup>

import { ref } from 'vue';

import { admin_login_request, is_login_request, admin_register_request} from '@/api/api.js'

import router from '@/router';

const isActive = ref(false)

const loginAdminId  = ref('')
const loginPassword = ref('')
const loginMessage  = ref("")

const registerAdminId       = ref('')
const registerUsername = ref('')
const registerPassword = ref('')
const registerPhone    = ref('')
const registerMessage  = ref("")

const isLoginAdminIdError    = ref(false)
const isLoginPasswordError    = ref(false)
const isRegisterAdminIdError = ref(false)
const isRegisterUsernameError = ref(false)
const isRegisterPasswordError = ref(false)
const isRegisterPhoneError    = ref(false)

const styleVar = ref({
	/* COLORS */
	/* 强制规定颜色代码 */
	"--white": "#e9e9e9",
	"--gray": "#333",
	"--blue": "#0367a6",
	"--lightblue": "#008997",
    // "--orange": "#ff8500",

	/* RADII */
	"--button-radius": "0.7rem",

	/* SIZES */
	"--max-width": "758px",
	"--max-height": "420px",
})

function goHome() {
	router.push('/')
	router.push('/')
}

async function login() {

	if (loginAdminId.value == '') {
		loginMessage.value = "请填写账号"
		isLoginAdminIdError.value = true
		return
	}
	isLoginAdminIdError.value = false
	if (loginPassword.value == '') {
		loginMessage.value = '请填写密码'
		isLoginPasswordError.value = true
		return
	}
	isLoginPasswordError.value = false

	var data = {
		'adminId': loginAdminId.value,
		'password': loginPassword.value,
	}

	var value = await admin_login_request(data)

	if (value['status'] == true) {
		router.push('/')
	}
	
	loginMessage.value = value['message']
	
	}

async function register() {  

	if (registerAdminId.value == '') {
		registerMessage.value = '请填写账号'
		isRegisterAdminIdError.value = true
		return
	}
	isRegisterAdminIdError.value = false
	if (registerUsername.value == '') {
		registerMessage.value = '请填写姓名'
		isRegisterUsernameError.value = true
		return
	}
	isRegisterUsernameError.value = false
	if (registerPassword.value == '') {
		registerMessage.value = '请填写密码'
		isRegisterPasswordError.value = true
		return
	}
	isRegisterPasswordError.value = false
	if (registerPhone.value == '') {
		registerMessage.value = '请填写电话'
		isRegisterPhoneError.value = true
		return
	}
	isRegisterPhoneError.value = false
	var data = {
		adminId: registerAdminId.value,
		username: registerUsername.value,
		password: registerPassword.value,
		phone: registerPhone.value
	}

	var value = await admin_register_request(data)

	if (value['status'] == true) {
		router.push('/')
	}

	registerMessage.value = value['message']


}

async function profile() {
	const value = await is_login_request();

	if (value['status'] == true) {
		loginMessage.value = '您已经登录了'
	} 
	// 没登录的话跳转到登录页面
	else {
	// router.push('/login');
	}
}
profile()

</script>   


<template>
<div id="main" :style=styleVar>

	<div class="logo">
		<div class="title">学生党员评价量化考核系统</div>
		<img @click="goHome" src="@img/国际数字经济学院Logo_with_name.png" alt="logo">
	</div>

	<div class="container" :class="{ rightPanelActive: isActive}">

		<div class="container__form container--signup">
			<div class="form" id="form1">
				<h2 class="form__title">管理员注册</h2>
				<input v-model = "registerAdminId " type = "text" placeholder     = "账号" class = "input" :class = "{'input_error': isRegisterIdError}" name       = "注册账号"/>
				<input v-model = "registerUsername" type = "text" placeholder     = "姓名" class = "input" :class = "{'input_error': isRegisterUsernameError}" name = "注册姓名"/>
				<input v-model = "registerPassword" type = "password" placeholder = "密码" class = "input" :class = "{'input_error': isRegisterPasswordError}" name = "注册密码"/>
				<input v-model = "registerPhone" type    = "Phone" placeholder    = "电话" class = "input" :class = "{'input_error': isRegisterPhoneError}" name    = "注册邮箱"/>
				<div class="message">
					{{registerMessage}}
				</div>
				<button @click="register" class="btn">注册</button>
			</div>
		</div>
		
		<div class="container__form container--signin">
			<div class="form" id="form2">
				<h2 class="form__title">管理员登录</h2>
				<input v-model = "loginAdminId" type  = "text" placeholder     = "账号" class = "input" :class = "{'input_error': isLoginAdminIdError}" name  = "登录账号"/>
				<input v-model = "loginPassword" type = "password" placeholder = "密码" class = "input" :class = "{'input_error': isLoginPasswordError}" name = "登录密码"/>
				<div class="message">
					{{loginMessage}}
				</div>
				<a @click="forget" href="#" class="link">忘记密码?</a>
				<button @click="login" class="btn">登录</button>
			</div>
		</div>
		
		<div class="container__overlay">
			<div class="overlay">
				<div class="overlay__panel overlay--left">
					<button @click="isActive=false" class="btn" id="signIn">登录</button>
				</div>
				<div class="overlay__panel overlay--right">
					<button @click="isActive=true" class="btn" id="signUp">注册</button>
				</div>
			</div>
		</div>
	</div>
</div>

</template>

<style scoped>
#main {
	display: flex;
	justify-content: center;
	margin: 0 auto;

	flex-direction: column;
	align-items: center;
	background-color: var(--white);
	background: url("@img/闽江学院门口.png");
	/* background-attachment: fixed; */
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	font-size: 16px;
    margin-top: 100px;
	min-width: 1200px;
	max-width: 1600px;
	min-height: 1000px;
	place-items: center;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
		Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
}

.logo {
	height: 120px;
	margin-top: -140px;
	margin-bottom: 40px;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
}
.logo .title{
	font-size: 70px;
	font-weight: 800;
	margin-top: 10px;
	margin-bottom: 10px;
	font-family: "清风行楷体";
	color: #303030;
}

.logo img {
	height: 100%;
	margin-bottom: 50px;
	object-fit: contain;
	cursor: pointer;
}

.form__title {
	font-weight: 300;
	margin: 0;
	margin-bottom: 1.25rem;
	color: var(--gray);
}

.link {
	color: var(--gray);
	font-size: 0.9rem;
	margin: 1.5rem 0;
	text-decoration: none;
}

.container {
	background-color: var(--white);
	border-radius: var(--button-radius);
	box-shadow: 0 0.9rem 1.7rem rgba(0, 0, 0, 0.25),
		0 0.7rem 0.7rem rgba(0, 0, 0, 0.22);
	height: var(--max-height);
	max-width: var(--max-width);
	overflow: hidden;
	position: relative;
	width: 100%;
}

.container__form {
	height: 100%;
	position: absolute;
	top: 0;
	transition: all 0.6s ease-in-out;
}

.container--signin {
	left: 0;
	width: 50%;
	z-index: 2;
}

.container--signin .link:hover {
    color: var(--blue);
}

.container.rightPanelActive .container--signin {
	transform: translateX(100%);
}

.container--signup {
	left: 0;
	opacity: 0;
	width: 50%;
	z-index: 1;
}

.container.rightPanelActive .container--signup {
	-webkit-animation: show 0.6s;
	        animation: show 0.6s;
	opacity: 1;
	transform: translateX(100%);
	z-index: 5;
}

.container__overlay {
	height: 100%;
	left: 50%;
	overflow: hidden;
	position: absolute;
	top: 0;
	transition: transform 0.6s ease-in-out;
	width: 50%;
	z-index: 100;
}

.container.rightPanelActive .container__overlay {
	transform: translateX(-100%);
}

.overlay {
	/* background-color: var(--lightblue); */
	background: url("@img/background_Login_blue.jpg");
	opacity: 0.95;
	background-attachment: fixed;
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	height: 100%;
	left: -100%;
	position: relative;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
	width: 200%;
}

.container.rightPanelActive .overlay {
	transform: translateX(50%);
}

.overlay__panel {
	align-items: center;
	display: flex;
	flex-direction: column;
	height: 100%;
	justify-content: center;
	position: absolute;
	text-align: center;
	top: 0;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
	width: 50%;
}

.overlay--left {
	transform: translateX(-20%);
}

.container.rightPanelActive .overlay--left {
	transform: translateX(0);
}

.overlay--right {
	right: 0;
	transform: translateX(0);
}

.container.rightPanelActive .overlay--right {
	transform: translateX(20%);
}

.btn {
	/* background-color: var(--blue); */
    background-color: var(--blue);
	background-image: linear-gradient(90deg, var(--blue) 0%, var(--blue) 74%);
	border-radius: 20px;
	border: 1px solid var(--blue);
	color: var(--white);
	cursor: pointer;
	font-size: 0.8rem;
	font-weight: bold;
	letter-spacing: 0.1rem;
	padding: 0.9rem 4rem;
	text-transform: uppercase;
	transition: transform 80ms ease-in;
}

.form > .btn {
	margin-top: 1.5rem;
}

.btn:active {
	transform: scale(0.95);
}

.btn:focus {
	outline: none;
}

.form {
	background-color: var(--white);
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 3rem;
	height: 100%;
	text-align: center;
}

.message {
	color: var(--gray);
	height: 20px;
    font-style: italic;
}

.input {
	background-color: #fff;
	border: none;
	padding: 0.9rem 0.9rem;
	margin: 0.5rem 0;
	width: 100%;
	border-radius: 20px;
	font-size: 14px;
	outline: none;
}

.input_error {
	border: 1px solid red;
}

@-webkit-keyframes show {
	0%,
	49.99% {
		opacity: 0;
		z-index: 1;
	}

	50%,
	100% {
		opacity: 1;
		z-index: 5;
	}
}

@keyframes show {
	0%,
	49.99% {
		opacity: 0;
		z-index: 1;
	}

	50%,
	100% {
		opacity: 1;
		z-index: 5;
	}
}
</style>