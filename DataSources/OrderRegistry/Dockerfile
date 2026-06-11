FROM mongo:7

# Copy initialization script into Mongo entrypoint folder
COPY init.js /docker-entrypoint-initdb.d/init.js
COPY orders.json /docker-entrypoint-initdb.d/orders.json