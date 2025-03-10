<template>
  <nav class="sidebar">
    <ul>
      <li v-for="item in menu" :key="item.text">
        <a
          :href="item.href"
          :class="{ active: item.active }"
          @click.prevent="$emit('menu-click', item)"
        >{{ item.text }}</a>
      </li>
    </ul>
    <button v-show="showBackBtn" class="back-btn" @click="$emit('go-back')">返回</button>
  </nav>
</template>

<script>
export default {
  name: 'AppSidebar',
  props: {
    menu: Array,
    showBackBtn: Boolean,
  },
};
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #e9ecef;
  padding: 20px 0;
  border-right: 1px solid #ddd;
  min-height: 100%;
}
.sidebar ul {
  list-style: none;
}
.sidebar ul li {
  margin-bottom: 10px;
}
.sidebar ul li a {
  display: block;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
  font-size: 16px;
}
.sidebar ul li a:hover {
  background-color: #007bff;
  color: white;
}
.sidebar ul li a.active {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}
.back-btn {
  position: fixed;
  bottom: 20px;
  left: 20px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  z-index: 1000;
}
.back-btn:hover {
  background-color: #0056b3;
}
</style>
