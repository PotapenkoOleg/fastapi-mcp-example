import httpx2
from fastapi import FastAPI

from fastmcp import Client, FastMCP
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from fastmcp.utilities.asgi_transport import (
    StreamingASGITransport,
    run_asgi_lifespan,
)


async def test_mounted_mcp():
    auth = StaticTokenVerifier(
        tokens={"test-token": {"client_id": "test-client", "scopes": []}}
    )
    mcp = FastMCP("Test Tools", auth=auth)

    @mcp.tool
    def add(a: int, b: int) -> int:
        return a + b

    mcp_app = mcp.http_app(path="/mcp")
    app = FastAPI(lifespan=mcp_app.lifespan)
    app.mount("/analytics", mcp_app)

    def http_client_factory(**kwargs):
        return httpx2.AsyncClient(
            transport=StreamingASGITransport(app),
            **kwargs,
        )

    transport = StreamableHttpTransport(
        url="http://testserver/analytics/mcp",
        auth="test-token",
        httpx_client_factory=http_client_factory,
    )
    async with run_asgi_lifespan(app):
        async with Client(transport) as client:
            result = await client.call_tool("add", {"a": 1, "b": 2})
            assert result.data == 3