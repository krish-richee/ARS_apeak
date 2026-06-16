# core.py  — all the heavy lifting, imported by both app.py and api.py
import pickle, os, json, faiss, numpy as np
from collections import defaultdict
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

INDEX_PATH    = "faiss_index/products.index"
META_PATH     = "faiss_index/products.pkl"
DB_PATH       = "db.json"
SEARCH_K      = 300
MAX_ALTS      = 3
PRICE_BAND    = 0.30
MAX_PER_BRAND = 2
GROQ_MODEL    = "llama-3.1-8b-instant"

# Load once at import time (no Streamlit cache needed here)
_idx = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    records = pickle.load(f)
base = faiss.downcast_index(_idx.index) if hasattr(_idx, "index") else faiss.downcast_index(_idx)
vectors = faiss.rev_swig_ptr(base.get_xb(), base.ntotal * base.d).reshape(base.ntotal, base.d).copy()

db: dict = json.load(open(DB_PATH)) if os.path.exists(DB_PATH) else {}

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", "")) if os.getenv("GROQ_API_KEY") else None

# ── helpers ──────────────────────────────────────────────────────
def avail(r):      return bool(r.get("is_in_stock")) and float(r.get("quantity", 0) or 0) > 0
def money(v):
    try: return f"${float(v or 0):,.0f}"
    except: return "—"
def short(v, n=200):
    t = " ".join(str(v or "").split())
    return t[:n-3].rsplit(" ", 1)[0]+"..." if len(t) > n else t
def feat_lines(text, n=5):
    return [p.strip() for p in str(text or "").replace("\n", "|").split("|") if p.strip()][:n]
def price_diff_label(ap, cp):
    try:
        a, c = float(ap), float(cp)
        if a <= 0 or c <= 0: return "", ""
        d = c - a; p = abs(d) / a * 100
        if abs(d) < 0.5: return "Same price", "same"
        return f"{p:.0f}% {'cheaper' if d<0 else 'costlier'}", "cheaper" if d<0 else "higher"
    except: return "", ""

def _price_ok(c, a, band=PRICE_BAND):
    try:
        ap = float(a.get("price") or 0)
        cp = float(c.get("price") or 0)
        return ap > 0 and cp > 0 and ap*(1-band) <= cp <= ap*(1+band)
    except: return False

# ── search ───────────────────────────────────────────────────────
def strict_ok(c, a, mode):
    if not avail(c) or c["product_id"] == a["product_id"]: return False
    if c["product_type"] != a["product_type"] or c["gender"] != a["gender"]: return False
    if not _price_ok(c, a): return False
    if mode == "same" and c["brand"] != a["brand"]: return False
    if mode == "diff" and c["brand"] == a["brand"]: return False
    return True

def relaxed_ok(c, a, mode):
    if not avail(c) or c["product_id"] == a["product_id"]: return False
    if not _price_ok(c, a, band=0.50): return False
    if mode == "same" and c["brand"] != a["brand"]: return False
    if mode == "diff" and c["brand"] == a["brand"]: return False
    return c["gender"] == a["gender"] or c["product_type"] == a["product_type"]

def find_alts(aidx: int, mode: str):
    anchor = records[aidx]
    vec = vectors[aidx:aidx+1].astype("float32")
    _, ids = _idx.search(vec, SEARCH_K)
    results, brands = [], defaultdict(int)
    for rid in ids[0]:
        if rid < 0 or rid >= len(records): continue
        c = records[int(rid)]
        if not strict_ok(c, anchor, mode): continue
        if mode == "diff":
            if brands[c["brand"]] >= MAX_PER_BRAND: continue
            brands[c["brand"]] += 1
        results.append(c)
        if len(results) >= MAX_ALTS: return results
    if mode == "diff":
        seen = {r["product_id"] for r in results}
        for rid in ids[0]:
            if rid < 0 or rid >= len(records): continue
            c = records[int(rid)]
            if c["product_id"] in seen or not relaxed_ok(c, anchor, mode): continue
            results.append(c); seen.add(c["product_id"])
            if len(results) >= MAX_ALTS: break
    return results

def get_rfy(anchor: dict, alts: list, mode: str) -> list:
    cache_key = f"rfy_{anchor['product_id']}_{mode}"
    if cache_key in db: return db[cache_key]
    # ... (same LLM logic as your app.py get_rfy) ...
    return []  # fallback

def save_db():
    try:
        with open(DB_PATH, "w") as f: json.dump(db, f, indent=2)
    except: pass