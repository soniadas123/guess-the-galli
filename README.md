# Guess the Galli

**Play it here: https://soniadas123.github.io/guess-the-galli/**

Guess 8 Bengaluru neighbourhoods from their street maps alone. Or open `streets_game.html` in any browser; it is a single self-contained file.

## Rebuild

```
conda activate sw_blr
python build_data.py   # downloads OSM streets (cached in data/graphs), writes data/metrics.csv and data/svgs.json
python make_game.py    # writes streets_game.html
```

You only need `build_data.py` if you change a locality's location. To edit text, just change `localities.py` or `game_template.html` and re-run `make_game.py`.

## Files

- `localities.py` - centre point, clue, "how to spot it" line and fun fact for each neighbourhood
- `build_data.py` - downloads streets with OSMnx, clips each to a 1 km square, draws it and computes the numbers for the hidden "map nerds" table
- `game_template.html` - the game page (styles, screens, scoring)
- `make_game.py` - fills the template with the data

## Contributors

- Sonia Das ([@soniadas123](https://github.com/soniadas123)) - idea, direction and design
- Built with help from Claude (Anthropic)

Street data &copy; OpenStreetMap contributors.
