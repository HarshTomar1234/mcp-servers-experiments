import sys
import os
import requests
import argparse
import json
from claude_mcp_client import ClaudeClient

def claude_mcp_server():
    mcp_url = os.environ.get("MCP_SERVER_URL", "http://localhost:8000")
    try:
        response = requests.get(f"{mcp_url}/health", timeout=2)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False
    
def main():
    parser = argparse.ArgumentParser(description="Ask Claude questions with web search capabilities")
    parser.add_argument("query", nargs="*", default="http://localhost:8000", help="the question to ask Claude about..")
    args = parser.parse_args()

    if not os.environ.get("CLAUDE_API_KEY"):
        print("Error: CLAUDE_API_KEY environment variable is not set.")
        sys.exit(1)

    if args.query:
        query = " ".join(args.query)
    else:
        query = input("Ask Claude")

    client = ClaudeClient()

    try:
        answer = client.get_final_answer(query)
        print("Answer", answer)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()




