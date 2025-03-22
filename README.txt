📄 AI Document Assistant + OCR

This project provides a smart assistant for interacting with document files (PDF) and images using modern NLP techniques.

---

🚀 Features

🖼 OCR from Images: Uses Google Gemini Flash 2.0 API to extract text from image files.  
📄 PDF QA with RAG: Asks questions on uploaded PDF documents using Retrieval-Augmented Generation (RAG).  
🤖 Multilingual Support: Works with Arabic and English documents.  
🔒 Runs Locally: No cloud model training required, secure on-premise LLMs.

---

🔧 Tech Stack

OCR API: Google Gemini Flash 2.0  
RAG Pipeline: Built with LangChain, FAISS, and LLaMA3.2-Vision (via Ollama).  
Embeddings: MiniLM model via all-minilm for semantic retrieval.  
Frontend: Interactive UI powered by Streamlit.

---

📁 Project Structure

📁 ai-doc-assistant-ocr  
│  
├── app.py  
├── rag.py  
├── requirements.txt  
├── README.md ← this file  
└── uploads/   ← folder to store uploaded PDFs and images  

---

🧪 Installation

```bash
pip install -r requirements.txt
