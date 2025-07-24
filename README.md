# **GitaGPT – English‑only Bhagavad‑Gita Chatbot**

🔱 *Ask Lord Kṛṣṇa anything… in your browser.*
Fast, offline embeddings + Groq’s **gemma‑2 9B‑IT** deliver contextual answers with cited shlokas—and a kid‑friendly summary line.

---

## Description

GitaGPT is a lightweight **Streamlit** chatbot that serves concise, citation‑rich answers to any question about the *Bhagavad‑Gītā*.

* 💡 Retrieves the most relevant shlokas from an on‑disk FAISS vectorstore (MiniLM embeddings)
* ⚡️ Generates English explanations using Groq’s ultra‑fast **gemma‑2 9B‑IT** model
* 👶 Adds a one‑line "kid version" so even young readers can grasp the teaching
* 🔗 Shows chapter & verse numbers *and* full IAST text, so you can verify every claim

## ✨ Key Features

| What                                       | Why it matters                                                      |
| ------------------------------------------ | ------------------------------------------------------------------- |
| **Adult answer + kid line**                | Makes wisdom accessible to all ages.                                |
| **Verse citations & IAST text**            | Trace every statement back to scripture.                            |
| **“Loading embedding vectors…” only once** | Embeddings are cached with `@st.cache_data` for snappy reloads.     |
| **🤔 Thinking spinner**                    | Clear feedback while the LLM works.                                 |
| **Streaming output**                       | Words appear instantly via `st.write_stream`, no next‑question lag. |
| **Groq gemma‑2 9B‑IT**                     | Open‑weights model served by Groq’s blazing low‑latency API.        |
| **FAISS local vectorstore**                | Mil‑second semantic retrieval; no external DB needed.               |

---

## 📸 Demo

> *<img width="1904" height="1012" alt="image" src="https://github.com/user-attachments/assets/f532c228-0cfe-4194-93af-864da973045e" />
*

---

## 🚀 Quick Start

```bash
# 1. Clone & enter the project
$ git clone https://github.com/<your‑org>/gita‑gpt.git
$ cd gita‑gpt

# 2. Create a virtual env (Python ≥ 3.10)
$ python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install requirements
$ pip install -r requirements.txt

# 4. Add your Groq API key
$ cp .env.example .env            # then edit .env
# ── or ──
$ echo "GROQ_API_KEY=sk_..." >> .env

# 5. Run the app
$ streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) and start chatting!

---

## 🗂️ Project Structure

```text
├── app.py                # Streamlit UI & main loop
├── bhagvatgeeta_new/     # FAISS index (768‑dim MiniLM vectors)
├── requirements.txt      # Pinned dependencies
├── .env.example          # Template for secrets
└── README.md             # You are here ✨
```

---

## 🔧 Configuration

| Variable       | Default            | Description                                |
| -------------- | ------------------ | ------------------------------------------ |
| `GROQ_API_KEY` | **required**       | Your Groq Cloud API key.                   |
| `MODEL_NAME`   | `gemma2-9b-it`     | Change if you deploy a different model.    |
| `EMBED_MODEL`  | `all-MiniLM-L6-v2` | Any sentence‑transformers model will work. |

---

## 🏗️ How It Works

1. **Embeddings**: `sentence‑transformers/all‑MiniLM‑L6‑v2` encodes each shloka once; vectors are stored in FAISS.
2. **Retrieval**: The user query is embedded and the k‑nearest verses are fetched.
3. **Prompting**: A handcrafted system prompt enforces tone, structure, and citation rules.
4. **LLM**: Groq’s hosted **gemma‑2 9B‑IT** generates the answer.
5. **Streaming**: Words are yielded one by one to the UI.

---

## 🤝 Contributing

1. Fork the repo & create your branch: `git checkout -b feature/awesome`
2. Commit your changes: `git commit -m 'Add awesome feature'`
3. Push to the branch: `git push origin feature/awesome`
4. Open a Pull Request.

All contributions—code, docs, tests, ideas—are welcome!

---

## 📝 License

Licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgements

* \[Bhagavad‑Gītā Sārvapalli Radhakrishnan (translation)]
* [Groq](https://groq.com/) for the lightning‑fast LLM API
* [Hugging Face](https://huggingface.co/) & `sentence-transformers`
* [Streamlit](https://streamlit.io/) for effortless front‑end magic

*Jai Shri Krishna!*
