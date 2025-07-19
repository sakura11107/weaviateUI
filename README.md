# Weaviate UI
一键 Docker 镜像（前端 Vite+Vue3，后端 Flask）。

## 使用
1. 克隆仓库  
git clone <你的仓库地址>
cd weaviateui
2. 在 `end/` 目录新建 `.env` 文件，写：
WEAVIATE_URL=https://your-weaviate-instance
3. 运行：
docker load -i weaviateui.tar
docker run -p 5000:5000 --env-file end/.env weaviateui
4. 浏览器访问 http://localhost:5000