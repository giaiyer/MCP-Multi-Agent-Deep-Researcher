import os
import requests
import sys

LINKUP_API_KEY = os.getenv("LINKUP_API_KEY")
LINKUP_API_URL = "https://api.linkup.so/v1/search"

def linkup_search(query: str, depth: str = "deep") -> str:
    if not LINKUP_API_KEY:
        raise ValueError("LINKUP_API_KEY is not set in environment variables.")
    headers = {
        "Authorization": f"Bearer {LINKUP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "depth": depth,
        "outputType": "sourcedAnswer"
    }
    try:
        response = requests.post(LINKUP_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer", "[No answer returned]")
        sources = data.get("sources", [])
        if sources:
            sources_str = "\n\nSources:\n" + "\n".join([f"- {src.get('url', src)}" for src in sources])
            return f"{answer}{sources_str}"
        return answer
    except Exception as e:
        return f"[LinkUp API error: {e}]"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linkup_only.py <query> [depth]")
        sys.exit(1)
    query = " ".join(sys.argv[1:2])
    depth = sys.argv[2] if len(sys.argv) > 2 else "deep"
    print(linkup_search(query, depth=depth)) 