import sys
from pathlib import Path

CURRENT = Path(__file__).resolve()

for parent in CURRENT.parents:
    if (parent / "app").exists():
        sys.path.insert(0, str(parent))
        break


import streamlit as st
import asyncio
from app.core.config import THINK_MODEL, NON_THINK_MODEL
from langchain_ollama import ChatOllama
from datetime import datetime
from typing import AsyncGenerator

async def stream_finance_one_liners(thinking: bool = False) -> AsyncGenerator[str, None]:
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
    
    should_yield = False if thinking else True

    async for chunk in model.astream(input=messages):
        if should_yield: yield chunk.content
        if thinking and chunk.content.strip() == '</think>': should_yield = not should_yield


st.set_page_config(page_title="Finance Co-pilot", layout="centered")

st.title("💸 Finance Co-pilot")
st.subheader("Your AI-powered assistant for smarter money decisions")

placeholder = st.empty()

def run_stream():
    async def runner():
        text = ""
        async for chunk in stream_finance_one_liners():
            text += chunk 
            placeholder.text(text)

    asyncio.run(runner())


if st.button("Hi"):
    run_stream()