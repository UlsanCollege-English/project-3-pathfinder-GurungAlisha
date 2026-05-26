"""Project 3: Pathfinder.

Implement graph utilities for an undirected weighted map.

Rules:
- Python 3.11+
- stdlib only
- weights must be positive integers (no zero or negative weights)
- graph representation: dict[str, dict[str, int]]

Example graph:

    {
        "Gate": {
            "Food Court": 4,
            "Stage": 7,
        },
        "Food Court": {
            "Gate": 4,
            "Rest Area": 3,
        },
    }

Students:
- Replace each NotImplementedError with your implementation.
- Keep function names and parameters exactly as written.
- Add helper functions if they make your code clearer.
"""

from __future__ import annotations

from collections import deque
import heapq
import json
import math
from pathlib import Path


Graph = dict[str, dict[str, int]]

_DATA_PATH = Path(__file__).parent.parent / "data" / "map.json"


def load_graph(path: str) -> Graph:
    """Load a weighted graph from a JSON file.

    The JSON file must contain a dictionary of dictionaries:

        {
            "A": {"B": 3, "C": 5},
            "B": {"A": 3},
            "C": {"A": 5}
        }

    Requirements:
    - Return the loaded graph.
    - Raise ValueError if the JSON top level is not a dictionary.
    - Raise ValueError if any neighbor list is not a dictionary.
    - Raise ValueError if any weight is not a positive integer.
    - Raise ValueError if any weight is 0 or negative.

    Note:
    This project uses an undirected graph. Your own map should include both
    directions for every edge, such as A -> B and B -> A.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Graph JSON must be a top-level dictionary.")

    for node, neighbors in data.items():
        if not isinstance(neighbors, dict):
            raise ValueError(
                f"Neighbors of '{node}' must be a dictionary, "
                f"got {type(neighbors).__name__}."
            )
        for neighbor, weight in neighbors.items():
            if not isinstance(weight, int) or isinstance(weight, bool):
                raise ValueError(
                    f"Weight for '{node}' -> '{neighbor}' must be an integer, "
                    f"got {type(weight).__name__}."
                )
            if weight <= 0:
                raise ValueError(
                    f"Weight for '{node}' -> '{neighbor}' must be positive, "
                    f"got {weight}."
                )

    return data


def get_neighbors(graph: Graph, node: str) -> dict[str, int]:
    """Return the neighbors and weights for node.

    If node is missing, return an empty dictionary.

    Example:
        graph = {"A": {"B": 4}}
        get_neighbors(graph, "A") -> {"B": 4}
        get_neighbors(graph, "Z") -> {}
    """
    return graph.get(node, {})


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Return nodes in breadth-first traversal order.

    Requirements:
    - If start is missing, return [].
    - Use a queue.
    - Use a visited set.
    - Follow the neighbor order from the dictionary.
    - Ignore weights for BFS traversal.

    Complexity target:
    - Time: O(V + E)
    - Space: O(V)
    """
    if start not in graph:
        return []

    visited: set[str] = {start}
    queue: deque[str] = deque([start])
    order: list[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dijkstra_distances(graph: Graph, start: str) -> dict[str, float]:
    """Return shortest distances from start to every reachable node.

    Requirements:
    - Use Dijkstra's algorithm.
    - Use heapq as the priority queue.
    - If start is missing, return {}.
    - Ignore unreachable nodes; they should not appear in the result.
    - All edge weights must be positive integers.
    - Raise ValueError if a zero or negative weight is found.

    Example:
        graph = {
            "A": {"B": 4, "C": 2},
            "B": {"A": 4},
            "C": {"A": 2}
        }

        dijkstra_distances(graph, "A") -> {"A": 0, "B": 4, "C": 2}

    Complexity target:
    - Time: O((V + E) log V)
    - Space: O(V)
    """
    if start not in graph:
        return {}

    distances: dict[str, float] = {start: 0}
    heap: list[tuple[float, str]] = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)

        if cost > distances.get(node, math.inf):
            continue

        for neighbor, weight in graph[node].items():
            if weight <= 0:
                raise ValueError(
                    f"Non-positive weight {weight} on '{node}' -> '{neighbor}'."
                )
            new_cost = cost + weight
            if new_cost < distances.get(neighbor, math.inf):
                distances[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return distances


def shortest_path(graph: Graph, start: str, target: str) -> list[str]:
    """Return the shortest path from start to target.

    Requirements:
    - Use Dijkstra's algorithm with path reconstruction.
    - Return a list of node names in path order.
    - If start or target is missing, return [].
    - If target is unreachable from start, return [].
    - If start == target and start exists, return [start].
    - Raise ValueError if a zero or negative weight is found.

    Example:
        shortest_path(graph, "A", "D") -> ["A", "C", "D"]

    Complexity target:
    - Dijkstra portion: O((V + E) log V)
    - Path reconstruction: O(P), where P is the number of nodes in the path
    """
    if start not in graph or target not in graph:
        return []

    if start == target:
        return [start]

    distances: dict[str, float] = {start: 0}
    previous: dict[str, str | None] = {start: None}
    heap: list[tuple[float, str]] = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)

        if cost > distances.get(node, math.inf):
            continue

        for neighbor, weight in graph[node].items():
            if weight <= 0:
                raise ValueError(
                    f"Non-positive weight {weight} on '{node}' -> '{neighbor}'."
                )
            new_cost = cost + weight
            if new_cost < distances.get(neighbor, math.inf):
                distances[neighbor] = new_cost
                previous[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    if target not in distances:
        return []

    path: list[str] = []
    current: str | None = target
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return path


def demo() -> None:
    """Print a short demonstration of your project.

    Your demo should:
    1. Load your graph from data/map.json.
    2. Print the number of locations.
    3. Print BFS order from one location.
    4. Print shortest distances from one location.
    5. Print one shortest path.

    This function is not directly graded by the public tests, but it is useful
    for your presentation/demo.
    """
    print("=" * 55)
    print("  Fantasy Village Pathfinder — Demo")
    print("=" * 55)

    graph = load_graph(str(_DATA_PATH))
    print(f"\n[1] Map loaded from: {_DATA_PATH.name}")

    print(f"[2] Number of locations: {len(graph)}")
    for loc in graph:
        print(f"     • {loc}")

    start = "Village Gate"
    bfs = bfs_order(graph, start)
    print(f"\n[3] BFS traversal from '{start}':")
    print("    " + " -> ".join(bfs))

    dists = dijkstra_distances(graph, start)
    print(f"\n[4] Shortest walking times from '{start}' (minutes):")
    for loc, d in sorted(dists.items(), key=lambda x: x[1]):
        print(f"     {d:>3} min  {loc}")

    target = "Wizard Tower"
    path = shortest_path(graph, start, target)
    total = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
    print(f"\n[5] Shortest path from '{start}' to '{target}':")
    print("    " + " -> ".join(path))
    print(f"    Total walking time: {total} minutes")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    demo()