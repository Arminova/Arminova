# Writes assets/impact-light.svg and assets/impact-dark.svg for the profile README: python3 tools/impact_svg.py assets
import sys, os
out = sys.argv[1]
W = 880
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": dict(card="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#59636e", after="#1a7f37", before="#c8d1da", accent="#0969da"),
    "dark": dict(card="#161b22", border="#30363d", text="#e6edf3", muted="#9198a1", after="#3fb950", before="#3d444d", accent="#4493f8"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def svg(t):
    p = []
    a = p.append
    y = 0
    a(f'<text x="0" y="{y+22}" font-size="20" font-weight="600" fill="{t["text"]}">What my TensorFold pull requests changed</text>')
    a(f'<text x="0" y="{y+44}" font-size="13" fill="{t["muted"]}">Numbers as TensorFold\'s changelog states them</text>')
    y += 66
    a(f'<text x="0" y="{y+16}" font-size="17" font-weight="600" fill="{t["text"]}">Flash Next on one DGX Spark (GB10)</text>')
    y += 32
    cards = [("2.4×", "faster server start", "200 s → 83 s", "#1368"),
             ("+11.5 %", "one-stream decode", "chat +8.7 % · code +6.3 %", "#1786"),
             ("+4–5 %", "cold prompts", "less work in every prompt pass", "#1764")]
    gap = 16
    cw = (W - 2 * gap) / 3
    ch = 124
    for i, (big, label, note, pr) in enumerate(cards):
        x = i * (cw + gap)
        a(f'<rect x="{x+0.5}" y="{y+0.5}" width="{cw-1}" height="{ch-1}" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>')
        a(f'<text x="{x+20}" y="{y+50}" font-size="36" font-weight="700" fill="{t["after"]}">{esc(big)}</text>')
        a(f'<text x="{x+20}" y="{y+76}" font-size="15" font-weight="600" fill="{t["text"]}">{esc(label)}</text>')
        a(f'<text x="{x+20}" y="{y+100}" font-size="13" fill="{t["muted"]}">{esc(note)}</text>')
        a(f'<text x="{x+cw-20}" y="{y+100}" font-size="13" font-weight="600" text-anchor="end" fill="{t["accent"]}">{pr}</text>')
    y += ch + 28

    def bars(title, pr, rows, unit, vmax):
        nonlocal y
        a(f'<text x="0" y="{y+16}" font-size="15" font-weight="600" fill="{t["text"]}">{esc(title)}</text>')
        a(f'<text x="{W}" y="{y+16}" font-size="13" font-weight="600" text-anchor="end" fill="{t["accent"]}">{pr}</text>')
        y += 28
        lx, bw = 70, W - 70 - 90
        for name, v, col in rows:
            w = max(4, bw * float(v) / vmax)
            a(f'<text x="0" y="{y+15}" font-size="13" fill="{t["muted"]}">{name}</text>')
            a(f'<rect x="{lx}" y="{y+2}" width="{w:.1f}" height="18" rx="4" fill="{t[col]}"/>')
            a(f'<text x="{lx+w+8:.1f}" y="{y+16}" font-size="13" font-weight="600" fill="{t["text"]}">{v} {unit}</text>')
            y += 26
        y += 18

    bars("Server start with Qwen3.8-Flash-Next-FP4-Local", "#1368", [("before", "200", "before"), ("after", "83", "after")], "s", 243)
    a(f'<line x1="0" y1="{y-4}" x2="{W}" y2="{y-4}" stroke="{t["border"]}"/>')
    y += 18
    a(f'<text x="0" y="{y+16}" font-size="17" font-weight="600" fill="{t["text"]}">Prompt tiles on an M1 Pro Mac: 62× faster</text>')
    y += 34
    bars("A 2,048-row prompt chunk", "#1590", [("before", "243", "before"), ("after", "3.9", "after")], "s", 243)
    bars("First token of a cold 930-token prompt", "#1590", [("before", "212", "before"), ("after", "2.0", "after")], "s", 243)
    H = y - 10
    body = "\n  ".join(p)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{FONT}" role="img" aria-label="Before and after numbers of my TensorFold pull requests">\n  {body}\n</svg>\n')

for name, t in THEMES.items():
    open(os.path.join(out, f"impact-{name}.svg"), "w").write(svg(t))
print("ok")
