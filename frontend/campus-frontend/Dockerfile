# ---- Сборка Vite
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci || npm i
COPY . .
RUN npm run build

# ---- Nginx
FROM nginx:alpine
# Статика собранного фронта
COPY --from=build /app/dist /usr/share/nginx/html
# Конфиг nginx (проксируем /api -> backend)
COPY nginx.conf /etc/nginx/conf.d/default.conf
