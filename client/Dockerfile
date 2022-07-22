FROM node:16-alpine

WORKDIR /client

COPY ./ ./

RUN chmod -R 777 /client

RUN npm cache clean --force

RUN npm install --legacy-peer-deps

RUN npm install -g expo-cli@5.4.4 --unsafe-perm --allow-root

CMD [ "npm", "start" ]