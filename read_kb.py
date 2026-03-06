import os

def read_knowledge_base():

    content = os.getenv("KNOWLEDGE_BASE_CONTENT", "")
    if not content:
        raise ValueError("KNOWLEDGE_BASE_CONTENT environment variable is not set")
    print(f"KB loaded: {len(content)} chars")
    return content

