"""Download street networks for each locality, compute metrics, draw SVGs.

Run with:  conda run -n sw_blr python build_data.py
Outputs:   data/metrics.csv, data/svgs.json, data/graphs/*.graphml
"""
import json
import math
from pathlib import Path

import numpy as np
import osmnx as ox
import pandas as pd
from shapely.geometry import Point, box

from localities import LOCALITIES

HALF_SIDE = 500  # metres, so each window is 1 km x 1 km
NUM_BINS = 36    # 10-degree bins for street orientation
UTM = "EPSG:32643"
DATA = Path("data")
GRAPHS = DATA / "graphs"


def slug(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")


def get_graph(loc):
    """Load the cached graph, or download it from OpenStreetMap."""
    path = GRAPHS / f"{slug(loc['name'])}.graphml"
    if path.exists():
        return ox.load_graphml(path)
    G = ox.graph_from_point((loc["lat"], loc["lon"]), dist=HALF_SIDE + 150,
                            dist_type="bbox", network_type="drive")
    ox.save_graphml(G, path)
    return G


def clip_to_window(G, loc):
    """Project to UTM and keep only nodes inside the 1 km square."""
    Gp = ox.project_graph(G, to_crs=UTM)
    centre, _ = ox.projection.project_geometry(Point(loc["lon"], loc["lat"]), to_crs=UTM)
    cx, cy = centre.x, centre.y
    window = box(cx - HALF_SIDE, cy - HALF_SIDE, cx + HALF_SIDE, cy + HALF_SIDE)
    inside = [n for n, d in Gp.nodes(data=True) if window.contains(Point(d["x"], d["y"]))]
    return Gp.subgraph(inside).copy(), window


def orientation_order(Gu):
    """Gu must be an unprojected, undirected graph.

    Boeing's orientation order: 0 = uniform (organic), 1 = perfect grid."""
    h = ox.bearing.orientation_entropy(Gu, num_bins=NUM_BINS, weight="length")
    h_max = math.log(NUM_BINS)
    h_grid = math.log(4)
    return 1 - ((h - h_grid) / (h_max - h_grid)) ** 2


def bearing_counts(Gu):
    """Length-weighted share of street length in each 10-degree bin (0-360)."""
    bearings, weights = [], []
    for u, v, d in Gu.edges(data=True):
        if u != v and not np.isnan(d["bearing"]):
            # count each undirected street in both directions
            bearings += [d["bearing"], (d["bearing"] + 180) % 360]
            weights += [d["length"], d["length"]]
    # shift by half a bin so that 0 degrees sits in the middle of the first bin
    edges = np.arange(-5, 360, 360 / NUM_BINS)
    shifted = (np.array(bearings) + 5) % 360 - 5
    counts, _ = np.histogram(shifted, bins=edges, weights=weights)
    return (counts / counts.sum()).round(4).tolist()


def street_svg(Gp, window):
    """Draw the clipped network as SVG paths in a 1000 x 1000 box."""
    edges = ox.graph_to_gdfs(Gp, nodes=False)
    edges = edges.clip(window)
    minx, miny, _, _ = window.bounds
    paths = []
    for geom in edges.geometry:
        lines = getattr(geom, "geoms", [geom])
        for line in lines:
            if line.geom_type != "LineString":
                continue
            pts = [f"{x - minx:.0f},{1000 - (y - miny):.0f}" for x, y in line.coords]
            paths.append("M" + "L".join(pts))
    return " ".join(paths)


def metrics(Gp, Gu):
    stats = ox.stats.basic_stats(Gp, area=(2 * HALF_SIDE) ** 2)
    props = stats["streets_per_node_proportions"]
    return {
        "orientation_order": round(orientation_order(Gu), 3),
        "intersection_density_km2": round(stats["intersection_density_km"], 1),
        "four_way_share": round(props.get(4, 0), 3),
        "three_way_share": round(props.get(3, 0), 3),
        "dead_end_share": round(props.get(1, 0), 3),
        "street_length_avg_m": round(stats["street_length_avg"], 1),
        "streets_per_node_avg": round(stats["streets_per_node_avg"], 2),
        "circuity_avg": round(stats["circuity_avg"], 3),
    }


def main():
    GRAPHS.mkdir(parents=True, exist_ok=True)
    rows, drawings = [], {}
    for loc in LOCALITIES:
        print("Processing", loc["name"])
        G = get_graph(loc)
        Gp, window = clip_to_window(G, loc)
        # bearings need lat/lon coordinates and one edge per street
        Gu = ox.convert.to_undirected(ox.project_graph(Gp, to_latlong=True))
        Gu = ox.bearing.add_edge_bearings(Gu)
        rows.append({"name": loc["name"], **metrics(Gp, Gu)})
        drawings[loc["name"]] = {"streets": street_svg(Gp, window),
                                 "bearings": bearing_counts(Gu)}
    df = pd.DataFrame(rows)
    df.to_csv(DATA / "metrics.csv", index=False)
    (DATA / "svgs.json").write_text(json.dumps(drawings))
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
