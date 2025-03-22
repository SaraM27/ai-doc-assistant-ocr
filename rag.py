import os
import google.generativeai as genai
from PIL import Image
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
# make sure to chnage the path
UPLOAD_FOLDER = "Users/Sabothneen/AANLP/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#  Setup Gemini API
def setup_gemini():
    """Configures Gemini API using environment variable"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "":
        raise ValueError("❌ Error: API Key is missing. Please set GEMINI_API_KEY.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

#  Extract Text from Image using Gemini
def extract_text_from_image(image_path):
    """Extracts text from an image using Google Gemini API (gemini-2.0-flash)"""
    try:
        model = setup_gemini()
        image = Image.open(image_path)
        prompt = "Extract all text from this image. Return only the text without additional commentary."
        response = model.generate_content([prompt, image])
        return response.text.strip() if response.text else "⚠️ No text found in image."
    except Exception as e:
        return f"❌ OCR Error: {str(e)}"

# Answer Questions Based on Extracted Text
def answer_question_from_text(extracted_text, question):
    """Uses Gemini to answer a question based on extracted text"""
    try:
        model = setup_gemini()
        prompt = f"Context:\n{extracted_text}\n\nQuestion: {question}\n\nAnswer concisely based on the provided text."
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "⚠️ No relevant answer found."
    except Exception as e:
        return f"❌ Error: {str(e)}"

#  Process PDF and Create Vectorstore
def process_pdf(pdf_path):
    """Processes and indexes a PDF file"""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    if not docs:
        return None, "⚠️ No content found in the PDF."

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=300, separators=[".", "؟", "\n", ":", "=", "/", " per ", " hundred ", " thousand "]
    )

    splits = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="all-minilm")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore, None

#  Create RAG Pipeline for PDF Question Answering
def create_rag_chain(vectorstore):
    """Creates a RAG-based retrieval system"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 7}) 
    llm = Ollama(model="llama3.2-vision")

    def query_rag(question):
        prompt = PromptTemplate(
            template="Context: {context}\n\nQuestion: {question}\n\n"
                     "Provide a **concise and direct answer** based on the document.",
            input_variables=["context", "question"]
        )
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | llm 
            | StrOutputParser()
        )
        return rag_chain.invoke(question)

    return query_rag
