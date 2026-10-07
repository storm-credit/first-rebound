"""Price only the two selected Houston rookie-scale routines; no team ledger."""

from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = "tools/build_hou_2021_selected_rookie_scale_price.py"
SOURCE = "research/BOS_OKC_HOU_2021_POST_T1_OPENING_INTERVALS_2026_10_07.json"
OUT = "research/HOU_2021_SELECTED_ROOKIE_SCALE_PRICE_2026_10_07.json"
MD = OUT.replace(".json", ".md")
SOURCE_SHA = "fc5a00f3268da6de99fe0b5d695e776ac8e3935090dfa4c54f5b086112f5aea6"
TEMP = Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-hou-rsc-price-20261007")
CBA = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf")
RAW = {
    "NBA_CAP_2017": (TEMP / "NBA_CAP_2017.html", "67e1c0e1126f3fcbced41896a26ee28d7dd14123cba36a9c6a19dd56017526a5", "https://www.nba.com/news/nba-salary-cap-set-2017-18-season-99093-million"),
    "NBA_CAP_2021": (TEMP / "NBA_CAP_2021.html", "9e2a73e5ca9b588bb58a662f5fc8b7f6fd00096b8efde6f40c65d9119c865082", "https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season"),
    "HOOPS_RUMORS_REPORT": (TEMP / "HOOPS_RUMORS_2021_ROOKIE_SCALE.html", "65e23ec684ad4e37567eb731b298c62a0999d335eae2fd2a4046e9434b73ea49", "https://www.hoopsrumors.com/2021/08/rookie-scale-salaries-for-2021-nba-first-round-picks.html"),
    "CBA_2017": (CBA, "66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a", "https://official.nba.com/2017-nba-collective-bargaining-agreement/"),
}
PAGES = {31: "b432874781695f94a2c94244a203ce8bcb5e6ba2ad5a08984a32e12ade038af3", 294: "17a15e17207724b7bd9314d9fd2276e8a52d3460d6c062e5641d4fb682a900f7", 296: "9a75832d9909847ff025943fbfd9edb11b962fb43922715e72e1874b3e309296", 297: "0d08812db4e42f2895a45a905ed8fe4f626368e7c1c2d50e3c4d91ded19b8f3f", 559: "48bb5add7364d332c1ffd051b5b89ba9f5ef769995048125a7cfd80c5c810037"}
PICKS = {2: "Jalen Green", 16: "Alperen Sengun"}


def require(value: bool, why: str):
    if not value:
        raise ValueError(why)


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode()).hexdigest()


class TableText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell, self.all_text = [], None, None, []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        self.all_text.append(data)
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def html_source(path: Path) -> TableText:
    result = TableText()
    result.feed(path.read_text(encoding="utf-8", errors="replace"))
    return result


def source_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def physical_pdf_page(page: int) -> str:
    raw = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(CBA), "-"], capture_output=True, check=True).stdout
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n").rstrip("\x0c")


def cba_page(page: int) -> str:
    body = physical_pdf_page(page)
    require(hashlib.sha256(body.encode()).hexdigest() == PAGES[page], f"CBA page {page} changed")
    return body


def source_inputs(root: Path):
    require(normalized_sha(root / SOURCE) == SOURCE_SHA, "Selected RSC source changed")
    source = source_json(root / SOURCE)
    require(source == json.loads((root / SOURCE).read_bytes().decode("utf-8-sig")), "Selected JSON loader differs from physical source")
    require(source["summary"]["new_selected_named_RSC_events"] == 2 and source["summary"]["remaining_unexecuted_reported_rows_in_requested_ranges"] == 80, "Selected scope changed")
    require(source["authority"]["whole_macro3_or_2021_22_season_complete"] is False and source["authority"]["manuscript_allowed"] is False, "Selected source promoted")
    for path, expected, _ in RAW.values():
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected, "Raw source changed: " + str(path))
    pages = {n: cba_page(n) for n in PAGES}
    require(all(pages[n] == physical_pdf_page(n) for n in PAGES), "CBA page loader differs from physical PDF")
    flat = {n: " ".join(text.split()) for n, text in pages.items()}
    require("2020-21 through 2023-24" in flat[31] and "preceding Salary Cap Year's Rookie Salary Scale" in flat[31], "CBA post-2019 annual scale rule missing")
    require("Baseline Rookie Scale" in flat[296] and "thirty percent (30%)" in flat[296] and "forty-five percent (45%)" in flat[297], "CBA 2019 baseline uplift rule missing")
    require("EXHIBIT B-2" in flat[559] and "2017-18 BASELINE ROOKIE SCALE" in flat[559], "CBA baseline table missing")
    require("one hundred twenty percent (120%)" in flat[294] and "Salary plus Unlikely Bonuses" in flat[294], "CBA upper limit missing")
    parsed = {}
    for name in ("NBA_CAP_2017", "NBA_CAP_2021", "HOOPS_RUMORS_REPORT"):
        path = RAW[name][0]
        loaded = html_source(path)
        physical = TableText()
        physical.feed(path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"))
        require((loaded.rows, loaded.all_text) == (physical.rows, physical.all_text), "HTML loader differs from physical source: " + name)
        parsed[name] = loaded
    cap17 = " ".join(parsed["NBA_CAP_2017"].all_text)
    cap21 = " ".join(parsed["NBA_CAP_2021"].all_text)
    require("Salary Cap has been set at $99.093 million for the 2017-18 season" in " ".join(cap17.split()), "NBA 2017 cap body missing")
    require("Salary Cap has been set at $112.414 million for the 2021-22 season" in " ".join(cap21.split()), "NBA 2021 cap body missing")
    reported = parsed["HOOPS_RUMORS_REPORT"].rows
    prices = {}
    for pick, name in PICKS.items():
        rows = [r for r in reported if len(r) == 6 and r[0] == name]
        require(len(rows) == 1, "Reported RSC price row missing: " + name)
        prices[pick] = [int(x.replace("$", "").replace(",", "")) for x in rows[0][1:]]
    return source, pages, prices


def build(root: Path = ROOT):
    source, pages, prices = source_inputs(root)
    selected = {x["pick"]: x for x in source["selected_named_contract_events"]}
    require(set(selected) == set(PICKS), "Two rookie picks changed")
    players = []
    ratio = Fraction(112414000, 99093000) * Fraction(145, 100)
    for pick, name in PICKS.items():
        action = selected[pick]
        require((action["player"], action["team"], action["selected_policy"], action["contract_class"]) == (name, "HOU", "120_PERCENT_OF_OFFICIAL_PICK_SCALE_SUBJECT_TO_SCALE_INPUT", "STANDARD_ROOKIE_SCALE"), "RSC selected actor/policy changed")
        require(action["lawful_UPC_term"]["initial_seasons"] == ["2021-22", "2022-23"] and action["lawful_UPC_term"]["third_and_fourth_options_separate"] is True and all("NOT_EXERCISED" in action["lawful_UPC_term"][k] for k in ("third_season_team_option", "fourth_season_team_option")), "RSC term/option changed")
        require(action["scale_constraints"]["unlikely_bonus"] == action["scale_constraints"]["new_signing_bonus"] == 0, "New bonus added")
        if pick == 16:
            require(action["foreign_contract_obstacle_lawfully_resolved_before_UPC"] is True and action["actual_foreign_release_document_certified"] is False, "Sengun foreign obligation boundary changed")
        matches = re.findall(rf"(?m)^\s*{pick}\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+([\d.]+)%", pages[559])
        require(len(matches) == 1, "CBA Exhibit B-2 baseline pick row changed")
        baseline = [int(Decimal(x.replace(",", "")) * 1000) for x in matches[0][:3]]
        option_raise = Decimal(matches[0][3]) / 100
        amounts = prices[pick][:4]
        require(sum(amounts) == prices[pick][4], "Reported total differs from four rows")
        scale100 = []
        discrepancies = []
        for base, max120 in zip(baseline, amounts[:3]):
            inferred = Fraction(max120 * 5, 6)
            require(inferred.denominator == 1, "120 percent report does not invert to integer scale")
            modeled_no_round = Fraction(base) * ratio
            gap = abs(inferred - modeled_no_round)
            require(gap <= 50, "Reported 2021 scale does not fit CBA baseline/cap calculation")
            scale100.append(int(inferred))
            discrepancies.append(str(round(float(gap), 3)))
        fourth_expected = int((Decimal(amounts[2]) * (1 + option_raise)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        require(amounts[3] == fourth_expected, "Reported fourth option price does not match CBA option rate")
        players.append({"pick": pick, "player": name, "team": "HOU", "reported_source_type": "SECONDARY_PUBLIC_2021_PRICE_TABLE_NOT_LEAGUE_UPC", "CBA_Exhibit_B2_2017_baseline_usd": baseline, "CBA_Exhibit_B2_fourth_option_raise_percent": str(option_raise * 100), "2021_scale_100_percent_inferred_from_report_usd": scale100, "independent_CBA_cap_formula_unrounded_distance_usd": discrepancies, "reference_reported_120_percent_proposal_usd_by_season": {"2021-22": amounts[0], "2022-23": amounts[1], "2023-24_if_third_option_exercised": amounts[2], "2024-25_if_fourth_option_exercised": amounts[3]}, "selected_statutory_salary_function": {"2021-22": f"1.2*operative_2021_RSC_scale(pick_{pick},year_1)", "2022-23": f"1.2*operative_2021_RSC_scale(pick_{pick},year_2)", "2023-24_if_third_option_exercised": f"1.2*operative_2021_RSC_scale(pick_{pick},year_3)", "2024-25_if_fourth_option_exercised": f"1.2*operative_2021_RSC_scale(pick_{pick},year_3)*(1+{option_raise})"}, "actual_selected_salary_usd_certified": None, "reference_first_two_seasons_usd": sum(amounts[:2]), "third_option_exercised_now": False, "fourth_option_exercised_now": False, "reference_four_year_if_both_options_later_exercised_usd": sum(amounts), "reported_point_matches_unrounded_formula_within_50_usd_not_legal_upper_proof": True, "operative_league_scale_or_exact_rounding_certified": False, "actual_private_contract_certified": False})
    combined = {"2021-22": sum(p["reference_reported_120_percent_proposal_usd_by_season"]["2021-22"] for p in players), "2022-23": sum(p["reference_reported_120_percent_proposal_usd_by_season"]["2022-23"] for p in players), "2023-24_if_both_third_options_exercised": sum(p["reference_reported_120_percent_proposal_usd_by_season"]["2023-24_if_third_option_exercised"] for p in players), "2024-25_if_both_fourth_options_exercised": sum(p["reference_reported_120_percent_proposal_usd_by_season"]["2024-25_if_fourth_option_exercised"] for p in players)}
    return {"schema": "HOU_2021_SELECTED_RSC_REFERENCE_PRICE_AND_STATUTORY_FUNCTION_V2", "status": "TWO_SELECTED_RSC_STATUTORY_FUNCTIONS_WITH_REPORTED_REFERENCE_POINTS_NO_NUMERIC_UPC_CERTIFICATION", "source_sha256": {SOURCE: SOURCE_SHA}, "source_hash_method": "UTF8_LF_SHA256", "self_sha256": normalized_sha(root / SELF), "raw_sources": {k: {"path": str(v[0]), "raw_sha256": v[1], "url": v[2]} for k, v in RAW.items()}, "CBA_pdf_page_text_sha256": {str(k): v for k, v in PAGES.items()}, "CBA_page_text_method": "pdftotext_-layout_single_page_UTF8_LF_strip_final_formfeed", "formula": "2017 Exhibit B-2 baseline x 1.45 (2019-20 uplift) x official 2021-22 cap / official 2017-18 cap; 2020-21 and 2021-22 annual changes telescope before unpublished rounding", "formula_cap_usd": {"2017-18": 99093000, "2021-22": 112414000}, "unpublished_annual_rounding_not_claimed_exact": True, "statutory_salary_policy": "1.2*operative_legal_2021_RSC_scale(pick,contract_year); fourth year if exercised follows Article VIII Section 1 option raise", "operative_official_2021_scale_table_physically_loaded": False, "reported_point_vs_unrounded_CBA_formula_is_similarity_not_legal_ceiling_proof": True, "players": players, "combined_reference_reported_120_percent_proposal_usd": combined, "combined_reference_first_two_seasons_usd": combined["2021-22"] + combined["2022-23"], "combined_reference_four_year_if_both_options_later_exercised_usd": sum(combined.values()), "option_years_not_live_liabilities_now": True, "unchanged_parent_scope": {"named_new_RSC_events": 2, "unexecuted_reported_rows": 80, "BOS_OKC_HOU_full_interval_legal_complete": False, "HOU_whole_six_category_team_cost_complete": False, "regular_season_15_plus_2_complete": False, "actual_contract_paper_or_medical_certified": False, "whole_2021_22_season_complete": False, "new_author_lock": False, "manuscript_allowed": False}, "design_gate": "CLOSED", "freeze": "v0.30 PARTIAL"}


def validate(packet, root: Path = ROOT):
    require(packet == build(root), "Saved RSC price differs from source-bound reconstruction")
    return []


def render(p):
    lines = ["# HOU 신인 2명 계약의 참고 가격과 법정 함수", "", "기존 T1 계약 루틴 2건의 선택 정책은 **해당 2021 신인 스케일의 120%**다. 아래 숫자는 2차 공개표의 참고 제안점이다. 리그가 실제 적용한 표·반올림·사적 UPC의 정확 달러로 인증하지 않는다.", "", "| 선수 | 2021–22 참고 | 2022–23 참고 | 3년차 옵션 참고·미행사 | 4년차 옵션 참고·미행사 |", "|---|---:|---:|---:|---:|"]
    for x in p["players"]:
        s = x["reference_reported_120_percent_proposal_usd_by_season"]
        lines.append(f"| {x['player']} (#{x['pick']}) | ${s['2021-22']:,} | ${s['2022-23']:,} | ${s['2023-24_if_third_option_exercised']:,} | ${s['2024-25_if_fourth_option_exercised']:,} |")
    lines += ["", f"공개표 참고 합계: 첫해 **${p['combined_reference_reported_120_percent_proposal_usd']['2021-22']:,}**, 첫 2시즌 **${p['combined_reference_first_two_seasons_usd']:,}**. 이는 법정 선택급여 확정액이 아니다. 실제 선택금액은 `1.2 × operative_legal_2021_RSC_scale(pick, contract_year)`이며, 4년차 옵션은 Article VIII §1의 3년차 대비 인상률을 따른다. 두 옵션은 현재 미행사다.", "", "2017 CBA Exhibit B-2와 Article VIII/Article I의 배수·연도별 cap 조정, NBA 공식 2017·2021 cap 발표로 공개 보고표의 100% 역산값을 비교했다. $50 이내 일치는 **유사성 검사**이며 보고 가격점이 실제 법정 120% 상한 이하라는 증명이 아니다. 리그의 실제 2021 스케일·매년 반올림을 이 자료에서 인증하지 못했다. 이를 사적 계약서 취득의 새 선행 게이트로 만들지 않는다.", "", "BOS·OKC·HOU 전체 명단/6범주 비용/첫 Chicago 경기까지의 적법 구간·상대 건강·시즌 승패는 여전히 미완료다. 실제 계약 접수·의료 인증 0, 원고 0, 설계/원고 게이트 CLOSED.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    packet = build()
    if args.write:
        (ROOT / OUT).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / MD).write_text(render(packet), encoding="utf-8")
    if args.check:
        validate(json.loads((ROOT / OUT).read_text(encoding="utf-8")))
        require((ROOT / MD).read_text(encoding="utf-8") == render(packet), "RSC price MD differs")
    if args.self_test:
        other = json.loads(json.dumps(packet))
        other["players"][0]["reference_reported_120_percent_proposal_usd_by_season"]["2021-22"] += 1
        try:
            validate(other)
        except ValueError:
            pass
        else:
            raise AssertionError("One-dollar salary shift accepted")
    print("PASS reference", packet["combined_reference_reported_120_percent_proposal_usd"], "unexecuted", packet["unchanged_parent_scope"]["unexecuted_reported_rows"])


if __name__ == "__main__":
    main()
