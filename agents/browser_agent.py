import webbrowser

SITE_SHORTCUTS = {
    "youtube": "https://youtube.com",
    "aarvan labs": "https://youtube.com/@aarvan_labs",
    "gmail": "https://mail.google.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "fiverr": "https://fiverr.com",
    "chatgpt": "https://chatgpt.com",
    "claude": "https://claude.ai",
    "canva": "https://canva.com",
    "portfolio": "https://arivumathi.in",
    "figma": "https://figma.com",
    "vercel": "https://vercel.com",
    "whatsapp": "https://web.whatsapp.com",
    "instagram": "https://instagram.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://linkedin.com",
    "stackoverflow": "https://stackoverflow.com",
    "groq": "https://console.groq.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://netflix.com",
}

class BrowserAgent:
    def execute(self, action: str, params: dict) -> str:
        action = action.lower().strip()

        # Extract target from ANY parameter key the brain might use
        target = (
            params.get("url") or
            params.get("site") or
            params.get("target") or
            params.get("website") or
            params.get("query") or
            params.get("name") or
            ""
        ).strip()

        # If action is search-related
        if any(x in action for x in ["search", "google", "look up", "find"]):
            return self.search_web(target)

        # Everything else = try to open
        # Also handle case where target is empty but action has the site name
        if not target:
            # Brain might put site name IN the action like "open youtube"
            for key in SITE_SHORTCUTS:
                if key in action:
                    target = key
                    break

        if target:
            return self.open_site(target)

        return "What site should I open da?"

    def open_site(self, target: str) -> str:
        if not target:
            return "No site specified da"

        target_lower = target.lower().strip()

        # Check shortcuts
        for key, url in SITE_SHORTCUTS.items():
            if key in target_lower or target_lower in key:
                webbrowser.open(url)
                return f"✅ Opened {key} → {url}"

        # Looks like a real URL
        if "." in target and " " not in target:
            if not target.startswith("http"):
                target = "https://" + target
            webbrowser.open(target)
            return f"✅ Opened: {target}"

        # Search it
        return self.search_web(target)

    def search_web(self, query: str) -> str:
        if not query:
            return "No search query da"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🔍 Searching Google for: {query}"