"""Public tests for Project 3: Pathfinder.

These tests check the required API and important graph edge cases.

Students should add at least 3 meaningful tests of their own.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.project import (
    bfs_order,
    dijkstra_distances,
    get_neighbors,
    load_graph,
    shortest_path,
)


def sample_graph() -> dict[str, dict[str, int]]:
    """Return a small undirected weighted graph with a unique shortest path."""
    return {
        "A": {"B": 4, "C": 2},
        "B": {"A": 4, "C": 1, "D": 5},
        "C": {"A": 2, "B": 1, "D": 8, "E": 10},
        "D": {"B": 5, "C": 8, "E": 2, "Z": 6},
        "E": {"C": 10, "D": 2, "Z": 3},
        "Z": {"D": 6, "E": 3},
    }


def disconnected_graph() -> dict[str, dict[str, int]]:
    """Return a graph with two disconnected components."""
    return {
        "A": {"B": 2},
        "B": {"A": 2},
        "X": {"Y": 1},
        "Y": {"X": 1},
    }


def cyclic_graph() -> dict[str, dict[str, int]]:
    """Return a graph with a cycle."""
    return {
        "A": {"B": 1, "C": 1},
        "B": {"A": 1, "C": 1},
        "C": {"A": 1, "B": 1, "D": 1},
        "D": {"C": 1},
    }


def test_load_graph_reads_json_file(tmp_path):
    graph_data = {
        "Gate": {"Food": 4, "Stage": 7},
        "Food": {"Gate": 4},
        "Stage": {"Gate": 7},
    }
    map_path = tmp_path / "map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    assert load_graph(str(map_path)) == graph_data


def test_load_graph_rejects_zero_weight(tmp_path):
    graph_data = {
        "A": {"B": 0},
        "B": {"A": 0},
    }
    map_path = tmp_path / "bad_map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError):
        load_graph(str(map_path))


def test_load_graph_rejects_negative_weight(tmp_path):
    graph_data = {
        "A": {"B": -3},
        "B": {"A": -3},
    }
    map_path = tmp_path / "bad_map.json"
    map_path.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError):
        load_graph(str(map_path))


def test_get_neighbors_existing_node():
    graph = sample_graph()

    assert get_neighbors(graph, "A") == {"B": 4, "C": 2}


def test_get_neighbors_missing_node_returns_empty_dict():
    graph = sample_graph()

    assert get_neighbors(graph, "Missing") == {}


def test_bfs_order_connected_graph():
    graph = sample_graph()

    assert bfs_order(graph, "A") == ["A", "B", "C", "D", "E", "Z"]


def test_bfs_order_missing_start_returns_empty_list():
    graph = sample_graph()

    assert bfs_order(graph, "Missing") == []


def test_bfs_order_handles_cycle_without_repeating_nodes():
    graph = cyclic_graph()

    result = bfs_order(graph, "A")

    assert result == ["A", "B", "C", "D"]
    assert len(result) == len(set(result))


def test_bfs_order_does_not_cross_disconnected_components():
    graph = disconnected_graph()

    assert bfs_order(graph, "A") == ["A", "B"]


def test_dijkstra_distances_from_start():
    graph = sample_graph()

    assert dijkstra_distances(graph, "A") == {
        "A": 0,
        "B": 3,
        "C": 2,
        "D": 8,
        "E": 10,
        "Z": 13,
    }


def test_dijkstra_missing_start_returns_empty_dict():
    graph = sample_graph()

    assert dijkstra_distances(graph, "Missing") == {}


def test_dijkstra_does_not_include_unreachable_nodes():
    graph = disconnected_graph()

    assert dijkstra_distances(graph, "A") == {"A": 0, "B": 2}


def test_dijkstra_rejects_zero_or_negative_weights():
    graph = {
        "A": {"B": 2},
        "B": {"A": 2, "C": 0},
        "C": {"B": 0},
    }

    with pytest.raises(ValueError):
        dijkstra_distances(graph, "A")


def test_shortest_path_returns_best_path():
    graph = sample_graph()

    assert shortest_path(graph, "A", "Z") == ["A", "C", "B", "D", "E", "Z"]


def test_shortest_path_start_equals_target():
    graph = sample_graph()

    assert shortest_path(graph, "A", "A") == ["A"]


def test_shortest_path_missing_start_or_target_returns_empty_list():
    graph = sample_graph()

    assert shortest_path(graph, "Missing", "A") == []
    assert shortest_path(graph, "A", "Missing") == []


def test_shortest_path_unreachable_returns_empty_list():
    graph = disconnected_graph()

    assert shortest_path(graph, "A", "Y") == []


# ---------------------------------------------------------------------------
# Custom tests (3 required)
# ---------------------------------------------------------------------------

def test_village_map_loads_and_has_correct_size():
    """Custom 1: the actual village map loads with exactly 8 nodes."""
    data_path = Path(__file__).parent.parent / "data" / "map.json"
    graph = load_graph(str(data_path))
    assert len(graph) == 7


def test_village_map_is_undirected():
    """Custom 2: every edge A->B has a matching B->A with the same weight."""
    data_path = Path(__file__).parent.parent / "data" / "map.json"
    graph = load_graph(str(data_path))
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            assert node in graph[neighbor], (
                f"Missing reverse edge '{neighbor}' -> '{node}'"
            )
            assert graph[neighbor][node] == weight, (
                f"Weight mismatch on '{neighbor}' -> '{node}'"
            )


def test_shortest_path_cost_matches_dijkstra():
    """Custom 3: sum of edge weights along the path equals the dijkstra distance."""
    graph = sample_graph()
    start, target = "A", "Z"
    path = shortest_path(graph, start, target)
    dists = dijkstra_distances(graph, start)
    path_cost = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
    assert path_cost == dists[target]