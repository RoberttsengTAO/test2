# 使用 Node 基礎映像
FROM node:18

# 設置工作目錄
WORKDIR /app

# 複製項目文件
COPY package*.json ./
COPY . .

# 安裝依賴並構建
RUN npm install
RUN npm run build

# 使用靜態服務器提供構建的文件
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
