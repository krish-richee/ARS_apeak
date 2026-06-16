
"""
generate_embeddings.py
Run ONCE. Embeds all APeak products using BAAI/bge-base-en-v1 (768 dims)
Saves: faiss_index/products.index + faiss_index/products.pkl
"""

import os, ast, json, pickle
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

CSV_PATH    = "data/APeak_Gold_Product_Catalogue_in_.csv"
INDEX_DIR   = "faiss_index"
INDEX_PATH  = f"{INDEX_DIR}/products.index"
META_PATH   = f"{INDEX_DIR}/products.pkl"
MODEL_NAME  = "BAAI/bge-base-en-v1.5"
VECTOR_DIM  = 768
BATCH_SIZE  = 32
EXCLUDE_CAT = ["Gift Cards"]

os.makedirs(INDEX_DIR, exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────────────
print("📦 Loading catalogue ...")
df = pd.read_csv(CSV_PATH)
df["price"]     = pd.to_numeric(df["price"],    errors="coerce").fillna(0)
df["quantity"]  = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
df["is_in_stock"] = df["is_in_stock"].astype(str).str.lower().str.strip()

# remove gift cards and disabled
df = df[~df["main_category"].isin(EXCLUDE_CAT)]
df = df[df["status"] == "Enabled"].reset_index(drop=True)
print(f"   {len(df):,} products after filtering")

# ── Helpers ──────────────────────────────────────────────────────────────────
def safe(val, default=""):
    return default if pd.isna(val) else str(val).strip()

def effective_price(row):
    sp = row.get("special_price", None)
    if sp and not pd.isna(sp) and float(sp) > 0:
        return float(sp)
    return float(row["price"]) if row["price"] > 0 else 0.0

def get_gender(main_cat):
    mc = safe(main_cat).lower()
    if "women"  in mc: return "Womens"
    if "men"    in mc: return "Mens"
    if "kid"    in mc: return "Kids"
    if "pack"   in mc: return "Packs"
    if "footwear" in mc: return "Footwear"
    return "Other"

def parse_colors(variants_str):
    """Extract unique colors from variants JSON."""
    if pd.isna(variants_str): return []
    try:
        variants = json.loads(variants_str)
        colors = set()
        for v in variants:
            attrs = v.get("additional_attributes_json", {})
            if isinstance(attrs, str):
                attrs = json.loads(attrs)
            c = attrs.get("color", "")
            if c: colors.add(c)
        return list(colors)
    except Exception:
        return []

def build_embed_text(row):
    """Text used for embedding — rich semantic content."""
    parts = [
        safe(row["product_name"]),
        "by", safe(row["brand"]),
        "|", safe(row["product_type"]),
        "|", safe(row["main_category"]),
        "|", safe(row.get("key_features", ""))[:300],
        "|", safe(row.get("short_description", ""))[:200],
    ]
    return " ".join(p for p in parts if p)

# ── Build metadata ────────────────────────────────────────────────────────────
print("🔧 Building metadata ...")
records = []
for _, row in df.iterrows():
    ep = effective_price(row)
    records.append({
        "product_id":    safe(row["product_id"]),
        "sku":           safe(row["sku"]),
        "product_name":  safe(row["product_name"]),
        "brand":         safe(row["brand"]),
        "product_type":  safe(row["product_type"]),
        "main_category": safe(row["main_category"]),
        "gender":        get_gender(row["main_category"]),
        "category":      safe(row.get("category", "")),
        "sub_category":  safe(row.get("sub_category", "")),
        "price":         ep,
        "original_price": float(row["price"]) if row["price"] > 0 else 0.0,
        "is_in_stock":   safe(row["is_in_stock"]) == "true",
        "quantity":      float(row["quantity"]),
        "key_features":  safe(row.get("key_features", ""))[:400],
        "short_desc":    safe(row.get("short_description", ""))[:200],
        "image_url":     safe(row.get("image_url", "")),
        "product_url":   safe(row.get("product_page_url", "")),
        "colors":        parse_colors(row.get("variants", None)),
        "embed_text":    build_embed_text(row),
    })

print(f"   {len(records):,} records built")

# ── Load model ───────────────────────────────────────────────────────────────
print(f"\n🤖 Loading {MODEL_NAME} ...")
model = SentenceTransformer(MODEL_NAME)
print("   Model loaded ✅")

# ── Embed in batches ─────────────────────────────────────────────────────────
texts  = [r["embed_text"] for r in records]
total  = len(texts)
all_vecs = []

print(f"\n🚀 Embedding {total:,} products in batches of {BATCH_SIZE} ...")
for start in range(0, total, BATCH_SIZE):
    end   = min(start + BATCH_SIZE, total)
    batch = texts[start:end]
    # BGE requires a query prefix for retrieval tasks
    batch_prefixed = [f"Represent this product for retrieval: {t}" for t in batch]
    vecs  = model.encode(batch_prefixed, normalize_embeddings=True, show_progress_bar=False)
    all_vecs.append(vecs)
    if (start // BATCH_SIZE) % 20 == 0:
        print(f"   {end}/{total} embedded ...", end="\r")

embeddings = np.vstack(all_vecs).astype("float32")
print(f"\n   ✅ Embeddings shape: {embeddings.shape}")

# ── Build FAISS index ────────────────────────────────────────────────────────
print("\n📐 Building FAISS index (IndexFlatIP — cosine via normalized vecs) ...")
index = faiss.IndexFlatIP(VECTOR_DIM)   # inner product = cosine on L2-normalized vecs
index = faiss.IndexIDMap(index)
ids   = np.arange(len(records)).astype("int64")
index.add_with_ids(embeddings, ids)
print(f"   {index.ntotal:,} vectors indexed ✅")

# ── Save ─────────────────────────────────────────────────────────────────────
faiss.write_index(index, INDEX_PATH)
with open(META_PATH, "wb") as f:
    pickle.dump(records, f)

print(f"\n✅ Done!")
print(f"   FAISS index → {INDEX_PATH}")
print(f"   Metadata    → {META_PATH}")
print(f"   Next step   → python3 batch_job.py")
