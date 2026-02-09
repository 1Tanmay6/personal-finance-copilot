import pytest
import sys
import time
from pathlib import Path

CURRENT = Path(__file__).resolve()

for parent in CURRENT.parents:
    if (parent / "app").exists():
        sys.path.insert(0, str(parent))
        break

from langchain_ollama import ChatOllama
from datetime import datetime
from typing import AsyncGenerator
from app.core.config import NON_THINK_MODEL, THINK_MODEL


async def stream_finance_one_liner(thinking: bool = False) -> AsyncGenerator[str, None]:
    prompt = f"""ROLE: Finance Copilot
- ALLOWED TOPICS: money, saving, spending, investing, budgeting, financial goals only.
- Output exactly ONE sentence.
- We are in {datetime.now()}"""

    messages = [
        ("system", prompt),
        ("human", "Hi"),
    ]

    model = ChatOllama(
        model=THINK_MODEL if thinking else NON_THINK_MODEL,
        temperature=0.8,
        validate_model_on_init=True,
    )

    should_yield = not thinking

    async for chunk in model.astream(input=messages):
        if should_yield:
            yield chunk.content

        if thinking and chunk.content.strip() == "</think>":
            should_yield = True

@pytest.mark.asyncio
async def test_stream_returns_text():
    chunks = []

    async for chunk in stream_finance_one_liner(thinking=False):
        chunks.append(chunk)

    full_text = "".join(chunks)

    assert isinstance(full_text, str)
    assert len(full_text.strip()) > 0


@pytest.mark.asyncio
async def test_stream_single_sentence():
    chunks = []

    async for chunk in stream_finance_one_liner(thinking=False):
        chunks.append(chunk)

    text = "".join(chunks).strip()

    # rough but practical check
    assert text.count(".") <= 1

@pytest.mark.asyncio
async def test_latency_under_10s():
    start = time.time()
    async for _ in stream_finance_one_liner():
        pass
    assert time.time() - start < 10