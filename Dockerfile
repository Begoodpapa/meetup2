FROM node:8.9
RUN npm config set proxy http://10.144.1.10:8080 \
      && npm config set https-proxy http://10.144.1.10:8080 \
      && npm install -g sails@0.12.14 \
      && npm install -g bower \
      && npm install -g forever \
      && npm cache clear --force
VOLUME /var/garden
EXPOSE 1337 1338 8081
