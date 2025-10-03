FROM node:lts-alpine as builder

WORKDIR /frontend
COPY . ./
RUN npm install && npm run build

FROM nginx:alpine as production
COPY --from=builder /frontend/dist /usr/share/nginx/html
COPY --from=builder /frontend/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

