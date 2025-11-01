# my_server.py
from fastmcp import FastMCP

# Give your server a friendly name (clients will see this)
mcp = FastMCP("Render Demo")

# --- Example tools (add your own!) ---

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def echo(text: str) -> str:
    """Echo text back to the caller."""
    return text

# Expose an ASGI application for deployment (served by uvicorn on Render)
app = mcp.http_app()

# Optional: local dev HTTP run (uncomment to run locally via `python my_server.py`)
# if __name__ == "__main__":
#     # For local testing over HTTP
#     # Visit http://127.0.0.1:8000 (MCP is a protocol; expect non-HTML responses)
#     mcp.run(transport="http", host="127.0.0.1", port=8000)
