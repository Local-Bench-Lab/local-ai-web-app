"""Check the agents' src/styles/tokens.css against the exact V1 design values (v1-design/build/build.py).

  python check_tokens.py [path/to/tokens.css]

Matches by value, not by name: every V1 colour must appear as a custom property, and every V1 text style's font size and
line height must appear. Prints each check and a score.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "..", "v1-design", "build", "build.py")).read()
C = eval(re.search(r"^C = (\{.*?\})", src, re.S | re.M).group(1))
TEXT = eval(re.search(r"^TEXT = (\{.*?\})", src, re.S | re.M).group(1))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "tools", "craft-config", "bench-board-app",
                                                         "src", "styles", "tokens.css")
css = open(path).read().lower()
props = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css))
values = " ".join(props.values())

ok = total = 0
for name, hexv in C.items():
    hit = [k for k, v in props.items() if hexv.lower() in v]
    total += 1; ok += bool(hit)
    print(f"{'✓' if hit else '✗'} colour {name:12s} {hexv}  {hit[0] if hit else 'missing'}")
for name, (fam, sty, size, lh) in TEXT.items():
    s = re.search(rf"\b{size}px\b|\b{size / 16:g}rem\b", values) is not None
    l = re.search(rf"\b{lh}px\b|\b{lh / 16:g}rem\b|\b{lh / size:.3g}\b", values) is not None
    total += 2; ok += s + l
    print(f"{'✓' if s and l else '✗'} text   {name:12s} {size}/{lh}  size {'ok' if s else 'missing'}, line height {'ok' if l else 'missing'}")
print(f"\nscore: {ok}/{total} V1 values found in {os.path.basename(path)}")
