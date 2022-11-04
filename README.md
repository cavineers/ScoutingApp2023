# ScoutingApp2023
Scouting App Code for the 2023 FRC Season

---
# Contents
1. [Installation](#installation)
2. [Running](#running)
   - [Testing](#testing)
   - [Release](#release)
3. [Modification](#modification)

---

## Installation

## Running
### Testing
During testing, we just hosted it locally using python `http.server`:
- Command in project dir: `python -m http.server 8080`
- Then go to  `localhost:8080/index.html` in a browser to connect.

### Release
[//]: # (Add info when we figure out how to distribute the finished product)

## Modification

When modifying this file for future competitions, a couple of changes need to be made.

1. A folder containing all of the assets needed for that competition must be added to [`comps`](comps).
2. A link going to a page in your competition's folder must be added in [`compselect.html`](compselect.html). The link for the newest competition should be added to the top. \
Example:
```
<!-- In compselect.html body -->
<ul ...>
    <li> <!-- Insert link to page for latest competition --> </li>
    ...
    <!-- Older links below -->
</ul>
```
3. All assets you add must be added to the `assets` array in [`sw.js`](sw.js).