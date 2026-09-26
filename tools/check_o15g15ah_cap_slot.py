"""Check only G15AH's conditional arithmetic and G15AF-derived name partition."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
g = json.loads((ROOT / "research/O15G15AH_DETROIT_AUG6_CAP_AND_OPENING_SLOT_SCREEN.json").read_text(encoding="utf-8"))
af = json.loads((ROOT / "research/O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.json").read_text(encoding="utf-8"))

limits = g["official_2021_22_limits"]
money = g["secondary_salary_candidates"]
assert money["plumlee_traded_display_cap_not_for_p0b"] > money["plumlee_untraded_base"]
assert money["plumlee_untraded_base"] + money["olynyk_first_year"] == 20_332_622
assert money["olynyk_first_year"] - limits["non_taxpayer_mle"] == 2_659_122
assert money["olynyk_first_year"] - limits["taxpayer_mle"] == 6_305_122
assert money["olynyk_first_year"] - limits["room_mle"] == 7_285_122

names = set(af["historical_august_12_retained"] + af["historical_august_12_added_or_resigned"])
for event in af["historical_events_after_august_12"]:
    names.difference_update(event["out"])
    names.update(event["in"])
names.difference_update(af["conditional_same_other_events"]["replaced_historical_players"])
names.update(af["conditional_same_other_events"]["replacement_players"])
names.add(af["conditional_same_other_events"]["plumlee_retained"])
used = set(g["g14_used"])
screen = set(g["g14_zero_allocated_minutes_screen_only"])
assert len(names) == 16 and len(used) == 10 and len(screen) == 6
assert not used & screen and used | screen == names
print("G15AH arithmetic and conditional 10+6 roster partition: PASS")
