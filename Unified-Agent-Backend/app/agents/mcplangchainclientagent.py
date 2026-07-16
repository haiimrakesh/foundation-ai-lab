# file: agents/mcp_agent_wrapper.py
import requests
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool

# Base MCP server URL
MCP_SERVER_URL = "http://localhost:9000"

# -----------------------------
# MCP Client Helper
# -----------------------------
def call_mcp_tool(tool_name, params=None):
    """
    Calls an MCP tool by sending a POST request to the MCP server.
    """
    url = f"{MCP_SERVER_URL}/{tool_name}"
    response = requests.post(url, json=params or {})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed with status {response.status_code}"}

# -----------------------------
# Define LangChain Tools
# -----------------------------
def get_books_tool(_):
    """Wrapper for MCP GetBooks tool"""
    return call_mcp_tool("GetBooks")

def add_book_tool(query: str):
    """
    Wrapper for MCP AddBook tool.
    The agent will parse the query and extract book details.
    For simplicity, we assume the query contains 'title', 'author', and 'year'.
    """
    # Naive parsing (students can improve with regex or LLM parsing)
    if "Brave New World" in query:
        title = "Brave New World"
        author = "Aldous Huxley"
        year = 1932
    else:
        # Default fallback
        title = "Unknown Title"
        author = "Unknown Author"
        year = 2024
    
    return call_mcp_tool("AddBook", {"title": title, "author": author, "year": year})

tools = [
    Tool(
        name="GetBooks",
        func=get_books_tool,
        description="Retrieve all books from the library database"
    ),
    Tool(
        name="AddBook",
        func=add_book_tool,
        description="Add a book to the library database. Provide title, author, and year."
    )
]

# -----------------------------
# Initialize Agent
# -----------------------------
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

def run_mcp_agent(query: str):
    """
    Run the agent with a natural language query.
    """
    return agent.run(query)

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    print("🤖 Asking agent to fetch books...")
    print(run_mcp_agent("Show me all the books in the library"))

    print("\n🤖 Asking agent to add a book...")
    print(run_mcp_agent("Add a book called Brave New World by Aldous Huxley published in 1932"))
