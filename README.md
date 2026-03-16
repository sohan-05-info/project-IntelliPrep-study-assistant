🚀 IntelliPrep – AI Study Assistant (Detailed Explanation):-

IntelliPrep is an intelligent AI-powered study assistant designed to help students interact with their textbooks in a conversational way. Instead of manually searching through PDFs, students can simply ask questions and receive context-aware answers generated using Retrieval-Augmented Generation (RAG).

🧠 Core Idea Behind IntelliPrep:-
Traditional study methods:

> Read long PDFs
> Manually search topics
> Watch random YouTube videos
> Waste time finding relevant information

IntelliPrep solves this by:

> Converting textbooks into vector embeddings
> Storing them in a vector database (ChromaDB)
> Retrieving only relevant content
> Generating structured answers using an LLM
> Suggesting related YouTube videos automatically

How to run?
> In terminal, active the virtual environment first and then type "streamlit src/main.py".


🧑‍🎓 Who Is It For?

> College students
> Competitive exam aspirants
> Engineering students
> Self-learners

Placement preparation candidates

⚙️ How IntelliPrep Works (Architecture Flow)
1️⃣ PDF Ingestion:-

> Student uploads or stores textbook PDFs.
> PDFs are split into smaller chunks.
> Each chunk is converted into embeddings using:
    sentence-transformers/all-MiniLM-L6-v2


2️⃣ Vector Storage (ChromaDB):-

Embeddings are stored in:

> vector_db/ (Book-level)
> chapters_vector_db/ (Chapter-level)
> This enables semantic search instead of keyword search.


3️⃣ User Question:-

Student asks:
“Explain Normalization in DBMS”

4️⃣ Retrieval (RAG):-

System:
> Converts user query into embedding
> Finds top relevant chunks using MMR search
> Sends only relevant content to LLM

This prevents hallucination and improves accuracy.

5️⃣ AI Answer Generation:-

Using: Groq LLM (LLaMA 3.3 70B)
The system generates:

> Context-based explanation
> Structured response
> Conversational style

6️⃣ YouTube Recommendation Engine:-

The system:
1. Takes user query
2. Searches YouTube using YouTubeSearchPython
3. Suggests top 3 relevant videos

This creates a hybrid learning experience: 
1. Text explanation
2. Video reinforcement


**Tech Stack**:- 

1. Frontend : **Streamlit**
2. LLM : **Groq (LLaMA 3.3 70B)**
3. Embeddings: **HuggingFace Transformers**
4. Vector DB: **ChromaDB**
5. Backend Logic: **LangChain**
6. PDF Loader: **PyPDFLoader**


📈 Future Expansion Possibilities:-

1. Resume-based question generation
2. Interview simulation
3. Performance analytics dashboard
4. User authentication
5. MCQ testing system
6. Admin panel
7. Cloud deployment
