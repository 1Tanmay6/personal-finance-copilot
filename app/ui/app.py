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
from app.core.database import Database
from app.core import get_logger
from app.services import DataService
from langchain_ollama import ChatOllama
from datetime import datetime
from typing import AsyncGenerator

logger = get_logger(__name__)

database = Database()
asyncio.run(database.db_check())
data_service = DataService(database)

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
    logger.info("Calling model for a quick one liner")

    try:
        model = ChatOllama(
            model=THINK_MODEL if thinking else NON_THINK_MODEL,
            validate_model_on_init=True,
            temperature=0.8
        )    
        
        should_yield = False if thinking else True

        logger.info("Starting stream")
        async for chunk in model.astream(input=messages):
            if should_yield: yield chunk.content
            if thinking and chunk.content.strip() == '</think>': should_yield = not should_yield
        logger.info("Stream completed")
    except Exception as e:
        logger.error("Calling ollama failed")
        st.text("See there is some issue connecting to ollama it is very unlikely that this code might be causing issue:\n1. Check if ollama is installed on your system\n2. Make sure you are serving the ollama (by `ollama serve`)")

st.set_page_config(page_title="Finance Co-pilot", layout="centered")

st.title("💸 Finance Co-pilot")
st.subheader("Your AI-powered assistant for smarter money decisions")

placeholder = st.empty()

def run_stream():
    logger.info("Generating one-liner")
    async def runner():
        text = ""
        async for chunk in stream_finance_one_liners():
            text += chunk 
            placeholder.text(text)

    asyncio.run(runner())


if st.button("Hi"):
    run_stream()