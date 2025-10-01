import json
from pathlib import Path
import re
from typing import Dict, Any, List, Tuple
import datetime
import traceback

DATA_DIR = Path(__file__).parent / "data"
TUTORIALS_DIR = Path(__file__).parent / "tutorials"
TUTORIALS_JSON = DATA_DIR / "tutorials.json"

def _safe_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\- ]+", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80].strip("-") or "untitled"

def load_tutorials() -> Dict[str, Any]:
    try:
        if not TUTORIALS_JSON.exists():
            return {"tutorials": []}
        return json.loads(TUTORIALS_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        # Fallback to empty structure on read error
        return {"tutorials": []}

def save_tutorials(data: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        TUTORIALS_DIR.mkdir(parents=True, exist_ok=True)
        TUTORIALS_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True, "Saved."
    except Exception as e:
        return False, f"Failed to save tutorials: {e}"

def add_tutorial(title: str, category: str, content_md: str, author: str="", tags: List[str]=None, difficulty: str=""):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    slug = _safe_slug(title)
    md_path = TUTORIALS_DIR / f"{slug}.md"
    try:
        md_path.write_text(content_md, encoding="utf-8")
    except Exception:
        traceback.print_exc()
        return False, "Could not write markdown file."
    data = load_tutorials()
    # If slug exists, bump with numeric suffix
    existing_slugs = {t.get("slug") for t in data.get("tutorials", [])}
    base = slug
    i = 2
    while slug in existing_slugs:
        slug = f"{base}-{i}"
        i += 1
    record = {
        "title": title.strip(),
        "slug": slug,
        "category": category,
        "author": author.strip(),
        "difficulty": difficulty,
        "tags": tags or [],
        "path": str(md_path.name),
        "created_at": now,
        "updated_at": now,
    }
    data.setdefault("tutorials", []).append(record)
    ok, msg = save_tutorials(data)
    return ok, msg

def update_tutorial(slug: str, new_content_md: str=None, **meta_updates):
    data = load_tutorials()
    for t in data.get("tutorials", []):
        if t.get("slug") == slug:
            if new_content_md is not None:
                md_path = TUTORIALS_DIR / t["path"]
                try:
                    md_path.write_text(new_content_md, encoding="utf-8")
                except Exception as e:
                    return False, f"Failed to update markdown file: {e}"
            for k, v in meta_updates.items():
                if k in ("title","category","author","difficulty","tags"):
                    t[k] = v
            t["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            ok, msg = save_tutorials(data)
            return ok, msg
    return False, "Tutorial not found."

def get_markdown(slug: str) -> str:
    data = load_tutorials()
    for t in data.get("tutorials", []):
        if t.get("slug") == slug:
            path = TUTORIALS_DIR / t["path"]
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                return "# Error\nCould not read tutorial content."
    return "# Not found\nThe requested tutorial does not exist."

def list_by_category(category: str) -> List[dict]:
    data = load_tutorials()
    return [t for t in data.get("tutorials", []) if t.get("category") == category]

def search(query: str) -> List[dict]:
    q = (query or "").strip().lower()
    if not q:
        return []
    data = load_tutorials()
    results = []
    for t in data.get("tutorials", []):
        hay = " ".join([
            t.get("title",""),
            t.get("category",""),
            " ".join(t.get("tags", [])),
        ]).lower()
        if q in hay:
            results.append(t)
            continue
        # soft search within content (best-effort)
        try:
            md = (TUTORIALS_DIR / t["path"]).read_text(encoding="utf-8").lower()
            if q in md:
                results.append(t)
        except Exception:
            pass
    return results
