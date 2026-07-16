# file: agents/tool_agent.py
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def add_book_tool(title, author, year):
    # Call REST API here
    return f"Book '{title}' added."

tools = [
    Tool(
        name="AddBook",
        func=lambda q: add_book_tool("Sample", "Author", 2024),
        description="Add a book to the library database"
    )
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

def tool_agent(query):
    return agent.run(query)
    