import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DEVICE = os.getenv("DEVICE", "cpu")

# Get project root
working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

# Folder paths
data_dir = os.path.join(parent_dir, "data_original")
vector_db_dir = os.path.join(parent_dir, "vector_db")
chapters_vector_db_dir = os.path.join(parent_dir, "chapters_vector_db")

# Ensure vector folders exist
os.makedirs(vector_db_dir, exist_ok=True)
os.makedirs(chapters_vector_db_dir, exist_ok=True)

# Better text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Stable embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": DEVICE}
)


# =====================================
# Book Level Vectorization
# =====================================
def vectorize_book_and_store_to_db(level, subject_name, vector_db_name):

    book_dir = os.path.join(data_dir, level, subject_name)

    if not os.path.exists(book_dir):
        print(f"Directory not found: {book_dir}")
        return

    documents = []

    for file in os.listdir(book_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(book_dir, file)

            try:
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
                print(f"Loaded: {file}")
            except Exception as e:
                print(f"Error loading {file}: {e}")

    if not documents:
        print(f"No PDFs found in {book_dir}")
        return

    text_chunks = text_splitter.split_documents(documents)

    vector_db_path = os.path.join(vector_db_dir, vector_db_name)

    Chroma.from_documents(
        documents=text_chunks,
        embedding=embedding,
        persist_directory=vector_db_path
    )

    print(f"{level}/{subject_name} book saved to vector DB.")


# =====================================
# Chapter Level Vectorization
# =====================================
def vectorize_chapters(level, subject_name):

    book_dir = os.path.join(data_dir, level, subject_name)

    if not os.path.exists(book_dir):
        print(f"Directory not found: {book_dir}")
        return

    for file in os.listdir(book_dir):

        if not file.lower().endswith(".pdf"):
            continue

        chapter_name = file[:-4]
        pdf_path = os.path.join(book_dir, file)

        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue

        texts = text_splitter.split_documents(documents)

        chapter_vector_path = os.path.join(
            chapters_vector_db_dir,
            f"{level}_{subject_name}_{chapter_name}"
        )

        Chroma.from_documents(
            documents=texts,
            embedding=embedding,
            persist_directory=chapter_vector_path
        )

        print(f"{level}/{subject_name}/{chapter_name} chapter vectorized.")