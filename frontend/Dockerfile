# ==== CONFIGURE =====
# Use a Node 16 base image
FROM node:18.16-alpine as build-image
# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files
COPY . .
# Build the app
RUN npm run build
# ==== RUN =======
# Expose the port on which the app will be running (3000 is the default that `serve` uses)

# Start the app

FROM nginx:alpine

COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build-image /app/build /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;"]