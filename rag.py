from sys_prompt import USER_PROMPT, SYSTEM_PROMPT
from conn import client
from vector_srch import vector_store

def run_rag(query: str) -> str:
    # 1. retrieve context
    context = vector_store(query)

    # 2. build prompt
    formatted_user_prompt = USER_PROMPT.format(context=context, query=query)

    # 3. LLM call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": formatted_user_prompt},
        ],
    )

    return response.choices[0].message.content


    

if __name__ == "__main__":
    query = "tell me about his experience"
    result = run_rag(query)
    print(result)