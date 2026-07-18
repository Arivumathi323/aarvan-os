import json
import os
from datetime import datetime

NOTES_FILE = r"D:\AARVAN-OS\memory\notes.json"

class NotesAgent:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
        if not os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, 'w') as f:
                json.dump([], f)

    def execute(self, action: str, params: dict) -> str:
        action = action.lower()

        if any(x in action for x in ["add", "create", "save", "write", "take"]):
            content = params.get("content", "") or params.get("note", "")
            title = params.get("title", "")
            return self.add_note(content, title)

        elif any(x in action for x in ["list", "show", "read", "get all"]):
            return self.list_notes()

        elif any(x in action for x in ["find", "search"]):
            query = params.get("query", "")
            return self.search_notes(query)

        elif any(x in action for x in ["delete", "remove"]):
            query = params.get("query", "") or params.get("title", "")
            return self.delete_note(query)

        return "Notes agent ready da"

    def add_note(self, content: str, title: str = "") -> str:
        if not content:
            return "Nothing to note da"

        with open(NOTES_FILE, 'r') as f:
            notes = json.load(f)

        note = {
            "id": len(notes) + 1,
            "title": title or f"Note {len(notes) + 1}",
            "content": content,
            "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
        }
        notes.append(note)

        with open(NOTES_FILE, 'w') as f:
            json.dump(notes, f, indent=2)

        return f"✅ Note saved: '{note['title']}'"

    def list_notes(self) -> str:
        with open(NOTES_FILE, 'r') as f:
            notes = json.load(f)

        if not notes:
            return "No notes yet da — say 'take a note' to add one"

        result = f"📝 Your Notes ({len(notes)} total):\n"
        for n in notes[-10:]:
            result += f"  [{n['id']}] {n['title']} — {n['timestamp']}\n"
            result += f"      {n['content'][:60]}{'...' if len(n['content']) > 60 else ''}\n"
        return result

    def search_notes(self, query: str) -> str:
        if not query:
            return self.list_notes()

        with open(NOTES_FILE, 'r') as f:
            notes = json.load(f)

        matches = [
            n for n in notes
            if query.lower() in n['content'].lower()
            or query.lower() in n['title'].lower()
        ]

        if not matches:
            return f"No notes found about '{query}' da"

        result = f"🔍 Found {len(matches)} notes about '{query}':\n"
        for n in matches:
            result += f"  [{n['id']}] {n['title']}: {n['content'][:80]}\n"
        return result

    def delete_note(self, query: str) -> str:
        with open(NOTES_FILE, 'r') as f:
            notes = json.load(f)

        original_count = len(notes)
        notes = [
            n for n in notes
            if query.lower() not in n['title'].lower()
            and query.lower() not in n['content'].lower()
        ]

        with open(NOTES_FILE, 'w') as f:
            json.dump(notes, f, indent=2)

        deleted = original_count - len(notes)
        return f"✅ Deleted {deleted} note(s) matching '{query}'"