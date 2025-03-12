<template>
  <button class="submit-button" @click.native="handleClick">{{ label }}</button>
</template>

  
  <script>
  export default {
    props: {
      label: { type: String, default: "确认" }
    },
    methods: {
      handleClick() {
        this.$emit("click");
      }
    }
  };
  </script>
  
  <style scoped>
  .submit-button {
    padding: 10px 15px;
    background-color: #87CEEB;
    border: none;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 5px;
  }
  </style>
  