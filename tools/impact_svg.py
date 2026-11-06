# Draws the four before/after graphics from data/tensorfold.json (the single source of every number on the page):
#   assets/impact-{light,dark}.svg          880 px wide, three cards a row
#   assets/impact-mobile-{light,dark}.svg   440 px wide, one card a row
# Usage: python3 tools/impact_svg.py [assets-dir]      (tools/refresh.py calls render_all() as well)
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "tensorfold.json")

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": dict(card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e", after="#1a7f37", before="#c8d1da", accent="#0969da"),
    "dark": dict(card="#161b22", border="#30363d", text="#e6edf3", muted="#9198a1", after="#3fb950", before="#3d444d", accent="#4493f8"),
}
LAYOUTS = {
    "desktop": dict(W=880, cols=3, gap=16, ch=134, bar_label=70, bar_tail=104, big=34, label_fs=15),
    "mobile": dict(W=440, cols=1, gap=10, ch=96, bar_label=56, bar_tail=104, big=30, label_fs=15),
}
SUBTITLE = "One pull request each · maintainer's A/B unless a card says own receipt"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def num(v):
    return f"{v:,}"


def entry_index(data):
    out = {}
    for m in data["models"]:
        for e in m["entries"]:
            out[e["pr"]] = e
    return out


def alt_text(data):
    parts = []
    for m in data["models"]:
        items = []
        idx = {e["pr"]: e for e in m["entries"]}
        for pr in m["graphic"]["cards"]:
            c = idx[pr]["card"]
            items.append(f"#{pr} {c['big']} {c['label']}")
        for b in ([] if m["graphic"]["cards"] else m["graphic"]["bars"]):
            cell = next(c for c in idx[b["pr"]]["cells"] if c.get("id") == b["cell"])
            items.append(f"#{b['pr']} {b['title']} {num(cell['before'])} {cell['unit']} to {num(cell['after'])} {cell['unit']}")
        parts.append(f"{m['name']}: " + "; ".join(items))
    return "What my TensorFold pull requests changed. " + ". ".join(parts)


def svg(data, t, lay):
    W = lay["W"]
    idx = entry_index(data)
    p = []
    a = p.append
    y = 0
    a(f'<text x="0" y="{y+22}" font-size="20" font-weight="600" fill="{t["text"]}">What my TensorFold pull requests changed</text>')
    a(f'<text x="0" y="{y+44}" font-size="13" fill="{t["muted"]}">{esc(SUBTITLE)}</text>')
    y += 66
    first = True
    for m in data["models"]:
        g = m["graphic"]
        if not first:
            a(f'<line x1="0" y1="{y-4}" x2="{W}" y2="{y-4}" stroke="{t["border"]}"/>')
            y += 18
        first = False
        a(f'<text x="0" y="{y+16}" font-size="17" font-weight="600" fill="{t["text"]}">{esc(m["graphic_heading"])}</text>')
        y += 32 if g["cards"] else 34
        cols, gap, ch = lay["cols"], lay["gap"], lay["ch"]
        cw = (W - (cols - 1) * gap) / cols
        for i, pr in enumerate(g["cards"]):
            e = idx[pr]
            c = e["card"]
            x = (i % cols) * (cw + gap)
            cy = y + (i // cols) * (ch + gap)
            a(f'<rect x="{x+0.5:g}" y="{cy+0.5:g}" width="{cw-1:g}" height="{ch-1}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>')
            tag = "own receipt" if e["measured_by"] == "own" else "maintainer's A/B"
            if cols > 1:
                bigsize = lay["big"] if len(c["big"]) <= 7 else lay["big"] - 5
                a(f'<text x="{x+20:g}" y="{cy+48}" font-size="{bigsize}" font-weight="700" fill="{t["after"]}">{esc(c["big"])}</text>')
                a(f'<text x="{x+20:g}" y="{cy+74}" font-size="{lay["label_fs"]}" font-weight="600" fill="{t["text"]}">{esc(c["label"])}</text>')
                a(f'<text x="{x+20:g}" y="{cy+96}" font-size="13" fill="{t["muted"]}">{esc(c["note"])}</text>')
                a(f'<text x="{x+20:g}" y="{cy+118}" font-size="12" fill="{t["muted"]}">{esc(tag)}</text>')
                a(f'<text x="{x+cw-20:g}" y="{cy+118}" font-size="13" font-weight="600" text-anchor="end" fill="{t["accent"]}">#{pr}</text>')
            else:
                a(f'<text x="18" y="{cy+57}" font-size="{lay["big"]}" font-weight="700" fill="{t["after"]}">{esc(c["big"])}</text>')
                a(f'<text x="150" y="{cy+32}" font-size="{lay["label_fs"]}" font-weight="600" fill="{t["text"]}">{esc(c["label"])}</text>')
                a(f'<text x="150" y="{cy+54}" font-size="13" fill="{t["muted"]}">{esc(c["note"])}</text>')
                a(f'<text x="150" y="{cy+76}" font-size="12" fill="{t["muted"]}">{esc(tag)}</text>')
                a(f'<text x="{W-16}" y="{cy+32}" font-size="13" font-weight="600" text-anchor="end" fill="{t["accent"]}">#{pr}</text>')
        if g["cards"]:
            rows = -(-len(g["cards"]) // cols)
            y += rows * ch + (rows - 1) * gap + 28
        vmax = max(next(c for c in idx[b["pr"]]["cells"] if c.get("id") == b["cell"])["before"] for b in g["bars"])
        for b in g["bars"]:
            cell = next(c for c in idx[b["pr"]]["cells"] if c.get("id") == b["cell"])
            a(f'<text x="0" y="{y+16}" font-size="14" font-weight="600" fill="{t["text"]}">{esc(b["title"])}</text>')
            a(f'<text x="{W}" y="{y+16}" font-size="13" font-weight="600" text-anchor="end" fill="{t["accent"]}">#{b["pr"]}</text>')
            y += 28
            lx = lay["bar_label"]
            bw = W - lx - lay["bar_tail"]
            for name, v, col in (("before", cell["before"], "before"), ("after", cell["after"], "after")):
                w = max(4, bw * float(v) / vmax)
                lab = f'{"about " if cell.get("approx") else ""}{num(v)} {cell["unit"]}'
                a(f'<text x="0" y="{y+15}" font-size="13" fill="{t["muted"]}">{name}</text>')
                a(f'<rect x="{lx}" y="{y+2}" width="{w:.1f}" height="18" rx="4" fill="{t[col]}"/>')
                a(f'<text x="{lx+w+8:.1f}" y="{y+16}" font-size="13" font-weight="600" fill="{t["text"]}">{esc(lab)}</text>')
                y += 26
            y += 18
    H = y - 10
    body = "\n  ".join(p)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{FONT}" role="img" aria-label="{esc(alt_text(data))}">\n  {body}\n</svg>\n')


def render_all(data):
    """{file name: svg text} for the four graphics."""
    out = {}
    for tname, t in THEMES.items():
        out[f"impact-{tname}.svg"] = svg(data, t, LAYOUTS["desktop"])
        out[f"impact-mobile-{tname}.svg"] = svg(data, t, LAYOUTS["mobile"])
    return out


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "assets")
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    for name, text in render_all(d).items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(text)
    print("ok")
