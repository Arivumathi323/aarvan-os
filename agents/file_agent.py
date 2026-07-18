import os
import subprocess
import glob

class FileAgent:
    def execute(self, action: str, params: dict) -> str:
        
        if action in ["open file", "open"]:
            path = params.get("path", "")
            return self.open_file(path)
        
        elif action in ["search files", "find file", "search"]:
            query = params.get("query", "")
            location = params.get("location", "D:\\")
            return self.search_files(query, location)
        
        elif action in ["list directory", "list files", "ls"]:
            path = params.get("path", os.getcwd())
            return self.list_directory(path)
        
        elif action in ["create file"]:
            path = params.get("path", "")
            content = params.get("content", "")
            return self.create_file(path, content)
        
        else:
            return ""
    
    def open_file(self, path: str) -> str:
        if not path:
            return "No file path provided"
        if os.path.exists(path):
            os.startfile(path)  # Windows opens with default app
            return f"Opened: {path}"
        return f"File not found: {path}"
    
    def search_files(self, query: str, location: str = "D:\\") -> str:
        if not query:
            return "No search query provided"
        
        results = []
        try:
            pattern = f"{location}/**/*{query}*"
            matches = glob.glob(pattern, recursive=True)[:10]
            
            if matches:
                result = f"Found {len(matches)} files matching '{query}':\n"
                for m in matches:
                    result += f"  {m}\n"
                return result
            else:
                return f"No files found matching '{query}'"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def list_directory(self, path: str) -> str:
        try:
            items = os.listdir(path)
            result = f"Contents of {path}:\n"
            for item in items[:20]:
                full = os.path.join(path, item)
                icon = "📁" if os.path.isdir(full) else "📄"
                result += f"  {icon} {item}\n"
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_file(self, path: str, content: str = "") -> str:
        try:
            with open(path, 'w') as f:
                f.write(content)
            return f"Created: {path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"