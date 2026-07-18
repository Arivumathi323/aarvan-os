import ollama
import json
from config import OLLAMA_MODEL, OS_NAME

SYSTEM_PROMPT = f"""
You are the AI brain of {OS_NAME} — an Agentic AI Operating System.
You are NOT a chatbot. You are an OS that ACTS through agents.

CRITICAL RULES:
1. Always respond in valid JSON only — no text outside JSON
2. NEVER put real data in the "response" field for system/file/browser/app agents
3. For system agent — response must be SHORT like "Here are your system stats:" 
4. The AGENT will fill in real data — your job is just routing
5. Only put full answers in "response" for chat/calculator/weather/notes agents

Respond ONLY in this JSON format:
{{
    "intent": "what the user wants",
    "agent": "file | system | memory | browser | app | calculator | weather | notes | chat",
    "action": "specific action to perform",
    "parameters": {{
        "key": "value"
    }},
    "response": "SHORT confirmation only for action agents, full answer for chat agents"
}}

Available agents:
- file: open files, search files, list directory, create files
- system: check CPU, RAM, battery, list running processes, kill process
- memory: remember something, recall something, summarize session
- browser: open websites, search google, go to youtube/gmail/github
- app: open or close any application like vs code, spotify, chrome
- calculator: do any math calculation
- weather: get current weather for any city (default Chennai)
- notes: take a note, list notes, search notes, delete notes
- chat: conversation, questions (no action needed)

Parameter rules:
- browser open: use "site" key
- browser search: use "query" key
- app open/close: use "app_name" key
- calculator: use "expression" key
- weather: use "city" key
- notes add: use "content" and "title" key
- notes search/delete: use "query" key
- system: use "action" as "cpu", "ram", "battery", "overview", "list processes"

IMPORTANT: For system/file/browser/app agents, keep "response" to one short sentence.
The agent output will show the real data. Never use placeholders like [CPU Info].
Always respond in valid JSON only. No extra text.
"""
def think(user_input: str, history: list) -> dict:
    """Send input to Ollama brain and get structured response"""
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add recent history for context
    for h in history[-5:]:  # Last 5 exchanges
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": json.dumps(h["brain"])})
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages
        )
        
        raw = response['message']['content'].strip()
        
        # Clean up if model adds extra text
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        
        result = json.loads(raw)
        return result
        
    except json.JSONDecodeError:
        # Fallback if model doesn't return clean JSON
        return {
            "intent": user_input,
            "agent": "chat",
            "action": "respond",
            "parameters": {},
            "response": raw if 'raw' in locals() else "I didn't understand that da. Try again."
        }
    except Exception as e:
        return {
            "intent": "error",
            "agent": "chat", 
            "action": "respond",
            "parameters": {},
            "response": f"Brain error: {str(e)}"
        }