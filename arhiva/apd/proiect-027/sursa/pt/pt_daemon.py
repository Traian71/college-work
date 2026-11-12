# Porneste puntea cisco-pt-mcp (port 7531, la care se conecteaza pluginul din Packet Tracer)
# si expune local POST http://127.0.0.1:7532/call {"tool": ..., "input": {...}} ca sa pot da comenzi din terminal.
import asyncio, json
from aiohttp import web
from mcp_server.bridge import PTBridge

async def main():
    br = PTBridge()
    await br.start()
    async def call(req):
        d = await req.json()
        try:
            r = await br.call_tool(d["tool"], d.get("input", {}))
        except Exception as e:
            r = {"error": str(e)}
        return web.json_response(r)
    async def status(req):
        return web.json_response({"connected": br.is_connected})
    app = web.Application(); app.router.add_post("/call", call); app.router.add_get("/status", status)
    r = web.AppRunner(app); await r.setup(); await web.TCPSite(r, "127.0.0.1", 7532).start()
    print("daemon gata", flush=True)
    await asyncio.Event().wait()

asyncio.run(main())
