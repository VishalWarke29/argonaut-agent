# -------------------------
# 📁 agent/hypothesis.py
# -------------------------

import os
from langchain_community.llms import GPT4All
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def suggest_hypotheses(text, api_key=None, local_model_path=None, n=3):
    prompt = f"""You are a research scientist. Based on the following text, suggest {n} possible research hypotheses or experimental directions:

{text[:3000]}

Start each suggestion with a dash (-).
"""

    try:
        if api_key:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)

        elif local_model_path:
            if not os.path.exists(local_model_path):
                return f"❌ Local model not found: {local_model_path}"

            # Auto-detect backend
            model_lower = local_model_path.lower()
            if "mistral" in model_lower:
                backend = "llama"
            elif "gpt4all-j" in model_lower or "groovy" in model_lower:
                backend = "gptj"
            else:
                backend = "auto"

            llm = GPT4All(model=local_model_path, backend=backend, verbose=False)

        else:
            return "❌ No LLM source provided (OpenAI key or local model path)."

        # ✅ Fix: handle both OpenAI and GPT4All return types
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"❌ Error generating hypotheses: {e}"