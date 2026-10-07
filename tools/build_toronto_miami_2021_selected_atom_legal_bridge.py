"""Join the selected Toronto T1 route to Miami's narrow 2021 Lowry atom.

This is an NBA historical-existence witness and a fictional NPC selection, not
an independent reconstruction of either club's private Team Salary ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fitz
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_toronto_miami_2021_selected_atom_legal_bridge.py"
OUT = "research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json"
MD = OUT[:-5] + ".md"
TOR = "simulation/TORONTO_2021_SELECTED_T1_OPERATING_FAMILY_2026_10_07.json"
SEED = "simulation/NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json"
DRAFT = "research/NBA_2021_FULL_DRAFT_WORKING_BOARD_2026_10_07.json"
BANK = "research/TORONTO_2021_10_25_NAMED_OPERATING_INPUT_BANK_2026_10_07.json"
REPO_PINS = {
    TOR: "676cb350acdd632dfc0a0b4cc82d8f1d085b243f21fe511caeb11bcc2b993118",
    SEED: "cfa2f49bb82baa49b2298d90c97cd7fd8075e91380424d40bfd44772d8228a2b",
    DRAFT: "90099928f9133c4087ee7871939ce58216d183bd186f5ebd3575a56c2348eeed",
    BANK: "7b6cba6e74044f3b52a79fa966498bca1771294c8bf109bb2213e712210c7096",
}
CACHE = Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-tor-mia-atom-20261007")
CBA = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf")
RAW = {
    "trade_tracker": (CACHE / "NBA_TRADE_TRACKER.html", "8d7668031d0e40ab915ffacd71f41555cecb08d23625f59e2408dbbc54cf7f7c"),
    "player_movement": (CACHE / "NBA_PLAYER_MOVEMENT.html", "acd74d61cc53bea11a7e574cbf63f1a487b65bcda5ce9e56847fd026bd078969"),
    "lowry_report": (CACHE / "NBA_LOWRY_REPORT.html", "230be10b3b38ba87a18c74f705a8e741b6230c75af41018b596ca1a62ab16d02"),
    "cap": (CACHE / "NBA_CAP.html", "9e2a73e5ca9b588bb58a662f5fc8b7f6fd00096b8efde6f40c65d9119c865082"),
    "salary_comparator": (CACHE / "BOARDROOM_LOWRY.html", "610ce9d16359405c0d3f126c21cee08d1b8a585a49d1c0c437d40b160c9783dd"),
    "miami_gamebook": (CACHE / "NBA_ORLMIA_20211025_BOOK.pdf", "33755f3f8a3f0ef69f12c5ea42d19688dafc396b5bc875f4e03be2cf12188cb2"),
    "garrett_two_way": (CACHE / "NBA_GARRETT_TW.html", "64cd8b84cd926224c8fb6ec58fa5974f35471cdad23d97714a6d0e0ea4e60fa1"),
    "reported_2021_apron": (CACHE / "SALARYSWISH_CAP.html", "970ac166d62d09d052de1c8419d2c53288aed9af1d51c5b10db3c063e41340b4"),
    "cba2017": (CBA, "66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a"),
}
RAW_URLS = {
    "trade_tracker": "https://www.nba.com/news/2021-offseason-trade-tracker",
    "player_movement": "https://www.nba.com/news/nba-player-movement-2021",
    "lowry_report": "https://www.nba.com/news/report-kyle-lowry-to-join-miami-heat-for-three-season-in-sign-and-trade",
    "cap": "https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season",
    "salary_comparator": "https://boardroom.tv/kyle-lowry-contract-salary-heat/",
    "miami_gamebook": "https://statsdmz.nba.com/pdfs/20211025/20211025_ORLMIA_book.pdf",
    "garrett_two_way": "https://gleague.nba.com/news/heat-sign-days-garrett-to-two-way-contracts",
    "reported_2021_apron": "https://www.salaryswish.com/salary-cap",
    "cba2017": "https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf",
}
LOWRY_YEARS = [26_984_128, 28_333_334, 29_682_540]
DRAGIC = 19_440_000
PRECIOUS = 2_711_280


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def norm_sha(path: Path) -> str:
    body = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def raw_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_text(doc: fitz.Document, index: int) -> str:
    return doc[index].get_text().replace("\r\n", "\n").replace("\r", "\n")


def html_body(path: Path) -> str:
    page = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in page(["script", "style", "nav", "footer"]):
        tag.decompose()
    return " ".join(page.stripped_strings)


def sources(root=ROOT):
    for name, digest in REPO_PINS.items():
        need(norm_sha(root / name) == digest, "Reviewed repository source changed: " + name)
    for name, (path, digest) in RAW.items():
        need(path.is_file() and raw_sha(path) == digest, "Primary/reference raw source unavailable or changed: " + name)
    tor = json.loads((root / TOR).read_text(encoding="utf-8-sig"))
    seed = json.loads((root / SEED).read_text(encoding="utf-8-sig"))
    draft = json.loads((root / DRAFT).read_text(encoding="utf-8-sig"))
    bank = json.loads((root / BANK).read_text(encoding="utf-8-sig"))
    need(tor == json.loads((root / TOR).read_text(encoding="utf-8-sig")), "Toronto loader differs from physical source")
    need(seed == json.loads((root / SEED).read_text(encoding="utf-8-sig")), "Miami seed loader differs from physical source")
    need(draft == json.loads((root / DRAFT).read_text(encoding="utf-8-sig")), "Draft loader differs from physical source")
    need(bank == json.loads((root / BANK).read_text(encoding="utf-8-sig")), "Toronto bank loader differs from physical source")
    need(tor["selected_transaction_atom"]["path"] == "T1_LOWRY_TO_MIA_DRAGIC_PRECIOUS_TO_TOR", "Toronto selected direction changed")
    need(tor["date_count"] == 4 and not tor["MIA_downstream_date_roster_updated_here"], "Toronto/Miami previous scope changed")
    need(tor["selected_roster"]["standard_count"] == 15 and tor["selected_roster"]["two_way_count"] == 2, "Toronto slot count changed")
    need(tor["selected_cost_screen"]["categories"]["trade_incoming_public_cap_points"]["names"] == {"Goran Dragic": DRAGIC, "Precious Achiuwa": PRECIOUS}, "Toronto selected incoming prices changed")
    lowry_prior = next(x for x in bank["expired_option_and_new_contract_ports"] if x["name"] == "Kyle Lowry")
    need(lowry_prior["old_reported_cap"] == 30_500_000, "Lowry prior reported salary changed")

    state = next(x for x in seed["team_game_bindings"] if x["date"] == "2021-05-16" and x["team"] == "MIA")
    need(state["state_id"] == "MIA:bf2645fe176e8884", "S2 Miami final seed changed")
    players = seed["roster_states"][state["state_id"]]["players"]
    base_std = {p["player"] for p in players if p["contract_class"] == "STANDARD"}
    base_tw = {p["player"] for p in players if p["contract_class"] == "TWO_WAY"}
    need(len(base_std) == 15 and len(base_tw) == 2 and {"Goran Dragic", "Precious Achiuwa", "Gabe Vincent", "Max Strus"} <= base_std | base_tw, "Miami 2020-21 seed changed")
    need(base_tw == {"Gabe Vincent", "Max Strus"}, "Miami old two-way class changed")
    mia_picks = [r for r in draft["rows"] if r["conditional_final_draft_rights_holder"] == "MIA"]
    need(not mia_picks, "Selected board now assigns Miami an owned 2021 pick")
    need({(r["pick"], r["conditional_final_draft_rights_holder"]) for r in draft["rows"] if r["origin"] == "MIA"} == {(18, "OKC"), (47, "ATL")}, "Miami-origin draft rights changed")

    tracker = html_body(RAW["trade_tracker"][0])
    movement = html_body(RAW["player_movement"][0])
    report = html_body(RAW["lowry_report"][0])
    salary = html_body(RAW["salary_comparator"][0])
    cap = html_body(RAW["cap"][0])
    garrett = html_body(RAW["garrett_two_way"][0])
    apron_report = html_body(RAW["reported_2021_apron"][0])
    segment = tracker.split("Lowry to Heat in sign-&-trade with Raptors (Aug. 6)", 1)[1].split("Pistons trade Thor", 1)[0]
    need("Heat get: Kyle Lowry" in segment and "Raptors get: Goran Dragic Precious Achiuwa" in segment, "Official trade atom changed")
    mia_movement = movement.split("Miami Heat Added:", 1)[1].split("Milwaukee Bucks", 1)[0]
    for phrase in ("Kyle Lowry (from Raptors)", "Via 2021 NBA Draft —", "Precious Achiuwa (traded to Raptors)", "Goran Dragic (traded to Raptors)", "Andre Iguodala (signed with Warriors)", "Kendrick Nunn (signed with Lakers)", "Trevor Ariza (signed with Lakers)", "Nemanja Bjelica (signed with Warriors)", "Caleb Martin **", "Markieff Morris", "P.J. Tucker"):
        need(phrase in mia_movement, "Official Miami offseason actor changed: " + phrase)
    need("three seasons and $85 million" in report and "August 6, 2021" in report, "NBA reported Lowry term or action date changed")
    for n in LOWRY_YEARS:
        need(f"${n:,}" in salary, "Public first-year/annual comparator changed")
    need("$112.414 million" in cap and "$136.606 million" in cap, "NBA 2021 cap/tax source changed")
    need("September 2, 2021" in garrett and "two-way contract" in garrett, "Garrett two-way provenance changed")
    need("2021-22 Aug 2, 2021" in apron_report and "$136,606,000 $143,002,000" in apron_report, "Reported 2021 apron row changed")

    cba = fitz.open(RAW["cba2017"][0])
    cba_pages = {p: page_text(cba, p - 1) for p in (233, 234, 235, 253, 254)}
    cba_hashes = {p: hashlib.sha256(t.encode()).hexdigest() for p, t in cba_pages.items()}
    need(cba_hashes == {233: "236194df68b0f343933e4b25e48bef4c80d2bbfba11006a87e9585687aae7ba3", 234: "6c47932b11835e0215ef806fdaf1ef3107d9b8c7dac0a3e208d179f14070f3c5", 235: "1f449a622bbc1500de8056f778ced65f1ed3e316cccc5e85d04511cf2f7d1f36", 253: "f35be5e4b1e7af94779ab9e72256c06ea86c5cfb17f0076aa159ada72badff9a", 254: "ff59fbc69a921ae3d87511f82fd59541017c8ab589720f530d3f3bcad9e595bb"}, "CBA locator text changed")
    cba_flat = {p: " ".join(t.split()) for p, t in cba_pages.items()}
    need("one hundred twenty-five percent (125%)" in cba_flat[233] and "plus $100,000" in cba_flat[234], "CBA simultaneous matching rule not observed")
    need("at least three (3) Seasons" in cba_flat[253] and "first Season of the Contract is fully protected" in cba_flat[254], "CBA S&T term/protection not observed")
    need("Tax Apron" in cba_pages[254], "CBA acquiring-team apron condition not observed")
    book = fitz.open(RAW["miami_gamebook"][0])
    first = page_text(book, 0)
    need(hashlib.sha256(first.encode()).hexdigest() == "47ccfafbf8dd63ba4ec28e655afe416669c3f4a7fb35b6d3528fde09ce46da50", "Official Miami book page changed")
    need("Monday, October 25, 2021" in first and "HOME: MIAMI HEAT" in first and "Inactive: Heat - Martin" in first, "Miami opening date or roster anchor changed")
    return tor, base_std, base_tw, first, cba_hashes


def selected_miami_roster(base_std, base_tw):
    removed = {"Goran Dragic", "Precious Achiuwa", "Andre Iguodala", "Kendrick Nunn", "Trevor Ariza", "Nemanja Bjelica"}
    need(removed <= base_std, "Original Miami departures not in S2 roster")
    additions = {"Kyle Lowry", "P.J. Tucker", "Markieff Morris"}
    standard = sorted((base_std - removed) | additions | base_tw)
    two_way = ["Caleb Martin", "Marcus Garrett"]
    need(len(standard) == 14 and len(set(standard)) == 14 and len(two_way) == 2 and not set(standard) & set(two_way), "Miami selected 14+2 fails")
    return standard, two_way, sorted(removed)


def build(root=ROOT):
    tor, base_std, base_tw, book, cba_hashes = sources(root)
    mia_seed_projection = {"STANDARD": sorted(base_std), "TWO_WAY": sorted(base_tw)}
    need(hashlib.sha256(json.dumps(mia_seed_projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == "1cbb7481d99cb152ec8e305c48efe1f54278569831fd26b820323b1dce8fa1d9", "Returned S2 Miami actor/class projection changed")
    need(tor == json.loads((root / TOR).read_text(encoding="utf-8-sig")), "Returned Toronto selection differs from physical source")
    standard, two_way, removed = selected_miami_roster(base_std, base_tw)
    expected_removed = {"Goran Dragic", "Precious Achiuwa", "Andre Iguodala", "Kendrick Nunn", "Trevor Ariza", "Nemanja Bjelica"}
    expected_standard = sorted((base_std - expected_removed) | {"Kyle Lowry", "P.J. Tucker", "Markieff Morris"} | base_tw)
    need(standard == expected_standard and two_way == ["Caleb Martin", "Marcus Garrett"] and removed == sorted(expected_removed), "Returned Miami class or actor differs from S2 and official source route")
    # Gamebook is an independent official identity witness, not a way to copy minutes.
    for name in standard + two_way:
        printed = {"Victor Oladipo": "Oladipo", "Caleb Martin": "Martin"}.get(name, name)
        need(printed in book, "Selected Miami name absent from official October book: " + name)
    need("Goran Dragic" not in book and "Precious Achiuwa" not in book, "Outgoing actor still in Miami book")
    outgoing = DRAGIC + PRECIOUS
    incoming = LOWRY_YEARS[0]
    bound = outgoing * 5 // 4 + 100_000
    need(outgoing == 22_151_280 and bound == 27_789_100 and incoming <= bound, "Miami simultaneous matching changed")
    reverse_bound = incoming * 5 // 4 + 100_000
    need(reverse_bound == 33_830_160 and outgoing <= reverse_bound, "Toronto reverse matching changed")
    need(incoming <= 30_500_000, "Lowry outgoing base-year-compensation premise changed")
    need(sum(LOWRY_YEARS) == 85_000_002, "Reported three-year salary reference changed")
    family = {
        "live_prior_standard_contracts": {"names": ["Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala"], "exact_current_charge_recomputed": False},
        "incoming_sign_and_trade": {"name": "Kyle Lowry", "public_first_year_reference_usd": incoming, "fictional_selected_term_seasons": 3, "first_year_fully_protected_condition": True},
        "other_standard_contracts_and_renewals": {"names": sorted(set(standard) - {"Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala", "Kyle Lowry"}), "current_charge_recomputed": False},
        "prior_dead_or_stretch_salary": {"Ryan Anderson_reported_prior_stretch_liability_released_as_zero": False, "exact_other_prior_liabilities_recomputed": False},
        "two_way_and_disqualified": {"names": two_way, "normal_team_salary_increment_selected": 0, "cash_stipend_zero_certified": False},
        "unsigned_holds_exceptions_and_other_apron_adjustments": {"historical_original_MIA_route_retained_as_whole_family": True, "unknown_private_Gamma_assumed_zero": False, "complete_itemized_value_recomputed": False},
    }
    need(len(family) == 6 and set(family["other_standard_contracts_and_renewals"]["names"]) | set(family["live_prior_standard_contracts"]["names"]) | {"Kyle Lowry"} == set(standard), "Six-category Miami names do not cover selected standard roster")
    result = {
        "schema": 1,
        "status": "AUTHOR_DELEGATED_NPC_MIA_SAME_OFFICIAL_LOWRY_ATOM_SELECTED_WITH_CONDITIONAL_SIX_COST_COUPLING_NOT_FULL_PRIVATE_CAP_RECOMPUTATION",
        "source_hash_method": "UTF8_BOM_STRIPPED_LF_SHA256_REPO__RAW_BYTES_SHA256_EXTERNAL",
        "source_sha256": {**REPO_PINS, SELF: norm_sha(root / SELF)},
        "raw_source_sha256": {k: v[1] for k, v in RAW.items()},
        "raw_source_locators": {k: {"url": RAW_URLS[k], "cache_path": str(v[0]), "raw_sha256": v[1]} for k, v in RAW.items()},
        "cba_pdf_page_text_sha256": {str(k): v for k, v in cba_hashes.items()},
        "official_gamebook_first_page_text_sha256": "47ccfafbf8dd63ba4ec28e655afe416669c3f4a7fb35b6d3528fde09ce46da50",
        "selected_atom": {
            "fictional_NPC_direction_selected": True,
            "source_historical_comparator": "NBA_OFFICIAL_AUG_06_2021_S_AND_T_SAME_PARTIES_AND_PLAYERS",
            "ordered_actions": ["Miami exercises Dragic's existing option before trade", "Toronto signs its prior player Lowry to a three-season first-year-protected S&T agreement within the public-reference price family", "One consented simultaneous assignment sends Dragic and Precious to Toronto and Lowry to Miami", "Miami uses the original route's remaining 2021 offseason contract and release family to its October 25 opening roster"],
            "lowry_public_comparator_usd_by_season": LOWRY_YEARS,
            "original_actual_UPC_and_receipt_certified": False,
            "selected_MIA_path_differs_from_official_trade_parties_or_price_reference": False,
            "Chicago_M1_A_or_2020_21_S2_assets_changed": False,
        },
        "conservative_simultaneous_match": {"MIA_outgoing_dragic_plus_precious": outgoing, "MIA_incoming_lowry_public_reference": incoming, "MIA_125_percent_plus_100k_bound": bound, "MIA_margin_usd": bound - incoming, "TOR_outgoing_lowry_public_reference": incoming, "TOR_incoming_dragic_plus_precious": outgoing, "TOR_125_percent_plus_100k_bound": reverse_bound, "TOR_margin_usd": reverse_bound - outgoing, "applies_as_sufficient_bound_even_if_below_tax_formula_allows_more": True, "base_year_compensation_adjustment_for_lowry_triggered": False, "other_bonus_or_trade_kicker_exact_zero_certified": False},
        "MIA_roster_handoff": {"S2_2021_05_16_source_state": "MIA:bf2645fe176e8884", "S2_standard_count": len(base_std), "S2_two_way_count": len(base_tw), "removed_standard": removed, "prior_two_way_converted_to_standard": sorted(base_tw), "new_standard": ["Kyle Lowry", "P.J. Tucker", "Markieff Morris"], "new_two_way": two_way, "opening_2021_10_25_standard": standard, "opening_2021_10_25_two_way": two_way, "standard_count": len(standard), "two_way_count": len(two_way), "MIA_owned_2021_draft_picks": 0, "actual_gamebook_minutes_or_result_imported": False},
        "six_apron_cost_categories": family,
        "apron_legal_scope": {
            "receiving_S_and_T_team": "MIA", "2021_22_NBA_cap_usd": 112_414_000, "2021_22_NBA_tax_usd": 136_606_000,
            "2021_22_reported_apron_usd": 143_002_000, "apron_number_source_class": "SECONDARY_HISTORICAL_REPORTED_ROW_NOT_NBA_PRIVATE_ACCOUNTING",
            "selected_historical_MIA_official_completed_transaction_is_legal_existence_witness": True,
            "same_named_MIA_offseason_roster_and_public_contract_route_selected_in_fiction": True,
            "six_category_transfer_policy": {
                "live_original": "Keep identical surviving Miami UPCs and their already-earned salary/bonus liabilities; do not waive them by inference.",
                "incoming_Lowry": "Use the same reported three-year annual price family, full first-year skill protection and valid Toronto prior-team S&T.",
                "other_standard": "Use the official Miami renewal/new-signing route represented by the same October 25 named roster, not merely identical names with arbitrary new prices.",
                "dead_and_stretch": "Retain Ryan Anderson and every other already-incurred amount; only a legally waivable future balance may be altered.",
                "two_way": "Preserve Martin/Garrett two-way classification and cap treatment without claiming cash stipends vanish.",
                "unsigned_holds_and_exceptions": "Preserve the original valid renunciations, exception use and apron-adjusted treatment, including any unresolved obligations.",
            },
            "observed_named_noncommon_MIA_player_or_draft_delta_vs_official_route": [],
            "counterfactual_S2_earned_bonus_or_other_noncommon_delta_usd": None,
            "counterfactual_S2_earned_obligations_preserved_not_zero_assumed": True,
            "historical_lawful_six_category_Gamma_exists": True,
            "fictional_Gamma_chosen_from_historical_lawful_family_only_if_all_S2_earned_obligations_fit": True,
            "feasibility_constraint": "sum(six Miami apron categories, including changed S2 earned obligations and all already incurred dead salary) <= 143002000 at and after receipt",
            "unknown_original_private_costs_inherited_as_unquantified_not_zero": True,
            "independent_six_category_numeric_TeamSalary_or_apron_certificate": False,
            "fictional_MIA_NBA_private_approval_receipt_certified": False,
            "conditional_legal_route_selected_but_S2_difference_not_ruled_out": True,
        },
        "toronto_four_date_handoff": {"selected_TOR_source": TOR, "selected_TOR_source_sha256": REPO_PINS[TOR], "date_count": tor["date_count"], "MIA_joint_trade_dependency_has_source_supported_conditional_route": True, "TOR_four_date_legal_execution_complete": False, "Toronto_four_games_scores_or_whole82_certified": False},
        "remaining_typed_inputs": ["S2 Miami already-earned bonus/other noncommon apron charge versus the historical lawful Miami route; preserve any delta and test the $143,002,000 bound before TOR four-date legal completion", "TOR four-date and MIA other-opponent actual availability/results and any overtime", "Any intentional departure from original MIA contract/bonus/exception/dead-salary route needs a new six-category apron recalculation"],
        "author_lock": False,
        "whole_macro3_G13_G14_complete": False,
        "manuscript_allowed": False,
        "freeze": "v0.30 PARTIAL / CLOSED",
    }
    need(result["MIA_roster_handoff"]["opening_2021_10_25_standard"] == standard and result["MIA_roster_handoff"]["opening_2021_10_25_two_way"] == two_way, "Returned Miami roster differs from physical source construction")
    need(result["conservative_simultaneous_match"]["MIA_margin_usd"] == 804_972, "Returned salary match differs from source construction")
    need(not result["apron_legal_scope"]["independent_six_category_numeric_TeamSalary_or_apron_certificate"] and not result["toronto_four_date_handoff"]["TOR_four_date_legal_execution_complete"], "Historical existence was promoted to private cap certificate")
    return result


def validate(value, root=ROOT):
    try:
        need(value == build(root), "Saved Miami atom differs from source-bound construction")
        return []
    except (ValueError, KeyError, TypeError, StopIteration, IndexError) as exc:
        return [str(exc)]


def markdown(value):
    m = value["conservative_simultaneous_match"]
    r = value["MIA_roster_handoff"]
    return "\n".join([
        "# Toronto–Miami 2021 Lowry 원자 거래의 선택된 법적 경로", "",
        "**범위:** 승인된 Chicago M1/A·S2를 바꾸지 않는 NPC 루틴 선택이다. NBA 공식 2021-08-06 거래와 같은 당사자·선수·공개 가격 계열을 Miami에서 채택한다. Toronto의 기존 네 역할 날짜가 요구한 Miami 원자 거래의 **조건부 법적 존재 경로**를 연결한다. S2에서 이미 발생한 보너스 등 차이를 아직 배제하지 못했으므로 Toronto 네 날짜의 법적 실행완료로 올리지 않는다.", "",
        "## 당사자·권리·명단", "",
        "Miami가 Dragic 옵션을 행사한 뒤, Toronto가 종전 소속 선수 Lowry를 3시즌 계약으로 사인 앤 트레이드한다. Miami는 Lowry를, Toronto는 Dragic·Precious를 받는다. [NBA 공식 거래원장](https://www.nba.com/news/2021-offseason-trade-tracker)의 8월 6일 기록과 같다. 이 소설의 NPC 행동으로 선택한 것이며 원역사 개인 계약서 원본을 보유했다는 뜻은 아니다.", "",
        f"S2 마지막 Miami 명단은 15 STD+2 TW. 원역사와 같은 Miami 이동/방출·재계약 가족을 거쳐 2021-10-25 개막 모델은 **{r['standard_count']} STD+{r['two_way_count']} TW**다. 공식 [NBA 선수 이동표](https://www.nba.com/news/nba-player-movement-2021)와 [10월 25일 경기책](https://statsdmz.nba.com/pdfs/20211025/20211025_ORLMIA_book.pdf)을 명단 출처로 쓴다. 경기책의 실제 출전분·점수는 대체세계에 이식하지 않는다. Miami는 현재 드래프트 보드에서 자신이 보유한 2021 픽이 없다(#18 OKC, #47 ATL).", "",
        "## 급여·CBA", "",
        f"Dragic ${m['MIA_outgoing_dragic_plus_precious']-PRECIOUS:,}+Precious ${PRECIOUS:,} = 발송 ${m['MIA_outgoing_dragic_plus_precious']:,}. Lowry 공개 1년차 비교점 ${m['MIA_incoming_lowry_public_reference']:,}은 2017 CBA Article VII §6(j)의 보수적인 동시교환 한도 125%+$100,000 = **${m['MIA_125_percent_plus_100k_bound']:,}**보다 **${m['MIA_margin_usd']:,}** 낮다. 반대쪽 Toronto도 같은 보수 한도 아래다. [NBA의 당시 3년 약 $85m 보도](https://www.nba.com/news/report-kyle-lowry-to-join-miami-heat-for-three-season-in-sign-and-trade)와 [연차별 공개 비교점](https://boardroom.tv/kyle-lowry-contract-salary-heat/)을 구분한다.", "",
        "Miami는 S&T 수취 팀이므로 Article VII §8(e)의 apron 제한을 받는다. 여섯 비용 범주를 `live 원계약 / Lowry 수취 / 다른 STD 재계약 / 과거 dead·stretch / TW / unsigned hold·예외`로 나눴다. 각 범주는 역사상 적법하게 완료된 Miami의 **같은 계약·보호·예외 경로**로 결합하며 이미 번 급여·Ryan Anderson stretch를 삭제하지 않는다. 공식 거래는 적법 가족의 존재 증거다. 다만 S2 대체경기에서 더 발생했을 수 있는 보너스 등 비공통액은 null로 남긴다. 따라서 가상 가족의 총액은 이 비공통액까지 더해 보고된 $143,002,000 apron 이하이어야 한다. 이 조건의 수치 검산과 정확 사적 계약·리그 접수는 아직 인증하지 않는다. [NBA 공식 2021 캡·택스](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season), [당시 apron 공개표](https://www.salaryswish.com/salary-cap), CBA 원문 PDF p233–235·253–254를 사용했다.", "",
        "## 아직 미선택", "",
        "Toronto–Chicago 네 경기의 점수/승패/연장과 상대 전체 건강, Miami의 다른 경기 결과는 그대로 미선택이다. 이번 선택은 시카고 주인공의 계약·우승·MVP와 실제 Miami 임상의료·비공개 NBA 접수를 확정하지 않는다. 전체 G13/G14와 원고 게이트는 CLOSED다.", "",
        f"[자료와 함수]({Path(OUT).name}) · raw SHA와 CBA 본문 지문은 JSON에 기록.", "",
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    expected = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(markdown(expected), encoding="utf-8")
    if args.check:
        saved = json.loads((ROOT / OUT).read_text(encoding="utf-8"))
        need(not validate(saved), "Miami atom saved JSON stale")
        need((ROOT / MD).read_text(encoding="utf-8") == markdown(expected), "Miami atom MD stale")
        print("CURRENT: Miami S&T atom, 14+2 named roster, conservative salary matching; private full cap unclaimed")


if __name__ == "__main__":
    main()
