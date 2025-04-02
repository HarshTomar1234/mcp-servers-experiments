from praisonaiagents import Agent, MCP
import gradio as gr



# search_agent = Agent(
#     instructions="""You help book apartments on Airbnb.""",
#     llm="ollama/llama3.2",
#     tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
# )

# search_agent.start("MUST USE airbnb_search Tool to Search. Search for Apartments in Paris for 2 nights. 04/28 - 04/30 for 2 adults. All Your Preference")


def search_agent(query):
    agnet = Agent(
    instructions="""You help book apartments on Airbnb.""",
    llm="ollama/llama3.2",
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
    )
    result = agnet.start(query)
    return f"## Airbnb Search Results\n\n{result}"

demo = gr.Interface(
    fn=search_agent,
    inputs=gr.Textbox(placeholder="I want to book an apartment in Paris for 2 nights..."),
    outputs=gr.Markdown(),
    title="Airbnb Booking Assistant",
    description="Enter your booking requirements below:"
)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)