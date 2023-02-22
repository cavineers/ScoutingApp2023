# ScoutingApp2023
Scouting App Code for the 2023 FRC Season

---
# Contents
1. [Installation](#installation)
   - [Python Packages](#python-packages)
2. [Running](#running)
3. [Modification](#modification)
   - [Adding Routes](#adding-routes)
   - [Adding Static Assets](#adding-static-assets)

---

## Installation
### Python Packages
The following packages need to be installed to run the Scouting App server:
- [Flask](https://pypi.org/project/Flask/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [waitress](https://pypi.org/project/waitress/)
- [pyzbar](https://pypi.org/project/pyzbar/)

They can be installed by running the command `python -m pip install <package-name>` in a terminal.

## Running
To quickrun the app, you can run the `main.py` file, which will host the app on localhost:8080.

To specify the host IP and port, use run `python -m ScoutingApp [host=<ip>] [port=<port>]`

## Modification

When modifying this file for future competitions, a couple of changes need to be made.

1. A [package](https://packaging.python.org/en/latest/tutorials/packaging-projects/)/file containing all of the backend code for that competition must be added to [`comps`](comps).
2. Add any html files for the competition under a new folder in [`templates`](templates), and any images/javascript/css in a new folder in [`static`](static).

### Adding Routes

### Adding Static Assets
