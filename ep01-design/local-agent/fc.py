"""Small MCP client for FigCraft running in the craft-apps container.

  fc = FigCraft()            # headless engine (figcraft-cli mcp)
  fc = FigCraft(attach=47800) # drive the visible app started with `figcraft --control 47800`
  fc = FigCraft(attach=47801, container="recorder")  # the app on the recorder's virtual screen

Calls go over stdio JSON-RPC to `figcraft-cli mcp` inside the container, so FigCraft and the
files it writes stay in the container (/config is series/fullstack/tools/craft-config on the GB10).
"""
import base64, json, subprocess

CLI = "/config/.local/bin/figcraft-cli"


class FigCraftError(RuntimeError):
    pass


class FigCraft:
    def __init__(self, attach=None, container="craft-apps"):
        user = "abc" if container == "craft-apps" else "1000:1000"  # the recorder runs as the host user
        cmd = ["docker", "exec", "-i", "-u", user, "-e", "HOME=/config", container, CLI, "mcp"]
        if attach:
            cmd += ["--attach", str(attach)]
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.n = 0
        self._rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "bench-board-build", "version": "1"}})
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")

    def _rpc(self, method, params):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params}) + "\n")
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise FigCraftError("figcraft-cli mcp exited")
            msg = json.loads(line)
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise FigCraftError(msg["error"])
                return msg["result"]

    def tool(self, _tool, **args):
        r = self._rpc("tools/call", {"name": _tool, "arguments": args})
        if r.get("isError"):
            raise FigCraftError(f"{_tool} {json.dumps(args)[:300]}: {r['content'][0].get('text')}")
        out = []
        for c in r.get("content", []):
            if c["type"] == "text":
                try:
                    out.append(json.loads(c["text"]))
                except ValueError:
                    out.append(c["text"])
            elif c["type"] == "image":
                out.append(base64.b64decode(c["data"]))
        return out[0] if len(out) == 1 else out

    def run(self, command, **params):
        return self.tool("run_command", command=command, params=params)

    def batch(self, steps, label="Batch"):
        return self.tool("batch", commands=[{"command": c, "params": p} for c, p in steps], label=label)

    def create(self, type, parent=None, **kw):
        args = {"type": type, **kw}
        if parent is not None:
            args["parent"] = parent
        return self.tool("create_node", **args)["id"]

    def set(self, ids, **props):
        ids = ids if isinstance(ids, list) else [ids]
        return self.tool("set_properties", ids=ids, props=props)

    def shot(self, path, ids=None, max_size=1600):
        args = {"maxSize": max_size}
        if ids:
            args["ids"] = ids
        r = self.tool("screenshot", **args)
        img = r if isinstance(r, bytes) else next(x for x in r if isinstance(x, bytes))
        open(path, "wb").write(img)

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=10)
