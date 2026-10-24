"""Bengaluru localities used in the game.

Each entry is the centre of a 1 km x 1 km window (lat/lon in WGS84), plus the
player-facing text: a clue, a line on how to spot it, and a fun fact.
"""

LOCALITIES = [
    {"name": "Jayanagar 4th Block", "lat": 12.9250, "lon": 77.5838,
     "clue": "That famous shopping complex, and very, very tidy streets",
     "spot_it": "The neatest grid in town: straight streets crossing at right angles, and almost none that just stop.",
     "fact": "When it was laid out in the late 1940s, Jayanagar was billed as one of the biggest planned neighbourhoods in Asia."},
    {"name": "Basavanagudi", "lat": 12.9422, "lon": 77.5737,
     "clue": "A giant Nandi, and a groundnut fair every winter",
     "spot_it": "A tidy grid with big roads slicing across it diagonally, plus a few roundabouts.",
     "fact": "The Kadlekai Parishe (groundnut fair) began as farmers offering their first harvest to the Bull Temple's Nandi."},
    {"name": "Malleshwaram", "lat": 13.0035, "lon": 77.5700,
     "clue": "Benne dosa queues at CTR, and jasmine sellers on 8th Cross",
     "spot_it": "Long straight 'mains' and 'crosses' in a near-perfect grid, with little lanes poking into the blocks.",
     "fact": "Malleshwaram and Basavanagudi were both laid out in 1898, after a plague outbreak pushed people out of the crowded old town."},
    {"name": "Chickpet (old Pete)", "lat": 12.9700, "lon": 77.5770,
     "clue": "Where all of Bengaluru shops for silk sarees and wedding stuff",
     "spot_it": "Nowhere else is this tangled: hundreds of tiny lanes crammed into one square.",
     "fact": "This is the old town Kempegowda founded in 1537. Streets were named after the trades on them, so you still have Balepet (bangles) and Akkipete (rice)."},
    {"name": "Koramangala", "lat": 12.9352, "lon": 77.6245,
     "clue": "Startup cafes, and Forum Mall is right there",
     "spot_it": "Lots of little grids that don't line up with each other, so streets point every which way.",
     "fact": "Koramangala's numbered blocks were each laid out separately, which is why getting from one to another feels like a puzzle."},
    {"name": "Indiranagar", "lat": 12.9719, "lon": 77.6412,
     "clue": "100 Feet Road, pubs and boutique shopping",
     "spot_it": "A strong grid, but the cross streets are staggered, so you get lots of T-junctions instead of crossroads.",
     "fact": "Indiranagar was built in the 1970s, mostly as housing for government employees, before 100 Feet Road turned into a party street."},
    {"name": "Whitefield", "lat": 12.9698, "lon": 77.7500,
     "clue": "Tech parks, and a commute you will tell your grandkids about",
     "spot_it": "A big ring of roads, and loads of streets that just stop: hello, gated complexes.",
     "fact": "Long before the tech parks, Whitefield was an Anglo-Indian farming settlement from the 1880s. That ring of roads is the old village layout."},
    {"name": "Electronic City Phase 1", "lat": 12.8452, "lon": 77.6602,
     "clue": "Giant campuses and the elevated tollway",
     "spot_it": "Almost empty! The campuses are so big, and their roads so private, that only a few long roads are left.",
     "fact": "Electronic City was set up in 1978, long before Bengaluru was called India's Silicon Valley."},
]
