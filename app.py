"""
GitaGPT – English‑only Streamlit chatbot.

• adult answer + kid line + referenced verses (IAST)
• shows “Loading embedding vectors…” once at startup
• shows 🤔 Thinking spinner for each question
• uses Groq gemma‑2 9B‑IT  (put GROQ_API_KEY in .env)
"""

import os, re, json, textwrap, time
import streamlit as st
from dotenv import load_dotenv
from io import StringIO

from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# ─── 0.  Env / API key check ──────────────────────────────
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY missing in .env"); st.stop()

# ─── 1.  Page & CSS ───────────────────────────────────────
st.set_page_config("Bhagavad Gita GPT)", "🚩", layout="wide")
st.markdown("""
<style>
.section{font-size:19px;font-weight:700;margin:18px 0 6px;}
.answer{font-size:18px;margin:4px 0 12px;}
.ref-line{font-size:18px;font-weight:700;color:#0b3d91;margin:14px 0 2px;}
.shloka{font-size:17px;font-style:italic;margin:0 0 14px;}
</style>
""", unsafe_allow_html=True)

# ─── 2.  Sidebar (sample questions) ───────────────────────
samples = [
    "What is the significance of the Kṣetra–Kṣetreśvara concept?",
    "How does the Gita reconcile karma and free will?",
    "Explain Jñāna Yoga vs Karma Yoga.",
]
with st.sidebar:
    st.title("Bhagavad Gita GPT 📖")
    st.write("Sample questions:")
    for q in samples: st.caption(q)
    st.markdown("<small>Model can err — verify verses.</small>", unsafe_allow_html=True)

# ─── 3.  Embeddings + FAISS (cached, show spinner) ─────────
with st.spinner("🔄 Loading embedding vectors…"):
    @st.cache_data(show_spinner=False)
    def load_emb():
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if "emb" not in st.session_state:
        st.session_state.emb = load_emb()

@st.cache_resource(show_spinner=False)
def load_db():
    return FAISS.load_local("bhagvatgeeta_new",
                            embeddings=st.session_state.emb,
                            allow_dangerous_deserialization=True)
if "db" not in st.session_state:
    st.session_state.db = load_db()

retriever = st.session_state.db.as_retriever()   # let FAISS decide k

# ─── 4.  LLM (cached) ─────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_llm():
    return ChatGroq(model="gemma2-9b-it", max_tokens=4096)
if "llm" not in st.session_state:
    st.session_state.llm = load_llm()

# ─── 5.  Long English prompt with your rules ──────────────
prompt_template = textwrap.dedent("""
O Partha,

Task: Answer questions based on the Bhagavad Gita in **English**, using the provided context.

Instructions (abridged):
• Retrieve relevant verses and summarise the key points.  
• Mention chapter & verse numbers and quote the shlokas (IAST).  
• Begin with “O Partha” and end with “Jai Shri Krishna”.  
• Maintain a respectful tone, stay concise, accurate, focused, no programming help, no personal opinions outside the Gita.

If greeted, greet; if thanked, thank; if forced off‑topic, reply “Sorry, Jai Shri Krishna!”.  
If unsure, say “I’m not sure yet, please ask something else. Jai Shri Krishna”.

<context>
{context}
</context>
Question: {input}
""")

prompt = ChatPromptTemplate.from_template(prompt_template)

# ─── 6.  Retrieval + LLM chain ────────────────────────────
chain = create_retrieval_chain(
    retriever,
    create_stuff_documents_chain(st.session_state.llm, prompt)
)

# ─── 7.  Stream helper ────────────────────────────────────
def stream_words(text, speed=0.03):
    for w in text.split():
        yield w + " "
        time.sleep(speed)

# ─── 8.  Chat history helpers ─────────────────────────────
if "hist" not in st.session_state: st.session_state.hist=[]
def log(role, body): st.session_state.hist.append({"role": role, "content": body})
def replay():        # show old messages on reload
    for m in st.session_state.hist:
        with st.chat_message(m["role"]):
            st.markdown(m["content"], unsafe_allow_html=True)

# ─── 9.  Main loop ────────────────────────────────────────
replay()
query = st.chat_input("Ask your Gita question…")
if query:
    # 9‑a.  Show the user’s message immediately
    with st.chat_message("user"):
        st.markdown(query)
    log("user", query)

    # 9‑b.  Generate the answer (spinner → LLM call)
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking…"):
            result = chain.invoke({"input": query})
        raw = result["answer"]          # full answer text

        # 9‑c.  **Stream** the words so the user sees them right away
        def word_gen(text: str):
            for w in text.split():
                yield w + " "
                time.sleep(0.03)        # typing speed‑feel

        st.write_stream(word_gen(raw))  # <-- built‑in Streamlit streaming
        log("assistant", raw)
