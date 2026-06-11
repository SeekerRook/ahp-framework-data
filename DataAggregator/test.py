from pymongo import MongoClient
from collections import defaultdict
import os

MATERIALS_DB_URL="mongodb://admin:toor@localhost:27018/"#os.environ['MATERIALS_DB_URL']
SUPPLIERS_DB_URL="mongodb://admin:toor@localhost:27019/"#os.environ['SUPPLIERS_DB_URL']
ORDERS_DB_URL="mongodb://admin:toor@localhost:27016/"#os.environ['ORDERS_DB_URL']
def FetchData():
    materials_client  = MongoClient(MATERIALS_DB_URL)
    suppliers_client = MongoClient(SUPPLIERS_DB_URL)
    orders_client     = MongoClient(ORDERS_DB_URL)
    materials_db  = materials_client["materialsDB"]
    suppliers_db = suppliers_client["suppliersDB"]
    orders_db     = orders_client["ordersDB"]
    materials_col = materials_db["materials"]
    suppliers_col = suppliers_db["suppliers"]
    orders_col    = orders_db["orders"]

    # ----------------------------
    # 2. Load materials metadata
    # ----------------------------

    materials = {}
    print([i for i in materials_col.find()])
    for m in materials_col.find():
        print(m)
        if m.get("type") not in materials:
            materials[m.get("type")] = []
        
        materials[m.get("type")].append({
            "materialID": m.get("materialID"),
            "C1": m.get("C1"),
            "C2": m.get("C2"),
            "C5": m.get("C5"),
            "C6": m.get("C6"),
        })
    suppliers = {}

    for s in suppliers_col.find():
        for m in s.get("materials"):
            if m.get("materialID") not in suppliers:
                suppliers[m.get("materialID")] = []
            suppliers[m.get("materialID")].append({
                "supplierID": s.get("supplierID"),
                "C3": m.get("C3"),
                "C7": m.get("C7"),
            })

    # ----------------------------
    # 3. Aggregate orders
    # ----------------------------
    stats = defaultdict(list)

    for o in orders_col.find():
        key = (o["pID"], o["supplier"])
        diff = o["nominal"] - o["actual"]  
        stats[key].append(diff)

    # ----------------------------
    # 4. Print combined report
    # ----------------------------

    alternatives = {}
    for mtype in materials:
        alternatives[mtype] = []
        for m in materials[mtype]:
            material = m["materialID"]
            C1 = m["C1"]
            C2 = m["C2"]
            C5 = m["C5"]
            C6 = m["C6"]
            for s in suppliers[material]:
                supplier = s["supplierID"]
                C3 = s["C3"]
                C7 = s["C7"]
                C4 = sum(stats[(material,supplier)])/len(stats[(material,supplier)])
                alternatives[mtype].append({
                    "materialID":material,
                    "supplierID":supplier,
                    "C1":C1,
                    "C2":C2,
                    "C3":C3,
                    "C4":C4,
                    "C5":C5,
                    "C6":C6,
                    "C7":C7,

                })
    return alternatives
if __name__ == "__main__":
    import json
    print(f'{json.dumps(FetchData(), indent=4)}')
# for (material_id, supplier), diffs in stats.items():

#     mat = materials.get(material_id, {})

#     mean_diff = sum(diffs) / len(diffs) if diffs else 0

#     print("Alternative 1:")
#     print(f"  material: {material_id}")
#     print(f"  material_type: {mat.get('material_type')}")
#     print(f"  supplier: {supplier}")
#     print(f"  C1: {mat.get('C1')}")
#     print(f"  C2: {mat.get('C2')}")
#     print(f"  C3: {mat.get('C3')}")
#     print(f"  C7: {mat.get('C7')}")
#     print(f"  meanDiff (actual - nominal): {mean_diff}")
#     print("-" * 50)

