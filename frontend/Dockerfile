# ==== CONFIGURE =====
# Use a Node 16 base image
FROM node:18.16-alpine as build-image
# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files
COPY . .
# Install dependencies
RUN npm install
# Build the app
RUN npm run build
# ==== RUN =======
FROM nginx:alpine
# Copy nginx config
COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf
# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*
# Copy the build output to replace the default nginx contents.
COPY --from=build-image /app/build /usr/share/nginx/html
# Expose port 80
EXPOSE 80
# Run nginx
CMD [ "nginx", "-g", "daemon off;"]