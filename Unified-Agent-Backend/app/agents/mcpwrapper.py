# file: mcp_server.py
from fastapi import FastAPI
from mcp.server import MCPServer, MCPHandler
import sqlite3

app = FastAPI()
mcp = MCPServer(app)  # Wrap FastAPI into MCP

# SQLite helper
def get_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()
    return {"message": "Book added"}

# MCP Handlers
@mcp.handler("GetBooks")
def handle_get_books(request):
    return {"books": get_books()}

@mcp.handler("AddBook")
def handle_add_book(request):
    title = request.params.get("title")
    author = request.params.get("author")
    year = request.params.get("year")
    return add_book(title, author, year)

# Run MCP server
if __name__ == "__main__":
    mcp.run(port=9000)
