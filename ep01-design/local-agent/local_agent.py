"""A minimal local design agent: a local model (Ollama on the GB10) drives FigCraft through its MCP server.

  python local_agent.py --model gpt-oss:120b --task tasks/01-styles.md [--attach 47800] [--doc /config/designs/x.figcraft]

The model gets FigCraft's MCP tools and a task (a section of the design brief). Each tool call it makes
goes to `figcraft-cli mcp` in the container; the result goes back to the model. Nothing leaves the
machine. Every message and tool call is logged to runs/<stamp>-<task>.jsonl for the video and for checking.
"""
import argparse, json, os, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fc import FigCraft, FigCraftError

HERE = os.path.dirname(os.path.abspath(__file__))
OLLAMA = "http://127.0.0.1:11434"
TOOLS = ["list_commands", "run_command", "batch", "create_node", "set_properties", "get_node",
         "inspect_document", "save_file"]
MAX_RESULT = 2500

SYSTEM = """You are a UI designer working in FigCraft, a Figma-class design tool, through its tools.
Coordinates are in pixels, x right, y down; x/y are relative to the parent. Children of an auto-layout
frame are placed by the layout (use layout, gap, padding, mainAlign, crossAlign, sizingH/sizingV).
Colours are "#RRGGBB". create_node returns the new layer's id; use those ids as parents.
Useful commands for run_command: style.create {type: paint|text, name, value}, style.apply {ids, style, target?},
component.create {ids}, component.combineVariants {ids}, component.addVariant {id, property, value},
instance.create {component, parent}, instance.setProperties {ids, properties}, edit.duplicate {ids, dx, dy},
proto.interaction.add {id, trigger {type: onClick|afterDelay, ms?}, action {type: navigate|changeTo|openOverlay|back, dest},
transition {type: instant|dissolve|smartAnimate|moveIn}, durationMs, easing}, proto.flow.add {start, name}.
Use list_layers to find ids of things that already exist. Use list_commands with a filter only if you need anything else.

Examples of exact calls:
  run_command {"command": "style.create", "params": {"type": "paint", "name": "bg", "value": [{"type": "solid", "color": "#0f1115"}]}}
  run_command {"command": "style.create", "params": {"type": "text", "name": "H1", "value": {"fontFamily": "Inter", "fontStyle": "Bold", "fontSize": 56, "lineHeight": 64}}}
  create_node {"type": "frame", "name": "Card", "x": 0, "y": 0, "width": 400, "height": 200, "props": {"layout": "vertical", "padding": 20, "gap": 12, "cornerRadius": 12}}
  create_node {"type": "text", "parent": 12, "text": "Hello", "props": {"sizingH": "fill"}}
  run_command {"command": "style.apply", "params": {"ids": [12], "style": "surface", "target": "fill"}}
  run_command {"command": "style.apply", "params": {"ids": [13], "style": "Body"}}
  run_command {"command": "component.create", "params": {"ids": [12]}}  -> {"id": <component id>}
  set_properties {"ids": [14], "props": {"name": "Type=Primary", "opacity": 0.4, "strokes": ["#2a2f3a"], "strokeWeight": 1}}
create_node and set_properties are tools of their own: call them directly, not through run_command.

FigCraft gotchas (important):
- A new frame gets a WHITE fill. For a page or card apply a paint style (style.apply target fill); for a
  layout container that should be see-through, create it with props {"fills": []}.
- New text is BLACK. After creating text, apply a text style AND a paint style for its colour.
- Only use the paint styles from the task (bg, surface, text, muted, accent ...). Never invent colours.
- Variant properties: a component named "Type=Primary" has the property "Type". To switch an instance,
  instance.setProperties {"ids": [id], "properties": {"Type": "Secondary"}}.
- Instance children have their own ids (get_node on the instance, depth 3). Change their text with
  set_properties {"characters": "..."} and their colour with style.apply.

Work step by step, check your work with get_node, and keep going until every part of the task is done.
When everything is done, reply with a short summary that ends with the word DONE and make no tool call."""


def ollama_chat(model, messages, tools, ctx):
    body = {"model": model, "messages": messages, "tools": tools, "stream": False,
            "options": {"temperature": 0, "num_ctx": ctx}}
    req = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=1800).read())
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 3:
                raise
            time.sleep(10 * (attempt + 1))  # Ollama sometimes answers 500 under memory pressure


LIST_LAYERS = {"type": "function", "function": {
    "name": "list_layers",
    "description": "List the layers on the current page (top-level frames, components and component sets with their "
                   "variants): id, type, name, x, y, width, height. Use it to find ids of things made earlier.",
    "parameters": {"type": "object", "properties": {}}}}


def list_layers(fc):
    page = fc.tool("inspect_document", depth=2)["pages"][0]
    rows = []
    for n in page.get("children", []):
        rows.append(f'{n["id"]} {n["type"]} "{n["name"]}" x{n["x"]:.0f} y{n["y"]:.0f} {n["width"]:.0f}x{n["height"]:.0f}')
        if n["type"] == "COMPONENT_SET":
            for v in n.get("children", []):
                rows.append(f'   {v["id"]} {v["type"]} "{v["name"]}" x{v["x"]:.0f} y{v["y"]:.0f} {v["width"]:.0f}x{v["height"]:.0f}')
    return "\n".join(rows) or "(empty page)"


def tree(n, depth=0, lines=None):
    """A compact one-line-per-layer view of get_node output, so results don't flood the context."""
    lines = [] if lines is None else lines
    bits = [f'{"  " * depth}{n.get("id")} {n.get("type")} "{n.get("name")}" {n.get("width", 0):.0f}x{n.get("height", 0):.0f}']
    if "x" in n:
        bits.append(f'at {n["x"]:.0f},{n["y"]:.0f}')
    lay = n.get("layout") or {}
    if isinstance(lay, dict) and lay.get("mode") not in (None, "none"):
        bits.append(f'layout={lay["mode"]} gap={lay.get("gap", 0):.0f}')
    fills = n.get("fills")
    if fills:
        bits.append("fill=" + ",".join(f.get("color", f.get("type", "?")) for f in fills))
    elif fills == []:
        bits.append("fill=none")
    st = n.get("styles") or {}
    used = [f"{k}:{v}" for k, v in st.items() if v]
    if used:
        bits.append("styles=" + ",".join(used))
    if n.get("characters") is not None:
        bits.append(f'text="{n["characters"][:40]}"')
    if n.get("visible") is False:
        bits.append("HIDDEN")
    if n.get("opacity") not in (None, 1, 1.0):
        bits.append(f'opacity={n["opacity"]}')
    if n.get("interactions"):
        bits.append(f'{len(n["interactions"])} interaction(s)')
    lines.append(" ".join(bits))
    for c in n.get("children", []):
        tree(c, depth + 1, lines)
    return lines


def with_defaults(fc, args):
    """FigCraft's raw defaults (white frames, fixed 100 px boxes) trip models up; give frames see-through
    fills and, inside an auto-layout parent, hug-height sizing, unless the model asked for something else."""
    if args.get("type") not in ("frame", "component"):
        return args
    props = dict(args.get("props") or {})
    if not any(k in props for k in ("fill", "fills")):
        props["fills"] = []
    if args.get("parent") is not None and "sizingV" not in props and "height" not in args:
        try:
            parent = fc.tool("get_node", id=args["parent"], depth=0)
            if (parent.get("layout") or {}).get("mode") not in (None, "none"):
                props["sizingV"] = "hug"
                props.setdefault("sizingH", "fill" if parent["layout"]["mode"] == "vertical" else "hug")
        except FigCraftError:
            pass
    return {**args, "props": props}


def lint(fc):
    """Generic problems the model can't see without eyes: white fills, black text, content spilling out."""
    page = fc.tool("inspect_document", depth=1)["pages"][0]
    out = []
    def walk(n, top):
        for f in n.get("fills") or []:
            if f.get("color", "").upper() in ("#FFFFFF", "#FFFFFFFF") and n.get("type") != "TEXT":
                out.append(f'{n["id"]} "{n["name"]}" in "{top}" has a white fill (use a style or fills [])')
            if f.get("color", "").upper() in ("#000000", "#000000FF") and n.get("type") == "TEXT":
                out.append(f'{n["id"]} text "{n["name"]}" in "{top}" is black (apply a colour style)')
        b = n.get("absoluteBounds")
        for c in n.get("children", []):
            cb = c.get("absoluteBounds")
            if b and cb and n.get("type") in ("FRAME", "COMPONENT", "INSTANCE") and c.get("visible") is not False \
                    and cb["y"] + cb["height"] > b["y"] + b["height"] + 2 and n.get("height", 0) < 1000:
                out.append(f'{c["id"]} "{c["name"]}" spills out of the bottom of {n["id"]} "{n["name"]}" in "{top}" '
                           f'({n["height"]:.0f} px tall): let the parent hug its content (sizingV "hug")')
            walk(c, top)
    for n in page.get("children", []):
        walk(fc.tool("get_node", id=n["id"], depth=12), n["name"])
    return out[:15]


def compact(name, res):
    if name == "create_node" and isinstance(res, dict) and "id" in res:
        return json.dumps({"id": res["id"]})
    if name == "set_properties":
        return "ok"
    if name == "get_node" and isinstance(res, dict):
        return "\n".join(tree(res))
    return res if isinstance(res, str) else json.dumps(res)


def run_checks(fc, task):
    """Lines under '## Checks' in the task: 'exists: NAME' (a top-level layer or component set),
    'in NAME: CHILD, CHILD' (named layers somewhere inside it) or 'set NAME: VARIANT, ...' (a component
    set with those variants). Returns the failures."""
    if "## Checks" not in task:
        return []
    page = fc.tool("inspect_document", depth=1)["pages"][0]
    top = {n["name"]: n["id"] for n in page.get("children", [])}
    fails = []
    for line in task.split("## Checks", 1)[1].strip().splitlines():
        line = line.strip("- ").strip()
        if line.startswith("set "):
            name, want = line[4:].split(":", 1)
            name = name.strip()
            node = next((n for n in page.get("children", []) if n["name"] == name), None)
            if node is None or node["type"] != "COMPONENT_SET":
                fails.append(f'"{name}" must be a component set (component.combineVariants), found '
                             f'{node["type"] if node else "nothing"}')
                continue
            have = {c["name"] for c in fc.tool("get_node", id=node["id"], depth=1).get("children", [])}
            for v in [x.strip() for x in want.split(",")]:
                if v not in have:
                    fails.append(f'component set "{name}" has no variant "{v}" (has: {", ".join(sorted(have))})')
            continue
        if line.startswith("exists:"):
            for name in [x.strip() for x in line[7:].split(",")]:
                if name not in top:
                    fails.append(f'missing top-level layer "{name}"')
        elif line.startswith("in ") and ":" in line:
            parent, kids = line[3:].split(":", 1)
            parent = parent.strip()
            if parent not in top:
                fails.append(f'missing top-level layer "{parent}"')
                continue
            names = set()
            def walk(n):
                names.add(n.get("name"))
                for c in n.get("children", []):
                    walk(c)
            walk(fc.tool("get_node", id=top[parent], depth=12))
            for k in [x.strip() for x in kids.split(",")]:
                if k not in names:
                    fails.append(f'"{parent}" has no layer named "{k}"')
    return fails


def mcp_tools(fc):
    out = [LIST_LAYERS]
    for t in fc._rpc("tools/list", {})["tools"]:
        if t["name"] in TOOLS:
            out.append({"type": "function", "function": {"name": t["name"], "description": t["description"][:900],
                                                         "parameters": t["inputSchema"]}})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-oss:120b")
    ap.add_argument("--task", required=True)
    ap.add_argument("--attach", type=int)
    ap.add_argument("--container", default="craft-apps")
    ap.add_argument("--doc", help="open this .figcraft first (headless)")
    ap.add_argument("--save", help="save the document here at the end")
    ap.add_argument("--max-steps", type=int, default=400)
    ap.add_argument("--ctx", type=int, default=131072)
    a = ap.parse_args()

    fc = FigCraft(attach=a.attach, container=a.container)
    if a.doc and not a.attach:
        fc.tool("open_file", path=a.doc)
    tools = mcp_tools(fc)
    task = open(a.task).read()
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    log = open(os.path.join(HERE, "runs", f"{stamp}-{os.path.basename(a.task).rsplit('.', 1)[0]}.jsonl"), "w")

    def note(kind, **kw):
        log.write(json.dumps({"t": round(time.time() - t0, 2), "kind": kind, **kw}) + "\n")
        log.flush()

    t0 = time.time()
    note("start", model=a.model, task=a.task)
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    calls = errors = nudges = repeats = 0
    last_err, stop, checks_sent = None, False, 0
    for step in range(a.max_steps):
        r = ollama_chat(a.model, messages, tools, a.ctx)
        msg = r["message"]
        messages.append({k: msg[k] for k in ("role", "content", "thinking", "tool_calls") if msg.get(k)})
        note("model", content=msg.get("content", ""), thinking=(msg.get("thinking") or "")[:2000],
             tool_calls=msg.get("tool_calls"), eval_count=r.get("eval_count"),
             tps=round(r["eval_count"] / (r["eval_duration"] / 1e9), 1) if r.get("eval_duration") else None)
        if not msg.get("tool_calls"):
            fails = (run_checks(fc, task) + lint(fc)) if "DONE" in (msg.get("content") or "") else None
            if fails:
                note("checks", fails=fails)
                print(f"[{time.time() - t0:6.1f} s] checks failed: {fails}")
                if checks_sent < 4:
                    checks_sent += 1
                    messages.append({"role": "user", "content": "Not done yet. The checker found:\n- " + "\n- ".join(fails)
                                     + "\nFix these with tool calls, then reply with a summary ending in DONE."})
                    continue
            if "DONE" in (msg.get("content") or "") or nudges >= 3:
                print(f"\n[{time.time() - t0:6.1f} s] done: {msg.get('content', '')[:600]}")
                break
            nudges += 1
            messages.append({"role": "user", "content": "Keep going: finish every part of the task with tool calls. "
                             "Reply with a summary ending in DONE only when all of it is done."})
            note("nudge")
            continue
        for tc in msg["tool_calls"]:
            name, args = tc["function"]["name"], tc["function"]["arguments"]
            if isinstance(args, str):
                args = json.loads(args or "{}")
            calls += 1
            try:
                if name == "list_layers":
                    res = list_layers(fc)
                else:
                    if name == "create_node":
                        args = with_defaults(fc, args)
                    res = fc.tool(name, **args)
                text = compact(name, res)
            except FigCraftError as e:
                errors += 1
                text = f"ERROR: {e}"
            except TypeError as e:
                errors += 1
                text = f"ERROR: bad arguments: {e}"
            key = json.dumps([name, args], sort_keys=True)
            if text.startswith("ERROR"):
                repeats = repeats + 1 if key == last_err else 1
                last_err = key
                if repeats >= 3:
                    text += (" — this exact call has now failed 3 times. Do not repeat it: read the error, "
                             "check the ids with list_layers or get_node, and try a different approach.")
                if repeats >= 6:
                    note("abort", reason="same failing call 6 times")
                    print("stopping: the same call failed 6 times")
                    stop = True
            else:
                last_err, repeats = None, 0
            if len(text) > MAX_RESULT:
                text = text[:MAX_RESULT] + "… (truncated; use get_node on a smaller part)"
            note("tool", name=name, args=args, result=text[:4000])
            print(f"[{time.time() - t0:6.1f} s] {name} {json.dumps(args)[:110]} -> {text[:90]}", flush=True)
            messages.append({"role": "tool", "content": text, "tool_name": name})
        if stop:
            break
    note("end", calls=calls, errors=errors, seconds=round(time.time() - t0, 1))
    print(f"{calls} tool calls, {errors} errors, {time.time() - t0:.0f} s")
    if a.save:
        print(fc.tool("save_file", path=a.save))
    fc.close()


if __name__ == "__main__":
    main()
