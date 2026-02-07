import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "../docs/api/search-index.json"
DESC_FILE = BASE_DIR / "descriptions.json"
NAME_FILE = BASE_DIR / "name.json"
OUTPUT_FILE = BASE_DIR / "../docs/api/search-index.zh.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(DESC_FILE, "r", encoding="utf-8") as f:
    descriptions = json.load(f)

with open(NAME_FILE, "r", encoding="utf-8") as f:
    names = json.load(f)

def apply(item):
    if not isinstance(item, dict):
        return

    item_id = item.get("id")
    if not item_id:
        return

    # 回填 description
    desc_zh = descriptions.get(item_id, {}).get("description_zh")
    if desc_zh:
        item["description"] = desc_zh

    # 回填 name
    name_zh = names.get(item_id, {}).get("name_zh")
    if name_zh:
        item["name"] = name_zh

def walk(obj):
    if isinstance(obj, list):
        for v in obj:
            walk(v)
    elif isinstance(obj, dict):
        apply(obj)
        for v in obj.values():
            walk(v)

walk(data)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"已生成中文索引文件：{OUTPUT_FILE}")
