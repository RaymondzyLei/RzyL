import json
from pathlib import Path

_keywords_path = Path(__file__).parent.parent.parent / "asserts" / "easter_egg" / "keywords.json"
EASTER_EGG_KEYWORDS: dict[str, list[str]] = json.loads(_keywords_path.read_text(encoding="utf-8"))