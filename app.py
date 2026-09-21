import streamlit as st
import pyrebase
import time

# ==========================================
# ⚙️ পেজ কনফিগারেশন (সবার আগে দিতে হবে)
# ==========================================
st.set_page_config(page_title="Items Builder Dashboard", page_icon="⚙️", layout="wide")

# ==========================================
# 🔥 Firebase Configuration
# ==========================================
firebaseConfig = {
    "apiKey": "AIzaSyBa79uyxk_TGjZazqJTbDg29n0fhYei9V0",
    "authDomain": "item-make.firebaseapp.com",
    "projectId": "item-make",
    "storageBucket": "item-make.firebasestorage.app",
    "messagingSenderId": "622193873192",
    "appId": "1:622193873192:web:076c4efc2118946e1d401d",
    "databaseURL": "https://item-make-default-rtdb.firebaseio.com"
}

# Initialize Firebase
try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    storage = firebase.storage()
except Exception as e:
    st.error(f"Firebase connection error: {e}")

# ==========================================
# 🔐 Session State (Login Check)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_page():
    st.title("🔒 Items Builder - Login")
    st.markdown("ওয়েবসাইটে প্রবেশ করতে আপনার সিক্রেট পাসওয়ার্ড দিন:")
    
    password = st.text_input("Password", type="password")
    
    if st.button("Login", type="primary"):
        if password == "Op999ffs2SgMLmn":
            st.session_state['logged_in'] = True
            st.success("✅ লগইন সফল হয়েছে!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")

# ==========================================
# 🚀 মূল অ্যাপ্লিকেশন
# ==========================================
def main_app():
    # সাইডবার নেভিগেশন
    st.sidebar.title("মেনু নেভিগেশন")
    menu_choice = st.sidebar.radio(
        "যেকোনো একটি পেজ সিলেক্ট করুন:",
        ("🏠 Home (Characters)", "👕 Add Items (Textures)", "🛠️ Bundle Builder")
    )

    st.sidebar.divider()
    if st.sidebar.button("🚪 লগআউট করুন"):
        st.session_state['logged_in'] = False
        st.rerun()

    # ==========================================
    # 🏠 PAGE 1: CHARACTER MANAGEMENT
    # ==========================================
    if menu_choice == "🏠 Home (Characters)":
        st.header("🏠 Character Management")
        st.write("এখানে আপনি মূল ক্যারেক্টার এবং Asset Bundle ফাইলগুলো আপলোড এবং ম্যানেজ করতে পারবেন।")
        
        tab1, tab2 = st.tabs(["🆕 নতুন ক্যারেক্টার আপলোড", "📂 ক্যারেক্টার ম্যানেজমেন্ট (এডিট/ডিলিট)"])
        
        # --- TAB 1: UPLOAD CHARACTERS ---
        with tab1:
            with st.form("character_upload_form", clear_on_submit=True):
                st.subheader("নতুন ক্যারেক্টার অ্যাড করুন")
                
                char_image = st.file_uploader("১. ক্যারেক্টারের ছবি (১২৮০x১২৮০ রেকমেন্ডেড)", type=['png', 'jpg', 'jpeg'])
                char_file = st.file_uploader("২. Asset Bundle ফাইল", type=['asset', 'bundle', 'txt', 'zip'])
                
                col1, col2 = st.columns(2)
                with col1:
                    char_name = st.text_input("৩. ক্যারেক্টারের নাম")
                    orig_name = st.text_input("৪. ফাইলের আসল নাম")
                with col2:
                    byte_size = st.text_input("৫. ফাইলের সাইজ (Byte Size)")
                
                st.divider()
                st.subheader("৬. Texture2D Path IDs (D, N, S)")
                categories = ["Hair", "Mask", "Body", "Pant", "Shoe"]
                path_ids = {}
                for cat in categories:
                    st.markdown(f"**{cat} Path IDs**")
                    p_col1, p_col2, p_col3 = st.columns(3)
                    with p_col1: d_id = st.text_input(f"{cat} D", key=f"d_{cat}")
                    with p_col2: n_id = st.text_input(f"{cat} N", key=f"n_{cat}")
                    with p_col3: s_id = st.text_input(f"{cat} S", key=f"s_{cat}")
                    path_ids[cat] = {"D": d_id, "N": n_id, "S": s_id}
                    
                st.divider()
                st.subheader("৭. Mesh IDs")
                mesh_ids = {}
                m_cols = st.columns(5)
                for i, cat in enumerate(categories):
                    with m_cols[i]:
                        mesh_ids[cat] = st.text_input(f"{cat} Mesh", key=f"mesh_{cat}")
                        
                submit_button = st.form_submit_button("ক্যারেক্টার সেভ করুন", type="primary")
                
                if submit_button:
                    if char_image and char_file and char_name:
                        with st.spinner("ফাইলগুলো আপলোড হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন..."):
                            try:
                                img_path = f"characters/images/{char_name}_{char_image.name}"
                                storage.child(img_path).put(char_image.getvalue())
                                img_url = storage.child(img_path).get_url(None)

                                bundle_path = f"characters/bundles/{char_name}_{char_file.name}"
                                storage.child(bundle_path).put(char_file.getvalue())
                                bundle_url = storage.child(bundle_path).get_url(None)

                                data = {
                                    "char_name": char_name, "orig_name": orig_name, "byte_size": byte_size,
                                    "path_ids": path_ids, "mesh_ids": mesh_ids,
                                    "image_url": img_url, "bundle_url": bundle_url
                                }
                                db.child("characters").push(data)
                                st.success(f"✅ '{char_name}' সফলভাবে ডাটাবেসে সেভ হয়েছে!")
                            except Exception as e:
                                st.error(f"আপলোড ফেইল হয়েছে: {e}")
                    else:
                        st.warning("⚠️ দয়া করে ছবি, ফাইল এবং ক্যারেক্টারের নাম অবশ্যই দিন।")
        
        # --- TAB 2: MANAGE CHARACTERS ---
        with tab2:
            st.subheader("সংরক্ষিত ক্যারেক্টারসমূহ")
            try:
                chars = db.child("characters").get().val()
                if chars:
                    for key, val in chars.items():
                        with st.expander(f"👤 {val.get('char_name', 'Unknown')}"):
                            col_img, col_info = st.columns([1, 2])
                            with col_img:
                                if val.get('image_url'): st.image(val['image_url'], use_container_width=True)
                            with col_info:
                                st.write(f"**আসল নাম:** {val.get('orig_name', 'N/A')}")
                                st.write(f"**সাইজ:** {val.get('byte_size', 'N/A')} Bytes")
                                st.write(f"[📦 Bundle ডাউনলোড করুন]({val.get('bundle_url', '#')})")
                                
                                btn_col1, btn_col2 = st.columns(2)
                                with btn_col1:
                                    if st.button("✏️ এডিট", key=f"edit_c_{key}", use_container_width=True):
                                        st.session_state['edit_char_id'] = key
                                with btn_col2:
                                    if st.button("🗑️ ডিলিট", key=f"del_c_{key}", type="secondary", use_container_width=True):
                                        db.child("characters").child(key).remove()
                                        st.success("ডিলিট হয়েছে!")
                                        time.sleep(1)
                                        st.rerun()
                                        
                    # EDIT FORM FOR CHARACTER
                    if 'edit_char_id' in st.session_state:
                        edit_key = st.session_state['edit_char_id']
                        if edit_key in chars:
                            curr = chars[edit_key]
                            st.divider()
                            st.subheader(f"✏️ আপডেট: {curr.get('char_name')}")
                            with st.form("edit_char_form"):
                                new_name = st.text_input("নতুন নাম", value=curr.get('char_name', ''))
                                new_orig = st.text_input("নতুন আসল নাম", value=curr.get('orig_name', ''))
                                new_size = st.text_input("নতুন সাইজ", value=curr.get('byte_size', ''))
                                
                                if st.form_submit_button("পরিবর্তন সেভ করুন", type="primary"):
                                    db.child("characters").child(edit_key).update({
                                        "char_name": new_name, "orig_name": new_orig, "byte_size": new_size
                                    })
                                    st.success("✅ আপডেট হয়েছে!")
                                    del st.session_state['edit_char_id']
                                    time.sleep(1)
                                    st.rerun()
                else:
                    st.info("ডাটাবেসে কোনো ক্যারেক্টার নেই।")
            except Exception as e:
                st.error(f"লোডিং সমস্যা: {e}")

    # ==========================================
    # 👕 PAGE 2: ITEMS MANAGEMENT
    # ==========================================
    elif menu_choice == "👕 Add Items (Textures)":
        st.header("👕 Items Management")
        st.write("এখানে আপনি Hair, Mask, Body, Pant, Shoe ক্যাটাগরিতে আইটেম যোগ এবং এডিট করতে পারবেন।")
        
        tab_i1, tab_i2 = st.tabs(["🆕 নতুন আইটেম আপলোড", "📂 আইটেম ম্যানেজমেন্ট (এডিট/ডিলিট)"])
        
        # --- TAB 1: UPLOAD ITEMS ---
        with tab_i1:
            with st.form("item_upload_form", clear_on_submit=True):
                st.subheader("নতুন আইটেম যোগ করুন")
                col1, col2 = st.columns(2)
                with col1:
                    item_name = st.text_input("১. আইটেমের নাম")
                    item_category = st.selectbox("২. ক্যাটাগরি", ["Hair", "Mask", "Body", "Pant", "Shoe"])
                with col2:
                    item_path_id = st.text_input("৩. Texture Path ID (ঐচ্ছিক)")
                    item_mesh_id = st.text_input("৪. Mesh ID (ঐচ্ছিক)")
                    
                item_image = st.file_uploader("৫. আইটেমের ছবি", type=['png', 'jpg', 'jpeg'])
                item_file = st.file_uploader("৬. আইটেমের ফাইল (ঐচ্ছিক)", type=['bundle', 'asset', 'obj'])
                
                if st.form_submit_button("আইটেম সেভ করুন", type="primary"):
                    if item_name and item_category:
                        with st.spinner("আপলোড হচ্ছে..."):
                            try:
                                img_url, file_url = "", ""
                                if item_image:
                                    img_path = f"items/{item_category}/{item_name}_{item_image.name}"
                                    storage.child(img_path).put(item_image.getvalue())
                                    img_url = storage.child(img_path).get_url(None)
                                if item_file:
                                    f_path = f"items/{item_category}/{item_name}_{item_file.name}"
                                    storage.child(f_path).put(item_file.getvalue())
                                    file_url = storage.child(f_path).get_url(None)
                                    
                                db.child("items").push({
                                    "item_name": item_name, "category": item_category,
                                    "path_id": item_path_id, "mesh_id": item_mesh_id,
                                    "image_url": img_url, "file_url": file_url
                                })
                                st.success(f"✅ '{item_name}' সেভ হয়েছে!")
                            except Exception as e:
                                st.error(f"আপলোডে সমস্যা: {e}")
                    else:
                        st.warning("⚠️ নাম এবং ক্যাটাগরি অবশ্যই দিন।")
                        
        # --- TAB 2: MANAGE ITEMS ---
        with tab_i2:
            st.subheader("সংরক্ষিত আইটেমসমূহ")
            try:
                items_data = db.child("items").get().val()
                if items_data:
                    for key, val in items_data.items():
                        cat = val.get('category', '')
                        emojis = {"Hair": "💇", "Shoe": "👟", "Pant": "👖", "Mask": "🎭", "Body": "👕"}
                        cat_emoji = emojis.get(cat, "👕")
                        
                        with st.expander(f"{cat_emoji} {val.get('item_name', 'Unknown')} ({cat})"):
                            col_img, col_info = st.columns([1, 2])
                            with col_img:
                                if val.get('image_url'): st.image(val['image_url'], use_container_width=True)
                            with col_info:
                                st.write(f"**Path ID:** {val.get('path_id', 'N/A')}")
                                st.write(f"**Mesh ID:** {val.get('mesh_id', 'N/A')}")
                                if val.get('file_url'): st.write(f"[📦 ফাইল]({val.get('file_url')})")
                                
                                btn_i1, btn_i2 = st.columns(2)
                                with btn_i1:
                                    if st.button("✏️ এডিট", key=f"edit_i_{key}", use_container_width=True):
                                        st.session_state['edit_item_id'] = key
                                with btn_i2:
                                    if st.button("🗑️ ডিলিট", key=f"del_i_{key}", type="secondary", use_container_width=True):
                                        db.child("items").child(key).remove()
                                        st.success("ডিলিট হয়েছে!")
                                        time.sleep(1)
                                        st.rerun()
                                        
                    # EDIT FORM FOR ITEMS
                    if 'edit_item_id' in st.session_state:
                        edit_key = st.session_state['edit_item_id']
                        if edit_key in items_data:
                            curr_i = items_data[edit_key]
                            st.divider()
                            st.subheader(f"✏️ আপডেট: {curr_i.get('item_name')}")
                            with st.form("edit_item_form"):
                                new_i_name = st.text_input("নতুন নাম", value=curr_i.get('item_name', ''))
                                new_i_path = st.text_input("নতুন Path ID", value=curr_i.get('path_id', ''))
                                new_i_mesh = st.text_input("নতুন Mesh ID", value=curr_i.get('mesh_id', ''))
                                
                                if st.form_submit_button("পরিবর্তন সেভ করুন", type="primary"):
                                    db.child("items").child(edit_key).update({
                                        "item_name": new_i_name, "path_id": new_i_path, "mesh_id": new_i_mesh
                                    })
                                    st.success("✅ আইটেম আপডেট হয়েছে!")
                                    del st.session_state['edit_item_id']
                                    time.sleep(1)
                                    st.rerun()
                else:
                    st.info("ডাটাবেসে কোনো আইটেম নেই।")
            except Exception as e:
                st.error(f"লোডিং সমস্যা: {e}")

    # ==========================================
    # 🛠️ PAGE 3: BUNDLE BUILDER
    # ==========================================
    elif menu_choice == "🛠️ Bundle Builder":
        st.header("🛠️ Bundle Builder / Modifier")
        st.write("ডাটাবেস থেকে ক্যারেক্টার ও আইটেম সিলেক্ট করে ফাইনাল মডিফাইড বান্ডেল তৈরি করুন।")
        
        try:
            chars_data = db.child("characters").get().val()
            items_data = db.child("items").get().val()
            
            if chars_data:
                char_names = ["-- একটি ক্যারেক্টার সিলেক্ট করুন --"] + [val.get('char_name') for key, val in chars_data.items()]
                selected_char = st.selectbox("১. মূল ক্যারেক্টার", char_names)
                
                st.divider()
                st.subheader("২. আইটেম সিলেক্ট করুন")
                
                hair_list, mask_list, body_list, pant_list, shoe_list = ["None"], ["None"], ["None"], ["None"], ["None"]
                
                if items_data:
                    for key, val in items_data.items():
                        c, n = val.get('category'), val.get('item_name')
                        if c == "Hair": hair_list.append(n)
                        elif c == "Mask": mask_list.append(n)
                        elif c == "Body": body_list.append(n)
                        elif c == "Pant": pant_list.append(n)
                        elif c == "Shoe": shoe_list.append(n)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    sel_hair = st.selectbox("💇 Hair", hair_list)
                    sel_mask = st.selectbox("🎭 Mask", mask_list)
                with col2:
                    sel_body = st.selectbox("👕 Body", body_list)
                    sel_pant = st.selectbox("👖 Pant", pant_list)
                with col3:
                    sel_shoe = st.selectbox("👟 Shoe", shoe_list)
                    
                st.divider()
                
                if st.button("🚀 Build Final Bundle", type="primary", use_container_width=True):
                    if selected_char == "-- একটি ক্যারেক্টার সিলেক্ট করুন --":
                        st.error("⚠️ প্রথমে একটি ক্যারেক্টার সিলেক্ট করতে হবে!")
                    else:
                        with st.spinner("UnityPy দিয়ে ফাইল প্রসেস হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
                            # ====================================================
                            # ⚠️ আপনার UnityPy লজিক (Python Script) এখানে বসাতে হবে।
                            # বর্তমানে এটি ডেমো হিসেবে ৩ সেকেন্ড লোডিং দেখাবে।
                            # ====================================================
                            time.sleep(3)
                            
                            st.success(f"✅ {selected_char} এর ফাইনাল Asset Bundle তৈরি হয়েছে!")
                            
                            # ডাউনলোডের অপশন
                            st.download_button(
                                label="📥 ডাউনলোড মডিফাইড ফাইল",
                                data=b"Dummy modified bundle file content. Replace this with real bytes.",
                                file_name=f"{selected_char}_Final_Bundle.asset",
                                mime="application/octet-stream",
                                use_container_width=True
                            )
            else:
                st.warning("⚠️ আপনার ডাটাবেসে কোনো ক্যারেক্টার নেই। আগে ক্যারেক্টার আপলোড করুন।")
        except Exception as e:
            st.error(f"ডেটা লোড করতে সমস্যা: {e}")

# ==========================================
# Run Application
# ==========================================
if not st.session_state['logged_in']:
    login_page()
else:
    main_app()
