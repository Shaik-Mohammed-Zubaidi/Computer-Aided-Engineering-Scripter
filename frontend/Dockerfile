############################
# 1. Build React assets
############################
FROM node:18-alpine AS builder
WORKDIR /web
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build            # outputs to /web/build

############################
# 2. Serve with Nginx
############################
FROM nginx:alpine
# Remove default nginx conf
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/app.conf
COPY --from=builder /web/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
