db = db.getSiblingDB("suppliersDB")

// Drop collection if it already exists (useful for re-runs)
db.suppliers.drop()

// Create collection with JSON Schema validation
db.createCollection("suppliers", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["supplierID", "materials"],
            properties: {
                supplierID: {
                    bsonType: "string",
                    description: "supplierID must be a string and is required"
                },

                materials: {
                    bsonType: "array",
                    description: "materials must be an array of material objects",
                    items: {
                        bsonType: "object",
                        required: ["materialID", "C3", "C5"],
                        properties: {
                            materialID: {
                                bsonType: "string",
                                description: "materialID must be a string"
                            },
                            C3: {
                                bsonType: ["int", "double"],
                                description: "C3 must be an integer"
                            },
                            C5: {
                                bsonType: ["int", "double"],
                                description: "C5 must be an integer"
                            }
                        }
                    }
                }
            }
        }
    }
})


// -------------------------
// Insert sample data
// -------------------------
const fs = require('fs')
const raw = fs.readFileSync("/docker-entrypoint-initdb.d/suppliers.json", "utf8")
const suppliers = JSON.parse(raw)
db.suppliers.insertMany(suppliers)
    // db.suppliers.insertMany([{
    //         supplierID: "sup1",
    //         materials: [{
    //                 materialID: "con_1",
    //                 C3: 12,
    //                 C7: 7
    //             },
    //             {
    //                 materialID: "con_2",
    //                 C3: 5,
    //                 C7: 9
    //             }
    //         ]
    //     },
    //     {
    //         supplierID: "sup2",
    //         materials: [{
    //             materialID: "con_1",
    //             C3: 20,
    //             C7: 11
    //         }]
    //     },
    //     {
    //         supplierID: "sup3",
    //         materials: [{
    //             materialID: "con_1",
    //             C3: 20,
    //             C7: 11
    //         }, {
    //             materialID: "fill_1",
    //             C3: 20,
    //             C7: 11
    //         }]
    //     },
    //     {
    //         supplierID: "sup4",
    //         materials: [{
    //             materialID: "fill_1",
    //             C3: 30,
    //             C7: 1
    //         }]
    //     }
    // ])