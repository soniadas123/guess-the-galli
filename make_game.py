"""Build streets_game.html from the locality text, metrics and street drawings.

Run with:  conda run -n sw_blr python make_game.py
"""
import json
from pathlib import Path

import pandas as pd

from localities import LOCALITIES

DATA = Path("data")


def main():
    metrics = pd.read_csv(DATA / "metrics.csv").set_index("name")
    drawings = json.loads((DATA / "svgs.json").read_text())

    rounds = []
    for loc in LOCALITIES:
        m = metrics.loc[loc["name"]]
        rounds.append({
            "name": loc["name"],
            "clue": loc["clue"],
            "spot_it": loc["spot_it"],
            "fact": loc["fact"],
            "streets": drawings[loc["name"]]["streets"],
            # only used in the hidden "for the map nerds" table
            "metrics": {
                "order": m.orientation_order,
                "density": m.intersection_density_km2,
                "four": m.four_way_share,
                "dead": m.dead_end_share,
                "length": m.street_length_avg_m,
            },
        })

    template = Path("game_template.html").read_text(encoding="utf-8")
    html = template.replace("__ROUNDS__", json.dumps(rounds))
    Path("streets_game.html").write_text(html, encoding="utf-8")
    print(f"Wrote streets_game.html with {len(rounds)} rounds")


if __name__ == "__main__":
    main()
