<template>
  <div class="input-field">
    <label :for="name">{{ label }}</label>
    <input 
      :id="name" 
      :value="modelValue" 
      @input="$emit('update:modelValue', $event.target.value)" 
      :type="type" 
      :placeholder="placeholder"
    />
  </div>
</template>

<script>
export default {
  props: {
    label: String,
    name: String,
    modelValue: String, // v-model 默认的 prop
    type: { type: String, default: "text" },
    placeholder: String
  },
  emits: ["update:modelValue"] // 必须声明 emits，否则 Vue 3 会报错
};
</script>

  
  <style scoped>
  .input-field {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
  input {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
  }
  </style>
  