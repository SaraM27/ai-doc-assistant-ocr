📄 AI Document Assistant + OCR

This project provides a smart assistant for interacting with document files (PDF) and images using modern NLP techniques.  
It supports real-time question answering on both PDF content and extracted image text (Arabic & English).

---

🚀 Features

📸 OCR from Images: Uses Google Gemini Flash 2.0 API to extract text from image files.  
❓ OCR QA: After extracting the text from images, users can ask questions based on the extracted text using Gemini API.  
📄 PDF QA with RAG: Asks questions on uploaded PDF documents using Retrieval-Augmented Generation (RAG).  
🤖 Multilingual Support: Works with Arabic and English documents.  
🔒 Secure On-Premise: The RAG pipeline (PDF QA) runs locally using on-premise LLMs like LLaMA3.2-Vision.

---

🔧 Tech Stack

OCR & Image QA: Google Gemini Flash 2.0  
RAG Pipeline: LangChain + FAISS + LLaMA3.2-Vision (via Ollama)  
Embeddings: all-minilm (MiniLM) via Ollama for semantic vector search  
Frontend: Streamlit (real-time web UI)

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
