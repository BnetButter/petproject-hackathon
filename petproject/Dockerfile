# Use the official Node.js LTS image from the Docker Hub
FROM node:lts

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the rest of your application code to the container
COPY package.json yarn.lock ./

RUN npm install react-scripts -g
RUN yarn install


