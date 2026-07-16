# file: agents/mcp_agent.py
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
import requests

llm = ChatOpenAI(model="gpt-4")

def call_mcp_tool(tool_name, params=None):
    # Simulate MCP call via HTTP
    resp = requests.post(f"http://localhost:9000/{tool_name}", json=params or {})
    return resp.json()

tools = [
    Tool(
        name="GetBooks",
        func=lambda _: call_mcp_tool("GetBooks"),
        description="Retrieve all books from library"
    ),
    Tool(
        name="AddBook",
        func=lambda q: call_mcp_tool("AddBook", {"title": "Sample", "author": "Author", "year": 2024}),
        description="Add a book to the library"
    )
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

def mcp_agent(query):
    return agent.run(query)
