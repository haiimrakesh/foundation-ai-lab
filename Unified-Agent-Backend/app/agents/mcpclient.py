# file: mcp_client.py
import requests

# Base URL of the MCP server
MCP_SERVER_URL = "http://localhost:9000"

# -----------------------------
# Helper function to call MCP tools
# -----------------------------
def call_mcp_tool(tool_name, params=None):
    """
    Calls a tool exposed by the MCP server.
    
    Arguments:
    - tool_name: Name of the MCP handler (e.g., "GetBooks", "AddBook")
    - params: Dictionary of parameters to send with the request
    
    Returns:
    - JSON response from the MCP server
    """
    url = f"{MCP_SERVER_URL}/{tool_name}"
    response = requests.post(url, json=params or {})
    
    # Check if request succeeded
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed with status {response.status_code}"}

# -----------------------------
# Example client usage
# -----------------------------
if __name__ == "__main__":
    # 1. Call GetBooks tool
    print("📚 Fetching all books from MCP server...")
    books = call_mcp_tool("GetBooks")
    print("Response:", books)

    # 2. Call AddBook tool
    print("\n➕ Adding a new book via MCP server...")
    new_book = call_mcp_tool("AddBook", {
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "year": 1932
    })
    print("Response:", new_book)

    # 3. Verify by fetching books again
    print("\n📚 Fetching updated book list...")
    updated_books = call_mcp_tool("GetBooks")
    print("Response:", updated_books)
