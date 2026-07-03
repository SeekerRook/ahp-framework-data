// Switch DB
db = db.getSiblingDB("materialsDB");

// Always reset for deterministic startup (safe in dev containers)
db.dropDatabase();

// Create collection with JSON schema validation
db.createCollection("materials", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["materialID", "type", "C1", "C2", "C6", "C7"],
            properties: {
                materialID: {
                    bsonType: "string",
                    description: "must be string"
                },
                type: {
                    bsonType: "string",
                    description: "must be string"
                },
                C1: {
                    bsonType: ["int", "double"],
                    description: "must be numeric"
                },
                C2: {
                    bsonType: ["int", "double"],
                    description: "must be numeric"
                },
                C6: {
                    bsonType: "int",
                    description: "must be integer"
                },
                C7: {
                    bsonType: "int",
                    description: "must be integer"
                }
            }
        }
    }
});

// Insert initial dataset
const fs = require('fs')
const raw = fs.readFileSync("/docker-entrypoint-initdb.d/materials.json", "utf8")
const materials = JSON.parse(raw)
db.materials.insertMany(materials)
    // db.materials.insertMany([{
    //         materialID: "con_1",
    //         type: "concrete",
    //         C1: 12,
    //         C2: 3,
    //         C5: 3,
    //         C6: 3
    //     },
    //     {
    //         materialID: "con_2",
    //         type: "concrete",
    //         C1: 20,
    //         C2: 7,
    //         C5: 5,
    //         C6: 9
    //     }, {
    //         materialID: "fill_1",
    //         type: "fillament",
    //         C1: 12,
    //         C2: 3,
    //         C5: 3,
    //         C6: 3
    //     }
    // ]);