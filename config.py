# ============================
# AARVAN OS — Core Config
# ============================

# AI Brain Settings
OLLAMA_MODEL = "llama3:latest"       # Local brain — already on your machine
OLLAMA_BASE_URL = "http://localhost:11434"
GROQ_API_KEY = ""                  # Add your key here as backup

# OS Identity
OS_NAME = "AARVAN OS"
OS_VERSION = "0.1-alpha"
CREATOR = "Arivu — Aarvan Technology"

# Memory Settings
SHORT_TERM_MEMORY = "memory/short_term.json"
LONG_TERM_MEMORY = "memory/long_term.json"
MAX_SHORT_TERM = 20                # Last 20 conversations kept in session

# Agent Settings
AGENTS_ENABLED = {
    "file": True,
    "system": True,
    "memory": True,
}