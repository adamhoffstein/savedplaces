# base image
FROM node:alpine

# use changes to package.json to force Docker not to use the cache
# when we change our application's nodejs dependencies:
COPY ./frontend/package.json /tmp/package.json
RUN cd /tmp && npm install
RUN mkdir -p /opt/app && cp -a /tmp/node_modules /opt/app/

WORKDIR /usr/app
ENV NODE_OPTIONS=--openssl-legacy-provider

COPY ./frontend ./

EXPOSE 8081
CMD [ "npm", "run", "serve"]