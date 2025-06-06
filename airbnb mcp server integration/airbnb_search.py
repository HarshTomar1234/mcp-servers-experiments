from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


from praisonaiagents import Agent, MCP

search_agent = Agent(
    instructions="""You help book apartments on Airbnb.""",
    llm="gpt-4o",
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"),
    
)

search_agent.start("I want to book an apartment in Paris for 2 nights. 03/28 - 03/30 for 2 adults")
