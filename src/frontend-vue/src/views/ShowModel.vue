<script setup>

import { ref } from 'vue'

// import { ModelStl } from 'vue-3d-model';

const params  = new URLSearchParams(location.search);
const model   = ref(params.get('model'));

</script>

<template>
<div></div>

<div id='main'>
    <div class="title">3D模型查看器</div>
    <div class="model">
        <model-stl :src="model"></model-stl>
    </div>
    
</div>

</template>

<style scoped>

</style>