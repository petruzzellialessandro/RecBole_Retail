# syntax=docker/dockerfile:1
FROM node:18-alpine

RUN apk add --update npm
WORKDIR /app
COPY package*.json  ./
RUN npm install
RUN npm ci

COPY . .

EXPOSE 3000
ENV PORT 3000

CMD ["npm", "start"]