FROM mongo:7

# Copy initialization script into Mongo entrypoint folder
COPY init.js /docker-entrypoint-initdb.d/init.js
COPY suppliers.json /docker-entrypoint-initdb.d/suppliers.json