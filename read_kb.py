import os

def read_knowledge_base():

    try:
        with open('./kb.md', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading knowledge base file: {e}")
        return ""
