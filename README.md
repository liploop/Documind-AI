# 🧠 DocuMind AI — Smart Document Assistant & Q&A

DocuMind AI adalah aplikasi web berbasis Artificial Intelligence (LLM) yang membantu pengguna menganalisis, merangkum, dan mengajukan pertanyaan dari dokumen PDF secara instan. Dilengkapi dengan sistem autentikasi pengguna dan penyimapan riwayat analisis di database SQLite.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## ✨ Fitur Utama
- **📄 PDF Text Extraction:** Ekstraksi otomatis teks dari berkas PDF menggunakan `pypdf`.
- **📝 Automated Summarization:** Merangkum poin-poin utama dokumen menggunakan model **Gemini 3.6 Flash**.
- **💬 Document Q&A (Context Injection):** Menjawab pertanyaan seputar isi dokumen secara interaktif.
- **🔐 User Authentication:** Registrasi dan Login aman berbasis enkripsi `bcrypt`.
- **💾 Session & Database History:** Menyimpan riwayat dokumen dan pesan obrolan per user di SQLite.

---

## 🛠️ Tech Stack
- **Frontend / UI:** Streamlit
- **AI Model:** Google Gemini API (`gemini-3.6-flash`)
- **Backend / DB:** Python, SQLite3, Bcrypt
- **Document Processing:** PyPDF, Python-dotenv

---

## 🚀 Cara Menjalankan secara Lokal

1. **Clone repository ini:**
   ```bash
   git clone [https://github.com/liploop/Documind-AI.git](https://github.com/liploop/Documind-AI.git)
   cd Documind-AI
