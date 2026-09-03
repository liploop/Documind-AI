# 🧠 DocuMind AI — Smart PDF Document Assistant

DocuMind AI adalah aplikasi asisten dokumen berbasis web yang memungkinkan pengguna untuk mengunggah dokumen PDF, menggenerasi rangkuman otomatis secara presisi, dan melakukan tanya jawab (Q&A) interaktif berdasarkan isi dokumen menggunakan **Google Gemini AI**.

🚀 **Live Demo:** [documind-ai-app.streamlit.app](https://documind-ai-app.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## ✨ Fitur Utama

- **🔐 Sistem Autentikasi Pengguna:**
  - Registrasi & Login dengan enkripsi password aman berbasis `bcrypt`.
  - Dukungan **Mode Guest** untuk uji coba cepat tanpa harus login.

- **📄 Ekstraksi & Analisis PDF:**
  - Pembacaan dan ekstraksi teks otomatis dari file PDF menggunakan `pypdf`.

- **🤖 Integrasi Google Gemini AI:**
  - Rangkuman otomatis isi dokumen secara cepat dan terstruktur.
  - Tanya Jawab (Q&A) kontekstual berbasis konten dokumen yang diunggah.

- **💾 Manajemen Data & Riwayat:**
  - Penyimpanan data pengguna, dokumen, dan riwayat chat interaktif menggunakan **SQLite**.

---

## 🛠️ Tech Stack

- **Frontend & Web Framework:** [Streamlit](https://streamlit.io/)
- **AI Model & SDK:** Google Gemini API ([`google-genai`](https://pypi.org/project/google-genai/)) — `gemini-3.6-flash`
- **Database:** SQLite
- **Security:** `bcrypt`
- **PDF Processing:** `pypdf`
- **Deployment Platform:** Streamlit Community Cloud

---

## 💻 Cara Menjalankan Secara Lokal

Jika Anda ingin menjalankan proyek ini di lingkungan lokal (*local development*):

### 1. Clone Repository
```bash
git clone [https://github.com/liploop/documind-ai.git](https://github.com/liploop/documind-ai.git)
cd documind-ai
