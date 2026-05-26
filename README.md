[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/RNukvtFO)
# Project 3: Pathfinder

## Map Theme

Fantasy village — a small medieval settlement with eight named locations connected by walking paths.

## Map Picture

![Project map](assets/map.png)

The map shows all eight locations as nodes, all eleven walking paths as edges, and the walking time in minutes as the weight on each edge.

## How the Graph Works

### Nodes

Each node is a named location in the fantasy village.

```text
Village Gate, Market Square, Blacksmith, Inn,
Town Hall, Wizard Tower, Temple, Graveyard
```

### Edges

Each edge is a walking path that connects two locations directly. Because the graph is undirected, every path works in both directions with the same cost.

### Weights

Each weight is the walking time in minutes between the two connected locations. All weights are positive integers.

## Features Implemented

- [x] Load graph from JSON
- [x] Get neighbors
- [x] BFS traversal
- [x] Dijkstra shortest distances
- [x] Shortest path reconstruction
- [x] Demo function
- [x] Extra tests

## How to Run

```bash
python src/project.py
```

The demo loads the map, prints all locations, shows BFS traversal from Village Gate, prints the shortest walking time to every location, and shows the fastest route from Village Gate to Graveyard.

## How to Test

```bash
pytest -q
```

All 20 tests should pass.

## Complexity

### BFS

Time:

```text
O(V + E)
```

Space:

```text
O(V)
```

Explanation:

`V` is the number of nodes and `E` is the number of edges. BFS enqueues and dequeues each node at most once, which costs `O(V)`. For each node it checks all of its neighbors, so across the whole traversal every edge is visited once, adding `O(E)`. The visited set and queue each hold at most `V` nodes at a time, so space is `O(V)`.

### Dijkstra

Time:

```text
O((V + E) log V)
```

Space:

```text
O(V)
```

Explanation:

`V` is the number of nodes and `E` is the number of edges. Each time a shorter path to a neighbor is found, that neighbor is pushed onto the `heapq` priority queue. In the worst case this happens once per edge, giving `O(E)` pushes. Each heap push or pop costs `O(log V)` because the heap holds at most `V` entries. The distances dictionary and the heap each hold at most `V` entries, so space is `O(V)`.

### Shortest Path Reconstruction

Time:

```text
O(P)
```

Space:

```text
O(P)
```

Explanation:

`P` is the number of nodes in the returned path. After Dijkstra finishes, reconstruction follows the `previous` dictionary one step at a time from the target back to the start, which takes `O(P)` steps. The path list built and reversed also holds `P` entries, so space is `O(P)`.

## Edge Cases

- [x] Missing start node — `bfs_order`, `dijkstra_distances`, and `shortest_path` return `[]` or `{}`
- [x] Missing target node — `shortest_path` returns `[]`
- [x] Start equals target — `shortest_path` returns `[start]`
- [x] Unreachable target — `shortest_path` returns `[]`; unreachable nodes are excluded from `dijkstra_distances`
- [x] Graph with a cycle — the visited set in BFS and the stale-entry skip in Dijkstra prevent infinite loops
- [x] Graph with one node — all functions handle a single isolated node without errors
- [x] Disconnected graph — only reachable nodes appear in `dijkstra_distances`; `shortest_path` returns `[]` for unreachable targets
- [x] Multiple possible paths — Dijkstra always picks the minimum-cost route
- [x] Zero weight rejected — `load_graph`, `dijkstra_distances`, and `shortest_path` all raise `ValueError`
- [x] Negative weight rejected — same as above

## Known Limitations

- Does not support directed graphs; every edge is bidirectional.
- Does not support negative weights; Dijkstra requires positive costs.
- When two paths tie on total cost, only one valid shortest path is returned.
- Does not use a GUI or interactive map view.

## Assistance & Sources

### AI Used?

Yes

### What AI Helped With

- Code structure and implementation of all required functions
- Designing the fantasy village map and edge weights
- Writing and organizing the test cases
- Drafting and reviewing this README

### Other Sources

- Python `collections.deque` documentation: https://docs.python.org/3/library/collections.html#collections.deque
- Python `heapq` documentation: https://docs.python.org/3/library/heapq.html
- Dijkstra's algorithm reviewed from course lecture notes