db = db.getSiblingDB("ordersDB")

// Drop collection if rerun (safe for dev)
db.orders.drop()

// Create collection with schema validation
db.createCollection("orders", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["orderID", "pID", "nominal", "actual", "supplier"],
            properties: {
                orderID: {
                    bsonType: "string",
                    description: "must be a string and is required"
                },

                pID: {
                    bsonType: "string",
                    description: "product ID must be a string and is required"
                },

                nominal: {
                    bsonType: ["int", "double"],
                    description: "nominal must be a number"
                },

                actual: {
                    bsonType: ["int", "double"],
                    description: "actual must be a number"
                },

                supplier: {
                    bsonType: "string",
                    description: "supplier must be a string"
                }
            }
        }
    }
})


// -----------------------------
// Insert sample Excel-like data
// -----------------------------

const fs = require('fs')
const raw = fs.readFileSync("/docker-entrypoint-initdb.d/orders.json", "utf8")
const orders = JSON.parse(raw)
db.orders.insertMany(orders)