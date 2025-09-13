from langchain_community.llms import GPT4All

model_path = "models/mistral-7b-instruct-v0.1.Q4_0.gguf"

llm = GPT4All(
    model=model_path,
    backend="llama",   # ✅ This is important for Mistral/GGUF
    verbose=True
)

response = llm("What is the capital of France?")
print(response)