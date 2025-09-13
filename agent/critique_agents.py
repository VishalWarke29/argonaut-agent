# ------------------------------
# ✅ Updated critique_agents.py
# ------------------------------
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from langchain_openai import ChatOpenAI
import os

from langchain_core.runnables import RunnableLambda


def run_critique_agent(persona, text, openai_api_key=None, local_model_path=None):
    template = """You are a {persona}. Given the following paper excerpt, provide a critique:

{text}

Respond with a critical analysis considering clarity, originality, and methodology.
"""

    prompt = PromptTemplate(
        input_variables=["persona", "text"],
        template=template
    )

    # Initialize LLM
    if openai_api_key:
        llm = ChatOpenAI(api_key=openai_api_key, temperature=0.7)
    elif local_model_path:
        if not os.path.exists(local_model_path):
            raise FileNotFoundError(f"❌ Model not found at {local_model_path}")
        # Dynamically select backend
        backend = "llama" if ".gguf" in local_model_path else "gptj"
        llm = GPT4All(model=local_model_path, backend=backend, verbose=False)
    else:
        raise ValueError("Missing LLM: provide OpenAI API key or local model path")

    # Use Runnable prompt pipeline (recommended)
    chain = prompt | llm
    response = chain.invoke({"persona": persona, "text": text})

    # Handle AIMessage type return
    if hasattr(response, "content"):
        return response.content
    return str(response)
