from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL
# from config import GROQ_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Generates a grounded response using only the retrieved text chunks as context.
    """
    fallback_msg = "I'm sorry, but I cannot find the answer to that question in the provided rule books."
    
    if not retrieved_chunks:
        return fallback_msg

    # Format the context visually for the LLM
    context_blocks = []
    for chunk in retrieved_chunks:
        block = f"=== START CHUNK (Game: {chunk['game']}) ===\n{chunk['text']}\n=== END CHUNK ==="
        context_blocks.append(block)
        
    formatted_context = "\n\n".join(context_blocks)
    
    # Construct the strict system prompt
    system_prompt = (
        "You are RulesBot, an expert helper that settles board game rule disputes.\n"
        "CRITICAL INSTRUCTION: Answer the user's question using ONLY the provided rules text context.\n"
        "Do not use any external knowledge or fill in gaps from memory. You must cite which game "
        "the rule comes from explicitly.\n"
        f"If the answer cannot be fully and completely found in the context chunks, reply exactly with: '{fallback_msg}'"
    )
    
    user_prompt = f"Context:\n{formatted_context}\n\nQuestion: {query}"
    
    try:
        completion = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0  # Keep responses deterministic and closely anchored to text
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"
