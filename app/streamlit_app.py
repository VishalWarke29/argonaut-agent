# ✅ Redesigned Argonaut UI with Aligned Theme Toggle
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit.components.v1 import html
from dotenv import load_dotenv
from agent.pdf_parser import parse_pdf
from agent.embedder import embed_text_chunks
from agent.qa_agent import ask_question
from agent.visualizer import extract_concepts, build_concept_graph, render_graph
from agent.hypothesis import suggest_hypotheses
from agent.memory import save_to_memory, display_memory
from agent.arxiv_fetcher import fetch_arxiv_papers
from agent.critique_agents import run_critique_agent
from fpdf import FPDF

# ===============
# 🌍 ENV & CONFIG
# ===============
load_dotenv()
os.makedirs("models", exist_ok=True)
st.set_page_config(page_title="Argonaut Research Agent", layout="wide")

# =====================
# 🌗 TOP-RIGHT THEME TOGGLE
# =====================
theme_toggle = """
<style>
#theme-toggle {
    position: fixed;
    top: 12px;
    right: 70px;
    z-index: 1000;
}
.switch {
    position: relative;
    display: inline-block;
    width: 44px;
    height: 24px;
}
.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}
.slider {
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;
}
.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}
input:checked + .slider {
    background-color: #444;
}
input:checked + .slider:before {
    transform: translateX(20px);
}
</style>
<div id=\"theme-toggle\">
  <label class=\"switch\">
    <input type=\"checkbox\" id=\"themeSwitch\" onchange=\"toggleTheme()\" />
    <span class=\"slider\"></span>
  </label>
</div>
<script>
let currentTheme = localStorage.getItem('theme') || 'dark';
document.getElementById("themeSwitch").checked = currentTheme === 'dark';
function toggleTheme() {
    let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    location.reload();
}
</script>
"""
html(theme_toggle)

# Apply theme based on session/localStorage
if "theme" not in st.session_state:
    st.session_state["theme"] = os.environ.get("STREAMLIT_THEME", "dark")

is_dark = st.session_state["theme"] == "dark"
st.markdown(f"""
<style>
body, .stApp {{
    background-color: {'#0E1117' if is_dark else '#FFFFFF'} !important;
    color: {'#F0F2F6' if is_dark else '#202020'} !important;
}}
.stButton > button {{
    background-color: #4A90E2; color: white;
    padding: 0.5rem 1rem; border-radius: 6px; transition: 0.3s ease;
}}
.stButton > button:hover {{ background-color: #3B7ED0; }}
.stTextInput input, .stTextArea textarea, .stSelectbox div {{
    border-radius: 6px !important;
}}
</style>
""", unsafe_allow_html=True)

# =====================
# 📌 SIDEBAR
# =====================
with st.sidebar:
    # st.image("path/to/logo.png", width=180)  # TODO: Uncomment when logo available
    st.markdown("### ⚙️ LLM Configuration")
    mode = st.radio("Choose Mode", ["OpenAI (cloud)", "GPT4All (offline)"], index=1)
    openai_api_key = st.text_input("🔑 OpenAI API Key", type="password") if mode == "OpenAI (cloud)" else None
    local_model_path = None

    if mode == "GPT4All (offline)":
        models = [f for f in os.listdir("./models") if f.endswith((".bin", ".gguf"))]
        if models:
            selected_model = st.selectbox("🧠 Local Model", models)
            local_model_path = os.path.join("./models", selected_model)
            st.success(f"Selected: {selected_model}")
        else:
            st.warning("No models found in /models")
            st.markdown("⬇️ [Download GPT4All Models](https://gpt4all.io/index.html#models)")
            st.stop()

    option = st.selectbox("📘 Mode", ["Upload PDF", "Search ArXiv"])

# =====================
# 📌 MAIN LAYOUT (Centered)
# =====================
st.markdown("""
    <div style='text-align: center; padding-top: 2rem;'>
        <h1 style='font-size: 2.5rem;'>🧠 Argonaut: Agentic Research Navigator</h1>
        <h4>Welcome to Argonaut: Your AI-powered Research Agent 🚀</h4>
    </div>
""", unsafe_allow_html=True)

if not openai_api_key and mode == "OpenAI (cloud)":
    st.markdown("""
        <div style='display: flex; justify-content: center; margin-top: 20px;'>
            <div style='background-color: #6b5b1f; padding: 10px 20px; border-radius: 6px; color: white;'>
                🔑 Please enter your OpenAI API key in the sidebar to proceed.
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 🔁 MAIN APP CONTINUES BELOW WITH EXISTING LOGIC (unchanged backend)
# You can paste your PDF and ArXiv logic after this block...

# Example stub (remove when full logic pasted):
# if option == "Upload PDF":
#     uploaded_file = st.file_uploader("Upload PDF")
#     ...
# elif option == "Search ArXiv":
#     query = st.text_input("Search")
#     ...




# with st.sidebar:
#     mode = st.radio("⚙️ Choose LLM Mode", ["OpenAI (cloud)", "GPT4All (offline)"])
#     openai_api_key = None
#     local_model_path = None

#     if mode == "OpenAI (cloud)":
#         openai_api_key = st.text_input("🔑 OpenAI API Key", type="password", key="openai_key_input")

#     elif mode == "GPT4All (offline)":
#         model_dir = "./models"
#         available_models = [f for f in os.listdir(model_dir) if f.endswith((".bin", ".gguf"))]

#         if available_models:
#             selected_model = st.selectbox("🧠 Choose GPT4All Model", available_models)
#             local_model_path = os.path.join(model_dir, selected_model)
#             st.session_state["selected_model_path"] = local_model_path
#             st.success(f"Using model: {selected_model}")
#         else:
#             st.warning("⚠️ No .bin or .gguf models found in `/models` folder.")
#             st.markdown("⬇️ [Download GPT4All Models](https://gpt4all.io/index.html#models)")
#             st.stop()

#     option = st.selectbox("📘 Mode", ["Upload PDF", "Search ArXiv"])

# if mode == "GPT4All (offline)":
#     local_model_path = st.session_state.get("selected_model_path")

# if not openai_api_key and mode == "OpenAI (cloud)":
#     st.warning("Please enter your OpenAI API key in the sidebar to proceed.")
#     st.stop()

# ========================
# 📄 Upload PDF Mode
# ========================
if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], key="pdf_uploader")

    if uploaded_file:
        if not st.session_state.pdf_text:
            text = parse_pdf(uploaded_file)
            st.session_state.pdf_text = text
            st.session_state.pdf_chunks = text.split("\n")
            st.session_state.vectorstore_pdf = embed_text_chunks(
                st.session_state.pdf_chunks, source_name=uploaded_file.name)

        st.success("✅ PDF uploaded and parsed.")
        st.text_area("📜 Extracted Text Preview", st.session_state.pdf_text[:2000], height=300)

        question = st.text_input("Enter a question about the paper", key="pdf_q")
        if st.button("Ask", key="pdf_ask") and question:
            answer = ask_question(
                st.session_state.vectorstore_pdf,
                question,
                openai_api_key=openai_api_key if mode == "OpenAI (cloud)" else None,
                local_model_path=local_model_path
            )
            st.session_state.last_pdf_answer = answer
            save_to_memory(question, answer, context=uploaded_file.name)

        if st.session_state.last_pdf_answer:
            st.success("💬 Answer:")
            st.write(st.session_state.last_pdf_answer)

        if st.button("Suggest Hypotheses", key="pdf_hypo"):
            ideas = suggest_hypotheses(
                st.session_state.pdf_text,
                api_key=openai_api_key if mode == "OpenAI (cloud)" else None,
                local_model_path=local_model_path
            )
            st.session_state.hypotheses_pdf = ideas
            save_to_memory("Hypotheses", ideas, context=uploaded_file.name)

        if st.session_state.hypotheses_pdf:
            st.markdown(st.session_state.hypotheses_pdf)

        import streamlit.components.v1 as components

        if st.button("Generate Concept Map", key="concept_map") or not st.session_state.concept_map_path:
            concepts = extract_concepts(st.session_state.pdf_text)
            graph = build_concept_graph(concepts)
            st.session_state.concept_map_path = render_graph(graph)

        if st.session_state.concept_map_path:
            st.markdown("### 🧠 Concept Map (Interactive)")
            with open(st.session_state.concept_map_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                components.html(html_content, height=600, scrolling=True)

        persona = st.selectbox("Choose Persona", ["Researcher", "Reviewer", "Explainer"], key="pdf_persona")
        if st.button("Run Critique", key="pdf_critique"):
            critique = run_critique_agent(
                persona,
                st.session_state.pdf_text[:3000],
                openai_api_key=openai_api_key if mode == "OpenAI (cloud)" else None,
                local_model_path=local_model_path
            )
            st.session_state.critique_pdf = critique

        if st.session_state.critique_pdf:
            st.markdown(f"**🧠 {persona} says:**")
            st.write(st.session_state.critique_pdf)

        st.subheader("📚 Recent Memory (Q&A)")
        memory = display_memory()
        for item in memory[-5:][::-1]:
            st.markdown(f"**Q:** {item['question']}")
            st.markdown(f"**A:** {item['answer']}")
            if item.get("context"):
                st.markdown(f"_📎 Context: {item['context']}_")

        if st.button("📄 Export Q&A to PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Paper: {uploaded_file.name}\n\n")
            if st.session_state.last_pdf_answer:
                pdf.multi_cell(0, 10, f"Q: {question}\nA: {st.session_state.last_pdf_answer}\n\n")
            if st.session_state.hypotheses_pdf:
                pdf.multi_cell(0, 10, "Hypotheses:\n" + st.session_state.hypotheses_pdf + "\n")
            if st.session_state.critique_pdf:
                pdf.multi_cell(0, 10, f"Critique ({persona}):\n{st.session_state.critique_pdf}")
            output_path = f"report_{uploaded_file.name.replace('.pdf','')}.pdf"
            pdf.output(output_path)
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name=output_path, mime="application/pdf")

# ========================
# 🌐 Search ArXiv Mode
# ========================
elif option == "Search ArXiv":
    arxiv_query = st.text_input("🔍 Enter arXiv query", "transformers for biology")
    num_results = st.slider("🔐 Number of papers", 1, 10, 3)

    if st.button("Search arXiv") and arxiv_query:
        with st.spinner("🔎 Searching..."):
            papers = fetch_arxiv_papers(arxiv_query, max_results=num_results)

        if not papers:
            st.warning("⚠️ No papers found.")
        else:
            st.session_state.arxiv_chunks = []
            st.subheader("📄 Retrieved Papers")
            for paper in papers:
                st.markdown(f"### {paper['title']}")
                st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
                st.markdown(f"🔗 [PDF]({paper.get('pdf_url', paper.get('url', '#'))})")
                st.markdown(f"🧠 {paper['summary'][:800]}...")
                st.session_state.arxiv_chunks.extend(paper['summary'].split("\n"))

            st.session_state.vectorstore_arxiv = embed_text_chunks(
                st.session_state.arxiv_chunks, source_name="arxiv_search")

    st.subheader("🤖 Ask a Question about These Papers")
    arxiv_question = st.text_input("Ask your question here (arXiv)", key="arxiv_q")
    if st.button("Ask ArXiv") and st.session_state.vectorstore_arxiv:
        st.session_state.arxiv_answer = ask_question(
            st.session_state.vectorstore_arxiv,
            st.session_state.arxiv_q,
            openai_api_key if mode == "OpenAI (cloud)" else None,
            local_model_path=local_model_path
        )

    if st.session_state.arxiv_answer:
        st.success("💬 Answer:")
        st.write(st.session_state.arxiv_answer)

    st.subheader("🧪 Suggest Hypotheses (arXiv)")
    if st.button("Suggest Hypotheses from ArXiv") and st.session_state.arxiv_chunks:
        combined_text = "\n".join(st.session_state.arxiv_chunks)
        st.session_state.arxiv_hypotheses = suggest_hypotheses(
            combined_text,
            api_key=openai_api_key if mode == "OpenAI (cloud)" else None,
            local_model_path=local_model_path
        )

    if st.session_state.arxiv_hypotheses:
        st.markdown(st.session_state.arxiv_hypotheses)