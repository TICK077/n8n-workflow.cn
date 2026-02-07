import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "../docs/api/search-index.json"
DESC_OUT = BASE_DIR / "descriptions.json"
NAME_OUT = BASE_DIR / "name.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

descriptions = {}
names = {}

def collect(item):
    if not isinstance(item, dict):
        return

    item_id = item.get("id")
    if not item_id:
        return

    # 提取 description
    if "description" in item and item_id not in descriptions:
        descriptions[item_id] = {
            "description_en": item["description"],
            "description_zh": ""
        }

    # 提取 name
    if "name" in item and item_id not in names:
        names[item_id] = {
            "name_en": item["name"],
            "name_zh": ""
        }

def walk(obj):
    if isinstance(obj, list):
        for v in obj:
            walk(v)
    elif isinstance(obj, dict):
        collect(obj)
        for v in obj.values():
            walk(v)

walk(data)

with open(DESC_OUT, "w", encoding="utf-8") as f:
    json.dump(descriptions, f, ensure_ascii=False, indent=2)

with open(NAME_OUT, "w", encoding="utf-8") as f:
    json.dump(names, f, ensure_ascii=False, indent=2)

print(f"已提取 description：{len(descriptions)} 条 → descriptions.json")
print(f"已提取 name：{len(names)} 条 → name.json")
