# -------------------------
# 📁 agent/memory.py
# -------------------------
import os
import json
from datetime import datetime

MEMORY_FILE = "memory.json"

def save_to_memory(question, answer, context=None):
    memory = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            memory = []
    memory.append({
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "context": context
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def display_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
