import os
from dotenv import load_dotenv
import streamlit as st
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory

from chatbot_utility import get_chapter_list
from get_yt_video import get_yt_video_link


# Load environment variables
load_dotenv()
DEVICE = os.getenv('DEVICE', 'cpu')

working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

data_dir = os.path.join(parent_dir, "data_original")

# Dynamically get Levels
levels_list = [
    folder for folder in os.listdir(data_dir)
    if os.path.isdir(os.path.join(data_dir, folder))
]


# =========================
# Vector DB Path Logic
# =========================
def get_vector_db_path(level, subject, chapter):

    if chapter == "All Chapters":
        return os.path.join(
            parent_dir,
            "vector_db",
            f"{level}_{subject}_vector_db"
        )

    return os.path.join(
        parent_dir,
        "chapters_vector_db",
        f"{level}_{subject}_{chapter}"
    )


# =========================
# Setup Chain
# =========================
def setup_chain(level, subject, chapter):

    vector_db_path = get_vector_db_path(level, subject, chapter)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": DEVICE}
    )

    vectorstore = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embeddings
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    memory = ConversationBufferMemory(
        llm=llm,
        output_key='answer',
        memory_key='chat_history',
        return_messages=True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        get_chat_history=lambda h: h,
        verbose=False
    )

    return chain


# =========================
# Streamlit UI
# =========================

st.set_page_config(
    page_title="IntellPrep - AI Study Assistant",
    page_icon="assets/logo.png",
    layout="centered"
)

col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.png", width=80)

with col2:
    st.title("IntelliPrep")

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_history" not in st.session_state:
    st.session_state.video_history = []


# =========================
# Level Selection
# =========================
selected_level = st.selectbox(
    "Select Level",
    levels_list,
    index=None
)

if selected_level:

    # Get subjects dynamically
    subject_path = os.path.join(data_dir, selected_level)
    subjects_list = [
        folder for folder in os.listdir(subject_path)
        if os.path.isdir(os.path.join(subject_path, folder))
    ]

    selected_subject = st.selectbox(
        "Select Subject",
        subjects_list,
        index=None
    )

    if selected_subject:

        chapter_list = get_chapter_list(selected_level, selected_subject)
        chapter_list.append("All Chapters")

        selected_chapter = st.selectbox(
            "Select Chapter",
            chapter_list,
            index=0
        )

        if selected_chapter:

            if (
                st.session_state.get("selected_chapter") != selected_chapter
                or st.session_state.get("selected_subject") != selected_subject
            ):
                st.session_state.chat_chain = setup_chain(
                    selected_level,
                    selected_subject,
                    selected_chapter
                )

            st.session_state.selected_chapter = selected_chapter
            st.session_state.selected_subject = selected_subject


# =========================
# Display Chat History
# =========================
for idx, message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and idx < len(st.session_state.video_history):
            video_refs = st.session_state.video_history[idx]
            if video_refs:
                st.subheader("Video Reference")
                for title, link in video_refs:
                    st.info(f"{title}\n\nLink: {link}")


# =========================
# Chat Input
# =========================
user_input = st.chat_input("Ask A Question...")

if user_input:

    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.video_history.append(None)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        response = st.session_state.chat_chain(
            {"question": user_input}
        )

        st.markdown(response['answer'])

        video_titles, video_links = get_yt_video_link(user_input)

        st.subheader("Video Reference")

        video_refs = []
        for i in range(min(3, len(video_titles))):
            st.info(f"{video_titles[i]}\n\nLink: {video_links[i]}")
            video_refs.append((video_titles[i], video_links[i]))

        st.session_state.chat_history.append(
            {"role": "assistant", "content": response['answer']}
        )
        st.session_state.video_history.append(video_refs)