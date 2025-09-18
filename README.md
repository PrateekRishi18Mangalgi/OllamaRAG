A powerful Retrieval-Augmented Generation (RAG) system that allows you to upload documents and chat with them using local AI models. Built with FAISS for efficient similarity search and Ollama for local LLM inference.
✨ Features

Multi-format Support: PDF, DOCX, TXT, and image files (JPG, PNG)
OCR Capability: Extract text from images using Tesseract
Local Processing: No data sent to external APIs - everything runs locally
Efficient Search: FAISS-powered vector similarity search
Smart Chunking: Intelligent text splitting with overlap for better context
Easy to Use: Simple command-line interface

🚀 Quick Start
Prerequisites

Install Ollama and pull required models:

bash   # Install Ollama (visit ollama.ai for instructions)
   ollama pull nomic-embed-text
   ollama pull llama2

Install Tesseract OCR (for image processing):

Windows: Download from GitHub releases
macOS: brew install tesseract
Linux: sudo apt-get install tesseract-ocr



Installation

Clone the repository:

bash   git clone https://github.com/yourusername/LocalDocChat.git
   cd LocalDocChat

Install Python dependencies:

bash   pip install -r requirements.txt
Usage

Ingest a document:

bash   python ingest.py
Enter the path to your file when prompted.

Chat with your document:

bash   python chat.py
Ask questions about the content you just ingested!
📁 Project Structure
LocalDocChat/
├── ingest.py          # Document ingestion and indexing
├── chat.py            # Query interface
├── requirements.txt   # Python dependencies
├── README.md         # This file
├── faiss_index       # Generated FAISS index (after first run)
└── docs.pkl          # Stored document chunks (after first run)
🔧 Configuration
You can modify these settings in the code:

CHUNK_SIZE: Size of text chunks (default: 500)
CHUNK_OVERLAP: Overlap between chunks (default: 50)
k: Number of similar chunks to retrieve (default: 3)

For Windows users, update the Tesseract path in ingest.py:
pythonpytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
📋 Requirements
faiss-cpu
numpy
ollama
PyPDF2
python-docx
Pillow
pytesseract
pickle-mixin
🔄 How It Works

Document Ingestion:

Extract text from various file formats
Split text into overlapping chunks
Generate embeddings using nomic-embed-text
Store in FAISS index for fast retrieval


Query Processing:

Convert user question to embedding
Find most similar document chunks
Send context + question to llama2
Return AI-generated answer



🎯 Supported File Types
FormatExtensionRequirementsPDF.pdfPyPDF2Word Document.docxpython-docxText.txtBuilt-inImages.jpg, .jpeg, .pngPillow + Tesseract
🛠️ Troubleshooting
Common Issues:

ModuleNotFoundError: Install missing dependencies with pip
Tesseract not found: Ensure Tesseract is installed and path is correct
Ollama connection error: Make sure Ollama is running (ollama serve)
Empty text extraction: Check if file is not corrupted or password-protected

🤝 Contributing

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
