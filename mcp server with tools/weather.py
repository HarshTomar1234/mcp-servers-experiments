from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Weather",
    host="0.0.0.0",
    port=8000
)
    

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a given location"""
    return f"The weather in California is sunny"

if __name__=="__main__":
    print("Starting Weather MCP server on http://localhost:8000")
    mcp.run(transport="sse")
