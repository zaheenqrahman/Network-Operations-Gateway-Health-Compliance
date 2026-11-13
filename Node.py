"""Remove nodes / links / power feeds from topology.yaml, then check each server still has a path to upstream.

  py netcheck.py                       full report (every single failure + breaking pairs)
  py netcheck.py --node core1          one scenario, with the path each server would use
  py netcheck.py --link acc1 core1 --feed A
"""
import argparse, itertools, re
from collections import defaultdict, deque
from pathlib import Path


def load(path):
    text = Path(path).read_text()
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:  # tiny fallback that understands this file's one-line {..} / [..] entries
        d = {"devices": [], "network_links": [], "power": {"psu_links": []}}
        for line in text.splitlines():
            line = line.split("#")[0].strip()
            if m := re.match(r"- \{(.+)\}$", line):
                kv = dict(p.strip().split(": ") for p in m.group(1).split(","))
                (d["devices"] if "name" in kv else d["power"]["psu_links"]).append(kv)
            elif m := re.match(r"- \[(.+),(.+)\]$", line):
                d["network_links"].append([m.group(1).strip(), m.group(2).strip()])
        return d


topo = load(Path(__file__).with_name("topology.yaml"))
nodes = [d["name"] for d in topo["devices"]]
servers = [d["name"] for d in topo["devices"] if d["role"] == "server"]
TARGET = next(d["name"] for d in topo["devices"] if d["role"] == "upstream")
links = [tuple(l) for l in topo["network_links"]]
psu_links = topo["power"]["psu_links"]
feeds = sorted({p["feed"] for p in psu_links})


def unpowered(down_feeds):
    """A device is dead only if every one of its PSUs sits on a failed feed."""
    by_dev = defaultdict(list)
    for p in psu_links:
        by_dev[p["device"]].append(p["feed"])
    return {dev for dev, fs in by_dev.items() if all(f in down_feeds for f in fs)}


def check(down_nodes=(), down_links=(), down_feeds=()):
    """Return {server: path list | 'DOWN' | None} for the given failures."""
    dead = set(down_nodes) | unpowered(down_feeds)
    cut = {frozenset(l) for l in down_links}
    adj = defaultdict(list)
    for a, b in links:
        if a in dead or b in dead or frozenset((a, b)) in cut:
            continue
        adj[a].append(b); adj[b].append(a)
    result = {}
    for s in servers:
        if s in dead:
            result[s] = "DOWN"; continue
        if TARGET in dead:
            result[s] = None; continue
        prev, q = {s: None}, deque([s])          # BFS, remembering how we got to each node
        while q:
            n = q.popleft()
            for m in adj[n]:
                if m not in prev:
                    prev[m] = n; q.append(m)
        if TARGET not in prev:
            result[s] = None; continue
        path, n = [], TARGET
        while n is not None:
            path.append(n); n = prev[n]
        result[s] = path[::-1]
    return result


def lost(result):
    return [s for s, r in result.items() if r is None]


def describe(label, result, detail=False):
    bad = lost(result)
    print(f"{label:28} {'LOST ' + ','.join(bad) if bad else 'OK'}")
    if detail:
        for s, r in result.items():
            print(f"    {s}: {'  >  '.join(r) if isinstance(r, list) else r or 'NO PATH to ' + TARGET}")


def full_report():
    print(f"baseline: {check()}\n")
    print("-- one node down --")
    for n in nodes:
        describe(n, check(down_nodes=(n,)))
    print("\n-- one link down --")
    for l in links:
        describe(f"{l[0]}-{l[1]}", check(down_links=(l,)))
    print("\n-- one power feed down --")
    for f in feeds:
        describe(f"feed {f}", check(down_feeds=(f,)))
    print("\n-- two failures that break a server NEITHER breaks alone --")
    things = [("node", n) for n in nodes if n not in servers + [TARGET]] + \
             [("link", l) for l in links] + [("feed", f) for f in feeds]

    def run(*ts):
        args = {"down_nodes": [], "down_links": [], "down_feeds": []}
        for kind, x in ts:
            args[f"down_{kind}s"].append(x)
        return check(**args)

    name = lambda t: f"{t[0]} {t[1] if t[0] != 'link' else '-'.join(t[1])}"
    found = 0
    for a, b in itertools.combinations(things, 2):
        new_loss = set(lost(run(a, b))) - set(lost(run(a))) - set(lost(run(b)))
        if new_loss:
            found += 1
            print(f"{name(a) + ' + ' + name(b):44} LOST {','.join(sorted(new_loss))}")
    if not found:
        print("none")


ap = argparse.ArgumentParser()
ap.add_argument("--node", action="append", default=[])
ap.add_argument("--link", nargs=2, action="append", default=[], metavar=("A", "B"))
ap.add_argument("--feed", action="append", default=[])
a = ap.parse_args()
if a.node or a.link or a.feed:
    for n in a.node:
        if n not in nodes: ap.error(f"unknown node {n}")
    describe("custom failure", check(a.node, a.link, a.feed), detail=True)
else:
    full_report()
