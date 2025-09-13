# 🧠 Argonaut: Agentic Research Navigator

Argonaut is an intelligent research assistant built with Streamlit and Python. It allows users to upload PDFs or search scientific literature, then interact with AI-powered tools for summarization, question answering, hypothesis generation, concept mapping, and critique.

---

## ✨ Features

- 📄 Upload PDF and parse full content
- 🔍 Ask questions and get intelligent answers (LLM-powered)
- 💡 Generate novel hypotheses from research context
- 🗺️ Visualize concepts with interactive graph maps
- 🧑‍🔬 Critique papers from multiple expert personas (e.g., Researcher, Reviewer, Explainer)
- 📚 Memory view: shows history of Q&A with context
- 🧾 Export answers and hypotheses into downloadable PDF reports
- 🌗 Toggle dark/light mode UI

---

## 📁 Project Structure

```
argonaut/
├── app/
│   └── streamlit_app.py         # Main Streamlit UI
├── agent/
│   ├── pdf_parser.py            # PDF reading logic
│   ├── embedder.py              # Embedding logic
│   ├── qa_agent.py              # LLM-based QA
│   ├── visualizer.py            # Concept graph visualization
│   ├── hypothesis.py            # Hypothesis generation
│   ├── memory.py                # Memory system
│   ├── arxiv_fetcher.py         # ArXiv paper fetcher
│   └── critique_agents.py       # AI critique system
├── models/                      # (Optional) Local models for GPT4All
├── static/                      # Stores generated concept maps
```

---

## ⚙️ Configuration

- Add `.env` file in root (optional for API keys)
- Place any GPT4All `.bin` or `.gguf` files in `/models` if using offline mode

---

## 📦 Dependencies

Make sure to install all dependencies with:

```bash
pip install -r requirements.txt
```

Recommended packages include:
- `streamlit`
- `openai`
- `fpdf`
- `spacy`
- `pyvis`
- `networkx`
- `pdfplumber`
- `sentence-transformers`
- `python-dotenv`

---

## 📝 Notes

- The app supports both OpenAI-based and offline GPT4All-based modes.
- Default theme is dark; toggle top-right for light mode.
- Concept maps are interactive and rendered via HTML.
- Critiques are generated based on selected personas.

---
