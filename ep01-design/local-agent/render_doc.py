"""Render every top-level layer of a .figcraft file to PNGs, plus the whole page, for checking."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build"))
from fc import FigCraft

doc, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
fc = FigCraft()
fc.tool("open_file", path=doc)
page = fc.tool("inspect_document", depth=1)["pages"][0]
for n in page["children"]:
    name = n["name"].replace("/", "-").replace(" ", "_").replace("–", "-")
    fc.shot(os.path.join(out, f"{n['id']:04d}-{name}.png"), ids=[n["id"]])
    print(n["id"], n["type"], n["name"], round(n["x"]), round(n["y"]), round(n["width"]), round(n["height"]))
fc.shot(os.path.join(out, "page.png"), max_size=2400)
fc.close()
