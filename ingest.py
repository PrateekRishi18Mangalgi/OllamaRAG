import os
import faiss
import pickle
import numpy as np
import pytesseract
from ollama import embeddings


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Optional libraries for file type support
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

try:
    import docx
except ImportError:
    docx = None

# ------------------ Config ------------------
INDEX_FILE = "faiss_index"
DOCS_FILE = "docs.pkl"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ------------------ Helpers ------------------
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        if not PdfReader:
            raise ImportError("PyPDF2 is required for PDF files")
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text

    elif ext in [".jpg", ".jpeg", ".png"]:
        if not Image or not pytesseract:
            raise ImportError("Pillow and pytesseract are required for image files")
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".docx":
        if not docx:
            raise ImportError("python-docx is required for DOCX files")
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError(f"❌ Unsupported file type: {ext}")

# ------------------ Main ------------------
file_path = input("Enter filename: ").strip()
if not os.path.exists(file_path):
    print(f"❌ File '{file_path}' not found!")
    exit()

try:
    text = extract_text_from_file(file_path)
except Exception as e:
    print(f"❌ Error extracting text: {e}")
    exit()

if not text.strip():
    print("❌ No text found in the file")
    exit()

# Split into chunks
chunks = chunk_text(text)
print(f"✅ Extracted {len(chunks)} chunks from {file_path}")

# Create embeddings
vectors = []
for chunk in chunks:
    emb = embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
    vectors.append(emb)

vectors = np.array(vectors).astype("float32")

# Initialize FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# Save FAISS index + chunks
faiss.write_index(index, INDEX_FILE)
with open(DOCS_FILE, "wb") as f:
    pickle.dump(chunks, f)

print(f"✅ Ingested {len(chunks)} chunks into FAISS index")
