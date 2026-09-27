import os
import json
import streamlit as st
from groq import Groq

# 1. Page Configuration & Flipkart Minutes x Zepto Theme
st.set_page_config(page_title="Zepto Minutes AI - Instant 10-Min Shopper", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0e0517;
        color: #f1f1f1;
    }
    .minutes-header {
        background: linear-gradient(135deg, #2b004d 0%, #15002a 100%);
        border: 1px solid #ff3269;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(255, 50, 105, 0.15);
    }
    .badge-flash {
        background: #ff3269;
        color: white;
        font-weight: 800;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .product-card {
        background: #1b0d2e;
        border: 1px solid #3d1c5e;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        transition: 0.2s ease-in-out;
    }
    .product-card:hover {
        border-color: #ff3269;
    }
    .prod-title {
        font-weight: 700;
        font-size: 0.98rem;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .prod-meta {
        font-size: 0.82rem;
        color: #a89bb8;
        margin-bottom: 8px;
    }
    .prod-price {
        font-size: 1.15rem;
        font-weight: 800;
        color: #00e676;
    }
    .cart-summary-box {
        background: #180929;
        border: 1px solid #4a1f73;
        border-radius: 14px;
        padding: 18px;
    }
    div.stButton > button {
        background: #ff3269 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        font-size: 0.85rem !important;
    }
    div.stButton > button:hover {
        background: #e02456 !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Secure API Key Setup (Streamlit Secrets or Environment Variable)
def get_groq_client():
    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if api_key:
            return Groq(api_key=api_key)
    except Exception:
        pass
    return None

# 3. Master Dark Store Inventory
INVENTORY = [
    {"id": "b1", "name": "Amul Taaza Toned Milk 1L", "price": 56, "cat": "Dairy", "unit": "1L Tetra Pack", "tags": ["milk", "doodh", "breakfast", "chai", "tea"]},
    {"id": "b2", "name": "English Oven Brown Bread 400g", "price": 50, "cat": "Bakery", "unit": "400g Pack", "tags": ["bread", "toast", "breakfast", "sandwich"]},
    {"id": "b3", "name": "Amul Pasteurised Butter 100g", "price": 58, "cat": "Dairy", "unit": "100g Pack", "tags": ["butter", "makkhan", "toast", "breakfast"]},
    {"id": "b4", "name": "Farm Fresh White Eggs (Pack of 6)", "price": 48, "cat": "Eggs", "unit": "6 pcs Box", "tags": ["egg", "eggs", "anda", "breakfast", "gym", "protein", "omelette"]},
    {"id": "p1", "name": "Cycle Pure Agarbatti (Incense Sticks)", "price": 60, "cat": "Pooja Needs", "unit": "100g Pack", "tags": ["pooja", "agarbatti", "incense", "mandir", "bhagwan"]},
    {"id": "p2", "name": "Mangaldeep Camphor (Kapur)", "price": 40, "cat": "Pooja Needs", "unit": "50g Jar", "tags": ["kapur", "camphor", "pooja", "aarti", "mandir"]},
    {"id": "p3", "name": "Amul Pure Cow Ghee 500ml", "price": 310, "cat": "Dairy", "unit": "500ml Pouch", "tags": ["ghee", "pooja", "cooking", "diya", "mandir"]},
    {"id": "c1", "name": "Vim Dishwash Bar with Scrubber", "price": 30, "cat": "Cleaning", "unit": "200g Bar", "tags": ["vim", "bartan", "dishwash", "cleaning", "kitchen", "safai"]},
    {"id": "c2", "name": "Harpic Power Plus Toilet Cleaner", "price": 99, "cat": "Cleaning", "unit": "500ml Bottle", "tags": ["harpic", "toilet", "cleaning", "safai", "bathroom"]},
    {"id": "c3", "name": "Colin Glass & Surface Cleaner", "price": 105, "cat": "Cleaning", "unit": "500ml Spray", "tags": ["colin", "glass", "spray", "cleaning", "safai"]},
    {"id": "v1", "name": "Fresh Red Onions (Pyaaz) 1kg", "price": 40, "cat": "Vegetables", "unit": "1kg Pack", "tags": ["onion", "pyaaz", "tadka", "sabzi", "cooking"]},
    {"id": "v2", "name": "Fresh Hybrid Tomatoes 500g", "price": 30, "cat": "Vegetables", "unit": "500g Pack", "tags": ["tomato", "tamatar", "tadka", "sabzi", "cooking"]},
    {"id": "v3", "name": "Everest Coriander (Dhaniya) Powder", "price": 45, "cat": "Spices", "unit": "100g Pack", "tags": ["masala", "dhaniya", "spices", "tadka", "cooking"]},
    {"id": "v4", "name": "Fortune Refined Sunflower Oil 1L", "price": 135, "cat": "Oils", "unit": "1L Pouch", "tags": ["oil", "cooking", "tel", "sunflower", "tadka"]},
    {"id": "r1", "name": "Wagh Bakri Premium CTC Tea 500g", "price": 280, "cat": "Tea", "unit": "500g Pouch", "tags": ["chai", "tea", "patti", "nashta", "relatives", "mehmaan", "guest"]},
    {"id": "r2", "name": "Parle-G Gold Premium Biscuits 1kg", "price": 110, "cat": "Biscuits", "unit": "1kg Family Pack", "tags": ["biscuit", "parle", "chai", "nashta", "guest", "mehmaan"]},
    {"id": "r3", "name": "Haldiram's Nagpur Spicy Bhujia Sev 400g", "price": 125, "cat": "Namkeen", "unit": "400g Pack", "tags": ["namkeen", "bhujia", "sev", "nashta", "mehmaan", "snacks"]},
    {"id": "m1", "name": "Maggi 2-Minute Masala Noodles (Pack of 4)", "price": 56, "cat": "Instant Food", "unit": "280g Pack", "tags": ["maggi", "noodles", "midnight", "hungry", "bhookh", "quick snack"]},
    {"id": "m2", "name": "Lay's India's Magic Masala 90g", "price": 30, "cat": "Chips", "unit": "90g Pouch", "tags": ["chips", "lays", "crunchy", "snack", "midnight", "movie"]},
    {"id": "m3", "name": "Act II Golden Butter Popcorn 150g", "price": 60, "cat": "Snacks", "unit": "150g Pack", "tags": ["popcorn", "movie", "snack", "binge", "crunchy"]},
    {"id": "m4", "name": "Coca-Cola Zero Sugar Cans (Pack of 2)", "price": 80, "cat": "Beverages", "unit": "2 x 300ml Cans", "tags": ["coke", "cold drink", "soda", "movie", "party", "drink"]},
    {"id": "g2", "name": "Amul Fresh Malai Paneer 200g", "price": 92, "cat": "Dairy", "unit": "200g Pack", "tags": ["paneer", "protein", "gym", "veg", "curry", "diet"]},
    {"id": "g3", "name": "Pintola All Natural Peanut Butter 350g", "price": 165, "cat": "Healthy", "unit": "350g Jar", "tags": ["peanut butter", "protein", "gym", "diet", "workout"]},
    {"id": "s1", "name": "Fresh Ginger (Adrak) 250g", "price": 35, "cat": "Fresh", "unit": "250g Pack", "tags": ["adrak", "ginger", "cold", "sardi", "cough", "kadha", "chai"]},
    {"id": "s2", "name": "Dabur 100% Pure Honey 250g", "price": 115, "cat": "Health", "unit": "250g Squeeze Bottle", "tags": ["honey", "shehad", "cough", "sardi", "throat"]},
]

# 4. Session State Setup
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# 5. Search & Intent Engine
def find_matching_products(query_text):
    q = query_text.lower()
    
    out_of_scope = ["iphone", "mobile", "phone", "laptop", "shoe", "shoes", "clothes", "shirt", "pant", "car", "bike", "tv", "watch"]
    for word in out_of_scope:
        if word in q:
            return "OUT_OF_SCOPE", []

    intent_map = {
        "breakfast": ["milk", "bread", "butter", "egg", "tea"],
        "pooja": ["agarbatti", "kapur", "ghee"],
        "safai": ["vim", "harpic", "colin", "cleaning"],
        "cleaning": ["vim", "harpic", "colin", "cleaning"],
        "tadka": ["onion", "tomato", "oil", "masala", "dhaniya"],
        "cooking": ["onion", "tomato", "oil", "masala"],
        "mehmaan": ["chai", "tea", "biscuit", "namkeen", "bhujia", "sweet"],
        "guest": ["chai", "tea", "biscuit", "namkeen", "bhujia"],
        "movie": ["popcorn", "coke", "chips", "cold drink"],
        "midnight": ["maggi", "noodles", "chips", "coke"],
        "bhookh": ["maggi", "noodles", "chips", "biscuit"],
        "gym": ["egg", "eggs", "protein", "paneer", "peanut butter"],
        "workout": ["protein", "egg", "eggs", "paneer", "peanut butter"],
        "sardi": ["adrak", "ginger", "honey", "chai"],
        "cold": ["adrak", "ginger", "honey"],
        "party": ["chips", "coke", "cold drink", "namkeen"]
    }

    tokens = set(q.split())
    for key, mapped_keywords in intent_map.items():
        if key in q:
            tokens.update(mapped_keywords)

    scored = []
    for item in INVENTORY:
        score = 0
        combined_text = (item.get("name", "") + " " + item.get("cat", "") + " " + " ".join(item.get("tags", []))).lower()
        for t in tokens:
            if t in combined_text:
                score += 2
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [item for _, item in scored[:6]]

    if not results:
        for item in INVENTORY:
            if any(t in item["name"].lower() for t in q.split()):
                results.append(item)

    return "MATCH_FOUND" if results else "NO_MATCH", results

# 6. Fast AI Shopper Note
def generate_ai_header(user_query, status, count):
    if status == "OUT_OF_SCOPE":
        return "📱 Electronics & Gadgets Not Delivered", "Humare 10-minute dark stores sirf grocery, fresh vegetables, aur daily essentials deliver karte hain. Mobile ya electronics uplabdh nahi hain."

    client = get_groq_client()
    if client:
        try:
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a Zepto Smart Assistant. Respond in 1 very short, sweet Hinglish sentence explaining the curated grocery items."},
                    {"role": "user", "content": f"User intent: '{user_query}'. Found {count} grocery items. Give a crisp 1-line reply."}
                ],
                max_tokens=40,
                temperature=0.3
            )
            return "⚡ Smart Bundle Curated in 10 Mins", res.choices[0].message.content.strip()
        except Exception:
            pass
            
    return "⚡ Smart Bundle Curated in 10 Mins", "Aapki requirement ke hisaab se best items ready hain!"

# 7. UI Header
st.markdown("""
<div class="minutes-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span class="badge-flash">⚡ Zepto Minutes AI</span>
            <h1 style="color:#ff3269; margin:6px 0 0 0; font-size:2rem; font-weight:900;">Instant Everyday Shopper</h1>
            <p style="color:#d4c4e8; margin:4px 0 0 0; font-size:0.95rem;">Type na karein, bas apna mood ya zarurat tap karein aur cart ready!</p>
        </div>
        <div style="text-align:right;">
            <div style="font-size:1.8rem; font-weight:900; color:#00e676;">⚡ 9-10 MINS</div>
            <div style="color:#aaa; font-size:0.8rem;">Real-time Dark Store Delivery</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 10 ONE-TAP BUTTONS (State-Locked)
st.write("🔥 **Tap for Quick 10-Min Delivery Bundles:**")

def select_bundle(bundle_query):
    st.session_state.search_term = bundle_query

r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
r1c1.button("☕ Mehmaan Aa Gaye", on_click=select_bundle, args=("Ghar me mehmaan aa gaye hain, chai aur nashta chahiye",))
r1c2.button("🙏 Pooja Samagri", on_click=select_bundle, args=("Ghar ki pooja aur aarti ke liye pooja samagri chahiye",))
r1c3.button("🧹 Ghar ki Safai", on_click=select_bundle, args=("Ghar ki safai ke liye cleaning items aur bartan bar do",))
r1c4.button("🍛 Sabzi ka Tadka", on_click=select_bundle, args=("Sabzi banane ke liye basic cooking tadka aur tel chahiye",))
r1c5.button("🍳 Daily Breakfast", on_click=select_bundle, args=("Subah ka breakfast banana hai, bread aur doodh chahiye",))

r2c1, r2c2, r2c3, r2c4, r2c5 = st.columns(5)
r2c1.button("🍿 Movie Night Snacks", on_click=select_bundle, args=("Ghar par movie night hai, popcorn aur cold drinks chahiye",))
r2c2.button("🌙 Midnight Cravings", on_click=select_bundle, args=("Raat me bhookh lagi hai, maggi aur snacks bhej do",))
r2c3.button("💪 Gym Diet / Protein", on_click=select_bundle, args=("Gym workout ke baad high protein diet meal items",))
r2c4.button("🤒 Sardi & Khasi", on_click=select_bundle, args=("Sardi aur cold ho gaya hai, kadha banane ka saman do",))
r2c5.button("🥳 Party Essentials", on_click=select_bundle, args=("Dosto ke sath party karni hai, cold drinks aur chips do",))

user_input = st.text_input("🔍 Or type manually:", key="search_term", placeholder="Try: 'sabzi tadka', 'movie snacks', 'safai ka saman'")

col_products, col_cart = st.columns([2.3, 1.1])

with col_products:
    if user_input.strip():
        status, matched_items = find_matching_products(user_input)
        title, explanation = generate_ai_header(user_input, status, len(matched_items))

        st.markdown(f"### {title}")
        st.info(f"💡 {explanation}")

        if status == "OUT_OF_SCOPE":
            st.warning("⚠️ **Zepto Catalog Notice:** Hum sirf Grocery, Snacks, Beverages aur Daily Essentials 10 minute me deliver karte hain. Mobile phones ya electronics uplabdh nahi hain.")
        elif not matched_items:
            st.warning("Koi matching item nahi mila! Kripya grocery, nashta, safai ya snacks se related search karein.")
        else:
            st.write(f"**⚡ Dark-Store Results ({len(matched_items)} items ready to dispatch):**")
            
            grid_cols = st.columns(2)
            for idx, item in enumerate(matched_items):
                with grid_cols[idx % 2]:
                    p_name = item.get("name", "Product")
                    p_unit = item.get("unit", "1 pack")
                    p_cat = item.get("cat", "Grocery")
                    p_price = item.get("price", 0)
                    p_id = item.get("id", f"prod_{idx}")

                    st.markdown(f"""
                    <div class="product-card">
                        <div class="prod-title">{p_name}</div>
                        <div class="prod-meta">{p_unit} • <span style="color:#ff3269;">{p_cat}</span></div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                            <div class="prod-price">₹{p_price}</div>
                            <div style="font-size:0.75rem; color:#aaa;">⚡ 10 mins</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    curr_qty = st.session_state.cart.get(p_id, 0)
                    b_col1, b_col2 = st.columns([1, 1])
                    with b_col1:
                        if st.button(f"➕ Add", key=f"add_{p_id}"):
                            st.session_state.cart[p_id] = curr_qty + 1
                            st.rerun()
                    with b_col2:
                        if curr_qty > 0:
                            if st.button(f"➖ Remove ({curr_qty})", key=f"rem_{p_id}"):
                                st.session_state.cart[p_id] -= 1
                                if st.session_state.cart[p_id] <= 0:
                                    del st.session_state.cart[p_id]
                                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 40px; color:#888;">
            <h3>🛒 Tap a button to see the magic!</h3>
            <p>Upar diye gaye 10 situations me se kisi ek par click karein.</p>
            <p>AI automatically aapki problem ko samajh kar best grocery bundle ready kar dega.</p>
        </div>
        """, unsafe_allow_html=True)

# 8. Real-Time Shopping Cart Sidebar
with col_cart:
    st.markdown('<div class="cart-summary-box">', unsafe_allow_html=True)
    st.markdown("### 🛍️ Zepto Checkout")
    
    if st.session_state.cart:
        item_total = 0
        
        for p_id, qty in list(st.session_state.cart.items()):
            prod = next((p for p in INVENTORY if p["id"] == p_id), None)
            if prod:
                cost = prod.get("price", 0) * qty
                item_total += cost
                
                prod_title_display = prod.get('name', '')[:22]
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.9rem;">
                    <span><b>{qty}x</b> {prod_title_display}...</span>
                    <span>₹{cost}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 0.5px dashed #4a1f73;'>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size:0.85rem; color:#bbb;">
            <div style="display:flex; justify-content:space-between;"><span>Item Total:</span><span>₹{item_total}</span></div>
            <div style="display:flex; justify-content:space-between;"><span>Handling Fee:</span><span>₹4</span></div>
            <div style="display:flex; justify-content:space-between; color:#00e676;"><span>Delivery Fee (10 Mins):</span><span>FREE</span></div>
            <div style="display:flex; justify-content:space-between; font-size:1.15rem; font-weight:800; color:#fff; margin-top:8px;">
                <span>To Pay:</span><span style="color:#00e676;">₹{item_total + 4}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        if st.button("⚡ Place Order (9 Mins)", key="pay_now"):
            st.balloons()
            st.success("🎉 Order Placed! Delivery partner arriving in 9 minutes.")
            st.session_state.cart = {}
    else:
        st.info("🛒 Aapka cart khali hai. Kisi bhi bundle se items '➕ Add' karein.")

    st.markdown('</div>', unsafe_allow_html=True)