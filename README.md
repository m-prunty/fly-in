
```
fly_in/
├── main.py                  # Entry point only — arg parsing, wires everything together
├── Makefile
├── README.md
├── pyproject.toml       # one source of truth — deps, mypy config, flake8
├── .python-version      # uv pins the interpreter
├── .venv/               # single env, no cross-package dependency headaches
│
├── parser/
│   ├── __init__.py
│   ├── file_parser.py       # Tokenises lines, validates syntax, raises ParseError
│   └── models.py            # Zone, Connection, DroneMap dataclasses (the graph data model)
│
├── simulation/
│   ├── __init__.py
│   ├── graph.py             # Adjacency list, BFS/pathfinding — NO networkx (forbidden)
│   ├── scheduler.py         # Turn-by-turn engine, capacity enforcement, conflict resolution
│   ├── drone.py             # Drone state machine (position, in-transit, delivered)
│   └── output.py           # Formats the D1-roof1 D2-corridorA stdout lines
│
├── display/
│   ├── __init__.py
│   ├── terminal.py          # Coloured terminal output using colorama/rich
│   └── gui.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py              # shared fixtures (sample DroneMap, small graphs)
    ├── test_parser.py
    ├── test_graph.py
    ├── test_scheduler.py
    ├── test_drone.py
    └── test_output.py


```

**Critical areas to hit:**

`test_parser.py`
- Valid file parses correctly
- Duplicate connection (a-b and b-a) raises error
- Invalid zone type raises error
- Missing `nb_drones` / missing start or end hub raises error
- Comments ignored
- Metadata in any order parsed correctly

`test_graph.py`
- Blocked zones excluded from all paths
- Restricted zones have cost 2
- Priority zones preferred when cost is equal
- Capacity matrix reflects `max_link_capacity` and `max_drones` correctly
- No path exists returns sensibly (not a crash)

`test_scheduler.py`
- Two drones don't exceed zone capacity on same turn
- Drone committed to restricted zone transit **must** complete next turn — can't wait on connection
- Drones moving out free capacity for same turn (the spec is explicit on this)
- All drones reach end zone, simulation terminates
- Deadlock doesn't cause infinite loop

`test_drone.py`
- State transitions: idle → moving → in-transit → delivered
- In-transit drone can't be rerouted

`test_output.py`
- Format matches `D<ID>-<zone>` exactly
- Delivered drones omitted from subsequent lines
- In-transit drones output `D<ID>-<connection>` not destination zone

