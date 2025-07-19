import axios from 'axios'

const axiosInstance = axios.create({
    baseURL: '/api',  // 前端开发时可配 Vite 代理
})
// 获取所有类
export const getClasses = () => axiosInstance.get('/classes')

// 获取类结构信息
export const getClassSchema = (className: string) =>
    axiosInstance.get(`/classes/${className}/schema`)

// 获取某类的对象列表（带分页）
export const getObjectsByClass = (className: string, limit = 20, offset = 0) =>
    axiosInstance.get(`/objects/${className}`, { params: { limit, offset } })

// 删除对象
export const deleteObject = (uuid: string) => axiosInstance.delete(`/objects/${uuid}`)

// 创建对象
export const createObject = (data: any) => axiosInstance.post(`/objects`, data)

// 删除整个类
export const deleteClass = (className: string) => axiosInstance.delete(`/api/classes/${className}`)


