from fastmcp import FastMCP

mcp = FastMCP("MyServer", 
version="1.0.0",
instructions="This is a sample FastMCP server for demonstration purposes.")

@mcp.tool
def hello(name: str) -> str:
    """Greet a user by name.

    Args:
        name: The name of the user to greet.

    Returns:
        A greeting message for the user.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Uses STDIO transport by default

# when you want to call this tool from command like use this.
# fastmcp call fastmcpcli.py hello name=Rakesh
# https://fastmcp.wiki/en/patterns/cli for more details

# use this command to inspect the tool and its parameters
# what llms can see when they call this tool
# fastmcp inspect fastmcpcli.py --format fastmcp