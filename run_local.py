#!/usr/bin/env python3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os

# 1) Point all OpenAI traffic at LM Studio
os.environ["OPENAI_BASE_URL"] = "http://10.220.63.201:1234/v1"
os.environ["OPENAI_API_KEY"] = "sk-lmstudio-local"

print("=" * 70)
print("TradingAgents + LM Studio (Qwen3-8B-Tool-Calling)")
print("=" * 70)
print(f"[SETUP] OPENAI_BASE_URL = {os.environ['OPENAI_BASE_URL']}")
print(f"[SETUP] OPENAI_API_KEY  = {os.environ['OPENAI_API_KEY']}")
print()

# 2) Patch langchain-openai ChatOpenAI
from langchain_openai import ChatOpenAI as OriginalChatOpenAI
_original_init = OriginalChatOpenAI.__init__

def patched_init(self, *args, **kwargs):
    # Force everything through LM Studio
    kwargs["base_url"] = "http://10.220.63.201:1234/v1"
    kwargs["api_key"] = "sk-lmstudio-local"
    kwargs["timeout"] = 300.0

    # If no model specified, default to your local one
    if "model" not in kwargs and "model_name" not in kwargs:
        kwargs["model"] = "qwen3-8b-tool-calling"

    print(f"[LLM] ChatOpenAI -> model={kwargs.get('model', kwargs.get('model_name'))}, "
          f"base_url={kwargs['base_url']}")
    return _original_init(self, *args, **kwargs)

OriginalChatOpenAI.__init__ = patched_init

print("[PATCH] ChatOpenAI globally patched to LM Studio\n")

# 3) Launch the CLI
from cli.main import app
app()

