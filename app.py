# # import pickle, os, json
# # from collections import defaultdict
# # import faiss, numpy as np
# # import streamlit as st
# # from groq import Groq
# # from dotenv import load_dotenv
# # load_dotenv()
# # INDEX_PATH    = "faiss_index/products.index"
# # META_PATH     = "faiss_index/products.pkl"
# # DB_PATH       = "db.json"
# # SEARCH_K      = 300
# # MAX_ALTS      = 3
# # PRICE_BAND    = 0.30
# # MAX_PER_BRAND = 2
# # GROQ_MODEL    = "llama-3.1-8b-instant"
# # st.set_page_config(page_title="APeak Alternatives", layout="wide", initial_sidebar_state="collapsed")
# # st.markdown("""
# # <style>
# # @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
# # * { box-sizing: border-box; margin: 0; padding: 0; }
# # html, body, [class*="css"] {
# #     font-family: 'Inter', sans-serif;
# #     background: 
# # #ffffff;
# #     color: 
# # #111827;
# # }
# # .block-container { padding: 0 2rem 3rem; max-width: 1260px; }
# # /* ── NAV BAR ── */
# # .navbar {
# #     background: #fff;
# #     border-bottom: 1px solid 
# # #e5e7eb;
# #     padding: 0.9rem 0;
# #     margin-bottom: 1.8rem;
# #     display: flex;
# #     align-items: center;
# #     justify-content: space-between;
# # }
# # .nav-logo { font-size: 1.15rem; font-weight: 800; color: 
# # #111827; letter-spacing: -0.02em; }
# # .nav-logo span { color: 
# # #2563eb; }
# # .nav-links { display: flex; gap: 1.5rem; }
# # .nav-link { font-size: 0.8rem; color: 
# # #6b7280; font-weight: 500; cursor: pointer; }
# # .nav-link:hover { color: 
# # #111827; }
# # /* ── BREADCRUMB ── */
# # .breadcrumb {
# #     font-size: 0.73rem; color: 
# # #9ca3af;
# #     margin-bottom: 1.2rem;
# # }
# # .breadcrumb span { color: 
# # #111827; font-weight: 500; }
# # /* ── PRODUCT SECTION ── */
# # .product-type-pill {
# #     display: inline-block;
# #     background: 
# # #f0f9ff; color: 
# # #0369a1;
# #     font-size: 0.68rem; font-weight: 700;
# #     padding: 0.18rem 0.6rem; border-radius: 20px;
# #     text-transform: uppercase; letter-spacing: 0.07em;
# #     margin-bottom: 0.6rem;
# # }
# # .product-title {
# #     font-size: 1.3rem; font-weight: 800;
# #     color: 
# # #111827; line-height: 1.3;
# #     margin-bottom: 0.3rem;
# # }
# # .product-brand {
# #     font-size: 0.82rem; color: 
# # #6b7280;
# #     margin-bottom: 0.8rem;
# # }
# # .price-main { font-size: 1.8rem; font-weight: 800; color: 
# # #111827; }
# # .price-orig { font-size: 0.95rem; color: 
# # #9ca3af; text-decoration: line-through; margin-left: 0.5rem; }
# # .price-off {
# #     font-size: 0.8rem; font-weight: 700;
# #     color: #fff; background: 
# # #16a34a;
# #     padding: 0.15rem 0.45rem; border-radius: 4px;
# #     margin-left: 0.5rem;
# # }
# # .stock-badge {
# #     display: inline-flex; align-items: center; gap: 0.3rem;
# #     font-size: 0.75rem; font-weight: 600;
# #     color: 
# # #16a34a; margin: 0.5rem 0 1rem;
# # }
# # .stock-dot { width: 7px; height: 7px; background: 
# # #16a34a; border-radius: 50%; }
# # /* ── PARAM GRID ── */
# # .param-title {
# #     font-size: 0.68rem; font-weight: 700;
# #     text-transform: uppercase; letter-spacing: 0.09em;
# #     color: 
# # #9ca3af; margin: 1.1rem 0 0.5rem;
# # }
# # .param-grid {
# #     display: grid; grid-template-columns: repeat(2, 1fr);
# #     gap: 0.45rem; margin-bottom: 0.8rem;
# # }
# # .param-box {
# #     border: 1px solid 
# # #e5e7eb; border-radius: 8px;
# #     padding: 0.6rem 0.75rem; background: 
# # #fafafa;
# # }
# # .param-label { font-size: 0.62rem; color: 
# # #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; }
# # .param-value { font-size: 0.86rem; font-weight: 600; color: 
# # #111827; margin-top: 0.1rem; }
# # /* ── FEATURES ── */
# # .feat-item {
# #     display: flex; align-items: flex-start; gap: 0.5rem;
# #     margin-bottom: 0.35rem;
# # }
# # .feat-check { color: 
# # #16a34a; font-size: 0.85rem; margin-top: 1px; flex-shrink: 0; }
# # .feat-text { font-size: 0.8rem; color: 
# # #374151; line-height: 1.45; }
# # /* ── DIVIDER ── */
# # .divider {
# #     border: none; border-top: 1px solid 
# # #e5e7eb;
# #     margin: 1.8rem 0;
# # }
# # /* ── ALT SECTION HEADER ── */
# # .alt-header {
# #     display: flex; align-items: center; gap: 0.9rem;
# #     margin-bottom: 1rem;
# # }
# # .alt-header-title {
# #     font-size: 1rem; font-weight: 700; color: 
# # #111827;
# #     white-space: nowrap;
# # }
# # .alt-header-line { flex: 1; height: 1px; background: 
# # #e5e7eb; }
# # .alt-header-count {
# #     font-size: 0.72rem; color: 
# # #9ca3af; white-space: nowrap;
# # }
# # /* ── ALT CARD ── */
# # .alt-card {
# #     border: 1px solid 
# # #e5e7eb;
# #     border-radius: 12px;
# #     padding: 1.1rem;
# #     background: #fff;
# #     height: 100%;
# #     transition: box-shadow 0.15s;
# # }
# # .alt-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.07); }
# # .alt-card.best { border: 2px solid 
# # #111827; }
# # .alt-rank-tag {
# #     display: inline-flex; align-items: center; gap: 0.25rem;
# #     font-size: 0.65rem; font-weight: 700;
# #     padding: 0.18rem 0.55rem; border-radius: 20px;
# #     margin-bottom: 0.55rem;
# #     text-transform: uppercase; letter-spacing: 0.06em;
# # }
# # .tag-best    { background: 
# # #111827; color: #fff; }
# # .tag-value   { background: 
# # #fef9c3; color: 
# # #854d0e; }
# # .tag-premium { background: 
# # #f5f3ff; color: 
# # #5b21b6; }
# # .alt-name {
# #     font-size: 0.9rem; font-weight: 700; color: 
# # #111827;
# #     line-height: 1.3; margin-bottom: 0.2rem;
# # }
# # .alt-brand { font-size: 0.75rem; color: 
# # #6b7280; margin-bottom: 0.5rem; }
# # .alt-price { font-size: 1.1rem; font-weight: 800; color: 
# # #111827; }
# # .alt-price-note {
# #     font-size: 0.72rem; font-weight: 600;
# #     color: 
# # #16a34a; margin-top: 0.15rem;
# # }
# # .alt-price-note.higher { color: 
# # #dc2626; }
# # .alt-stock {
# #     font-size: 0.7rem; color: 
# # #16a34a; font-weight: 600;
# #     margin: 0.35rem 0 0.7rem;
# # }
# # /* ── 3 POINTS ── */
# # .points-label {
# #     font-size: 0.62rem; font-weight: 700;
# #     text-transform: uppercase; letter-spacing: 0.08em;
# #     color: 
# # #9ca3af; margin: 0.65rem 0 0.4rem;
# #     border-top: 1px solid 
# # #f3f4f6; padding-top: 0.65rem;
# # }
# # .point-row {
# #     display: flex; align-items: flex-start; gap: 0.45rem;
# #     margin-bottom: 0.4rem;
# # }
# # .point-num {
# #     width: 17px; height: 17px; border-radius: 50%;
# #     background: 
# # #f3f4f6; color: 
# # #6b7280;
# #     font-size: 0.6rem; font-weight: 700;
# #     display: flex; align-items: center; justify-content: center;
# #     flex-shrink: 0; margin-top: 1px;
# # }
# # .point-text { font-size: 0.78rem; color: 
# # #374151; line-height: 1.5; }
# # /* ── COLORS ── */
# # .color-chip {
# #     display: inline-block;
# #     font-size: 0.67rem; color: 
# # #374151;
# #     background: 
# # #f3f4f6; border: 1px solid 
# # #e5e7eb;
# #     border-radius: 20px; padding: 0.12rem 0.45rem;
# #     margin: 0.15rem 0.15rem 0 0;
# # }
# # /* ── FAQ (real ecommerce style) ── */
# # .faq-section { margin-top: 2.5rem; }
# # .faq-header-row {
# #     display: flex; align-items: flex-start;
# #     justify-content: space-between; gap: 2rem;
# #     margin-bottom: 2rem;
# # }
# # .faq-header-left { flex: 1; }
# # .faq-eyebrow {
# #     font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
# #     text-transform: uppercase; color: 
# # #2563eb; margin-bottom: 0.5rem;
# # }
# # .faq-main-title {
# #     font-size: 1.5rem; font-weight: 800; color: 
# # #111827;
# #     line-height: 1.25; margin-bottom: 0.5rem;
# # }
# # .faq-subtitle {
# #     font-size: 0.83rem; color: 
# # #6b7280; line-height: 1.6; max-width: 480px;
# # }
# # .faq-contact-box {
# #     background: 
# # #f9fafb; border: 1px solid 
# # #e5e7eb;
# #     border-radius: 12px; padding: 1.1rem 1.3rem;
# #     min-width: 220px; max-width: 260px;
# # }
# # .faq-contact-title { font-size: 0.8rem; font-weight: 700; color: 
# # #111827; margin-bottom: 0.3rem; }
# # .faq-contact-text { font-size: 0.72rem; color: 
# # #6b7280; line-height: 1.55; }
# # .faq-contact-link {
# #     display: inline-block; margin-top: 0.6rem;
# #     font-size: 0.72rem; font-weight: 600; color: 
# # #2563eb;
# #     text-decoration: none;
# # }
# # .faq-group { margin-bottom: 0.25rem; }
# # .faq-group-label {
# #     font-size: 0.6rem; font-weight: 800; letter-spacing: 0.12em;
# #     text-transform: uppercase; color: 
# # #d1d5db;
# #     padding: 1.2rem 0 0.4rem;
# #     display: flex; align-items: center; gap: 0.5rem;
# # }
# # .faq-group-label::after {
# #     content: ''; flex: 1; height: 1px; background: 
# # #f3f4f6;
# # }
# # .faq-item {
# #     border-bottom: 1px solid 
# # #f3f4f6;
# # }
# # .faq-q-row {
# #     display: flex; align-items: center; gap: 0.75rem;
# #     padding: 0.95rem 0;
# #     cursor: pointer;
# # }
# # .faq-q-icon {
# #     width: 28px; height: 28px; border-radius: 7px;
# #     background: 
# # #f9fafb; border: 1px solid 
# # #e5e7eb;
# #     display: flex; align-items: center; justify-content: center;
# #     font-size: 0.8rem; flex-shrink: 0;
# # }
# # .faq-q-text {
# #     font-size: 0.87rem; font-weight: 600; color: 
# # #111827;
# #     flex: 1; line-height: 1.4;
# # }
# # .faq-q-chevron { font-size: 0.7rem; color: 
# # #9ca3af; flex-shrink: 0; }
# # .faq-a {
# #     font-size: 0.82rem; color: 
# # #4b5563;
# #     line-height: 1.7; padding: 0 0 1rem 2.5rem;
# # }
# # .faq-a strong { color: 
# # #111827; }
# # .faq-a ul { margin: 0.5rem 0 0 1rem; }
# # .faq-a li { margin-bottom: 0.25rem; }
# # /* ── FOOTER ── */
# # .footer {
# #     border-top: 1px solid 
# # #e5e7eb;
# #     padding-top: 1.5rem; margin-top: 3rem;
# #     display: flex; justify-content: space-between; align-items: center;
# # }
# # .footer-text { font-size: 0.72rem; color: 
# # #9ca3af; }
# # #MainMenu, footer, header { visibility: hidden; }
# # div[data-testid="stExpander"] {
# #     border: none !important;
# #     border-bottom: 1px solid 
# # #f3f4f6 !important;
# #     border-radius: 0 !important;
# #     background: transparent !important;
# # }
# # div[data-testid="stExpander"] summary {
# #     font-size: 0.87rem !important;
# #     font-weight: 600 !important;
# #     color: 
# # #111827 !important;
# #     padding: 0.95rem 0 !important;
# # }
# # div[data-testid="stExpander"] summary:hover {
# #     color: 
# # #2563eb !important;
# # }

# # /* ── Clean white theme + compact FAQ overrides ── */
# # .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
# #     background: #ffffff !important;
# #     color: #111827 !important;
# # }
# # .stMarkdown, .stMarkdown p, .stText, label {
# #     color: #111827 !important;
# # }
# # .faq-header-row {
# #     margin-bottom: 0.75rem !important;
# # }
# # .faq-header-left {
# #     max-width: 520px !important;
# # }
# # .faq-eyebrow {
# #     font-size: 0.6rem !important;
# #     color: #2563eb !important;
# #     margin-bottom: 0.3rem !important;
# # }
# # .faq-main-title {
# #     font-size: 1rem !important;
# #     color: #0f172a !important;
# #     margin-bottom: 0.25rem !important;
# # }
# # .faq-subtitle {
# #     font-size: 0.68rem !important;
# #     color: #4b5563 !important;
# #     line-height: 1.45 !important;
# #     max-width: 420px !important;
# # }
# # div[data-testid="stExpander"] {
# #     border: 1px solid #dbe3ef !important;
# #     border-radius: 8px !important;
# #     background: #ffffff !important;
# #     margin-bottom: 0.35rem !important;
# #     box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
# #     overflow: hidden !important;
# # }
# # div[data-testid="stExpander"] summary {
# #     font-size: 0.76rem !important;
# #     font-weight: 700 !important;
# #     color: #0f172a !important;
# #     padding: 0.46rem 0.68rem !important;
# #     background: #ffffff !important;
# # }
# # div[data-testid="stExpander"] summary:hover {
# #     color: #2563eb !important;
# #     background: #f8fafc !important;
# # }
# # div[data-testid="stExpander"] summary p {
# #     color: #0f172a !important;
# #     font-size: 0.76rem !important;
# #     font-weight: 700 !important;
# # }
# # div[data-testid="stExpanderDetails"] {
# #     background: #ffffff !important;
# #     padding: 0 0.68rem 0.55rem !important;
# # }
# # div[data-testid="stExpanderDetails"] p,
# # div[data-testid="stExpanderDetails"] li,
# # .faq-a {
# #     color: #374151 !important;
# #     font-size: 0.71rem !important;
# #     line-height: 1.55 !important;
# #     padding-left: 0 !important;
# # }
# # div[data-testid="stExpander"] svg {
# #     color: #334155 !important;
# #     fill: #334155 !important;
# # }
# # </style>
# # """, unsafe_allow_html=True)
# # # ── Load ──────────────────────────────────────────────────────────────────────
# # @st.cache_resource(show_spinner=False)
# # def load_assets():
# #     idx = faiss.read_index(INDEX_PATH)
# #     with open(META_PATH,"rb") as f: recs = pickle.load(f)
# #     base = faiss.downcast_index(idx.index) if hasattr(idx,"index") else faiss.downcast_index(idx)
# #     vecs = faiss.rev_swig_ptr(base.get_xb(), base.ntotal*base.d).reshape(base.ntotal,base.d).copy()
# #     return idx, recs, vecs
# # @st.cache_resource(show_spinner=False)
# # def load_db():
# #     if os.path.exists(DB_PATH):
# #         with open(DB_PATH) as f: return json.load(f)
# #     return {}
# # @st.cache_resource(show_spinner=False)
# # def get_groq_client():
# #     key = os.getenv("GROQ_API_KEY","")
# #     if not key:
# #         return None
# #     return Groq(api_key=key)
# # index, records, vectors = load_assets()
# # db = load_db()
# # groq_client = get_groq_client()
# # # ── Helpers ───────────────────────────────────────────────────────────────────
# # def avail(r): return bool(r.get("is_in_stock")) and float(r.get("quantity",0) or 0)>0
# # def money(v):
# #     try:
# #         value = float(v or 0)
# #         return f"${value:,.0f}" if value.is_integer() else f"${value:,.2f}"
# #     except: return "—"
# # def pct_off(o,c):
# #     try:
# #         o,c=float(o),float(c)
# #         if o>c>0: return f"{int((o-c)/o*100)}% off"
# #     except: pass
# #     return ""
# # def price_diff(ap,cp):
# #     try:
# #         a,c=float(ap),float(cp)
# #         if a<=0 or c<=0: return "",""
# #         d=c-a; p=abs(d)/a*100
# #         if abs(d)<0.5: return "Same price","same"
# #         return f"{p:.0f}% {'cheaper' if d<0 else 'more expensive'}","cheaper" if d<0 else "higher"
# #     except: return "",""
# # def clean_cat(v): return str(v or "").strip() or "Other"
# # def short(v,n=140):
# #     t=" ".join(str(v or "").split())
# #     return t[:n-3].rsplit(" ",1)[0]+"..." if len(t)>n else t
# # def feat_lines(text,n=4):
# #     return [p.strip() for p in str(text or "").replace("\n","|").split("|") if p.strip()][:n]
# # def plabel(r): return f"{r['product_name']}  ·  {r['brand']}  ·  {money(r['price'])}"
# # # ── Search ────────────────────────────────────────────────────────────────────
# # def strict_ok(c,a,mode):
# #     if not avail(c): return False
# #     if c["product_id"]==a["product_id"]: return False
# #     if c["product_type"]!=a["product_type"]: return False
# #     if c["gender"]!=a["gender"]: return False
# #     ap=float(a.get("price",0) or 0)
# #     if ap>0:
# #         cp=float(c.get("price",0) or 0)
# #         if not (ap*(1-PRICE_BAND)<=cp<=ap*(1+PRICE_BAND)): return False
# #     if mode=="same" and c["brand"]!=a["brand"]: return False
# #     if mode=="diff" and c["brand"]==a["brand"]: return False
# #     return True
# # def relaxed_ok(c,a,mode):
# #     if not avail(c): return False
# #     if c["product_id"]==a["product_id"]: return False
# #     ap=float(a.get("price",0) or 0)
# #     if ap>0:
# #         cp=float(c.get("price",0) or 0)
# #         if not (ap*(1-PRICE_BAND)<=cp<=ap*(1+PRICE_BAND)): return False
# #     if mode=="same" and c["brand"]!=a["brand"]: return False
# #     if mode=="diff" and c["brand"]==a["brand"]: return False
# #     return c["gender"]==a["gender"] or c["product_type"]==a["product_type"]
# # def find_alts(aidx,mode):
# #     anchor=records[aidx]
# #     vec=vectors[aidx:aidx+1].astype("float32")
# #     scores,ids=index.search(vec,SEARCH_K)
# #     results,brands=[],defaultdict(int)
# #     for score,rid in zip(scores[0],ids[0]):
# #         if rid<0 or rid>=len(records): continue
# #         c=records[int(rid)]
# #         if not strict_ok(c,anchor,mode): continue
# #         if mode=="diff":
# #             if brands[c["brand"]]>=MAX_PER_BRAND: continue
# #             brands[c["brand"]]+=1
# #         results.append((c,False))
# #         if len(results)>=MAX_ALTS: return results,False
# #     seen={r[0]["product_id"] for r in results}
# #     for score,rid in zip(scores[0],ids[0]):
# #         if rid<0 or rid>=len(records): continue
# #         c=records[int(rid)]
# #         if c["product_id"] in seen: continue
# #         if not relaxed_ok(c,anchor,mode): continue
# #         results.append((c,True))
# #         if len(results)>=MAX_ALTS: break
# #     return results, any(r[1] for r in results)
# # # ── LLM points ────────────────────────────────────────────────────────────────
# # def get_points(anchor, alts, mode):
# #     cache_key = f"pts_{anchor['product_id']}_{mode}"
# #     if cache_key in db: return db[cache_key]
# #     if not groq_client:
# #         result={}
# #         for i,(c,_) in enumerate(alts):
# #             feats=feat_lines(c.get("key_features",""),3)
# #             note,_=price_diff(anchor["price"],c["price"])
# #             result[f"alt_{i+1}"]=[
# #                 feats[0] if feats else f"Shares the same {c['product_type'].lower()} construction and intended use case as your selected product",
# #                 note if note else f"Priced similarly to your pick — {c['brand']} positions this as a direct category equivalent",
# #                 f"A practical swap for {c['gender'].lower()} shoppers who want a ready-to-ship option without compromising on build quality",
# #             ]
# #         return result
# #     cands_text="\n".join([
# #         f"Alternative {i+1}:\n"
# #         f"  Name: {c['product_name']}\n"
# #         f"  Brand: {c['brand']}\n"
# #         f"  Price: {money(c['price'])}\n"
# #         f"  Gender: {c['gender']}\n"
# #         f"  Type: {c['product_type']}\n"
# #         f"  Key Features: {short(c.get('key_features',''),250)}\n"
# #         f"  Colors: {', '.join(c.get('colors',[])[:3]) or 'N/A'}"
# #         for i,(c,_) in enumerate(alts)
# #     ])
# #     prompt=f"""You are a senior product specialist at APeak, a premium outdoor apparel and gear retailer. A customer has selected a product and wants to know which alternatives are genuinely worth considering.
# # CUSTOMER'S SELECTED PRODUCT:
# #   Name: {anchor['product_name']}
# #   Brand: {anchor['brand']}
# #   Type: {anchor['product_type']}
# #   Gender: {anchor['gender']}
# #   Price: {money(anchor['price'])}
# #   Key Features: {short(anchor.get('key_features',''),300)}
# #   Colors: {', '.join(anchor.get('colors',[])[:4]) or 'N/A'}
# # ALTERNATIVES TO EVALUATE ({len(alts)} total, {"same brand lineup" if mode=="same" else "cross-brand comparison"}):
# # {cands_text}
# # Your job: For EACH alternative, write exactly 3 punchy, specific sentences a knowledgeable store associate would say to a customer standing in front of them.
# # Sentence 1 — THE MATCH: What specific construction detail, technology, or feature makes this a legitimate substitute? Name the actual spec (fabric weight, waterproof rating, insulation type, sole tech, etc.) if it appears in the features. Don't say "similar product" — say WHY it's similar.
# # Sentence 2 — THE DIFFERENCE: One concrete, meaningful way this product diverges from the selected item — could be price, a specific material upgrade or downgrade, a fit difference (slim vs relaxed), a technology trade-off, or a use-case nuance. Be direct. Numbers help ("$8 less", "200g lighter", "rated to -10°C vs -5°C").
# # Sentence 3 — THE BUYER: Name the exact type of customer or scenario this alternative is best for. Be specific ("ideal for casual hikers who want warmth on day treks without the bulk of a puffer jacket", not "a good choice for outdoor enthusiasts").
# # Rules:
# # - Never use vague phrases like "great alternative", "similar quality", "worth considering", or "good option"
# # - Never repeat information already obvious from the product name or brand
# # - If features data is thin, infer intelligently from the product type and price point — don't leave sentences generic
# # - Sound like a trusted expert, not a marketing copywriter
# # Return ONLY valid JSON (no markdown, no preamble, no trailing text):
# # {{"alt_1":["sentence 1","sentence 2","sentence 3"],"alt_2":["sentence 1","sentence 2","sentence 3"],"alt_3":["sentence 1","sentence 2","sentence 3"]}}"""
# #     try:
# #         resp=groq_client.chat.completions.create(
# #             model=GROQ_MODEL,
# #             messages=[
# #                 {"role":"system","content":"You are a helpful retail product expert. Return valid JSON only. No markdown, no preamble, no explanation — just the JSON object."},
# #                 {"role":"user","content":prompt}
# #             ],
# #             max_tokens=900, temperature=0.35
# #         )
# #         raw=resp.choices[0].message.content.strip()
# #         if "" in raw:
# #             for p in raw.split(""):
# #                 if "{" in p: raw=p.strip(); break
# #         if raw.lower().startswith("json"): raw=raw[4:].strip()
# #         if "{" in raw and "}" in raw:
# #             raw=raw[raw.index("{"):raw.rindex("}")+1]
# #         result=json.loads(raw)
# #         db[cache_key]=result
# #         try:
# #             with open(DB_PATH,"w") as f: json.dump(db,f,indent=2)
# #         except: pass
# #         return result
# #     except Exception as e:
# #         result={}
# #         for i,(c,_) in enumerate(alts):
# #             feats=feat_lines(c.get("key_features",""),3)
# #             note,_=price_diff(anchor["price"],c["price"])
# #             result[f"alt_{i+1}"]=[
# #                 feats[0] if feats else f"Built on the same {c['product_type'].lower()} platform — shares the core construction DNA with your selected product",
# #                 note if note else f"{c['brand']} takes a slightly different design approach, with distinct colorways and branding details",
# #                 f"Best suited for {c['gender'].lower()} shoppers who need a confirmed in-stock option in the same category",
# #             ]
# #         return result
# # # ══════════════════════════════════════════════════════════════════
# # # PAGE
# # # ══════════════════════════════════════════════════════════════════
# # # navbar
# # st.markdown("""
# # <div class="navbar">
# #   <div class="nav-logo">A<span>Peak</span></div>
# #   <div class="nav-links">
# #     <span class="nav-link">All Products</span>
# #     <span class="nav-link">Categories</span>
# #     <span class="nav-link">Brands</span>
# #     <span class="nav-link">Sale</span>
# #   </div>
# # </div>
# # """, unsafe_allow_html=True)
# # # selectors
# # avail_idx=[i for i,r in enumerate(records) if avail(r)]
# # cats=sorted({clean_cat(records[i]["main_category"]) for i in avail_idx})
# # c1,c2=st.columns([1,2.2])
# # with c1: sel_cat=st.selectbox("Category",cats,label_visibility="collapsed")
# # with c2:
# #     cat_idx=sorted([i for i in avail_idx if clean_cat(records[i]["main_category"])==sel_cat],
# #                    key=lambda i:(records[i]["product_type"],records[i]["brand"],records[i]["product_name"]))
# #     sel_idx=st.selectbox("Product",cat_idx,format_func=lambda i:plabel(records[i]),label_visibility="collapsed")
# # anchor=records[sel_idx]
# # # breadcrumb
# # st.markdown(f"""
# # <div class="breadcrumb">
# #   Home · {anchor['main_category']} · {anchor['product_type']} · <span>{anchor['product_name']}</span>
# # </div>
# # """, unsafe_allow_html=True)
# # # ── main product section ──────────────────────────────────────────
# # img_col, info_col = st.columns([1,1.4], gap="large")
# # with img_col:
# #     if anchor.get("image_url"):
# #         st.image(anchor["image_url"], use_container_width=True)
# #     else:
# #         st.markdown("""<div style="height:300px;background:
# # #f9fafb;border:1px solid 
# # #e5e7eb;
# #         border-radius:12px;display:flex;align-items:center;justify-content:center;
# #         font-size:4rem;">🏷️</div>""", unsafe_allow_html=True)
# # with info_col:
# #     st.markdown(f'<div class="product-type-pill">{anchor["product_type"]}</div>', unsafe_allow_html=True)
# #     st.markdown(f'<div class="product-title">{anchor["product_name"]}</div>', unsafe_allow_html=True)
# #     st.markdown(f'<div class="product-brand">by <strong>{anchor["brand"]}</strong> &nbsp;·&nbsp; {anchor["gender"]} &nbsp;·&nbsp; {anchor["main_category"]}</div>', unsafe_allow_html=True)
# #     orig=anchor.get("original_price",0)
# #     curr=anchor.get("price",0)
# #     off=pct_off(orig,curr)
# #     st.markdown(f"""
# #     <div style="margin:0.5rem 0 0.3rem;display:flex;align-items:baseline;flex-wrap:wrap;gap:0.3rem;">
# #       <span class="price-main">{money(curr)}</span>
# #       {"<span class='price-orig'>"+money(orig)+"</span>" if off else ""}
# #       {"<span class='price-off'>"+off+"</span>" if off else ""}
# #     </div>
# #     """, unsafe_allow_html=True)
# #     if avail(anchor):
# #         st.markdown(f'<div class="stock-badge"><div class="stock-dot"></div>In Stock &nbsp;·&nbsp; {int(float(anchor.get("quantity",0)))} units available</div>', unsafe_allow_html=True)
# #     # params
# #     st.markdown('<div class="param-title">Product Details</div>', unsafe_allow_html=True)
# #     cols_html=", ".join(anchor.get("colors",[])[:4]) or "—"
# #     st.markdown(f"""
# #     <div class="param-grid">
# #       <div class="param-box"><div class="param-label">Brand</div><div class="param-value">{anchor['brand']}</div></div>
# #       <div class="param-box"><div class="param-label">Gender</div><div class="param-value">{anchor['gender']}</div></div>
# #       <div class="param-box"><div class="param-label">SKU</div><div class="param-value" style="font-size:0.75rem">{anchor['sku']}</div></div>
# #       <div class="param-box"><div class="param-label">Available Colors</div><div class="param-value" style="font-size:0.77rem">{cols_html}</div></div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     # features
# #     feats=feat_lines(anchor.get("key_features",""),5)
# #     if feats:
# #         st.markdown('<div class="param-title">Key Features</div>', unsafe_allow_html=True)
# #         items="".join(f'<div class="feat-item"><span class="feat-check">✓</span><span class="feat-text">{f}</span></div>' for f in feats)
# #         st.markdown(items, unsafe_allow_html=True)
# #     if anchor.get("product_url"):
# #         st.markdown("<br>", unsafe_allow_html=True)
# #         st.link_button("View Full Product →", anchor["product_url"])
# # # ── ALTERNATIVES ──────────────────────────────────────────────────
# # st.markdown('<hr class="divider">', unsafe_allow_html=True)
# # if "mode" not in st.session_state: st.session_state.mode="same"
# # st.markdown('<div style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:0.75rem;">Compare With Best Alternatives</div>', unsafe_allow_html=True)
# # b1,b2,_=st.columns([1,1,3])
# # with b1:
# #     if st.button("🔁  Same Brand", use_container_width=True,
# #                  type="primary" if st.session_state.mode=="same" else "secondary"):
# #         st.session_state.mode="same"; st.rerun()
# # with b2:
# #     if st.button("🔀  Different Brand", use_container_width=True,
# #                  type="primary" if st.session_state.mode=="diff" else "secondary"):
# #         st.session_state.mode="diff"; st.rerun()
# # st.markdown("<br>", unsafe_allow_html=True)
# # alts, has_fallback = find_alts(sel_idx, st.session_state.mode)
# # if alts:
# #     mode_label = "Same Brand" if st.session_state.mode=="same" else "Different Brand"
# #     st.markdown(f"""
# #     <div class="alt-header">
# #       <div class="alt-header-title">Your Pick vs {len(alts)} Best {mode_label} Alternative{"s" if len(alts)>1 else ""}</div>
# #       <div class="alt-header-line"></div>
# #       <div class="alt-header-count">Showing {len(alts)} of {MAX_ALTS} max</div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     with st.spinner("Generating comparison..."):
# #         pts = get_points(anchor, alts, st.session_state.mode)
# #     tags     = ["Best Overall","Best Value","Premium Pick"]
# #     tag_cls  = ["tag-best","tag-value","tag-premium"]
# #     tag_icon = ["⭐","💰","👑"]
# #     cols = st.columns(len(alts), gap="medium")
# #     for i,(col,(cand,fallback)) in enumerate(zip(cols,alts)):
# #         with col:
# #             card_cls = "alt-card best" if i==0 else "alt-card"
# #             tag_label= tags[i] if i<3 else "Alternative"
# #             tcls     = tag_cls[i] if i<3 else "tag-best"
# #             ticon    = tag_icon[i] if i<3 else "⭐"
# #             note, ncls = price_diff(anchor["price"], cand["price"])
# #             points_list = pts.get(f"alt_{i+1}", [])
# #             if cand.get("image_url"):
# #                 st.image(cand["image_url"], use_container_width=True)
# #             else:
# #                 st.markdown('<div style="height:100px;background:#f9fafb;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:0.5rem">🏷️</div>', unsafe_allow_html=True)
# #             colors_chips = "".join(f'<span class="color-chip">{c}</span>' for c in cand.get("colors",[])[:3])
# #             points_html  = ""
# #             if points_list:
# #                 rows = "".join(f'<div class="point-row"><div class="point-num">{j+1}</div><div class="point-text">{p}</div></div>' for j,p in enumerate(points_list[:3]))
# #                 points_html = f'<div class="points-label">Why this alternative</div>{rows}'
# #             note_html = f'<div class="alt-price-note {ncls}">{note}</div>' if note else ""
# #             st.markdown(f"""
# #             <div class="{card_cls}">
# #               <span class="alt-rank-tag {tcls}">{ticon} {tag_label}</span>
# #               <div class="alt-name">{cand['product_name']}</div>
# #               <div class="alt-brand">{cand['brand']} &nbsp;·&nbsp; {cand['product_type']}</div>
# #               <div class="alt-price">{money(cand['price'])}</div>
# #               {note_html}
# #               <div class="alt-stock">✓ In Stock &nbsp;·&nbsp; {int(float(cand.get('quantity',0)))} units</div>
# #               {"<div>"+colors_chips+"</div>" if colors_chips else ""}
# #               {points_html}
# #             </div>
# #             """, unsafe_allow_html=True)
# #             if cand.get("product_url"):
# #                 st.link_button(f"View Product", cand["product_url"], use_container_width=True)
# # else:
# #     st.markdown("""
# #     <div style="background:
# # #f9fafb;border:1px solid 
# # #e5e7eb;border-radius:10px;
# #     padding:2rem;text-align:center;">
# #       <div style="font-size:1.5rem;margin-bottom:0.5rem">🔍</div>
# #       <div style="font-size:0.88rem;color:
# # #374151;font-weight:600;margin-bottom:0.3rem">
# #         No alternatives found right now
# #       </div>
# #       <div style="font-size:0.78rem;color:
# # #9ca3af">
# #         Try switching between Same Brand and Different Brand, or select another product.
# #       </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# # # ── FAQs ──────────────────────────────────────────────────────────
# # st.markdown('<hr class="divider">', unsafe_allow_html=True)
# # st.markdown("""
# # <div class="faq-header-row">
# #   <div class="faq-header-left">
# #     <div class="faq-eyebrow">FAQ</div>
# #     <div class="faq-main-title">Quick Questions</div>
# #     <div class="faq-subtitle">
# #       Simple answers before you compare or open a product page.
# #     </div>
# #   </div>
# # </div>
# # """, unsafe_allow_html=True)

# # faqs = [
# #     ("Are these alternatives in stock?",
# #      """Yes. Products shown here are filtered to include only items currently marked in stock."""),
# #     ("How close are the prices?",
# #      """Alternatives stay within <strong>30%</strong> of the selected product price, so the comparison remains useful."""),
# #     ("Can I choose a size or color here?",
# #      """Use <strong>View Product</strong> to open the product page and select available sizes, colors, and quantity."""),
# #     ("Why do some products cost less?",
# #      """A lower price can come from brand, color, sale status, or small feature differences. Check the comparison notes before choosing."""),
# #     ("Can I return an alternative?",
# #      """Returns follow the store policy shown on the product page. Please review it before checkout."""),
# # ]

# # for q, a in faqs:
# #     with st.expander(q):
# #         st.markdown(f'<div class="faq-a">{a}</div>', unsafe_allow_html=True)
# # # footer
# # st.markdown("""
# # <div class="footer">
# #   <div class="footer-text">© 2025 APeak · Powered by FAISS + BAAI/bge-base-en-v1.5 + Groq LLaMA 3.1</div>
# #   <div class="footer-text">All alternatives confirmed in-stock at time of search</div>
# # </div>
# # """, unsafe_allow_html=True)





# import pickle, os, json
# from collections import defaultdict
# import faiss, numpy as np
# import streamlit as st
# from groq import Groq
# from dotenv import load_dotenv
# load_dotenv()

# INDEX_PATH    = "faiss_index/products.index"
# META_PATH     = "faiss_index/products.pkl"
# DB_PATH       = "db.json"
# SEARCH_K      = 300
# MAX_ALTS      = 3
# PRICE_BAND    = 0.30
# MAX_PER_BRAND = 2
# GROQ_MODEL    = "llama-3.1-8b-instant"

# st.set_page_config(page_title="APeak Alternatives", layout="wide", initial_sidebar_state="collapsed")
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
# * { box-sizing: border-box; margin: 0; padding: 0; }
# html, body, [class*="css"] {
#     font-family: 'Inter', sans-serif;
#     background: #ffffff;
#     color: #111827;
# }
# .block-container { padding: 0 2rem 3rem; max-width: 1260px; }
# /* ── NAV BAR ── */
# .navbar {
#     background: #fff;
#     border-bottom: 1px solid #e5e7eb;
#     padding: 0.9rem 0;
#     margin-bottom: 1.8rem;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
# }
# .nav-logo { font-size: 1.15rem; font-weight: 800; color: #111827; letter-spacing: -0.02em; }
# .nav-logo span { color: #2563eb; }
# .nav-links { display: flex; gap: 1.5rem; }
# .nav-link { font-size: 0.8rem; color: #6b7280; font-weight: 500; cursor: pointer; }
# .nav-link:hover { color: #111827; }
# /* ── BREADCRUMB ── */
# .breadcrumb {
#     font-size: 0.73rem; color: #9ca3af;
#     margin-bottom: 1.2rem;
# }
# .breadcrumb span { color: #111827; font-weight: 500; }
# /* ── PRODUCT SECTION ── */
# .product-type-pill {
#     display: inline-block;
#     background: #f0f9ff; color: #0369a1;
#     font-size: 0.68rem; font-weight: 700;
#     padding: 0.18rem 0.6rem; border-radius: 20px;
#     text-transform: uppercase; letter-spacing: 0.07em;
#     margin-bottom: 0.6rem;
# }
# .product-title {
#     font-size: 1.3rem; font-weight: 800;
#     color: #111827; line-height: 1.3;
#     margin-bottom: 0.3rem;
# }
# .product-brand {
#     font-size: 0.82rem; color: #6b7280;
#     margin-bottom: 0.8rem;
# }
# .price-main { font-size: 1.8rem; font-weight: 800; color: #111827; }
# .price-orig { font-size: 0.95rem; color: #9ca3af; text-decoration: line-through; margin-left: 0.5rem; }
# .price-off {
#     font-size: 0.8rem; font-weight: 700;
#     color: #fff; background: #16a34a;
#     padding: 0.15rem 0.45rem; border-radius: 4px;
#     margin-left: 0.5rem;
# }
# .stock-badge {
#     display: inline-flex; align-items: center; gap: 0.3rem;
#     font-size: 0.75rem; font-weight: 600;
#     color: #16a34a; margin: 0.5rem 0 1rem;
# }
# .stock-dot { width: 7px; height: 7px; background: #16a34a; border-radius: 50%; }
# /* ── PARAM GRID ── */
# .param-title {
#     font-size: 0.68rem; font-weight: 700;
#     text-transform: uppercase; letter-spacing: 0.09em;
#     color: #9ca3af; margin: 1.1rem 0 0.5rem;
# }
# .param-grid {
#     display: grid; grid-template-columns: repeat(2, 1fr);
#     gap: 0.45rem; margin-bottom: 0.8rem;
# }
# .param-box {
#     border: 1px solid #e5e7eb; border-radius: 8px;
#     padding: 0.6rem 0.75rem; background: #fafafa;
# }
# .param-label { font-size: 0.62rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; }
# .param-value { font-size: 0.86rem; font-weight: 600; color: #111827; margin-top: 0.1rem; }
# /* ── FEATURES ── */
# .feat-item {
#     display: flex; align-items: flex-start; gap: 0.5rem;
#     margin-bottom: 0.35rem;
# }
# .feat-check { color: #16a34a; font-size: 0.85rem; margin-top: 1px; flex-shrink: 0; }
# .feat-text { font-size: 0.8rem; color: #374151; line-height: 1.45; }
# /* ── DIVIDER ── */
# .divider {
#     border: none; border-top: 1px solid #e5e7eb;
#     margin: 1.8rem 0;
# }
# /* ── ALT SECTION HEADER ── */
# .alt-header {
#     display: flex; align-items: center; gap: 0.9rem;
#     margin-bottom: 1rem;
# }
# .alt-header-title {
#     font-size: 1rem; font-weight: 700; color: #111827;
#     white-space: nowrap;
# }
# .alt-header-line { flex: 1; height: 1px; background: #e5e7eb; }
# .alt-header-count {
#     font-size: 0.72rem; color: #9ca3af; white-space: nowrap;
# }
# /* ── ALT CARD ── */
# .alt-card {
#     border: 1px solid #e5e7eb;
#     border-radius: 12px;
#     padding: 1.1rem;
#     background: #fff;
#     height: 100%;
#     transition: box-shadow 0.15s;
# }
# .alt-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.07); }
# .alt-card.best { border: 2px solid #111827; }
# .alt-rank-tag {
#     display: inline-flex; align-items: center; gap: 0.25rem;
#     font-size: 0.65rem; font-weight: 700;
#     padding: 0.18rem 0.55rem; border-radius: 20px;
#     margin-bottom: 0.55rem;
#     text-transform: uppercase; letter-spacing: 0.06em;
# }
# .tag-best    { background: #111827; color: #fff; }
# .tag-value   { background: #fef9c3; color: #854d0e; }
# .tag-premium { background: #f5f3ff; color: #5b21b6; }
# .alt-name {
#     font-size: 0.9rem; font-weight: 700; color: #111827;
#     line-height: 1.3; margin-bottom: 0.2rem;
# }
# .alt-brand { font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; }
# .alt-price { font-size: 1.1rem; font-weight: 800; color: #111827; }
# .alt-price-note {
#     font-size: 0.72rem; font-weight: 600;
#     color: #16a34a; margin-top: 0.15rem;
# }
# .alt-price-note.higher { color: #dc2626; }
# .alt-stock {
#     font-size: 0.7rem; color: #16a34a; font-weight: 600;
#     margin: 0.35rem 0 0.7rem;
# }
# /* ── 3 POINTS ── */
# .points-label {
#     font-size: 0.62rem; font-weight: 700;
#     text-transform: uppercase; letter-spacing: 0.08em;
#     color: #9ca3af; margin: 0.65rem 0 0.4rem;
#     border-top: 1px solid #f3f4f6; padding-top: 0.65rem;
# }
# .point-row {
#     display: flex; align-items: flex-start; gap: 0.45rem;
#     margin-bottom: 0.4rem;
# }
# .point-num {
#     width: 17px; height: 17px; border-radius: 50%;
#     background: #f3f4f6; color: #6b7280;
#     font-size: 0.6rem; font-weight: 700;
#     display: flex; align-items: center; justify-content: center;
#     flex-shrink: 0; margin-top: 1px;
# }
# .point-text { font-size: 0.78rem; color: #374151; line-height: 1.5; }
# /* ── COLORS ── */
# .color-chip {
#     display: inline-block;
#     font-size: 0.67rem; color: #374151;
#     background: #f3f4f6; border: 1px solid #e5e7eb;
#     border-radius: 20px; padding: 0.12rem 0.45rem;
#     margin: 0.15rem 0.15rem 0 0;
# }
# /* ── FAQ ── */
# .faq-section { margin-top: 2.5rem; }
# .faq-header-row {
#     display: flex; align-items: flex-start;
#     justify-content: space-between; gap: 2rem;
#     margin-bottom: 2rem;
# }
# .faq-header-left { flex: 1; }
# .faq-eyebrow {
#     font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
#     text-transform: uppercase; color: #2563eb; margin-bottom: 0.5rem;
# }
# .faq-main-title {
#     font-size: 1.5rem; font-weight: 800; color: #111827;
#     line-height: 1.25; margin-bottom: 0.5rem;
# }
# .faq-subtitle {
#     font-size: 0.83rem; color: #6b7280; line-height: 1.6; max-width: 480px;
# }
# .faq-contact-box {
#     background: #f9fafb; border: 1px solid #e5e7eb;
#     border-radius: 12px; padding: 1.1rem 1.3rem;
#     min-width: 220px; max-width: 260px;
# }
# .faq-contact-title { font-size: 0.8rem; font-weight: 700; color: #111827; margin-bottom: 0.3rem; }
# .faq-contact-text { font-size: 0.72rem; color: #6b7280; line-height: 1.55; }
# .faq-contact-link {
#     display: inline-block; margin-top: 0.6rem;
#     font-size: 0.72rem; font-weight: 600; color: #2563eb;
#     text-decoration: none;
# }
# .faq-group { margin-bottom: 0.25rem; }
# .faq-group-label {
#     font-size: 0.6rem; font-weight: 800; letter-spacing: 0.12em;
#     text-transform: uppercase; color: #d1d5db;
#     padding: 1.2rem 0 0.4rem;
#     display: flex; align-items: center; gap: 0.5rem;
# }
# .faq-group-label::after {
#     content: ''; flex: 1; height: 1px; background: #f3f4f6;
# }
# .faq-item { border-bottom: 1px solid #f3f4f6; }
# .faq-q-row {
#     display: flex; align-items: center; gap: 0.75rem;
#     padding: 0.95rem 0; cursor: pointer;
# }
# .faq-q-icon {
#     width: 28px; height: 28px; border-radius: 7px;
#     background: #f9fafb; border: 1px solid #e5e7eb;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 0.8rem; flex-shrink: 0;
# }
# .faq-q-text {
#     font-size: 0.87rem; font-weight: 600; color: #111827;
#     flex: 1; line-height: 1.4;
# }
# .faq-q-chevron { font-size: 0.7rem; color: #9ca3af; flex-shrink: 0; }
# .faq-a {
#     font-size: 0.82rem; color: #4b5563;
#     line-height: 1.7; padding: 0 0 1rem 2.5rem;
# }
# .faq-a strong { color: #111827; }
# .faq-a ul { margin: 0.5rem 0 0 1rem; }
# .faq-a li { margin-bottom: 0.25rem; }
# /* ── FOOTER ── */
# .footer {
#     border-top: 1px solid #e5e7eb;
#     padding-top: 1.5rem; margin-top: 3rem;
#     display: flex; justify-content: space-between; align-items: center;
# }
# .footer-text { font-size: 0.72rem; color: #9ca3af; }
# #MainMenu, footer, header { visibility: hidden; }
# div[data-testid="stExpander"] {
#     border: none !important;
#     border-bottom: 1px solid #f3f4f6 !important;
#     border-radius: 0 !important;
#     background: transparent !important;
# }
# div[data-testid="stExpander"] summary {
#     font-size: 0.87rem !important;
#     font-weight: 600 !important;
#     color: #111827 !important;
#     padding: 0.95rem 0 !important;
# }
# div[data-testid="stExpander"] summary:hover {
#     color: #2563eb !important;
# }
# .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
#     background: #ffffff !important;
#     color: #111827 !important;
# }
# .stMarkdown, .stMarkdown p, .stText, label {
#     color: #111827 !important;
# }
# .faq-header-row { margin-bottom: 0.75rem !important; }
# .faq-header-left { max-width: 520px !important; }
# .faq-eyebrow {
#     font-size: 0.6rem !important;
#     color: #2563eb !important;
#     margin-bottom: 0.3rem !important;
# }
# .faq-main-title {
#     font-size: 1rem !important;
#     color: #0f172a !important;
#     margin-bottom: 0.25rem !important;
# }
# .faq-subtitle {
#     font-size: 0.68rem !important;
#     color: #4b5563 !important;
#     line-height: 1.45 !important;
#     max-width: 420px !important;
# }
# div[data-testid="stExpander"] {
#     border: 1px solid #dbe3ef !important;
#     border-radius: 8px !important;
#     background: #ffffff !important;
#     margin-bottom: 0.35rem !important;
#     box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
#     overflow: hidden !important;
# }
# div[data-testid="stExpander"] summary {
#     font-size: 0.76rem !important;
#     font-weight: 700 !important;
#     color: #0f172a !important;
#     padding: 0.46rem 0.68rem !important;
#     background: #ffffff !important;
# }
# div[data-testid="stExpander"] summary:hover {
#     color: #2563eb !important;
#     background: #f8fafc !important;
# }
# div[data-testid="stExpander"] summary p {
#     color: #0f172a !important;
#     font-size: 0.76rem !important;
#     font-weight: 700 !important;
# }
# div[data-testid="stExpanderDetails"] {
#     background: #ffffff !important;
#     padding: 0 0.68rem 0.55rem !important;
# }
# div[data-testid="stExpanderDetails"] p,
# div[data-testid="stExpanderDetails"] li,
# .faq-a {
#     color: #374151 !important;
#     font-size: 0.71rem !important;
#     line-height: 1.55 !important;
#     padding-left: 0 !important;
# }
# div[data-testid="stExpander"] svg {
#     color: #334155 !important;
#     fill: #334155 !important;
# }
# /* ── FIX: constrain alt card image height so it stays consistent ── */
# .alt-img-wrap {
#     width: 100%;
#     aspect-ratio: 1 / 1;
#     overflow: hidden;
#     border-radius: 8px;
#     margin-bottom: 0.75rem;
#     background: #f9fafb;
#     display: flex;
#     align-items: center;
#     justify-content: center;
# }
# .alt-img-wrap img {
#     width: 100%;
#     height: 100%;
#     object-fit: cover;
# }
# </style>
# """, unsafe_allow_html=True)

# # ── Load ──────────────────────────────────────────────────────────────────────
# @st.cache_resource(show_spinner=False)
# def load_assets():
#     idx = faiss.read_index(INDEX_PATH)
#     with open(META_PATH, "rb") as f:
#         recs = pickle.load(f)
#     base = faiss.downcast_index(idx.index) if hasattr(idx, "index") else faiss.downcast_index(idx)
#     vecs = faiss.rev_swig_ptr(base.get_xb(), base.ntotal * base.d).reshape(base.ntotal, base.d).copy()
#     return idx, recs, vecs

# @st.cache_resource(show_spinner=False)
# def load_db():
#     if os.path.exists(DB_PATH):
#         with open(DB_PATH) as f:
#             return json.load(f)
#     return {}

# @st.cache_resource(show_spinner=False)
# def get_groq_client():
#     key = os.getenv("GROQ_API_KEY", "")
#     if not key:
#         return None
#     return Groq(api_key=key)

# index, records, vectors = load_assets()
# db = load_db()
# groq_client = get_groq_client()

# # ── Helpers ───────────────────────────────────────────────────────────────────
# def avail(r):
#     return bool(r.get("is_in_stock")) and float(r.get("quantity", 0) or 0) > 0

# def money(v):
#     try:
#         value = float(v or 0)
#         return f"${value:,.0f}" if value == int(value) else f"${value:,.2f}"
#     except:
#         return "—"

# def pct_off(o, c):
#     try:
#         o, c = float(o), float(c)
#         if o > c > 0:
#             return f"{int((o - c) / o * 100)}% off"
#     except:
#         pass
#     return ""

# def price_diff(ap, cp):
#     try:
#         a, c = float(ap), float(cp)
#         if a <= 0 or c <= 0:
#             return "", ""
#         d = c - a
#         p = abs(d) / a * 100
#         if abs(d) < 0.5:
#             return "Same price", "same"
#         return f"{p:.0f}% {'cheaper' if d < 0 else 'more expensive'}", "cheaper" if d < 0 else "higher"
#     except:
#         return "", ""

# def clean_cat(v):
#     return str(v or "").strip() or "Other"

# def short(v, n=140):
#     t = " ".join(str(v or "").split())
#     return t[:n - 3].rsplit(" ", 1)[0] + "..." if len(t) > n else t

# def feat_lines(text, n=4):
#     return [p.strip() for p in str(text or "").replace("\n", "|").split("|") if p.strip()][:n]

# def plabel(r):
#     return f"{r['product_name']}  ·  {r['brand']}  ·  {money(r['price'])}"

# # ── Search ────────────────────────────────────────────────────────────────────
# def strict_ok(c, a, mode):
#     if not avail(c): return False
#     if c["product_id"] == a["product_id"]: return False
#     if c["product_type"] != a["product_type"]: return False
#     if c["gender"] != a["gender"]: return False
#     ap = float(a.get("price", 0) or 0)
#     if ap > 0:
#         cp = float(c.get("price", 0) or 0)
#         if not (ap * (1 - PRICE_BAND) <= cp <= ap * (1 + PRICE_BAND)): return False
#     if mode == "same" and c["brand"] != a["brand"]: return False
#     if mode == "diff" and c["brand"] == a["brand"]: return False
#     return True

# def relaxed_ok(c, a, mode):
#     """Pass 2: widen price band to 50%, require only gender OR product_type to match."""
#     if not avail(c): return False
#     if c["product_id"] == a["product_id"]: return False
#     ap = float(a.get("price", 0) or 0)
#     if ap > 0:
#         cp = float(c.get("price", 0) or 0)
#         if not (ap * 0.5 <= cp <= ap * 1.5): return False
#     if mode == "same" and c["brand"] != a["brand"]: return False
#     if mode == "diff" and c["brand"] == a["brand"]: return False
#     return c["gender"] == a["gender"] or c["product_type"] == a["product_type"]

# def last_resort_ok(c, a, mode):
#     """Pass 3: only brand-mode + 50% price band — ignore type/gender entirely."""
#     if not avail(c): return False
#     if c["product_id"] == a["product_id"]: return False
#     ap = float(a.get("price", 0) or 0)
#     if ap > 0:
#         cp = float(c.get("price", 0) or 0)
#         if not (ap * 0.5 <= cp <= ap * 1.5): return False
#     if mode == "same" and c["brand"] != a["brand"]: return False
#     if mode == "diff" and c["brand"] == a["brand"]: return False
#     return True

# def find_alts(aidx, mode):
#     anchor = records[aidx]
#     vec = vectors[aidx:aidx + 1].astype("float32")
#     scores, ids = index.search(vec, SEARCH_K)
#     results, brands = [], defaultdict(int)

#     # ── Pass 1: strict (same type + gender + 30% price) ──
#     for score, rid in zip(scores[0], ids[0]):
#         if rid < 0 or rid >= len(records): continue
#         c = records[int(rid)]
#         if not strict_ok(c, anchor, mode): continue
#         if mode == "diff":
#             if brands[c["brand"]] >= MAX_PER_BRAND: continue
#             brands[c["brand"]] += 1
#         results.append((c, False))
#         if len(results) >= MAX_ALTS:
#             return results, False

#     # ── Pass 2: relaxed (gender OR type, 50% price band) ──
#     seen = {r[0]["product_id"] for r in results}
#     for score, rid in zip(scores[0], ids[0]):
#         if rid < 0 or rid >= len(records): continue
#         c = records[int(rid)]
#         if c["product_id"] in seen: continue
#         if not relaxed_ok(c, anchor, mode): continue
#         results.append((c, True))
#         seen.add(c["product_id"])
#         if len(results) >= MAX_ALTS:
#             break

#     # ── Pass 3: last resort (brand-mode only, ignore type/gender) ──
#     if len(results) < MAX_ALTS:
#         for score, rid in zip(scores[0], ids[0]):
#             if rid < 0 or rid >= len(records): continue
#             c = records[int(rid)]
#             if c["product_id"] in seen: continue
#             if not last_resort_ok(c, anchor, mode): continue
#             results.append((c, True))
#             seen.add(c["product_id"])
#             if len(results) >= MAX_ALTS:
#                 break

#     return results, any(r[1] for r in results)

# # ── LLM points ────────────────────────────────────────────────────────────────
# def get_points(anchor, alts, mode):
#     cache_key = f"pts_{anchor['product_id']}_{mode}"
#     if cache_key in db:
#         return db[cache_key]
#     if not groq_client:
#         result = {}
#         for i, (c, _) in enumerate(alts):
#             feats = feat_lines(c.get("key_features", ""), 3)
#             note, _ = price_diff(anchor["price"], c["price"])
#             result[f"alt_{i + 1}"] = [
#                 feats[0] if feats else f"Shares the same {c['product_type'].lower()} construction and intended use case as your selected product",
#                 note if note else f"Priced similarly to your pick — {c['brand']} positions this as a direct category equivalent",
#                 f"A practical swap for {c['gender'].lower()} shoppers who want a ready-to-ship option without compromising on build quality",
#             ]
#         return result

#     cands_text = "\n".join([
#         f"Alternative {i + 1}:\n"
#         f"  Name: {c['product_name']}\n"
#         f"  Brand: {c['brand']}\n"
#         f"  Price: {money(c['price'])}\n"
#         f"  Gender: {c['gender']}\n"
#         f"  Type: {c['product_type']}\n"
#         f"  Key Features: {short(c.get('key_features', ''), 250)}\n"
#         f"  Colors: {', '.join(c.get('colors', [])[:3]) or 'N/A'}"
#         for i, (c, _) in enumerate(alts)
#     ])

#     prompt = f"""You are a senior product specialist at APeak, a premium outdoor apparel and gear retailer. A customer has selected a product and wants to know which alternatives are genuinely worth considering.

# CUSTOMER'S SELECTED PRODUCT:
#   Name: {anchor['product_name']}
#   Brand: {anchor['brand']}
#   Type: {anchor['product_type']}
#   Gender: {anchor['gender']}
#   Price: {money(anchor['price'])}
#   Key Features: {short(anchor.get('key_features', ''), 300)}
#   Colors: {', '.join(anchor.get('colors', [])[:4]) or 'N/A'}

# ALTERNATIVES TO EVALUATE ({len(alts)} total, {"same brand lineup" if mode == "same" else "cross-brand comparison"}):
# {cands_text}

# Your job: For EACH alternative, write exactly 3 punchy, specific sentences a knowledgeable store associate would say to a customer standing in front of them.

# Sentence 1 — THE MATCH: What specific construction detail, technology, or feature makes this a legitimate substitute? Name the actual spec (fabric weight, waterproof rating, insulation type, sole tech, etc.) if it appears in the features. Don't say "similar product" — say WHY it's similar.
# Sentence 2 — THE DIFFERENCE: One concrete, meaningful way this product diverges from the selected item — could be price, a specific material upgrade or downgrade, a fit difference (slim vs relaxed), a technology trade-off, or a use-case nuance. Be direct. Numbers help ("$8 less", "200g lighter", "rated to -10°C vs -5°C").
# Sentence 3 — THE BUYER: Name the exact type of customer or scenario this alternative is best for. Be specific ("ideal for casual hikers who want warmth on day treks without the bulk of a puffer jacket", not "a good choice for outdoor enthusiasts").

# Rules:
# - Never use vague phrases like "great alternative", "similar quality", "worth considering", or "good option"
# - Never repeat information already obvious from the product name or brand
# - If features data is thin, infer intelligently from the product type and price point — don't leave sentences generic
# - Sound like a trusted expert, not a marketing copywriter

# Return ONLY valid JSON (no markdown, no preamble, no trailing text):
# {{"alt_1":["sentence 1","sentence 2","sentence 3"],"alt_2":["sentence 1","sentence 2","sentence 3"],"alt_3":["sentence 1","sentence 2","sentence 3"]}}"""

#     try:
#         resp = groq_client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=[
#                 {"role": "system", "content": "You are a helpful retail product expert. Return valid JSON only. No markdown, no preamble, no explanation — just the JSON object."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=900, temperature=0.35
#         )
#         raw = resp.choices[0].message.content.strip()
#         if "```" in raw:
#             for p in raw.split("```"):
#                 if "{" in p:
#                     raw = p.strip()
#                     break
#         if raw.lower().startswith("json"):
#             raw = raw[4:].strip()
#         if "{" in raw and "}" in raw:
#             raw = raw[raw.index("{"):raw.rindex("}") + 1]
#         result = json.loads(raw)
#         db[cache_key] = result
#         try:
#             with open(DB_PATH, "w") as f:
#                 json.dump(db, f, indent=2)
#         except:
#             pass
#         return result
#     except Exception as e:
#         result = {}
#         for i, (c, _) in enumerate(alts):
#             feats = feat_lines(c.get("key_features", ""), 3)
#             note, _ = price_diff(anchor["price"], c["price"])
#             result[f"alt_{i + 1}"] = [
#                 feats[0] if feats else f"Built on the same {c['product_type'].lower()} platform — shares the core construction DNA with your selected product",
#                 note if note else f"{c['brand']} takes a slightly different design approach, with distinct colorways and branding details",
#                 f"Best suited for {c['gender'].lower()} shoppers who need a confirmed in-stock option in the same category",
#             ]
#         return result

# # ══════════════════════════════════════════════════════════════════
# # PAGE
# # ══════════════════════════════════════════════════════════════════

# # navbar
# st.markdown("""
# <div class="navbar">
#   <div class="nav-logo">A<span>Peak</span></div>
#   <div class="nav-links">
#     <span class="nav-link">All Products</span>
#     <span class="nav-link">Categories</span>
#     <span class="nav-link">Brands</span>
#     <span class="nav-link">Sale</span>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # selectors
# avail_idx = [i for i, r in enumerate(records) if avail(r)]
# cats = sorted({clean_cat(records[i]["main_category"]) for i in avail_idx})
# c1, c2 = st.columns([1, 2.2])
# with c1:
#     sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
# with c2:
#     cat_idx = sorted(
#         [i for i in avail_idx if clean_cat(records[i]["main_category"]) == sel_cat],
#         key=lambda i: (records[i]["product_type"], records[i]["brand"], records[i]["product_name"])
#     )
#     sel_idx = st.selectbox("Product", cat_idx, format_func=lambda i: plabel(records[i]), label_visibility="collapsed")

# anchor = records[sel_idx]

# # breadcrumb
# st.markdown(f"""
# <div class="breadcrumb">
#   Home · {anchor['main_category']} · {anchor['product_type']} · <span>{anchor['product_name']}</span>
# </div>
# """, unsafe_allow_html=True)

# # ── main product section ──────────────────────────────────────────
# img_col, info_col = st.columns([1, 1.4], gap="large")

# with img_col:
#     if anchor.get("image_url"):
#         st.image(anchor["image_url"], use_container_width=True)
#     else:
#         st.markdown("""<div style="height:300px;background:#f9fafb;border:1px solid #e5e7eb;
#         border-radius:12px;display:flex;align-items:center;justify-content:center;
#         font-size:4rem;">🏷️</div>""", unsafe_allow_html=True)

# with info_col:
#     st.markdown(f'<div class="product-type-pill">{anchor["product_type"]}</div>', unsafe_allow_html=True)
#     st.markdown(f'<div class="product-title">{anchor["product_name"]}</div>', unsafe_allow_html=True)
#     st.markdown(f'<div class="product-brand">by <strong>{anchor["brand"]}</strong> &nbsp;·&nbsp; {anchor["gender"]} &nbsp;·&nbsp; {anchor["main_category"]}</div>', unsafe_allow_html=True)

#     orig = anchor.get("original_price", 0)
#     curr = anchor.get("price", 0)
#     off  = pct_off(orig, curr)
#     st.markdown(f"""
#     <div style="margin:0.5rem 0 0.3rem;display:flex;align-items:baseline;flex-wrap:wrap;gap:0.3rem;">
#       <span class="price-main">{money(curr)}</span>
#       {"<span class='price-orig'>" + money(orig) + "</span>" if off else ""}
#       {"<span class='price-off'>" + off + "</span>" if off else ""}
#     </div>
#     """, unsafe_allow_html=True)

#     if avail(anchor):
#         st.markdown(f'<div class="stock-badge"><div class="stock-dot"></div>In Stock &nbsp;·&nbsp; {int(float(anchor.get("quantity", 0)))} units available</div>', unsafe_allow_html=True)

#     st.markdown('<div class="param-title">Product Details</div>', unsafe_allow_html=True)
#     cols_html = ", ".join(anchor.get("colors", [])[:4]) or "—"
#     st.markdown(f"""
#     <div class="param-grid">
#       <div class="param-box"><div class="param-label">Brand</div><div class="param-value">{anchor['brand']}</div></div>
#       <div class="param-box"><div class="param-label">Gender</div><div class="param-value">{anchor['gender']}</div></div>
#       <div class="param-box"><div class="param-label">SKU</div><div class="param-value" style="font-size:0.75rem">{anchor['sku']}</div></div>
#       <div class="param-box"><div class="param-label">Available Colors</div><div class="param-value" style="font-size:0.77rem">{cols_html}</div></div>
#     </div>
#     """, unsafe_allow_html=True)

#     feats = feat_lines(anchor.get("key_features", ""), 5)
#     if feats:
#         st.markdown('<div class="param-title">Key Features</div>', unsafe_allow_html=True)
#         items = "".join(f'<div class="feat-item"><span class="feat-check">✓</span><span class="feat-text">{f}</span></div>' for f in feats)
#         st.markdown(items, unsafe_allow_html=True)

#     if anchor.get("product_url"):
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.link_button("View Full Product →", anchor["product_url"])

# # ── ALTERNATIVES ──────────────────────────────────────────────────
# st.markdown('<hr class="divider">', unsafe_allow_html=True)

# if "mode" not in st.session_state:
#     st.session_state.mode = "same"

# st.markdown('<div style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:0.75rem;">Compare With Best Alternatives</div>', unsafe_allow_html=True)

# b1, b2, _ = st.columns([1, 1, 3])
# with b1:
#     if st.button("🔁  Same Brand", use_container_width=True,
#                  type="primary" if st.session_state.mode == "same" else "secondary"):
#         st.session_state.mode = "same"
#         st.rerun()
# with b2:
#     if st.button("🔀  Different Brand", use_container_width=True,
#                  type="primary" if st.session_state.mode == "diff" else "secondary"):
#         st.session_state.mode = "diff"
#         st.rerun()

# st.markdown("<br>", unsafe_allow_html=True)

# alts, has_fallback = find_alts(sel_idx, st.session_state.mode)

# if alts:
#     mode_label = "Same Brand" if st.session_state.mode == "same" else "Different Brand"
#     st.markdown(f"""
#     <div class="alt-header">
#       <div class="alt-header-title">Your Pick vs {len(alts)} Best {mode_label} Alternative{"s" if len(alts) > 1 else ""}</div>
#       <div class="alt-header-line"></div>
#       <div class="alt-header-count">Showing {len(alts)} of {MAX_ALTS} max</div>
#     </div>
#     """, unsafe_allow_html=True)

#     with st.spinner("Generating comparison..."):
#         pts = get_points(anchor, alts, st.session_state.mode)

#     tags     = ["Best Overall", "Best Value", "Premium Pick"]
#     tag_cls  = ["tag-best", "tag-value", "tag-premium"]
#     tag_icon = ["⭐", "💰", "👑"]

#     # ── FIX: always render 3 columns so images stay the same size ──
#     cols = st.columns(3, gap="medium")

#     for i, (cand, fallback) in enumerate(alts):
#         with cols[i]:
#             card_cls  = "alt-card best" if i == 0 else "alt-card"
#             tag_label = tags[i] if i < 3 else "Alternative"
#             tcls      = tag_cls[i] if i < 3 else "tag-best"
#             ticon     = tag_icon[i] if i < 3 else "⭐"
#             note, ncls = price_diff(anchor["price"], cand["price"])
#             points_list = pts.get(f"alt_{i + 1}", [])

#             # image — wrapped in a square aspect-ratio container for consistent sizing
#             if cand.get("image_url"):
#                 st.markdown(
#                     f'<div class="alt-img-wrap"><img src="{cand["image_url"]}" /></div>',
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     '<div class="alt-img-wrap" style="font-size:2rem;">🏷️</div>',
#                     unsafe_allow_html=True
#                 )

#             colors_chips = "".join(f'<span class="color-chip">{c}</span>' for c in cand.get("colors", [])[:3])
#             points_html  = ""
#             if points_list:
#                 rows = "".join(
#                     f'<div class="point-row"><div class="point-num">{j + 1}</div><div class="point-text">{p}</div></div>'
#                     for j, p in enumerate(points_list[:3])
#                 )
#                 points_html = f'<div class="points-label">Why this alternative</div>{rows}'

#             note_html = f'<div class="alt-price-note {ncls}">{note}</div>' if note else ""

#             st.markdown(f"""
#             <div class="{card_cls}">
#               <span class="alt-rank-tag {tcls}">{ticon} {tag_label}</span>
#               <div class="alt-name">{cand['product_name']}</div>
#               <div class="alt-brand">{cand['brand']} &nbsp;·&nbsp; {cand['product_type']}</div>
#               <div class="alt-price">{money(cand['price'])}</div>
#               {note_html}
#               <div class="alt-stock">✓ In Stock &nbsp;·&nbsp; {int(float(cand.get('quantity', 0)))} units</div>
#               {"<div>" + colors_chips + "</div>" if colors_chips else ""}
#               {points_html}
#             </div>
#             """, unsafe_allow_html=True)

#             if cand.get("product_url"):
#                 st.link_button("View Product", cand["product_url"], use_container_width=True)

# else:
#     st.markdown("""
#     <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;
#     padding:2rem;text-align:center;">
#       <div style="font-size:1.5rem;margin-bottom:0.5rem">🔍</div>
#       <div style="font-size:0.88rem;color:#374151;font-weight:600;margin-bottom:0.3rem">
#         No alternatives found right now
#       </div>
#       <div style="font-size:0.78rem;color:#9ca3af">
#         Try switching between Same Brand and Different Brand, or select another product.
#       </div>
#     </div>
#     """, unsafe_allow_html=True)

# # ── FAQs ──────────────────────────────────────────────────────────
# st.markdown('<hr class="divider">', unsafe_allow_html=True)
# st.markdown("""
# <div class="faq-header-row">
#   <div class="faq-header-left">
#     <div class="faq-eyebrow">FAQ</div>
#     <div class="faq-main-title">Quick Questions</div>
#     <div class="faq-subtitle">
#       Simple answers before you compare or open a product page.
#     </div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# faqs = [
#     ("Are these alternatives in stock?",
#      """Yes. Products shown here are filtered to include only items currently marked in stock."""),
#     ("How close are the prices?",
#      """Alternatives stay within <strong>30%</strong> of the selected product price, so the comparison remains useful."""),
#     ("Can I choose a size or color here?",
#      """Use <strong>View Product</strong> to open the product page and select available sizes, colors, and quantity."""),
#     ("Why do some products cost less?",
#      """A lower price can come from brand, color, sale status, or small feature differences. Check the comparison notes before choosing."""),
#     ("Can I return an alternative?",
#      """Returns follow the store policy shown on the product page. Please review it before checkout."""),
# ]

# for q, a in faqs:
#     with st.expander(q):
#         st.markdown(f'<div class="faq-a">{a}</div>', unsafe_allow_html=True)

# # footer
# st.markdown("""
# <div class="footer">
#   <div class="footer-text">© 2025 APeak · Powered by FAISS + BAAI/bge-base-en-v1.5 + Groq LLaMA 3.1</div>
#   <div class="footer-text">All alternatives confirmed in-stock at time of search</div>
# </div>
# """, unsafe_allow_html=True)




import pickle, os, json
from collections import defaultdict
import faiss, numpy as np
import streamlit as st
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

st.set_page_config(page_title="APeak Alternatives", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #ffffff; color: #111827; }
.block-container { padding: 0 2rem 3rem; max-width: 1260px; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background: #ffffff !important; color: #111827 !important; }
.stMarkdown, .stMarkdown p, .stText, label { color: #111827 !important; }
/* NAV */
.navbar { background:#fff; border-bottom:1px solid #e5e7eb; padding:0.9rem 0; margin-bottom:1.8rem; display:flex; align-items:center; justify-content:space-between; }
.nav-logo { font-size:1.15rem; font-weight:800; color:#111827; letter-spacing:-0.02em; }
.nav-logo span { color:#2563eb; }
.nav-links { display:flex; gap:1.5rem; }
.nav-link { font-size:0.8rem; color:#6b7280; font-weight:500; cursor:pointer; }
/* BREADCRUMB */
.breadcrumb { font-size:0.73rem; color:#9ca3af; margin-bottom:1.2rem; }
.breadcrumb span { color:#111827; font-weight:500; }
/* PRODUCT HERO */
.product-type-pill { display:inline-block; background:#f0f9ff; color:#0369a1; font-size:0.68rem; font-weight:700; padding:0.18rem 0.6rem; border-radius:20px; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.6rem; }
.product-title { font-size:1.3rem; font-weight:800; color:#111827; line-height:1.3; margin-bottom:0.3rem; }
.product-brand { font-size:0.82rem; color:#6b7280; margin-bottom:0.8rem; }
.price-main { font-size:1.8rem; font-weight:800; color:#111827; }
.price-orig { font-size:0.95rem; color:#9ca3af; text-decoration:line-through; margin-left:0.5rem; }
.price-off { font-size:0.8rem; font-weight:700; color:#fff; background:#16a34a; padding:0.15rem 0.45rem; border-radius:4px; margin-left:0.5rem; }
.stock-badge { display:inline-flex; align-items:center; gap:0.3rem; font-size:0.75rem; font-weight:600; color:#16a34a; margin:0.5rem 0 1rem; }
.stock-dot { width:7px; height:7px; background:#16a34a; border-radius:50%; }
.param-title { font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:0.09em; color:#9ca3af; margin:1.1rem 0 0.5rem; }
.param-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:0.45rem; margin-bottom:0.8rem; }
.param-box { border:1px solid #e5e7eb; border-radius:8px; padding:0.6rem 0.75rem; background:#fafafa; }
.param-label { font-size:0.62rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.05em; }
.param-value { font-size:0.86rem; font-weight:600; color:#111827; margin-top:0.1rem; }
.feat-item { display:flex; align-items:flex-start; gap:0.5rem; margin-bottom:0.35rem; }
.feat-check { color:#16a34a; font-size:0.85rem; margin-top:1px; flex-shrink:0; }
.feat-text { font-size:0.8rem; color:#374151; line-height:1.45; }
.divider { border:none; border-top:1px solid #e5e7eb; margin:1.8rem 0; }
/* RFY BOX */
.rfy-box { background:#faf5ff; border:1.5px solid #d8b4fe; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1.25rem; }
.rfy-title { font-size:0.65rem; font-weight:800; text-transform:uppercase; letter-spacing:0.12em; color:#7c3aed; margin-bottom:0.65rem; display:flex; align-items:center; gap:0.4rem; }
.rfy-row { display:flex; align-items:flex-start; gap:0.5rem; margin-bottom:0.45rem; }
.rfy-arrow { color:#7c3aed; font-size:0.72rem; margin-top:2px; flex-shrink:0; }
.rfy-text { font-size:0.8rem; color:#374151; line-height:1.5; }
.rfy-text strong { color:#111827; }
.rfy-text em { color:#6b7280; font-style:normal; }
/* SECTION META */
.section-meta { font-size:0.68rem; color:#9ca3af; font-weight:600; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.5rem; }
/* ANCHOR ROW */
.anchor-row { display:flex; align-items:center; background:#f0f9ff; border:1px solid #bfdbfe; border-radius:10px 10px 0 0; padding:0.7rem 1rem; gap:1rem; }
.anchor-name-block { flex:2; min-width:0; }
.anchor-name { font-size:0.88rem; font-weight:700; color:#111827; }
.anchor-sub { font-size:0.68rem; color:#6b7280; margin-top:0.1rem; }
.anchor-badge { display:inline-block; font-size:0.56rem; font-weight:700; padding:0.1rem 0.4rem; border-radius:20px; background:#dbeafe; color:#1d4ed8; text-transform:uppercase; letter-spacing:0.06em; margin-left:0.4rem; vertical-align:middle; }
.anchor-price { flex:0 0 auto; font-size:0.95rem; font-weight:800; color:#111827; }
/* PARAM PILLS */
.param-pill-row { display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap; flex:3; }
.ppill { display:flex; align-items:center; gap:0.22rem; }
.ppill-icon { font-size:0.72rem; color:#9ca3af; }
.ppill-val { font-size:0.74rem; color:#374151; font-weight:500; }
.ppill-val.green { color:#16a34a; font-weight:600; }
/* ALT ROW */
.alt-row-wrap { border:1px solid #e5e7eb; border-top:none; background:#fff; transition:background 0.12s; }
.alt-row-wrap:last-child { border-radius:0 0 10px 10px; }
.alt-row-wrap:hover { background:#fafbfc; }
.alt-row-wrap.alt-highlighted { background:#faf5ff; border-left:3px solid #7c3aed; }
.alt-row { display:flex; align-items:center; padding:0.75rem 1rem; gap:1rem; cursor:default; }
.alt-img { width:60px; height:60px; object-fit:cover; border-radius:7px; background:#f9fafb; flex-shrink:0; }
.alt-img-ph { width:60px; height:60px; border-radius:7px; background:#f9fafb; display:flex; align-items:center; justify-content:center; font-size:1.4rem; flex-shrink:0; }
.alt-name-block { flex:0 0 200px; min-width:0; }
.alt-name { font-size:0.84rem; font-weight:700; color:#111827; line-height:1.25; }
.alt-sub { font-size:0.66rem; color:#6b7280; margin-top:0.1rem; }
.alt-badge { display:inline-block; font-size:0.54rem; font-weight:700; padding:0.1rem 0.38rem; border-radius:20px; text-transform:uppercase; letter-spacing:0.06em; vertical-align:middle; margin-left:0.3rem; }
.ab-rec { background:#7c3aed; color:#fff; }
.ab-value { background:#fef9c3; color:#854d0e; }
.ab-premium { background:#f5f3ff; color:#5b21b6; }
.alt-price-block { flex:0 0 90px; }
.alt-price { font-size:0.92rem; font-weight:800; color:#111827; }
.alt-price-note { font-size:0.67rem; font-weight:600; color:#16a34a; margin-top:0.05rem; }
.alt-price-note.higher { color:#dc2626; }
/* FOOTER */
.footer { border-top:1px solid #e5e7eb; padding-top:1.5rem; margin-top:3rem; display:flex; justify-content:space-between; align-items:center; }
.footer-text { font-size:0.72rem; color:#9ca3af; }
/* FAQ */
.faq-eyebrow { font-size:0.6rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#2563eb; margin-bottom:0.3rem; }
.faq-main-title { font-size:1rem; font-weight:800; color:#111827; margin-bottom:0.25rem; }
.faq-subtitle { font-size:0.68rem; color:#4b5563; line-height:1.45; max-width:420px; margin-bottom:0.75rem; }
.faq-a { font-size:0.71rem; color:#374151; line-height:1.55; padding-bottom:0.55rem; }
.faq-a strong { color:#111827; }
#MainMenu, footer, header { visibility:hidden; }
div[data-testid="stExpander"] { border:1px solid #dbe3ef !important; border-radius:8px !important; background:#ffffff !important; margin-bottom:0.35rem !important; box-shadow:0 1px 2px rgba(15,23,42,0.04) !important; overflow:hidden !important; }
div[data-testid="stExpander"] summary { font-size:0.76rem !important; font-weight:700 !important; color:#0f172a !important; padding:0.46rem 0.68rem !important; background:#ffffff !important; }
div[data-testid="stExpander"] summary:hover { color:#2563eb !important; background:#f8fafc !important; }
div[data-testid="stExpander"] summary p { color:#0f172a !important; font-size:0.76rem !important; font-weight:700 !important; }
div[data-testid="stExpanderDetails"] { background:#ffffff !important; padding:0 0.68rem 0.55rem !important; }
div[data-testid="stExpanderDetails"] p, div[data-testid="stExpanderDetails"] li { color:#374151 !important; font-size:0.71rem !important; line-height:1.55 !important; padding-left:0 !important; }
div[data-testid="stExpander"] svg { color:#334155 !important; fill:#334155 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_assets():
    idx = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        recs = pickle.load(f)
    base = faiss.downcast_index(idx.index) if hasattr(idx, "index") else faiss.downcast_index(idx)
    vecs = faiss.rev_swig_ptr(base.get_xb(), base.ntotal * base.d).reshape(base.ntotal, base.d).copy()
    return idx, recs, vecs

@st.cache_resource(show_spinner=False)
def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f:
            return json.load(f)
    return {}

@st.cache_resource(show_spinner=False)
def get_groq_client():
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        return None
    return Groq(api_key=key)

index, records, vectors = load_assets()
db = load_db()
groq_client = get_groq_client()

# ── Helpers ───────────────────────────────────────────────────────
def avail(r):
    return bool(r.get("is_in_stock")) and float(r.get("quantity", 0) or 0) > 0

def money(v):
    try:
        return f"${float(v or 0):,.0f}"
    except:
        return "—"

def pct_off(o, c):
    try:
        o, c = float(o), float(c)
        if o > c > 0:
            return f"{int((o - c) / o * 100)}% off"
    except:
        pass
    return ""

def price_diff_label(ap, cp):
    try:
        a, c = float(ap), float(cp)
        if a <= 0 or c <= 0: return "", ""
        d = c - a
        p = abs(d) / a * 100
        if abs(d) < 0.5: return "Same price", "same"
        return f"{p:.0f}% {'cheaper' if d < 0 else 'costlier'}", "cheaper" if d < 0 else "higher"
    except:
        return "", ""

def clean_cat(v):
    return str(v or "").strip() or "Other"

def short(v, n=140):
    t = " ".join(str(v or "").split())
    return t[:n - 3].rsplit(" ", 1)[0] + "..." if len(t) > n else t

def feat_lines(text, n=4):
    return [p.strip() for p in str(text or "").replace("\n", "|").split("|") if p.strip()][:n]

def plabel(r):
    return f"{r['product_name']}  ·  {r['brand']}  ·  {money(r['price'])}"

# ── Search ────────────────────────────────────────────────────────
def strict_ok(c, a, mode):
    if not avail(c): return False
    if c["product_id"] == a["product_id"]: return False
    if c["product_type"] != a["product_type"]: return False
    if c["gender"] != a["gender"]: return False
    ap = float(a.get("price", 0) or 0)
    if ap > 0:
        cp = float(c.get("price", 0) or 0)
        if not (ap * (1 - PRICE_BAND) <= cp <= ap * (1 + PRICE_BAND)): return False
    if mode == "same" and c["brand"] != a["brand"]: return False
    if mode == "diff" and c["brand"] == a["brand"]: return False
    return True

def relaxed_ok(c, a, mode):
    if not avail(c): return False
    if c["product_id"] == a["product_id"]: return False
    ap = float(a.get("price", 0) or 0)
    if ap > 0:
        cp = float(c.get("price", 0) or 0)
        if not (ap * 0.5 <= cp <= ap * 1.5): return False
    if mode == "same" and c["brand"] != a["brand"]: return False
    if mode == "diff" and c["brand"] == a["brand"]: return False
    return c["gender"] == a["gender"] or c["product_type"] == a["product_type"]

def last_resort_ok(c, a, mode):
    if not avail(c): return False
    if c["product_id"] == a["product_id"]: return False
    ap = float(a.get("price", 0) or 0)
    if ap > 0:
        cp = float(c.get("price", 0) or 0)
        if not (ap * 0.5 <= cp <= ap * 1.5): return False
    if mode == "same" and c["brand"] != a["brand"]: return False
    if mode == "diff" and c["brand"] == a["brand"]: return False
    return True

def find_alts(aidx, mode):
    anchor = records[aidx]
    vec = vectors[aidx:aidx + 1].astype("float32")
    scores, ids = index.search(vec, SEARCH_K)
    results, brands = [], defaultdict(int)
    for score, rid in zip(scores[0], ids[0]):
        if rid < 0 or rid >= len(records): continue
        c = records[int(rid)]
        if not strict_ok(c, anchor, mode): continue
        if mode == "diff":
            if brands[c["brand"]] >= MAX_PER_BRAND: continue
            brands[c["brand"]] += 1
        results.append((c, False))
        if len(results) >= MAX_ALTS:
            return results, False
    seen = {r[0]["product_id"] for r in results}
    for score, rid in zip(scores[0], ids[0]):
        if rid < 0 or rid >= len(records): continue
        c = records[int(rid)]
        if c["product_id"] in seen: continue
        if not relaxed_ok(c, anchor, mode): continue
        results.append((c, True))
        seen.add(c["product_id"])
        if len(results) >= MAX_ALTS: break
    if len(results) < MAX_ALTS:
        for score, rid in zip(scores[0], ids[0]):
            if rid < 0 or rid >= len(records): continue
            c = records[int(rid)]
            if c["product_id"] in seen: continue
            if not last_resort_ok(c, anchor, mode): continue
            results.append((c, True))
            seen.add(c["product_id"])
            if len(results) >= MAX_ALTS: break
    return results, any(r[1] for r in results)

# ── LLM: single "Which is right for you" box ─────────────────────
def get_rfy(anchor, alts, mode):
    cache_key = f"rfy2_{anchor['product_id']}_{mode}"
    if cache_key in db:
        return db[cache_key]

    def fallback():
        out = []
        # one bullet for anchor
        feats_a = feat_lines(anchor.get("key_features", ""), 1)
        out.append({
            "scenario": f"you want to keep your original pick",
            "product": anchor["product_name"],
            "reason": feats_a[0][:50] if feats_a else "your selected product"
        })
        for c, _ in alts:
            note, _ = price_diff_label(anchor["price"], c["price"])
            feats = feat_lines(c.get("key_features", ""), 1)
            out.append({
                "scenario": feats[0][:55] if feats else f"you prefer {c['brand']}",
                "product": c["product_name"],
                "reason": note or "similar specifications"
            })
        return out

    if not groq_client:
        return fallback()

    cands_text = "\n".join([
        f"Alt {i+1}: {c['product_name']} by {c['brand']} · {money(c['price'])} · {short(c.get('key_features',''), 180)}"
        for i, (c, _) in enumerate(alts)
    ])
    mode_ctx = "same-brand lineup" if mode == "same" else "cross-brand alternatives"

    prompt = f"""You are a product advisor at an outdoor apparel store.
Write a "Which is right for you?" decision guide for a customer comparing these products.

SELECTED: {anchor['product_name']} · {anchor['brand']} · {money(anchor['price'])}
Features: {short(anchor.get('key_features',''), 200)}

ALTERNATIVES ({mode_ctx}):
{cands_text}

Write exactly {len(alts) + 1} decision bullets — first one for the anchor product, then one per alternative.

Each bullet must have:
- scenario: starts with "you want" (NOT "if you want") — max 8 words — mention a real feature or need
- product: exact product name from above
- reason: max 7 words — mention a real spec or price difference — use Rs. for prices

Rules:
- Never start scenario with "if" — just "you want..."
- Be specific, not generic
- Use $ currency

Return ONLY a valid JSON array, no markdown:
[{{"scenario":"you want...","product":"exact name","reason":"real spec or price"}}]"""

    try:
        resp = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Return valid JSON array only. No markdown. Use $ for all prices."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500, temperature=0.3
        )
        raw = resp.choices[0].message.content.strip()
        if "```" in raw:
            for p in raw.split("```"):
                if "[" in p: raw = p.strip(); break
        if raw.lower().startswith("json"): raw = raw[4:].strip()
        if "[" in raw and "]" in raw:
            raw = raw[raw.index("["):raw.rindex("]") + 1]
        result = json.loads(raw)

        # fix any stray $ that LLM might have used
        for item in result:
            for key in ["scenario", "reason"]:
                item[key] = item[key].replace("$", "Rs. ")

        db[cache_key] = result
        try:
            with open(DB_PATH, "w") as f:
                json.dump(db, f, indent=2)
        except:
            pass
        return result
    except:
        return fallback()

# ── Render alternatives section ───────────────────────────────────
def render_alternatives(anchor, alts, mode):
    mode_label = "Same Brand" if mode == "same" else "Different Brand"

    # ── 1. RFY box ──
    with st.spinner("Generating recommendation..."):
        rfy = get_rfy(anchor, alts, mode)

    # rfy_rows_html = ""
    # for item in rfy:
    #     scenario = item.get("scenario", "").strip()
    #     # remove any leading "if " to avoid "If if"
    #     if scenario.lower().startswith("if "):
    #         scenario = scenario[3:].strip()
    #     # remove any trailing period
    #     scenario = scenario.rstrip(".")
    #     product  = item.get("product", "")
    #     reason   = item.get("reason", "").replace("$", "Rs. ")

    #     rfy_rows_html += f"""
    #     <div class="rfy-row">
    #       <span class="rfy-arrow">→</span>
    #       <span class="rfy-text">If {scenario} → <strong>{product}</strong> <em>({reason})</em></span>
    #     </div>"""

    rows = ""
    for item in rfy:
        scenario = item.get("scenario", "").strip()
        if scenario.lower().startswith("if "):
            scenario = scenario[3:].strip()
        scenario = scenario.rstrip(".")
        product  = item.get("product", "")
        reason   = item.get("reason", "").replace("$", "Rs. ")
        rows += '<div class="rfy-row"><span class="rfy-arrow">→</span><span class="rfy-text">If ' + scenario + ' → <strong>' + product + '</strong> <em>(' + reason + ')</em></span></div>'

    st.markdown('<div class="rfy-box"><div class="rfy-title">✦ Which is right for you</div>' + rows + '</div>', unsafe_allow_html=True)

    # ── 2. Section label ──
    st.markdown(f"""
    <div class="section-meta">
      Your Pick vs {len(alts)} Best {mode_label} Alternative{"s" if len(alts)>1 else ""}
      &nbsp;·&nbsp; Showing {len(alts)} of {MAX_ALTS} max
    </div>""", unsafe_allow_html=True)

    # ── 3. Anchor "Your Pick" row ──
    feats_a = feat_lines(anchor.get("key_features", ""), 2)
    anchor_feats_html = ""
    for f in feats_a:
        txt = f[:55] + "…" if len(f) > 55 else f
        anchor_feats_html += f'<span class="ppill"><span class="ppill-icon">·</span><span class="ppill-val">{txt}</span></span>'

    colors_a = ", ".join(anchor.get("colors", [])[:2]) or "—"
    qty_a    = int(float(anchor.get("quantity", 0) or 0))

    st.markdown(f"""
    <div class="anchor-row">
      <div style="flex-shrink:0;">
        {"<img style='width:54px;height:54px;object-fit:cover;border-radius:7px;' src='" + anchor['image_url'] + "' />" if anchor.get('image_url') else '<div style="width:54px;height:54px;border-radius:7px;background:#f0f9ff;display:flex;align-items:center;justify-content:center;font-size:1.3rem;">🏷️</div>'}
      </div>
      <div class="anchor-name-block">
        <div class="anchor-name">{anchor['product_name']} <span class="anchor-badge">Your Pick</span></div>
        <div class="anchor-sub">{anchor['brand']} &nbsp;·&nbsp; {anchor['product_type']}</div>
      </div>
      <div class="param-pill-row">
        <span class="ppill"><span class="ppill-icon">🎨</span><span class="ppill-val">{colors_a}</span></span>
        <span class="ppill"><span class="ppill-icon">👤</span><span class="ppill-val">{anchor.get('gender','—')}</span></span>
        <span class="ppill"><span class="ppill-icon ppill-val green">✓</span><span class="ppill-val green">{qty_a} in stock</span></span>
        {anchor_feats_html}
      </div>
      <div class="anchor-price">{money(anchor.get('price', 0))}</div>
    </div>""", unsafe_allow_html=True)

    # ── 4. Alt rows ──
    badge_labels = ["best overall", "best value", "premium pick"]
    badge_cls    = ["ab-rec", "ab-value", "ab-premium"]
    row_cls_map  = ["alt-highlighted", "", ""]

    for i, (cand, fallback) in enumerate(alts):
        note, direction = price_diff_label(anchor["price"], cand["price"])
        price_note_html = f'<div class="alt-price-note {direction}">{note}</div>' if note else ""
        qty  = int(float(cand.get("quantity", 0) or 0))
        bl   = badge_labels[i] if i < len(badge_labels) else "alternative"
        bcl  = badge_cls[i]    if i < len(badge_cls)    else "ab-rec"
        rcl  = row_cls_map[i]  if i < len(row_cls_map)  else ""

        img_html = (
            f'<img class="alt-img" src="{cand["image_url"]}" />'
            if cand.get("image_url")
            else '<div class="alt-img-ph">🏷️</div>'
        )

        feats_c = feat_lines(cand.get("key_features", ""), 2)
        feat_pills = ""
        for f in feats_c:
            txt = f[:60] + "…" if len(f) > 60 else f
            feat_pills += f'<span class="ppill"><span class="ppill-icon">·</span><span class="ppill-val">{txt}</span></span>'

        colors_c = ", ".join(cand.get("colors", [])[:2]) or "—"

        view_btn = ""
        if cand.get("product_url"):
            view_btn = f'<a href="{cand["product_url"]}" target="_blank" style="font-size:0.68rem;font-weight:600;color:#2563eb;text-decoration:none;white-space:nowrap;flex-shrink:0;">View →</a>'

        st.markdown(f"""
        <div class="alt-row-wrap {rcl}">
          <div class="alt-row">
            {img_html}
            <div class="alt-name-block">
              <div class="alt-name">{cand['product_name']} <span class="alt-badge {bcl}">{bl}</span></div>
              <div class="alt-sub">{cand['brand']} &nbsp;·&nbsp; {cand['product_type']}</div>
            </div>
            <div class="param-pill-row">
              <span class="ppill"><span class="ppill-icon">🎨</span><span class="ppill-val">{colors_c}</span></span>
              <span class="ppill"><span class="ppill-icon">👤</span><span class="ppill-val">{cand.get('gender','—')}</span></span>
              <span class="ppill"><span class="ppill-icon ppill-val green">✓</span><span class="ppill-val green">{qty} in stock</span></span>
              {feat_pills}
            </div>
            <div class="alt-price-block">
              <div class="alt-price">{money(cand['price'])}</div>
              {price_note_html}
            </div>
            {view_btn}
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.62rem;color:#bbb;margin-top:0.4rem;">ⓘ Ranked on semantic similarity · stock confirmed at time of search</p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="nav-logo">A<span>Peak</span></div>
  <div class="nav-links">
    <span class="nav-link">All Products</span>
    <span class="nav-link">Categories</span>
    <span class="nav-link">Brands</span>
    <span class="nav-link">Sale</span>
  </div>
</div>
""", unsafe_allow_html=True)

avail_idx = [i for i, r in enumerate(records) if avail(r)]
cats = sorted({clean_cat(records[i]["main_category"]) for i in avail_idx})

c1, c2 = st.columns([1, 2.2])
with c1:
    sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
with c2:
    cat_idx = sorted(
        [i for i in avail_idx if clean_cat(records[i]["main_category"]) == sel_cat],
        key=lambda i: (records[i]["product_type"], records[i]["brand"], records[i]["product_name"])
    )
    sel_idx = st.selectbox("Product", cat_idx, format_func=lambda i: plabel(records[i]), label_visibility="collapsed")

anchor = records[sel_idx]

st.markdown(f"""
<div class="breadcrumb">
  Home · {anchor['main_category']} · {anchor['product_type']} · <span>{anchor['product_name']}</span>
</div>""", unsafe_allow_html=True)

# ── Main product ──────────────────────────────────────────────────
img_col, info_col = st.columns([1, 1.4], gap="large")

with img_col:
    if anchor.get("image_url"):
        st.image(anchor["image_url"], use_container_width=True)
    else:
        st.markdown('<div style="height:300px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:4rem;">🏷️</div>', unsafe_allow_html=True)

with info_col:
    st.markdown(f'<div class="product-type-pill">{anchor["product_type"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="product-title">{anchor["product_name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="product-brand">by <strong>{anchor["brand"]}</strong> &nbsp;·&nbsp; {anchor["gender"]} &nbsp;·&nbsp; {anchor["main_category"]}</div>', unsafe_allow_html=True)

    orig = anchor.get("original_price", 0)
    curr = anchor.get("price", 0)
    off  = pct_off(orig, curr)
    st.markdown(f"""
    <div style="margin:0.5rem 0 0.3rem;display:flex;align-items:baseline;flex-wrap:wrap;gap:0.3rem;">
      <span class="price-main">{money(curr)}</span>
      {"<span class='price-orig'>" + money(orig) + "</span>" if off else ""}
      {"<span class='price-off'>" + off + "</span>" if off else ""}
    </div>""", unsafe_allow_html=True)

    if avail(anchor):
        st.markdown(f'<div class="stock-badge"><div class="stock-dot"></div>In Stock &nbsp;·&nbsp; {int(float(anchor.get("quantity",0)))} units available</div>', unsafe_allow_html=True)

    st.markdown('<div class="param-title">Product Details</div>', unsafe_allow_html=True)
    cols_html = ", ".join(anchor.get("colors", [])[:4]) or "—"
    st.markdown(f"""
    <div class="param-grid">
      <div class="param-box"><div class="param-label">Brand</div><div class="param-value">{anchor['brand']}</div></div>
      <div class="param-box"><div class="param-label">Gender</div><div class="param-value">{anchor['gender']}</div></div>
      <div class="param-box"><div class="param-label">SKU</div><div class="param-value" style="font-size:0.75rem">{anchor['sku']}</div></div>
      <div class="param-box"><div class="param-label">Available Colors</div><div class="param-value" style="font-size:0.77rem">{cols_html}</div></div>
    </div>""", unsafe_allow_html=True)

    feats = feat_lines(anchor.get("key_features", ""), 5)
    if feats:
        st.markdown('<div class="param-title">Key Features</div>', unsafe_allow_html=True)
        items = "".join(f'<div class="feat-item"><span class="feat-check">✓</span><span class="feat-text">{f}</span></div>' for f in feats)
        st.markdown(items, unsafe_allow_html=True)

    if anchor.get("product_url"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("View Full Product →", anchor["product_url"])

# ── ALTERNATIVES ──────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if "mode" not in st.session_state:
    st.session_state.mode = "same"

st.markdown('<div style="font-size:1rem;font-weight:700;color:#111827;margin-bottom:0.75rem;">Compare With Best Alternatives</div>', unsafe_allow_html=True)

b1, b2, _ = st.columns([1, 1, 3])
with b1:
    if st.button("🔁  Same Brand", use_container_width=True,
                 type="primary" if st.session_state.mode == "same" else "secondary"):
        st.session_state.mode = "same"; st.rerun()
with b2:
    if st.button("🔀  Different Brand", use_container_width=True,
                 type="primary" if st.session_state.mode == "diff" else "secondary"):
        st.session_state.mode = "diff"; st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

alts, has_fallback = find_alts(sel_idx, st.session_state.mode)

if not alts:
    st.markdown("""
    <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:2rem;text-align:center;">
      <div style="font-size:1.5rem;margin-bottom:0.5rem">🔍</div>
      <div style="font-size:0.88rem;color:#374151;font-weight:600;margin-bottom:0.3rem">Exploring other options</div>
      <div style="font-size:0.78rem;color:#9ca3af">Try switching between Same Brand and Different Brand, or select another product.</div>
    </div>""", unsafe_allow_html=True)
else:
    render_alternatives(anchor, alts, st.session_state.mode)

# ── FAQs ─────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="faq-eyebrow">FAQ</div>
<div class="faq-main-title">Quick Questions</div>
<div class="faq-subtitle">Simple answers before you compare or open a product page.</div>
""", unsafe_allow_html=True)

faqs = [
    ("Are these alternatives in stock?", "Yes. Only in-stock items with confirmed quantity are shown."),
    ("How close are the prices?", "Alternatives stay within <strong>30%</strong> of the selected product price."),
    ("Can I choose a size or color here?", "Use <strong>View →</strong> to open the product page and select size, color, and quantity."),
    ("Why do some products cost less?", "Price differences can reflect brand, color, sale status, or minor spec changes."),
    ("Can I return an alternative?", "Returns follow the store policy shown on the product page. Please review before checkout."),
]
for q, a in faqs:
    with st.expander(q):
        st.markdown(f'<div class="faq-a">{a}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  <div class="footer-text">© 2025 APeak · Powered by FAISS + BAAI/bge-base-en-v1.5 + Groq LLaMA 3.1</div>
  <div class="footer-text">All alternatives confirmed in-stock at time of search</div>
</div>
""", unsafe_allow_html=True)    