from collection import deque

graph = {
    "interent": {"upstream"},
    "upstream": {"internet", "core1", "core2"},
    "core1": {"acc1", "upstream"},
    "core2": {"acc1", "upstream"},
    "acc1": {"core1", "core2", "srv1"},
    "srv1": {"accl"}
}

def reachable(graph, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return seen

def remove_node(graph, node):
    return {n: edges - {node} for n, edges in graph.items() if n!= node}

before = reachable(graph, "srv1")
print("Before: ", before, "| internet reachable?", "internet" in before)

broken = remove_node(graph, "upstream")
after = reachable(broken, "srv1")
print("After reaching upstream: ", after, "| internet reachable?", "internet" in after)
