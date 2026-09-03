import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
import database as db

# Inisialisasi Database SQLite
db.init_db()

# Konfigurasi Halaman
st.set_page_config(
    page_title="DocuMind AI — Smart Document Assistant",
    page_icon="🧠",
    layout="wide"
)

# Load Environment Variables
load_dotenv(override=True)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = str(st.secrets["GEMINI_API_KEY"]).strip()
elif os.getenv("GEMINI_API_KEY"):
    api_key = str(os.getenv("GEMINI_API_KEY")).strip()

if not api_key:
    st.error("⚠️ `GEMINI_API_KEY` tidak ditemukan! Periksa Secrets di Streamlit Cloud.")
    st.stop()

# Inisialisasi Client SDK Baru
client = genai.Client(api_key=api_key)

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "current_doc_id" not in st.session_state:
    st.session_state.current_doc_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "summary" not in st.session_state:
    st.session_state.summary = ""

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# --- SIDEBAR AUTH & NAVIGASI ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/brain.png", width=64)
    st.title("DocuMind AI")
    st.divider()

    # Logika Jika Belum Login
    if st.session_state.user_id is None:
        st.subheader("🔐 Auth Portal")
        tab_login, tab_register = st.tabs(["Login", "Register"])
        
        with tab_login:
            user_input = st.text_input("Username", key="login_user")
            pass_input = st.text_input("Password", type="password", key="login_pass")
            if st.button("Masuk", use_container_width=True):
                uid = db.login_user(user_input, pass_input)
                if uid:
                    st.session_state.user_id = uid
                    st.session_state.username = user_input
                    st.success("Login Berhasil!")
                    st.rerun()
                else:
                    st.error("Username atau password salah.")

        with tab_register:
            reg_user = st.text_input("Username Baru", key="reg_user")
            reg_pass = st.text_input("Password Baru", type="password", key="reg_pass")
            if st.button("Daftar", use_container_width=True):
                if reg_user and reg_pass:
                    ok, msg = db.register_user(reg_user, reg_pass)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Mohon isi semua kolom.")
                    
        st.info("💡 **Mode Guest:** Anda bisa langsung mengunggah dokumen tanpa login, tetapi riwayat chat & dokumen akan hilang saat halaman di-refresh.")

    else:
        # Logika Jika Sudah Login
        st.write(f"👤 Login sebagai: **{st.session_state.username}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.current_doc_id = None
            st.session_state.chat_history = []
            st.session_state.summary = ""
            st.rerun()

        st.divider()
        st.subheader("📜 Riwayat Dokumen Anda")
        user_docs = db.get_user_documents(st.session_state.user_id)
        
        if user_docs:
            for d_id, d_name, d_summary in user_docs:
                if st.button(f"📄 {d_name}", key=f"doc_{d_id}", use_container_width=True):
                    st.session_state.current_doc_id = d_id
                    st.session_state.summary = d_summary
                    st.session_state.chat_history = db.get_chat_history(d_id)
                    st.rerun()
        else:
            st.caption("Belum ada dokumen yang tersimpan.")

# --- MAIN CONTENT AREA ---
st.title("🧠 Smart Document Summarizer & Q&A")
st.markdown("Analisis dokumen interaktif berbasis AI. *Login untuk menyimpan riwayat analisis Anda secara permanen.*")
st.divider()

uploaded_file = st.file_uploader("Unggah Dokumen PDF Baru", type=["pdf"])

# Logika Pemrosesan File PDF Baru
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    # Simpan ke DB jika user sudah login
    if st.session_state.user_id and (st.session_state.current_doc_id is None):
        doc_id = db.save_document(st.session_state.user_id, uploaded_file.name)
        st.session_state.current_doc_id = doc_id
        st.session_state.chat_history = []
        st.session_state.summary = ""

    col_summary, col_chat = st.columns([1, 1], gap="large")

    # --- RANGKUMAN DOKUMEN ---
    with col_summary:
        with st.container(border=True):
            st.subheader("📝 Rangkuman Dokumen")
            
            if st.button("✨ Buat Rangkuman Otomatis", type="primary"):
                with st.spinner("Menggenerasi rangkuman..."):
                    prompt_summary = f"Rangkum dokumen berikut secara ringkas:\n\n{pdf_text}"
                    response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt_summary
                    )
                    st.session_state.summary = response.text
                    
                    if st.session_state.current_doc_id:
                        db.update_summary(st.session_state.current_doc_id, response.text)

            if st.session_state.summary:
                st.markdown("---")
                st.markdown(st.session_state.summary)

    # --- CHAT Q&A ---
    with col_chat:
        with st.container(border=True):
            st.subheader("💬 Tanya Jawab Dokumen")
            
            chat_container = st.container(height=380)
            with chat_container:
                for role, text in st.session_state.chat_history:
                    with st.chat_message(role):
                        st.write(text)

            user_query = st.chat_input("Tulis pertanyaan Anda...")
            if user_query:
                st.session_state.chat_history.append(("user", user_query))
                if st.session_state.current_doc_id:
                    db.save_chat_message(st.session_state.current_doc_id, "user", user_query)

                prompt_qa = f"Isi Dokumen:\n{pdf_text}\n\nPertanyaan: {user_query}"
                response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt_qa
                )
                
                st.session_state.chat_history.append(("assistant", response.text))
                if st.session_state.current_doc_id:
                    db.save_chat_message(st.session_state.current_doc_id, "assistant", response.text)
                
                st.rerun()

elif st.session_state.current_doc_id and st.session_state.user_id:
    st.info("📌 Anda sedang melihat riwayat dokumen dari Database. Unggah PDF baru di atas untuk membuat analisis baru.")
    st.markdown(f"**Hasil Rangkuman:**\n{st.session_state.summary}")
