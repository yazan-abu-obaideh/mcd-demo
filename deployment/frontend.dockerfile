FROM node:20.8.0-alpine3.18 as builder

WORKDIR /build

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install

COPY frontend/ .

RUN npm run build


FROM nginx

COPY --from=builder /build/dist/mcd/ /usr/share/nginx/html/
