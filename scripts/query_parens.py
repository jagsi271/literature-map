"""Make AND-over-OR precedence explicit in OpenAlex search strings.

OpenAlex runs search strings Lucene-style: in an unparenthesised mix such as
  "a" OR "b" OR "c" AND (x)
the AND operands become required and the OR operands optional, so the search behaves like
"c" AND (x) -- although the OQL the API echoes back shows the intended "a" OR "b" OR ("c" AND x).
`explicit(q)` rewrites a query so that every AND-chain that sits next to an OR is wrapped in
parentheses, giving the standard precedence (AND binds tighter than OR) at every level.

Usage: python3 scripts/query_parens.py        (lists the queries in queries.yaml that change)
"""
import re
import sys
from pathlib import Path

TOKEN = re.compile(r'"[^"]*"|\(|\)|\bAND\b|\bOR\b|\bNOT\b|[^\s()"]+')


def _parse(tokens, i=0):
    """Return (list of items, next index). Items are operands (str or list) and operators."""
    items = []
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            sub, i = _parse(tokens, i + 1)
            items.append(sub)
            continue
        elif t == ")":
            return items, i + 1
        else:
            items.append(t)
        i += 1
    return items, i


def _render(items):
    # split into operand groups joined by AND (or NOT), separated by OR
    parts, cur = [], []
    for it in items:
        if it == "OR":
            parts.append(cur)
            cur = []
        else:
            cur.append(it)
    parts.append(cur)

    def r(x):
        return "(" + _render(x) + ")" if isinstance(x, list) else x

    rendered = []
    for p in parts:
        s = " ".join(r(x) for x in p)
        has_and = any(x in ("AND", "NOT") for x in p)
        rendered.append(f"({s})" if has_and and len(parts) > 1 else s)
    return " OR ".join(rendered)


def explicit(q: str) -> str:
    items, _ = _parse(TOKEN.findall(q))
    return _render(items)


def _norm(q):
    return " ".join(TOKEN.findall(q))


if __name__ == "__main__":
    import yaml
    cfg = yaml.safe_load((Path(__file__).resolve().parent.parent / "queries.yaml").read_text())
    groups = list(cfg["themes"].items()) + list((cfg.get("supplementary") or {}).items())
    n = 0
    for t, tc in groups:
        for i, q in enumerate(tc["queries"], 1):
            e = explicit(q)
            if _norm(e) != _norm(q):
                n += 1
                print(f"{t} q{i}:\n  old: {q}\n  new: {e}")
    print(n, "queries change")
