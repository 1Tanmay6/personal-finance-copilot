import time
import asyncio
from langchain_ollama import ChatOllama
from datetime import datetime
from app.core.config import NON_THINK_MODEL, THINK_MODEL

async def main(thinking: bool = False) -> str:
    prompt  = f"""ROLE: Finance Copilot

    - ALLOWED TOPICS: money, saving, spending, investing, budgeting, financial goals only.
    - STYLE: witty, fun, marketing-style one-liners (short + impactful).
    - FORMAT RULES (MANDATORY):
            - you can add something like 'welcome' or something.
            - Output exactly ONE sentence
            - One-liner only
            - No extra words, no commentary, no lists
            - If the topic is outside finance, redirect with a finance-related one-liner. We are in {datetime.now()}"""

    messages = [
            ("system", prompt),
            ("human", "Hi"),
        ]
    
    model = ChatOllama(
        model=THINK_MODEL if thinking else NON_THINK_MODEL,
        validate_model_on_init=True,
        temperature=0.8
    )    
    
    values = []
    should_print = False if thinking else True

    async for chunk in model.astream(input=messages):
        if should_print: print(chunk.content, end='', flush=True)
        if thinking and chunk.content.strip() == '</think>': should_print = not should_print
        values.append(chunk.content)
    print()

    return ''.join(values)

if __name__ == "__main__":
    st = time.time()
    asyncio.run(main(thinking=False))
    en = time.time()
    print(f"Time taken for the model to respond: {en-st}")