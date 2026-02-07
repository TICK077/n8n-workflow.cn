import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "../docs/api/search-index.json"
TRANSLATION_FILE = BASE_DIR / "descriptions.json"
OUTPUT_FILE = BASE_DIR / "../docs/api/search-index.zh.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(TRANSLATION_FILE, "r", encoding="utf-8") as f:
    translations = json.load(f)

def apply(item):
    # 关键防护：只处理 dict
    if not isinstance(item, dict):
        return

    item_id = item.get("id")
    if not item_id:
        return

    zh = translations.get(item_id, {}).get("description_zh")
    if zh:
        item["description"] = zh

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

print(f"已生成：{OUTPUT_FILE}")
