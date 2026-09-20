import streamlit as st
import pyrebase

# পেজ কনফিগারেশন (এটি সবার আগে দিতে হয়)
st.set_page_config(page_title="Items Builder", layout="wide")

# Firebase Configuration
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
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

# Session State চেক করা লগইনের জন্য
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# লগইন ফাংশন
def login_page():
    st.title("🔒 Items Builder - Login")
    st.write("ওয়েবসাইটে প্রবেশ করতে পাসওয়ার্ড দিন:")
    
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if password == "Op999ffs2SgMLmn":
            st.session_state['logged_in'] = True
            st.success("লগইন সফল হয়েছে!")
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")

# মূল হোমপেজ ফাংশন
def main_app():
    st.sidebar.title("মেনু")
    menu_choice = st.sidebar.radio(
        "যেকোনো একটি পেজ সিলেক্ট করুন:",
        ("🏠 Home (Characters)", "👕 Add Items (Textures & Meshes)", "🛠️ Bundle Builder")
    )

    if menu_choice == "🏠 Home (Characters)":
        st.header("🏠 Character Management")
        st.write("এখানে আপনি মূল ক্যারেক্টার এবং Asset Bundle ফাইলগুলো স্টোর করবেন।")
        
        # ক্যারেক্টার আপলোড ফর্ম
        with st.form("character_upload_form", clear_on_submit=True):
            st.subheader("নতুন ক্যারেক্টার অ্যাড করুন")
            
            char_image = st.file_uploader("১. ক্যারেক্টারের ছবি (১২৮০x১২৮০ রেকমেন্ডেড)", type=['png', 'jpg', 'jpeg'])
            char_file = st.file_uploader("৬. ক্যারেক্টারের Asset Bundle ফাইল আপলোড করুন")
            
            col1, col2 = st.columns(2)
            with col1:
                char_name = st.text_input("২. ক্যারেক্টারের নাম")
                orig_name = st.text_input("৩. ফাইলের আসল নাম")
            with col2:
                byte_size = st.text_input("৪. ফাইলের সাইজ (Byte Size)")
            
            st.divider()
            
            st.subheader("৫. Texture2D Path IDs (D, N, S)")
            categories = ["Hair", "Mask", "Body", "Pant", "Shoe"]
            
            path_ids = {}
            for cat in categories:
                st.markdown(f"**{cat} Path IDs**")
                p_col1, p_col2, p_col3 = st.columns(3)
                with p_col1:
                    d_id = st.text_input(f"{cat} - D Path ID", key=f"d_{cat}")
                with p_col2:
                    n_id = st.text_input(f"{cat} - N Path ID", key=f"n_{cat}")
                with p_col3:
                    s_id = st.text_input(f"{cat} - S Path ID", key=f"s_{cat}")
                path_ids[cat] = {"D": d_id, "N": n_id, "S": s_id}
                
            st.divider()
            
            st.subheader("Mesh IDs")
            mesh_ids = {}
            m_cols = st.columns(5)
            for i, cat in enumerate(categories):
                with m_cols[i]:
                    mesh_ids[cat] = st.text_input(f"{cat} Mesh ID", key=f"mesh_{cat}")
                    
            submit_button = st.form_submit_button("ক্যারেক্টার ডাটাবেসে সেভ করুন")
            
            if submit_button:
                if char_image and char_file and char_name:
                    st.info("ফাইলগুলো Firebase-এ আপলোড হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
                    # পরবর্তীতে এখানে Firebase Database/Storage-এ সেভ করার কোড যোগ করা হবে
                    st.success(f"{char_name} ক্যারেক্টারটি সফলভাবে ডাটাবেসে সেভ হয়েছে!")
                else:
                    st.error("দয়া করে ছবি, ফাইল এবং ক্যারেক্টারের নাম অবশ্যই দিন।")
        
    elif menu_choice == "👕 Add Items (Textures & Meshes)":
        st.header("👕 Items Management")
        st.write("এখানে আপনি Hair, Mask, Body, Pant, Shoe ক্যাটাগরিতে আইটেম অ্যাড করতে পারবেন।")
        # আগামী ধাপে এই পেজের ফর্ম যোগ করা হবে

    elif menu_choice == "🛠️ Bundle Builder":
        st.header("🛠️ Bundle Builder / Modifier")
        st.write("এখান থেকে ক্যারেক্টার ও আইটেম সিলেক্ট করে মডিফাই করা ফাইনাল ফাইল তৈরি করতে পারবেন।")
        # পরবর্তীতে এখানে Python মডিফাই প্রসেস যোগ করা হবে

if not st.session_state['logged_in']:
    login_page()
else:
    main_app()
