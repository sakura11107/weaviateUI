<template>
  <el-card>
    <div style="margin-bottom: 1rem">
      <el-button type="primary" @click="loadObjects">刷新数据</el-button>
      <el-button type="success" @click="viewSchema">查看结构</el-button>
      <el-button type="danger" @click="handleDeleteClass">删除该类</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="objects" stripe>
      <el-table-column prop="id" label="UUID" width="250" />
      <el-table-column
          v-for="key in fieldKeys"
          :key="key"
          :label="key"
      >
        <template #default="{ row }">
          <div
              class="ellipsis-cell"
              @click="openDetail(row.properties[key], key)"
          >
            {{ truncateText(formatValuePlain(row.properties[key])) }}
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-divider></el-divider>
    <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="totalCount"
        :background="true"
        layout="total, sizes, prev, pager, next, jumper"
        :page-sizes="[5, 10, 20, 50]"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
    />
    <!-- 字段详情弹窗 -->
    <el-dialog v-model="showDialog" :title="dialogTitle" width="60%">
      <pre style="white-space: pre-wrap;">{{ dialogContent }}</pre>
    </el-dialog>

    <!-- 类结构弹窗 -->
    <el-dialog v-model="schemaDialogVisible" :title="`类结构：${props.className}`" width="60%">
      <VueJsonPretty :data="classSchemaData" :deep="2" :showLine="true" />
    </el-dialog>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getObjectsByClass, deleteObject, deleteClass, getClassSchema } from '../api/weaviate.ts'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

const classSchemaData = ref({})

const props = defineProps<{ className: string }>()
const objects = ref<any[]>([])
const fieldKeys = ref<string[]>([])
const showDialog = ref(false)
const dialogTitle = ref('')
const dialogContent = ref('')
const schemaDialogVisible = ref(false)

const pageSize = ref(10)
const currentPage = ref(1)
const totalCount = ref(0)

const loadObjects = async () => {
  const offset = (currentPage.value - 1) * pageSize.value
  const res = await getObjectsByClass(props.className, pageSize.value, offset)
  objects.value = res.data.objects || []
  totalCount.value = res.data.total || 0
  fieldKeys.value = objects.value.length
      ? Object.keys(objects.value[0].properties || {})
      : []
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadObjects()
}

// 提取对象 ID
const extractId = (beacon: string) => beacon?.split('/').pop() || ''

// 判断是否是 ISO 时间
const isISOString = (val: string) => {
  return /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(val)
}

// 格式化字段值（纯文本，用于弹窗）
const formatValuePlain = (val: any): string => {
  if (Array.isArray(val)) {
    return val.map((item) => {
      if (typeof item === 'object' && item?.beacon) {
        return extractId(item.beacon)
      }
      return formatValuePlain(item)
    }).join('\n')
  } else if (typeof val === 'object' && val !== null) {
    return JSON.stringify(val, null, 2)
  } else if (typeof val === 'string' && isISOString(val)) {
    return new Date(val).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })
  } else {
    return String(val)
  }
}

// 截断展示内容
const truncateText = (text: string, length = 60): string => {
  return text.length > length ? text.slice(0, length) + '...' : text
}

// 点击字段，打开弹窗查看详情
const openDetail = (val: any, key: string) => {
  dialogTitle.value = `字段：${key}`
  dialogContent.value = formatValuePlain(val)
  showDialog.value = true
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadObjects()
}

// 删除单个对象
const handleDelete = async (uuid: string) => {
  await deleteObject(uuid)
  await loadObjects()
}

// 删除整个类
const handleDeleteClass = async () => {
  try {
    await ElMessageBox.confirm(
        `确定要删除类 "${props.className}" 吗？此操作不可恢复！`,
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
    )
    await deleteClass(props.className)
    ElMessage.success('删除成功')
    objects.value = []
    fieldKeys.value = []
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 查看类结构
const viewSchema = async () => {
  const res = await getClassSchema(props.className)
  classSchemaData.value = res.data
  schemaDialogVisible.value = true
}

watch(() => props.className, loadObjects, { immediate: true })
</script>

<style scoped>
.ellipsis-cell {
  max-height: 4em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  color: #409EFF;
}
</style>
