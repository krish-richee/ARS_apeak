
"""
api.py — APeak Alternative Finder API
Run: uvicorn api:app --reload --port 8003
Swagger: http://localhost:8003/docs
"""
import pickle, os, json, faiss, numpy as np
from collections import defaultdict
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# ── Config ────────────────────────────────────────────────────────
INDEX_PATH    = "faiss_index/products.index"
META_PATH     = "faiss_index/products.pkl"
DB_PATH       = "db.json"
SEARCH_K      = 300
MAX_ALTS      = 3
PRICE_BAND    = 0.30
MAX_PER_BRAND = 2
GROQ_MODEL    = "llama-3.1-8b-instant"

# ── Load once at startup ──────────────────────────────────────────
_idx = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    records: list[dict] = pickle.load(f)
_base = faiss.downcast_index(_idx.index) if hasattr(_idx, "index") else faiss.downcast_index(_idx)
vectors = faiss.rev_swig_ptr(_base.get_xb(), _base.ntotal * _base.d).reshape(_base.ntotal, _base.d).copy()
db: dict = json.load(open(DB_PATH)) if os.path.exists(DB_PATH) else {}
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY","")) if os.getenv("GROQ_API_KEY") else None

# ── App ───────────────────────────────────────────────────────────
app = FastAPI(
    title="APeak Alternative Finder",
    description="Send a SKU + brand mode, get back in-stock alternatives with AI comparison notes.",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Request / Response models ─────────────────────────────────────
class AlternativeRequest(BaseModel):
    sku: str = Field(..., example="pg77391", description="Product SKU")
    mode: Literal["same_brand", "diff_brand"] = Field(
        ...,
        example="same_brand",
        description="'same_brand' = alternatives from the same brand only. 'diff_brand' = alternatives from other brands."
    )

class ProductOut(BaseModel):
    sku:            str
    product_name:   str
    brand:          str
    product_type:   str
    gender:         str
    main_category:  str
    price:          float
    original_price: float | None = None
    quantity:       int
    colors:         list[str]
    key_features:   str
    product_url:    str | None = None
    image_url:      str | None = None

class AltOut(BaseModel):
    product:         ProductOut
    price_note:      str   # "12% cheaper"
    price_direction: str   # "cheaper" | "higher" | "same"

class AlternativeResponse(BaseModel):
    anchor:       ProductOut
    mode:         str
    alternatives: list[AltOut]
    rfy:          list[dict]   # which-is-right-for-you bullets

# ── Helpers ───────────────────────────────────────────────────────
def avail(r): return bool(r.get("is_in_stock")) and float(r.get("quantity",0) or 0) > 0
def money(v):
    try: return f"${float(v or 0):,.0f}"
    except: return "—"
def short(v, n=200):
    t = " ".join(str(v or "").split())
    return t[:n-3].rsplit(" ",1)[0]+"..." if len(t)>n else t
def feat_lines(text, n=3):
    return [p.strip() for p in str(text or "").replace("\n","|").split("|") if p.strip()][:n]
def price_diff_label(ap, cp):
    try:
        a, c = float(ap), float(cp)
        if a<=0 or c<=0: return "", ""
        d=c-a; p=abs(d)/a*100
        if abs(d)<0.5: return "Same price","same"
        return f"{p:.0f}% {'cheaper' if d<0 else 'costlier'}", "cheaper" if d<0 else "higher"
    except: return "", ""
def _price_ok(c, a, band=PRICE_BAND):
    try:
        ap=float(a.get("price") or 0); cp=float(c.get("price") or 0)
        return ap>0 and cp>0 and ap*(1-band)<=cp<=ap*(1+band)
    except: return False
def _to_out(r):
    return ProductOut(
        sku           = r.get("sku",""),
        product_name  = r["product_name"],
        brand         = r["brand"],
        product_type  = r["product_type"],
        gender        = r["gender"],
        main_category = r["main_category"],
        price         = float(r.get("price") or 0),
        original_price= float(r.get("original_price") or 0) or None,
        quantity      = int(float(r.get("quantity") or 0)),
        colors        = r.get("colors",[]),
        key_features  = r.get("key_features",""),
        product_url   = r.get("product_url"),
        image_url     = r.get("image_url"),
    )
def _find_sku(sku: str):
    sku_l = sku.strip().lower()
    for i, r in enumerate(records):
        if r.get("sku","").strip().lower() == sku_l:
            return i, r
    raise HTTPException(status_code=404, detail=f"SKU '{sku}' not found. Use GET /skus to browse available SKUs.")

# ── Search ────────────────────────────────────────────────────────
def strict_ok(c, a, mode):
    if not avail(c) or c["product_id"]==a["product_id"]: return False
    if c["product_type"]!=a["product_type"] or c["gender"]!=a["gender"]: return False
    if not _price_ok(c, a): return False
    if mode=="same" and c["brand"]!=a["brand"]: return False
    if mode=="diff" and c["brand"]==a["brand"]: return False
    return True

def relaxed_ok(c, a, mode):
    if not avail(c) or c["product_id"]==a["product_id"]: return False
    if not _price_ok(c, a, band=0.50): return False
    if mode=="same" and c["brand"]!=a["brand"]: return False
    if mode=="diff" and c["brand"]==a["brand"]: return False
    return c["gender"]==a["gender"] or c["product_type"]==a["product_type"]

def find_alts(aidx, mode):
    anchor = records[aidx]
    vec = vectors[aidx:aidx+1].astype("float32")
    _, ids = _idx.search(vec, SEARCH_K)
    results, brands = [], defaultdict(int)
    for rid in ids[0]:
        if rid<0 or rid>=len(records): continue
        c = records[int(rid)]
        if not strict_ok(c, anchor, mode): continue
        if mode=="diff":
            if brands[c["brand"]]>=MAX_PER_BRAND: continue
            brands[c["brand"]]+=1
        results.append(c)
        if len(results)>=MAX_ALTS: return results
    if mode=="diff":
        seen={r["product_id"] for r in results}
        for rid in ids[0]:
            if rid<0 or rid>=len(records): continue
            c=records[int(rid)]
            if c["product_id"] in seen or not relaxed_ok(c,anchor,mode): continue
            results.append(c); seen.add(c["product_id"])
            if len(results)>=MAX_ALTS: break
    return results

# ── LLM ──────────────────────────────────────────────────────────
def get_rfy(anchor, alts, mode):
    cache_key=f"rfy_{anchor['product_id']}_{mode}"
    if cache_key in db: return db[cache_key]
    def fallback():
        out=[{"scenario":"you want to keep your original pick","product":anchor["product_name"],"reason":"your selected product"}]
        for c in alts:
            note,_=price_diff_label(anchor["price"],c["price"])
            feats=feat_lines(c.get("key_features",""),1)
            out.append({"scenario":feats[0][:55] if feats else f"you prefer {c['brand']}","product":c["product_name"],"reason":note or "similar specs"})
        return out
    if not groq_client: return fallback()
    cands_text="\n".join([f"Alt {i+1}: {c['product_name']} · {c['brand']} · {money(c['price'])} · {short(c.get('key_features',''),150)}" for i,c in enumerate(alts)])
    prompt=f"""Product advisor at APeak. Write "Which is right for you?" guide.
SELECTED: {anchor['product_name']} · {anchor['brand']} · {money(anchor['price'])}
Features: {short(anchor.get('key_features',''),180)}
ALTERNATIVES: {cands_text}
Write {len(alts)+1} bullets (anchor first, then one per alt).
Each: scenario (starts "you want", max 8 words, real need), product (exact name), reason (max 7 words, real spec or price delta).
Return ONLY valid JSON array, no markdown:
[{{"scenario":"you want...","product":"name","reason":"spec"}}]"""
    try:
        resp=groq_client.chat.completions.create(model=GROQ_MODEL,messages=[{"role":"system","content":"Return valid JSON array only. No markdown."},{"role":"user","content":prompt}],max_tokens=400,temperature=0.3)
        raw=resp.choices[0].message.content.strip()
        if "```" in raw:
            for p in raw.split("```"):
                if "[" in p: raw=p.strip(); break
        if raw.lower().startswith("json"): raw=raw[4:].strip()
        if "[" in raw and "]" in raw: raw=raw[raw.index("["):raw.rindex("]")+1]
        result=json.loads(raw)
        db[cache_key]=result
        try:
            with open(DB_PATH,"w") as f: json.dump(db,f,indent=2)
        except: pass
        return result
    except: return fallback()

# ══════════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════════

@app.post(
    "/alternatives",
    response_model=AlternativeResponse,
    summary="Get alternatives for a product SKU",
    description="""
Send a JSON body with `sku` and `mode`:

```json
{ "sku": "pg77391", "mode": "same_brand" }
```
or
```json
{ "sku": "pg77391", "mode": "diff_brand" }
```

**`same_brand`** — returns up to 3 alternatives from the **same brand**, within ±30% price.  
**`diff_brand`** — returns up to 3 alternatives from **different brands** (max 2 per brand), within ±30% price.  

All results are confirmed in-stock. The `rfy` array contains AI-generated "which is right for you" bullets.
""",
)
def get_alternatives(body: AlternativeRequest):
    # map mode string to internal key
    internal_mode = "same" if body.mode == "same_brand" else "diff"
    aidx, anchor  = _find_sku(body.sku)
    alts          = find_alts(aidx, internal_mode)
    rfy           = get_rfy(anchor, alts, internal_mode)

    return AlternativeResponse(
        anchor       = _to_out(anchor),
        mode         = body.mode,
        alternatives = [
            AltOut(product=_to_out(c), price_note=note, price_direction=direction)
            for c in alts
            for note, direction in [price_diff_label(anchor["price"], c["price"])]
        ],
        rfy = rfy,
    )


@app.get(
    "/skus",
    summary="Browse available SKUs",
    description="Use this to find valid SKUs before calling POST /alternatives.",
)
def list_skus(
    brand:    str | None = None,
    category: str | None = None,
    gender:   str | None = None,
):
    recs = [r for r in records if avail(r)]
    if brand:    recs = [r for r in recs if r["brand"].lower()    == brand.lower()]
    if category: recs = [r for r in recs if r["main_category"].lower() == category.lower()]
    if gender:   recs = [r for r in recs if r["gender"].lower()   == gender.lower()]
    return [
        {"sku": r["sku"], "product_name": r["product_name"],
         "brand": r["brand"], "price": float(r.get("price",0)),
         "category": r["main_category"]}
        for r in recs
    ]


@app.get("/health", summary="Health check")
def health():
    return {"status":"ok","products_loaded":len(records),"index_vectors":int(_idx.ntotal)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8003, reload=True)
