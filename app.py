import streamlit as st
import os
from PIL import Image
from rag import process_pdf, create_rag_chain, extract_text_from_image, answer_question_from_text
# make sure to chnage the path 
UPLOAD_FOLDER = "Users/Sabothneen/AANLP/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("📄 AI Document Assistant + OCR 📸")

tab1, tab2 = st.tabs(["📂 Ask Questions (RAG)", "📸 Extract Text & Ask Questions"])

#  Tab 1: Upload PDF and Ask Questions
with tab1:
    st.subheader("📂 Upload and Ask Questions About a PDF")
    
    uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

        with st.spinner("🔄 Processing PDF..."):
            vectorstore, error_msg = process_pdf(file_path)
            
            if error_msg:
                st.error(error_msg)
                st.stop()

            st.success("✅ PDF processed successfully!")
            rag_chain = create_rag_chain(vectorstore)

            question = st.text_input("💬 Ask a question about the PDF:")
            if st.button("Get Answer"):
                if question:
                    with st.spinner("🤖 Generating response..."):
                        response = rag_chain(question)  
                        st.write("### 🤖 Answer:")
                        st.write(response)
                else:
                    st.warning("⚠️ Please enter a question.")

#  Tab 2: Upload Image, Extract Text, and Ask Questions
with tab2:
    st.subheader("📸 Upload an Image to Extract Text & Ask Questions")

    uploaded_image = st.file_uploader("📤 Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_image:
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)

        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())

        st.image(image_path, caption="📸 Uploaded Image", use_column_width=True)
        st.success(f"✅ Image '{uploaded_image.name}' uploaded successfully!")

        with st.spinner("🔄 Extracting text..."):
            extracted_text = extract_text_from_image(image_path)

        st.write("### 📝 Extracted Text:")
        st.write(extracted_text)

        if extracted_text and "⚠️" not in extracted_text:
            st.subheader("💬 Ask a Question About Extracted Text")
            question = st.text_input("🔍 Enter your question:")
            
            if st.button("Get Answer from Image Text"):
                with st.spinner("🤖 Generating response..."):
                    answer = answer_question_from_text(extracted_text, question)
                    st.write("### 🤖 Answer:")
                    st.write(answer)
