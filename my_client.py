import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)
for _ in range(100):
    asyncio.run(call_tool("hello"))
#asyncio.run(call_tool("Ford"))