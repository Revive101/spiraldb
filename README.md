# spiraldb


## Schemas

JSON Schemas for each data type live in `schemas/`. `scripts/validate.py` maps each data directory to its schema, and the `Validate JSON schemas` GitHub Action runs it on every PR and push to `main`.

```sh
pip install jsonschema
python scripts/validate.py            # everything
python scripts/validate.py NpcInventory/NPCInventories_1026-A.json   # specific files
```
