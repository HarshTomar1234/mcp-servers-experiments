import os
import re
import json
import requests

from typing import Dict, List, Any, Optional, Union, Literal

from dataclasses import dataclass, asdict
import openai
import anthropic

DUCKDUCKGO_ENDPOINT = "https://api.duckduckgo.com"
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

LLMProvider = Literal["claude"]

@dataclass
class DDGRequest:
    q: str
    format: str = "json"
    no_html: int = 1
    skip_disambig: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    

@dataclass
class WebSearchRequest:
    title: str
    url: str
    description: str

class MCPClient:
    def __init__(self, endpoint: str = DUCKDUCKGO_ENDPOINT):
        self.endpoint = endpoint
        
    def search_web(self, query: str, limit: int = 10) -> List[WebSearchRequest]:
        request = DDGRequest(q=query)

        try:
            response = requests.get(self.endpoint, params=request.to_dict())
            response.raise_for_status()

            data = response.json()

            results = []
            if data.get("Abstract"):
                results.append(WebSearchRequest(
                    title=data.get("Heading", ""),
                    url=data.get("AbstractURL", ""),
                    description=data.get("Abstract", "")
                ))
            
            return results
        
        except Exception as e:
            print(f"Error searching web: {e}")
            return []
        
class ClaudeMCPBridge:

    def __init__(self, llm_provider: LLMProvider = "claude"):
        self.mcp_client = MCPClient()
        self.llm_provider = llm_provider

        if llm_provider == "claude":
            if not CLAUDE_API_KEY:
                raise ValueError("CLAUDE_API_KEY environment variable is not set")
            self.claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


    def extract_website_queries_with_llm(self, user_message: str) -> List[str]:
            if self.llm_provider == "claude":
                return self._extract_queries_with_claude(user_message)
            else:
                return ["error"]
            
    def _extract_queries_with_claude(self, user_message: str) -> List[str]:
        try:
            # Try using the anthropic client first
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                temperature=0.1,
                max_tokens=1000,
                system="You are a helpful assistant that identifies web search queries in user message. Extract any specific website or topic queries the user wants information about. Return results as a JSON object with a 'queries' field containing an array of strings. If no queries are found, return an empty array.",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            content = response.content[0].text
            json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
            
            if json_match:
                result = json.loads(json_match.group(1))
                return result.get('queries', [])
            else: 
                try:
                    result = json.loads(content)
                    return result.get('queries', [])
                except json.JSONDecodeError:
                    return []
                    
        except Exception as e:
            print(f"Error extracting queries with anthropic client: {e}")
            # Fallback: return a simple query extraction
            return [user_message] if user_message else [] 
        
    def handle_claude_tool_call(self, tool_params: Dict[str, Any]) -> Dict[str, Any]:
        query = tool_params.get("query", "")
        if not query:
            return {"error": "No query provided"}
        
        results = self.mcp_client.search_web(query)

        return {
            "results": [asdict(result) for result in results]
        }

# Standalone function for import compatibility
def handle_claude_tool_call(tool_params: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function that creates a bridge instance and handles tool calls"""
    bridge = ClaudeMCPBridge()
    return bridge.handle_claude_tool_call(tool_params)

            




