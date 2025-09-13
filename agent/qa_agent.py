# -------------------------
# 📁 agent/qa_agent.py
# -------------------------
import os
from langchain.chains import RetrievalQA
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI
from langchain_community.llms import GPT4All

def ask_question(vectorstore, question, openai_api_key=None, local_model_path=None):
    if openai_api_key:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, api_key=openai_api_key)
    elif local_model_path:
        if not os.path.exists(local_model_path):
            raise FileNotFoundError("GPT4All model not found")

        # 🧠 Auto-detect backend
        model_name = os.path.basename(local_model_path).lower()
        if ".gguf" in model_name or "mistral" in model_name:
            backend = "llama"
        elif "gpt4all-j" in model_name:
            backend = "gptj"
        else:
            backend = "auto"

        llm = GPT4All(model=local_model_path, backend=backend, verbose=False)

    else:
        raise ValueError("Must provide OpenAI key or local path")

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    return qa.run(question)