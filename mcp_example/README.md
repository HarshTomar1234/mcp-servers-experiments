# Weather Information MCP Server

A Model Control Protocol (MCP) server for retrieving weather alerts and information using the National Weather Service API.

## Features

- Get active weather alerts for any US state
- Interactive chat interface using GROQ LLM
- Built-in conversation memory
- Simple API for integrating weather data in your applications

## Installation

### Prerequisites

- Python 3.9+
- pip or uv package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp_example
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your GROQ API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Configuration

The MCP server configuration is stored in `server/weather.json`. You can modify this to change the server settings or add new tools.

## Usage

### Starting the Weather MCP Server

To run the weather MCP server:

```bash
mcp run server/weather.py
```

To run with the MCP Inspector for debugging:

```bash
mcp dev server/weather.py
```

### Getting Weather Alerts

You can directly use the Python API:

```python
import asyncio
from server.weather import get_alerts

async def main():
    # Get weather alerts for California
    result = await get_alerts("CA")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Using the Chat Interface

The project includes an interactive chat interface powered by GROQ LLM:

```bash
python server/client.py
```

In the chat, you can:
- Ask for weather alerts for any US state
- Type 'clear' to reset conversation history
- Type 'exit' or 'quit' to end the conversation

## API Reference

### Weather Tools

#### `get_alerts(state: str) -> str`

Gets weather alerts for a US state.

**Parameters:**
- `state` (str): Two-letter US state code (e.g. CA, NY)

**Returns:**
- String containing formatted weather alerts information

## Troubleshooting

### API Key Issues

If you encounter errors related to the GROQ API key:
1. Ensure your `.env` file exists and contains a valid API key
2. If no `.env` file is present, the application will prompt you to enter your key manually
3. Check that you have the proper permissions and quotas for your GROQ API key

### Connection Issues

If you're having trouble connecting to the National Weather Service API:
1. Check your internet connection
2. The NWS API may have rate limits or be experiencing downtime
3. Ensure your User-Agent is set correctly in the requests

## License

[Specify your license here]

## Acknowledgements

- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [GROQ](https://groq.com/) for providing the LLM capabilities
- [Model Control Protocol (MCP)](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp)
