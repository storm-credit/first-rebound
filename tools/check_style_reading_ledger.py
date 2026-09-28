"""Check G11 reading progress from chapter evidence, without storing novel text."""

import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/STYLE_READING_OBSERVATIONS.json"
OFFICIAL_BODY_HOSTS = {
    "www.munpia.com": "Munpia",
    "ridibooks.com": "Ridi",
    "page.kakao.com": "KakaoPage",
    "series.naver.com": "NaverSeries",
    "www.joara.com": "Joara",
}


def check(data):
    errors = []
    plan, observed = data["planned"], data["observed"]
    target = (plan["works"] * plan["first_five_chapters_per_work"]
              + plan["core_works"] * (plan["core_chapters"] - plan["first_five_chapters_per_work"]))
    if plan["total_chapters"] != target:
        errors.append("planned total does not match first-five plus core-extra target")

    complete = [r for r in data["readings"] if r.get("scope") == "COMPLETE_CHAPTER"]
    per_work = defaultdict(set)
    body_platforms = set()
    seen = set()
    for r in data["readings"]:
        key = (r.get("work"), r.get("chapter"))
        if key in seen:
            errors.append(f"duplicate reading: {key}")
        seen.add(key)
        if r.get("raw_text_retained") is not False or r.get("verbatim_excerpt") is not None:
            errors.append(f"raw text retained: {key}")
        if r.get("scope") != "COMPLETE_CHAPTER":
            continue
        per_work[r["work"]].add(r["chapter"])
        host = urlparse(r["url"]).hostname
        platform = OFFICIAL_BODY_HOSTS.get(host)
        if platform is None:
            errors.append(f"unverified body platform: {host}")
        else:
            body_platforms.add(platform)

    first_five = set(range(1, plan["first_five_chapters_per_work"] + 1))
    first_twenty = set(range(1, plan["core_chapters"] + 1))
    expected = {
        "complete_chapters": len(complete),
        "works_first_five_complete": sum(first_five <= chapters for chapters in per_work.values()),
        "works_first_twenty_complete": sum(first_twenty <= chapters for chapters in per_work.values()),
        "unread_chapters_against_default_target": target - len(complete),
    }
    for name, value in expected.items():
        if observed[name] != value:
            errors.append(f"{name}: observed {observed[name]}, derived {value}")
    if set(observed["body_platforms"]) != body_platforms:
        errors.append("body_platforms differs from complete-chapter official hosts")
    if len(observed["body_platforms"]) != len(body_platforms):
        errors.append("duplicate body platform")
    if data.get("manuscript_allowed") is not False or data.get("author_locked") is not False:
        errors.append("reading ledger promoted into canon or manuscript")
    return errors, expected, sorted(body_platforms)


if __name__ == "__main__":
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    issues, counts, platforms = check(ledger)
    print(json.dumps({"PASS": not issues, "derived": counts, "platforms": platforms,
                      "errors": issues}, ensure_ascii=False))
    raise SystemExit(bool(issues))
