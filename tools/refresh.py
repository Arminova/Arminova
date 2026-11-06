#!/usr/bin/env python3
# Refreshes the TensorFold totals line of the profile:
#   1. pulls the totals (merged PRs, lines added, commits on main) from GitHub into data/tensorfold.json,
#   2. rewrites the block of README.md between <!-- stats:start --> and <!-- stats:end -->.
# Re-running with nothing new changes no file. Needs the GitHub CLI (`gh`), logged in, unless --offline.
#   python3 tools/refresh.py             refresh everything
#   python3 tools/refresh.py --offline   rewrite from the data file only
#   python3 tools/refresh.py --check     change nothing; exit 1 if any file would change
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "tensorfold.json")
README = os.path.join(ROOT, "README.md")


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


# ---------- README blocks ----------

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


BLOCKS = {"stats": block_stats}


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
    outputs = {DATA: dump(data)}
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
