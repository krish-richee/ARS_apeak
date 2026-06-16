"""
batch_job.py
Run ONCE after generate_embeddings.py.
Reads vectors directly from FAISS — NO model download needed.
Queries FAISS → applies 4 hard constraints → stores top 10 candidates.
NO LLM calls here. LLM runs in app.py on first user pick.
"""

import os, json, pickle
import numpy as np
import faiss

INDEX_PATH    = "faiss_index/products.index"
META_PATH     = "faiss_index/products.pkl"
DB_PATH       = "db.json"
VECTOR_DIM    = 768
TOP_K         = 100
STORE_TOP     = 10
PRICE_BAND    = 0.40
MAX_PER_BRAND = 2

# ── Load ──────────────────────────────────────────────────────────────────────
print("📦 Loading FAISS index + metadata ...")
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    records = pickle.load(f)
print(f"   {len(records):,} products loaded")
print(f"   {index.ntotal:,} vectors in FAISS index")
print(f"   index type: {type(index)}")

# ── Extract ALL vectors at once from FAISS ────────────────────────────────────
# The saved index is IndexIDMap(IndexFlatIP).  Unwrap/downcast the inner index
# before calling get_xb; reconstruct_n on IndexIDMap can abort the process.
print("\n🔧 Extracting all vectors from FAISS index ...")
try:
    base_index = faiss.downcast_index(index.index) if hasattr(index, "index") else faiss.downcast_index(index)
    if not hasattr(base_index, "get_xb"):
        raise TypeError(f"{type(base_index)} does not expose get_xb")
    if base_index.d != VECTOR_DIM:
        raise ValueError(f"index dim is {base_index.d}, expected {VECTOR_DIM}")

    all_vectors = faiss.rev_swig_ptr(
        base_index.get_xb(),
        base_index.ntotal * base_index.d,
    ).reshape(base_index.ntotal, base_index.d).copy()
    print(f"   Extracted via get_xb: {all_vectors.shape}")
except Exception as e:
    raise RuntimeError(
        "Could not extract vectors from FAISS. Re-run generate_embeddings.py "
        "to rebuild the index as IndexIDMap(IndexFlatIP)."
    ) from e

# verify vectors are not all zeros
nonzero = np.count_nonzero(all_vectors.sum(axis=1))
print(f"   Non-zero vectors: {nonzero:,} / {len(records):,}")

# ── Lookups ───────────────────────────────────────────────────────────────────
id_to_rec  = {i: r for i, r in enumerate(records)}
pid_to_idx = {r["product_id"]: i for i, r in enumerate(records)}

# ── 4 Hard Constraints ────────────────────────────────────────────────────────
def passes_hard_constraints(candidate, anchor, same_brand):
    if not candidate.get("is_in_stock", False):
        return False
    if candidate.get("quantity", 0) <= 0:
        return False
    if candidate["product_type"] != anchor["product_type"]:
        return False
    if candidate["gender"] != anchor["gender"]:
        return False
    anchor_price = anchor["price"]
    if anchor_price > 0:
        if not (anchor_price * (1 - PRICE_BAND) <= candidate["price"] <= anchor_price * (1 + PRICE_BAND)):
            return False
    if candidate["product_id"] == anchor["product_id"]:
        return False
    if same_brand and candidate["brand"] != anchor["brand"]:
        return False
    if not same_brand and candidate["brand"] == anchor["brand"]:
        return False
    return True

# ── Query using pre-extracted vectors ────────────────────────────────────────
def query_candidates(anchor_rec, anchor_idx, same_brand):
    vec = all_vectors[anchor_idx:anchor_idx+1]  # shape (1, 768)

    scores, indices = index.search(vec, TOP_K)
    scores  = scores[0]
    indices = indices[0]

    filtered    = []
    brands_seen = {}

    for score, i in zip(scores, indices):
        if i < 0 or i >= len(records):
            continue
        candidate = id_to_rec[i]

        if not passes_hard_constraints(candidate, anchor_rec, same_brand):
            continue

        if not same_brand:
            b = candidate["brand"]
            if brands_seen.get(b, 0) >= MAX_PER_BRAND:
                continue
            brands_seen[b] = brands_seen.get(b, 0) + 1

        filtered.append({
            "product_id":     candidate["product_id"],
            "sku":            candidate["sku"],
            "product_name":   candidate["product_name"],
            "brand":          candidate["brand"],
            "product_type":   candidate["product_type"],
            "gender":         candidate["gender"],
            "price":          candidate["price"],
            "original_price": candidate.get("original_price", candidate["price"]),
            "is_in_stock":    candidate["is_in_stock"],
            "quantity":       candidate["quantity"],
            "key_features":   candidate["key_features"][:300],
            "short_desc":     candidate["short_desc"],
            "image_url":      candidate["image_url"],
            "product_url":    candidate["product_url"],
            "colors":         candidate["colors"],
            "score":          round(float(score), 4),
        })

        if len(filtered) >= STORE_TOP:
            break

    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered[:STORE_TOP]

# ── Resume ────────────────────────────────────────────────────────────────────
if os.path.exists(DB_PATH):
    with open(DB_PATH) as f:
        db = json.load(f)
    # reset — old db has same=0 diff=0 everywhere, need to reprocess
    has_empty = sum(1 for v in db.values() if len(v.get("same_brand_candidates",[])) == 0 and len(v.get("diff_brand_candidates",[])) == 0)
    if has_empty > len(db) * 0.5:
        print(f"\n   ⚠️  Old db has empty candidates — resetting and reprocessing")
        db = {}
    else:
        print(f"\n   Resuming — {len(db):,} already done")
else:
    db = {}

# ── Batch loop ────────────────────────────────────────────────────────────────
total = len(records)
print(f"\n🎯 Processing {total:,} products ...\n")

for idx, anchor_rec in enumerate(records):
    pid = anchor_rec["product_id"]
    if pid in db and (
        len(db[pid].get("same_brand_candidates",[])) > 0 or
        len(db[pid].get("diff_brand_candidates",[])) > 0
    ):
        continue

    same = query_candidates(anchor_rec, idx, same_brand=True)
    diff = query_candidates(anchor_rec, idx, same_brand=False)

    db[pid] = {
        "product_id":    pid,
        "sku":           anchor_rec["sku"],
        "product_name":  anchor_rec["product_name"],
        "brand":         anchor_rec["brand"],
        "product_type":  anchor_rec["product_type"],
        "gender":        anchor_rec["gender"],
        "main_category": anchor_rec["main_category"],
        "price":         anchor_rec["price"],
        "original_price": anchor_rec.get("original_price", anchor_rec["price"]),
        "is_in_stock":   anchor_rec["is_in_stock"],
        "quantity":      anchor_rec["quantity"],
        "key_features":  anchor_rec["key_features"],
        "short_desc":    anchor_rec["short_desc"],
        "image_url":     anchor_rec["image_url"],
        "product_url":   anchor_rec["product_url"],
        "colors":        anchor_rec["colors"],
        "same_brand_candidates": same,
        "diff_brand_candidates": diff,
        "same_brand": [],
        "diff_brand": [],
    }

    if (idx + 1) % 200 == 0 or idx < 5:
        print(f"   [{idx+1:4}/{total}] {anchor_rec['product_type']:25} | "
              f"{anchor_rec['brand'][:18]:18} | "
              f"same={len(same):2} diff={len(diff):2}")

    if (idx + 1) % 200 == 0:
        with open(DB_PATH, "w") as f:
            json.dump(db, f, indent=2)
        print(f"   💾 saved {len(db):,} to db.json")

with open(DB_PATH, "w") as f:
    json.dump(db, f, indent=2)

# ── Summary ───────────────────────────────────────────────────────────────────
has_same = sum(1 for v in db.values() if len(v.get("same_brand_candidates",[])) > 0)
has_diff = sum(1 for v in db.values() if len(v.get("diff_brand_candidates",[])) > 0)
print(f"\n✅ Done — {len(db):,} products in db.json")
print(f"   Products with same_brand candidates: {has_same:,}")
print(f"   Products with diff_brand candidates: {has_diff:,}")
print(f"   Next: streamlit run app.py")
