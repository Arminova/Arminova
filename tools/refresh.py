#!/usr/bin/env python3
# Refreshes the profile from data/tensorfold.json and GitHub:
#   1. pulls the totals (merged PRs, lines added, commits on main) from GitHub into the data file,
#   2. checks every before -> after against its stated percentage,
#   3. redraws the four SVGs in assets/ (tools/impact_svg.py),
#   4. rewrites the blocks of README.md between <!-- name:start --> and <!-- name:end -->.
# Re-running with nothing new changes no file. Needs the GitHub CLI (`gh`), logged in, unless --offline.
#   python3 tools/refresh.py             refresh everything
#   python3 tools/refresh.py --offline   redraw and rewrite from the data file only
#   python3 tools/refresh.py --check     change nothing; exit 1 if any file would change
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impact_svg  # noqa: E402

ROOT = impact_svg.ROOT
DATA = impact_svg.DATA
README = os.path.join(ROOT, "README.md")
ASSETS = os.path.join(ROOT, "assets")


# ---------- GitHub ----------

def gh(*args):
    r = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"gh api {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def fetch_totals(repo, author):
    q = f"repo:{repo} is:pr is:merged author:{author}"
    found = sorted(int(n) for n in gh("-X", "GET", "search/issues", "-f", f"q={q}", "-f", "per_page=100",
                                        "--jq", ".items[].number").split())
    by_pr = {}
    for n in found:
        a, m = gh(f"repos/{repo}/pulls/{n}", "--jq", '[.additions, .merged_at[0:10]] | @tsv').split()
        by_pr[str(n)] = {"additions": int(a), "merged": m}
    shas = gh("--paginate", f"repos/{repo}/commits?author={author}&per_page=100", "--jq", ".[].sha[0:9]").split()
    return {
        "merged_prs": len(found),
        "lines_added": sum(v["additions"] for v in by_pr.values()),
        "commits_on_main": len(shas),
        "by_pr": by_pr,
        "commit_shas": sorted(shas),
    }


# ---------- checks ----------

def decimals(v):
    s = repr(float(v))
    return len(s.split(".")[1]) if "." in s and not s.endswith(".0") else (1 if isinstance(v, float) else 0)


def check_cell(pr, c):
    """The stated percentage must be possible for the printed before and after (they are rounded)."""
    if "before" not in c or "after" not in c or "change_pct" not in c:
        return None
    b, a = float(c["before"]), float(c["after"])
    hb, ha = 0.5 * 10 ** -decimals(c["before"]), 0.5 * 10 ** -decimals(c["after"])
    cands = [((a + da) / (b + db) - 1) * 100 for da in (-ha, ha) for db in (-hb, hb)]
    lo, hi = min(cands), max(cands)
    s = float(c["change_pct"])
    # stated as printed: +3.7 % means [3.65, 3.75); +2 % means [1.5, 2.5)
    d = len(c["change_text"].split(".")[1].split()[0]) if "." in c["change_text"] and c.get("pct_stated") else 0
    half = 0.5 * 10 ** -d if c.get("pct_stated") else 0.05
    if hi < s - half or lo > s + half:
        return f"#{pr} {c['label']}: {c['before']} -> {c['after']} gives {lo:.2f} to {hi:.2f} %, data says {s} %"
    return None


def validate(data):
    problems = []
    seen = {p["pr"] for p in data["pull_requests"]}
    for m in data["models"]:
        for e in m["entries"]:
            if e["pr"] not in seen:
                problems.append(f"#{e['pr']} has gains but is missing from pull_requests")
            if e["measured_by"] not in ("maintainer", "own"):
                problems.append(f"#{e['pr']}: measured_by must be maintainer or own")
            for s in e["sources"]:
                if not s["url"].startswith(("http", "L")):
                    problems.append(f"#{e['pr']}: bad source {s['url']}")
            for c in e["cells"]:
                msg = check_cell(e["pr"], c)
                if msg:
                    problems.append(msg)
        for pr in m["graphic"]["cards"]:
            if pr not in {e["pr"] for e in m["entries"]}:
                problems.append(f"graphic card #{pr} not in model {m['id']}")
    return problems


# ---------- README blocks ----------

def source_url(data, u):
    return f"{data['changelog']}#{u}" if u.startswith("L") else u


def fmt_cell(c):
    lab = c["label"]
    if "before" in c and "after" in c:
        if c.get("approx"):
            txt = f"{lab}: about {c['before']:,} {c['unit']} → about {c['after']:,} {c['unit']}"
        else:
            txt = f"{lab}: {c['before']:,} → {c['after']:,} {c['unit']}"
    elif "before_text" in c:
        txt = f"{lab}: {c['before_text']} → {c['after_text']}"
    else:
        txt = f"{lab}"
    ch = c.get("change_text")
    if ch:
        dag = "†" if c.get("derived") else ""
        txt += f" ({ch}{dag})" if ("before" in c or "before_text" in c) else f": {ch}{dag}"
    return txt


def esc_cell(s):
    return s.replace("|", "\\|")


def pr_link(data, n):
    return f"[#{n}](https://github.com/{data['repo']}/pull/{n})"


def block_picture(data):
    alt = impact_svg.alt_text(data).replace('"', "'")
    return "\n".join([
        "<picture>",
        '  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/impact-mobile-dark.svg">',
        '  <source media="(max-width: 600px)" srcset="assets/impact-mobile-light.svg">',
        '  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">',
        f'  <img alt="{alt}" src="assets/impact-light.svg">',
        "</picture>",
    ])


def block_stats(data):
    t = data["totals"]
    repo = data["repo"]
    pulls = f"https://github.com/{repo}/pulls?q=is%3Apr+is%3Amerged+author%3A{data['author']}"
    commits = f"https://github.com/{repo}/commits/main/?author={data['author']}"
    lines = [
        f"**TensorFold** (upstream: [{repo}](https://github.com/{repo})): "
        f"**{t['merged_prs']}** [pull requests merged]({pulls}) · **{t['lines_added']:,}** lines added · "
        f"**{t['commits_on_main']}** [commits on main]({commits})",
        "",
        "<sub>Counted from GitHub by [tools/refresh.py](tools/refresh.py). Pull requests: those GitHub shows as merged. "
        "Lines added: the sum of those pull requests' additions. Commits: authored by me on TensorFold's main branch"
        + (f"; {data['definitions']['commits_note']}" if data["definitions"].get("commits_note") else "")
        + ".</sub>",
    ]
    return "\n".join(lines)


def block_gains(data):
    out = [
        "## What my pull requests changed, model by model",
        "",
        "Each row is one pull request, in the order they landed, with the gain the maintainer or I measured for it. "
        "Every number says who measured it and links its source: the maintainer's A/B comment on the pull request, "
        "[TensorFold's changelog](" + data["changelog"] + "), or my own receipt in the pull request description. "
        "The rows are separate before/after runs and do not add up to one total.",
    ]
    for m in data["models"]:
        out += ["", f"### {m['name']} · {m['subtitle']}", "",
                f"Checkpoint: `{m['checkpoint']}` unless a row says otherwise.", "",
                "| Pull request | What it changed | Result | Measured by | Source |",
                "|---|---|---|---|---|"]
        for e in m["entries"]:
            res = "<br>".join(esc_cell(fmt_cell(c)) for c in e["cells"])
            if e.get("checkpoint"):
                res = f"{esc_cell(e['checkpoint'])}<br>" + res
            if e["notes"]:
                res += "<br><sub>" + esc_cell(" ".join(e["notes"])) + "</sub>"
            src = " · ".join(f"[{s['label']}]({source_url(data, s['url'])})" for s in e["sources"])
            out.append(f"| {pr_link(data, e['pr'])} | {esc_cell(e['what'])} | {res} | {esc_cell(e['measured_text'])} | {src} |")
    out += ["", "† computed from the two stated figures; every other percentage is as the source states it."]
    return "\n".join(out)


def block_prs(data):
    by = data["totals"].get("by_pr", {})
    out = ["| Pull request | What it does | Status |", "|---|---|---|"]
    rows = []
    for p in data["pull_requests"]:
        n = p["pr"]
        if p["state"] == "merged":
            day = by.get(str(n), {}).get("merged", "")
            status = f"Merged {day}".strip()
        else:
            day = p["landed"]
            ev = " · ".join(f"[{e['label']}]({e['url']})" for e in p["evidence"][:2])
            status = f"Landed {day}: my commit is on main, but GitHub shows the pull request closed, not merged. {ev}"
        rows.append((day, n, f"| {pr_link(data, n)} | {esc_cell(p['table_what'])} | {status} |"))
    rows.sort(key=lambda r: (r[0], r[1]), reverse=True)
    return "\n".join(out + [r[2] for r in rows])


BLOCKS = {"impact": block_picture, "stats": block_stats, "gains": block_gains, "prs": block_prs}


def rewrite_readme(text, data):
    for name, fn in BLOCKS.items():
        pat = re.compile(rf"(<!-- {name}:start -->\n)(.*?)(\n<!-- {name}:end -->)", re.S)
        if not pat.search(text):
            sys.exit(f"README.md has no <!-- {name}:start --> ... <!-- {name}:end --> markers")
        body = fn(data)
        text = pat.sub(lambda m: m.group(1) + body + m.group(3), text)
    return text


# ---------- main ----------

def dump(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main():
    offline = "--offline" in sys.argv
    check = "--check" in sys.argv
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    exit_code = 0
    if not offline:
        totals = fetch_totals(data["repo"], data["author"])
        data["totals"] = totals
        known = {p["pr"] for p in data["pull_requests"]}
        new = [int(n) for n in totals["by_pr"] if int(n) not in known]
        if new:
            print("NEW MERGED PRs without an entry in data/tensorfold.json: " + ", ".join(f"#{n}" for n in new)
                  + "  -> add their gains and table rows, then re-run", file=sys.stderr)
            exit_code = 1
    problems = validate(data)
    for pmsg in problems:
        print("DATA PROBLEM:", pmsg, file=sys.stderr)
    if problems:
        sys.exit(2)

    outputs = {DATA: dump(data)}
    for name, text in impact_svg.render_all(data).items():
        outputs[os.path.join(ASSETS, name)] = text
    with open(README, encoding="utf-8") as f:
        outputs[README] = rewrite_readme(f.read(), data)

    changed = []
    for path, text in outputs.items():
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != text:
            changed.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
    t = data["totals"]
    if t:
        print(f"totals: {t['merged_prs']} merged PRs, {t['lines_added']:,} lines added, {t['commits_on_main']} commits on main")
    print(("would change: " if check else "changed: ") + (", ".join(changed) if changed else "nothing"))
    if check and changed:
        exit_code = exit_code or 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
