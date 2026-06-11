from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from collections import defaultdict
import os

app = FastAPI(title="Materials API")

MATERIALS_DB_URL = os.environ["MATERIALS_DB_URL"]
SUPPLIERS_DB_URL = os.environ["SUPPLIERS_DB_URL"]
ORDERS_DB_URL    = os.environ["ORDERS_DB_URL"]


def get_clients():
    return (
        MongoClient(MATERIALS_DB_URL),
        MongoClient(SUPPLIERS_DB_URL),
        MongoClient(ORDERS_DB_URL),
    )


def fetch_data() -> dict:
    materials_client, suppliers_client, orders_client = get_clients()

    try:
        materials_col = materials_client["materialsDB"]["materials"]
        suppliers_col = suppliers_client["suppliersDB"]["suppliers"]
        orders_col    = orders_client["ordersDB"]["orders"]

        # Load materials metadata grouped by type
        materials: dict[str, list] = {}
        for m in materials_col.find():
            mtype = m.get("type")
            if mtype not in materials:
                materials[mtype] = []
            materials[mtype].append({
                "materialID": m.get("materialID"),
                "C1": m.get("C1"),
                "C2": m.get("C2"),
                "C5": m.get("C5"),
                "C6": m.get("C6"),
            })

        # Load supplier info keyed by materialID
        suppliers: dict[str, list] = {}
        for s in suppliers_col.find():
            for m in s.get("materials", []):
                mid = m.get("materialID")
                if mid not in suppliers:
                    suppliers[mid] = []
                suppliers[mid].append({
                    "supplierID": s.get("supplierID"),
                    "C3": m.get("C3"),
                    "C7": m.get("C7"),
                })

        # Aggregate order diffs per (materialID, supplierID)
        stats: dict = defaultdict(list)
        for o in orders_col.find():
            key = (o["pID"], o["supplier"])
            stats[key].append(o["actual"] - o["nominal"])

        # Build alternatives report
        alternatives: dict[str, list] = {}
        for mtype, mats in materials.items():
            alternatives[mtype] = []
            for m in mats:
                material = m["materialID"]
                for s in suppliers.get(material, []):
                    supplier = s["supplierID"]
                    diffs = stats[(material, supplier)]
                    C4 = sum(diffs) / len(diffs) if diffs else None
                    alternatives[mtype].append({
                        "materialID": material,
                        "supplierID": supplier,
                        "C1": m["C1"],
                        "C2": m["C2"],
                        "C3": s["C3"],
                        "C4": C4,
                        "C5": m["C5"],
                        "C6": m["C6"],
                        "C7": s["C7"],
                    })

        return alternatives

    finally:
        materials_client.close()
        suppliers_client.close()
        orders_client.close()


@app.get("/alternatives", summary="Get all material alternatives with supplier scores")
def get_alternatives():
    try:
        return fetch_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alternatives/{material_type}", summary="Get alternatives for a specific material type")
def get_alternatives_by_type(material_type: str):
    try:
        data = fetch_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if material_type not in data:
        raise HTTPException(status_code=404, detail=f"Material type '{material_type}' not found")
    return {material_type: data[material_type]}


@app.get("/health")
def health():
    return {"status": "ok"}