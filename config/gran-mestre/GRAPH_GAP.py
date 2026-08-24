#!/usr/bin/env python3
"""
GRAPH_GAP.py — Graph Gap Analysis do cérebro neural.
Detecta clusters isolados e sugere novas sinapses entre eles.

Uso:
  python3 GRAPH_GAP.py                    # Análise completa
  python3 GRAPH_GAP.py --suggest          # + Sugestões de novos links
  python3 GRAPH_GAP.py --json             # JSON para processamento
"""
import json, os, sys
from collections import defaultdict, Counter
from datetime import datetime

VAULT = "/mnt/dados/cerebro com IA"

def load_manifest():
    path = os.path.join(VAULT, ".manifest.json")
    with open(path) as f:
        return json.load(f)

def build_graph(manifest):
    """Build adjacency list from [[wikilinks]]."""
    graph = defaultdict(set)
    for page, data in manifest.items():
        name = page.split("/")[-1].replace(".md", "")
        for link in data.get("links", []):
            graph[name].add(link)
            # Ensure back-reference
            graph[link].add(name)
    return graph

def find_communities(graph, max_iter=100):
    """Simple label propagation for community detection."""
    nodes = list(graph.keys())
    labels = {node: i for i, node in enumerate(nodes)}

    for _ in range(max_iter):
        shuffled = list(nodes)
        import random
        random.shuffle(shuffled)
        changed = False
        for node in shuffled:
            if node not in graph or not graph[node]:
                continue
            neighbor_labels = [labels[n] for n in graph[node] if n in labels]
            if not neighbor_labels:
                continue
            most_common = Counter(neighbor_labels).most_common(1)[0][0]
            if labels[node] != most_common:
                labels[node] = most_common
                changed = True
        if not changed:
            break

    # Group by label
    communities = defaultdict(list)
    for node, label in labels.items():
        communities[label].append(node)
    return list(communities.values())

def analyze_gaps(manifest, communities):
    """Find gaps between communities."""
    # Build set of all nodes per community
    comm_sets = [set(c) for c in communities]

    # Count inter-community links
    inter_links = defaultdict(int)
    intra_links = defaultdict(int)

    for page, data in manifest.items():
        name = page.split("/")[-1].replace(".md", "")
        my_comm = None
        for i, cs in enumerate(comm_sets):
            if name in cs:
                my_comm = i
                break
        for link in data.get("links", []):
            link_name = link.split("/")[-1].replace(".md", "").replace("]]", "")
            for i, cs in enumerate(comm_sets):
                if link_name in cs:
                    if i == my_comm:
                        intra_links[my_comm] += 1
                    else:
                        inter_links[(my_comm, i)] += 1
                    break

    # Communities with no inter-community links are "isolated"
    communities_with_links = set()
    for (c1, c2) in inter_links:
        communities_with_links.add(c1)
        communities_with_links.add(c2)

    isolated = [i for i in range(len(communities)) if i not in communities_with_links]

    return inter_links, intra_links, isolated

def suggest_new_links(manifest, communities):
    """Suggest new [[links]] between isolated communities."""
    suggestions = []
    comm_sets = [set(c) for c in communities]

    for i in range(len(communities)):
        for j in range(i + 1, len(communities)):
            # Find nodes in community i that don't link to community j
            nodes_i = [n for n in communities[i] if n in [p.split("/")[-1].replace(".md", "") for p in manifest]]
            nodes_j = [n for n in communities[j] if n in [p.split("/")[-1].replace(".md", "") for p in manifest]]

            if nodes_i and nodes_j:
                # Suggest linking the most central node of each community
                suggestions.append(f"{nodes_i[0]} ⟷ {nodes_j[0]}")

    return suggestions

def generate_report(manifest, communities, inter_links, intra_links, isolated, suggestions):
    print("=" * 56)
    print("  GRAPH GAP ANALYSIS — Cérebro Neural Obsidian")
    print("=" * 56)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    n = len(manifest)
    total_links = sum(len(v.get("links", [])) for v in manifest.values())
    print(f"  Neurônios totais: {n}")
    print(f"  Sinapses totais:  {total_links}")
    print()

    # Communities
    print(f"  Comunidades detectadas: {len(communities)}")
    for i, comm in enumerate(communities):
        intra = intra_links.get(i, 0)
        size = len(comm)
        marker = " 🔒 ISOLADA" if i in isolated else ""
        print(f"    C{i}: {size} neurônios, {intra} links internos{marker}")
        for node in comm:
            print(f"      - {node}")
    print()

    # Gap analysis
    if isolated:
        print(f"  🔴 CLUSTERS ISOLADOS ({len(isolated)}):")
        for i in isolated:
            print(f"    Comunidade {i} — {len(communities[i])} neurônios sem links externos")
            for node in communities[i]:
                print(f"      - {node}")
    else:
        print("  ✅ Nenhum cluster isolado — rede bem conectada")
    print()

    # Suggested links
    if suggestions:
        print(f"  💡 NOVAS SINAPSES SUGERIDAS ({len(suggestions)}):")
        for s in suggestions:
            print(f"    [[{s}]]")
    else:
        print("  💡 Nenhuma nova sinapse necessária")
    print("=" * 56)

    return {
        "neurons": n,
        "synapses": total_links,
        "communities": len(communities),
        "isolated": len(isolated),
        "suggestions": len(suggestions)
    }

if __name__ == "__main__":
    manifest = load_manifest()
    graph = build_graph(manifest)
    communities = find_communities(graph)
    inter_links, intra_links, isolated = analyze_gaps(manifest, communities)

    if "--suggest" in sys.argv:
        suggestions = suggest_new_links(manifest, communities)
    else:
        suggestions = []

    result = generate_report(manifest, communities, inter_links, intra_links, isolated, suggestions)

    if "--json" in sys.argv:
        import json as j
        print(j.dumps(result, indent=2))
