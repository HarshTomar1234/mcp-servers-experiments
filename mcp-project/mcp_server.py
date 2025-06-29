import os
import json
from flask import Flask, request, jsonify
from mcp_integration import ClaudeMCPBridge, handle_claude_tool_call

PORT = os.environ.get("PORT", 8000)

app = Flask(__name__)
bridge = ClaudeMCPBridge()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "name": "MCP server",
        "status": "running",
        "endpoints": [
            {"path": "/tool_call", "method": "POST", "description": "Handle tool calls from Claude",
             "path": "/health", "method": "GET", "description": "Health check endpoint"}
        ]})

@app.route("/tool_call", methods=["POST"])
def tool_call():
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400

    tool_name = request.json.get("name")
    parameters = request.json.get("parameters", {})

    if tool_name != "fetch_web_content":
        return jsonify({"error": "Unknown tool name"}), 400
    
    result = handle_claude_tool_call(parameters)
    return jsonify({"results": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

