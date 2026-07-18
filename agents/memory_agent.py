import json
import os
from datetime import datetime
from config import SHORT_TERM_MEMORY, LONG_TERM_MEMORY

class MemoryAgent:
    def __init__(self):
        self._ensure_files()
    
    def _ensure_files(self):
        for path in [SHORT_TERM_MEMORY, LONG_TERM_MEMORY]:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)
    
    def execute(self, action: str, params: dict) -> str:
        if action in ["remember", "save", "store"]:
            content = params.get("content", "")
            return self.remember(content)
        
        elif action in ["recall", "what did i", "retrieve"]:
            query = params.get("query", "")
            return self.recall(query)
        
        elif action in ["summarize session", "session summary"]:
            return self.summarize()
        
        return ""
    
    def remember(self, content: str) -> str:
        with open(LONG_TERM_MEMORY, 'r') as f:
            memories = json.load(f)
        
        memories.append({
            "timestamp": datetime.now().isoformat(),
            "content": content
        })
        
        with open(LONG_TERM_MEMORY, 'w') as f:
            json.dump(memories, f, indent=2)
        
        return f"Remembered: {content}"
    
    def recall(self, query: str) -> str:
        with open(LONG_TERM_MEMORY, 'r') as f:
            memories = json.load(f)
        
        if not memories:
            return "No memories stored yet da"
        
        # Simple keyword search
        matches = [m for m in memories if query.lower() in m['content'].lower()]
        
        if matches:
            result = f"Found {len(matches)} memories about '{query}':\n"
            for m in matches[-5:]:
                result += f"  [{m['timestamp'][:10]}] {m['content']}\n"
            return result
        
        return f"No memories found about '{query}'"
    
    def summarize(self) -> str:
        with open(SHORT_TERM_MEMORY, 'r') as f:
            session = json.load(f)
        
        if not session:
            return "Nothing in this session yet"
        
        result = f"This session ({len(session)} exchanges):\n"
        for s in session[-5:]:
            result += f"  You: {s['user'][:50]}...\n"
        return result