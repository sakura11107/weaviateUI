<template>
  <el-card>
    <el-container style="height: 100vh">
      <el-aside width="180px">
        <ClassList :selected="currentClass" @select="currentClass = $event" />
      </el-aside>
      <el-main style="overflow: auto;">
        <ObjectTable v-if="currentClass" :className="currentClass" />
      </el-main>
    </el-container>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ClassList from './views/ClassList.vue'
import ObjectTable from './views/ObjectTable.vue'
const currentClass = ref('')
</script>

<style>
html body{
  overflow: hidden;
}
</style>