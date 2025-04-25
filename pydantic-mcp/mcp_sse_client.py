import os
import asyncio
import logfire
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

# Deno  (JSR package)
# Windows : irm https://deno.land/install.ps1 | iex
# MacOS/ Linux : curl -fsSL https://deno.land/install.sh | sh

# # run this is powershell
"""
deno run \
  -N -R=node_modules -W=node_modules --node-modules-dir=auto \
  jsr:@pydantic/mcp-run-python [stdio|sse|warmup]
"""

# where:

# -N -R=node_modules -W=node_modules (alias of --allow-net --allow-read=node_modules --allow-write=node_modules) allows network access and read+write access to ./node_modules. These are required so Pyodide can download and cache the Python standard library and packages
# --node-modules-dir=auto tells deno to use a local node_modules directory
# stdio runs the server with the Stdio MCP transport — suitable for running the process as a subprocess locally
# sse runs the server with the SSE MCP transport — running the server as an HTTP server to connect locally or remotely
# warmup will run a minimal Python script to download and cache the Python standard library. This is also useful to check the server is running correctly.


# for logfire logging and monitoring check out logfire docs

logfire.configure()
logfire.instrument_pydantic_ai()

os.environ["GROQ_API_KEY"] = "put your groq api key here"

server = MCPServerHTTP(url='http://localhost:3001/sse')  
agent = Agent('groq:llama-3.3-70b-versatile', mcp_servers=[server])  


async def main():
    async with agent.run_mcp_servers():  
        result = await agent.run('What are the top 10 popular places for destination wedding?')
    print(result.output)
    

asyncio.run(main())