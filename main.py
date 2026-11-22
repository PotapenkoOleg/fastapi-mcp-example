from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP
from pydantic import BaseModel
import uvicorn

import httpx2

# if __name__ == "__main__":
#     pass
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")



@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)