<template>
  <el-button type="primary" @click="refreshClasses">刷新列表</el-button>
  <el-divider></el-divider>
  <el-card>
    <el-menu
        class="el-menu-vertical-demo"
        :active-index="props.selected"
        :unique-opened="true"
    >
    <el-menu-item
        v-for="cls in classes"
        :key="cls.class"
        :index="cls.class"
        @click="$emit('select', cls.class)"
    >
      {{ cls.class }}
    </el-menu-item>
    </el-menu>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from 'vue'
import { getClasses } from '../api/weaviate.ts'

const props = defineProps<{ selected: string }>()

const classes = ref<any[]>([])

const fetchClasses = async () => {
  try {
    const res = await getClasses()
    classes.value = res.data.classes || []
  } catch (error) {
    console.error('Failed to fetch classes:', error)
  }
}

onMounted(fetchClasses)

const refreshClasses = () => {
  fetchClasses()
}
</script>

<style scoped>
.el-menu-vertical-demo {
  width: 200px;
  min-height: 400px;
}
</style>
