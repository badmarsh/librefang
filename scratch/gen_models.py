import json

models = [
    # fast
    {"id": "qwen3.6-flash", "display_name": "Qwen 3.6 Flash (Thinking)", "provider": "qwen", "tier": "fast", "aliases": ["monitor-agent-primary", "feed-triage", "fast"]},
    {"id": "qwen3.5-flash", "display_name": "Qwen 3.5 Flash", "provider": "qwen", "tier": "fast", "aliases": []},
    {"id": "qwen-flash", "display_name": "Qwen Flash", "provider": "qwen", "tier": "fast", "aliases": []},
    
    # standard
    {"id": "qwen-plus-latest", "display_name": "Qwen Plus Latest", "provider": "qwen", "tier": "standard", "aliases": ["qwen-plus", "outreach-agent-primary", "reply-drafter", "standard"]},
    
    # reasoning
    {"id": "qwen3.6-35b-a3b", "display_name": "Qwen 3.6 35B A3B (Thinking)", "provider": "qwen", "tier": "reasoning", "aliases": ["misinfo-classifier", "reasoning"]},
    {"id": "qwen3.6-27b", "display_name": "Qwen 3.6 27B (Thinking)", "provider": "qwen", "tier": "reasoning", "aliases": []},
    
    # flagship-reasoning
    {"id": "qwen3-235b-a22b", "display_name": "Qwen 3 235B A22B", "provider": "qwen", "tier": "flagship-reasoning", "aliases": ["orchestrator-primary", "investigator-agent-primary", "debunk-engine-primary", "flagship-reasoning"]},
    {"id": "qwen3.5-397b-a17b", "display_name": "Qwen 3.5 397B A17B", "provider": "qwen", "tier": "flagship-reasoning", "aliases": []},
    {"id": "qwen3-next-80b-thinking", "display_name": "Qwen 3 Next 80B Thinking", "provider": "qwen", "tier": "flagship-reasoning", "aliases": []},
    
    # flagship
    {"id": "qwen-max", "display_name": "Qwen Max", "provider": "qwen", "tier": "flagship", "aliases": ["flagship"]},
    {"id": "qwen3-next-80b-instruct", "display_name": "Qwen 3 Next 80B Instruct", "provider": "qwen", "tier": "flagship", "aliases": []},
    
    # coding
    {"id": "qwen3-coder-30b-a3b-instruct", "display_name": "Qwen 3 Coder 30B A3B Instruct", "provider": "qwen", "tier": "coding", "aliases": ["code-agent", "coding"]},
    
    # vision
    {"id": "qwen-vl-max-latest", "display_name": "Qwen VL Max Latest", "provider": "qwen", "tier": "vision", "aliases": ["visual-analyst-primary", "vision"]},
    {"id": "qwen3-vl-235b-a22b-instruct", "display_name": "Qwen 3 VL 235B A22B Instruct", "provider": "qwen", "tier": "vision", "aliases": ["visual-analyst-fast"]},
    
    # translation
    {"id": "qwen-mt-plus", "display_name": "Qwen MT Plus", "provider": "qwen", "tier": "translation", "aliases": ["translation-agent-primary", "translation"]},
    {"id": "qwen-mt-turbo", "display_name": "Qwen MT Turbo", "provider": "qwen", "tier": "translation", "aliases": ["translation-agent-fallback"]},
    {"id": "qwen-mt-flash", "display_name": "Qwen MT Flash", "provider": "qwen", "tier": "translation", "aliases": []},
    
    # long-context
    {"id": "qwen2.5-14b-instruct-1m", "display_name": "Qwen 2.5 14B Instruct 1M", "provider": "qwen", "tier": "long-context", "aliases": ["archive-agent-primary", "long-context"]},
    {"id": "qwen2.5-7b-instruct-1m", "display_name": "Qwen 2.5 7B Instruct 1M", "provider": "qwen", "tier": "long-context", "aliases": []},
    
    # embedding
    {"id": "text-embedding-v4", "display_name": "Text Embedding V4", "provider": "qwen", "tier": "embedding", "aliases": ["default-embedding", "embedding"]},
    {"id": "text-embedding-v3", "display_name": "Text Embedding V3", "provider": "qwen", "tier": "embedding", "aliases": []},
    
    # local
    {"id": "gemma2", "display_name": "Gemma 2 (Ollama)", "provider": "ollama", "tier": "local", "aliases": ["local"]},
    {"id": "qwen2.5vl", "display_name": "Qwen 2.5 VL (Ollama)", "provider": "ollama", "tier": "local", "aliases": []},
    
    # nvidia
    {"id": "nim-giant", "display_name": "NVIDIA NIM Giant (Llama 405B)", "provider": "nvidia", "tier": "nvidia", "aliases": ["nvidia"]},
    {"id": "llama-3.3-70b", "display_name": "Llama 3.3 70B (NVIDIA)", "provider": "nvidia", "tier": "nvidia", "aliases": []},
    
    # free (OpenRouter)
    {"id": "openrouter/google/gemma-2-9b-it:free", "display_name": "Gemma 2 9B (Free)", "provider": "openrouter", "tier": "free", "aliases": ["openrouter-free", "free"]},
    {"id": "openrouter/meta-llama/llama-3.3-70b-instruct", "display_name": "Llama 3.3 70B (OpenRouter)", "provider": "openrouter", "tier": "free", "aliases": []},
    
    # paid (OpenRouter)
    {"id": "openrouter/openai/gpt-4o", "display_name": "GPT-4o (Paid)", "provider": "openrouter", "tier": "paid", "aliases": ["paid"]},
]

# Add common fields
for m in models:
    m.setdefault("context_window", 128000)
    m.setdefault("max_output_tokens", 4096)
    m.setdefault("input_cost_per_m", 0.0)
    m.setdefault("output_cost_per_m", 0.0)
    m.setdefault("supports_tools", True)
    m.setdefault("supports_vision", "vl" in m["id"].lower() or "vision" in m["id"].lower())
    m.setdefault("supports_streaming", True)

with open("/home/ubuntu/.openfang/custom_models.json", "w") as f:
    json.dump(models, f, indent=2)
