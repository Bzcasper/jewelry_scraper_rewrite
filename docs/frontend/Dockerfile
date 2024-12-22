# Frontend Dockerfile

# Base image for Node.js
FROM node:16 as build

# Set working directory
WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Build the frontend application
COPY frontend/ .
RUN npm run build

# Use a lightweight web server to serve the built application
FROM nginx:1.21-alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose the application port
EXPOSE 80

# Start the server
CMD ["nginx", "-g", "daemon off;"]
