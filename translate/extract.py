import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "../docs/api/search-index.json"
OUTPUT_FILE = BASE_DIR / "./descriptions.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

result = {}

# 情况 1：最常见 —— 顶层是 list
if isinstance(data, list):
    for item in data:
        if "id" in item and "description" in item:
            result[item["id"]] = {
                "description_en": item["description"],
                "description_zh": ""
            }

# 情况 2：顶层是 dict，里面包了一层
elif isinstance(data, dict):
    for v in data.values():
        if isinstance(v, list):
            for item in v:
                if "id" in item and "description" in item:
                    result[item["id"]] = {
                        "description_en": item["description"],
                        "description_zh": ""
                    }

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"已提取 {len(result)} 条 description → {OUTPUT_FILE}")
