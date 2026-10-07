"""Bounded Miami 2021-22 apron witness for the selected Toronto/Miami atom.

Public salary rows support a chosen fictional no-extra-obligation family. They
are not an NBA private ledger or evidence of actual player consent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "research/TORONTO_MIAMI_2021_SELECTED_ATOM_LEGAL_BRIDGE_2026_10_07.json"
OUTPUT = ROOT / "research/MIAMI_2021_SELECTED_APRON_CLOSURE_2026_10_07.json"
REPORT = OUTPUT.with_suffix(".md")
RAW_DIR = Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-mia-apron-close-20261007")
CBA = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cba-matching-2026-10-04/2017_NBA_CBA.pdf")
PARENT_SHA = "719b2ff19583d6373a2c165988c9fc55b298fce3728dc8763df2d3f327357278"
CBA_SHA = "66d620ebf682e2ffc55698394fb4635d738bf0e0250aad34f9cc137a25bf051a"
CBA_PAGE_TEXT_SHA = {
    216: "dfbea7597d0b3913e9da06ffcd40ce135e257074cc3223b34230175b8084ade2",
    240: "894e9af9d73b50ed7208a6188c8fa7990be625dfe863b85945ff20c57ae85a65",
    241: "43236045b17a96dc3b0a2fc34452c83b383a4b6aacc623d961ec8cdb7ebb6f60",
    286: "4f56817f8f2df1a8158267dbe16e84e9d3ecd2650e4675a70ad485defe7a3966",
}
APRON = 143_002_000

# The cap-hit values are exact public-row inputs, not a claim that an NBA
# private accounting record was obtained. Dead money uses the higher of two
# public reports (5,214,583 / 5,214,584).
ROWS = {
    "Bam Adebayo": ("bam-adebayo", "2c7ca6d32d4bcb951be9aa0ecf33ef55026d3f6ab7cf4154191fe82e638e4f44", 28_103_500, 0),
    "Dewayne Dedmon": ("dewayne-dedmon", "8afc0380b9638ce8294ccb2ed9eaf7aa910129e1c461f1b5a267fd49193b09d8", 1_669_178, 0),
    "Duncan Robinson": ("duncan-robinson", "fae6b22e19413669b24a01fd97c01fc1f5715fcd6308b7706ec97fd1621cae41", 15_650_000, 0),
    "Gabe Vincent": ("gabe-vincent", "5bfee923085c4c65cff21eb228e72dd9bc93b136740a230d55557ba450e2e476", 1_669_178, 0),
    "Jimmy Butler": ("jimmy-butler", "193fbee165e5f7b3382a58c6778f5813cba3398f1175b9d94439e9e5314f0bcf", 36_016_200, 0),
    "KZ Okpala": ("kz-okpala", "94783c2a090dfd05aeed9a767818c5d33a5a18283e08e254a89c49cb87a5a6b8", 1_782_621, 0),
    "Kyle Lowry": ("kyle-lowry", "6bec8fb618503b7bf06b4df01ab60db22a698a6693efe0a8844cd2b747d57e40", 26_984_128, 0),
    "Markieff Morris": ("markieff-morris", "c039b407f4e868103768b427a7e0d6ead5d2aeb9a9f5e6e8b85e7d8c3c996241", 1_669_178, 0),
    "Max Strus": ("max-strus", "0d2583547e296e197c4b34e413d349d0dbca51f708b45a541fc962c0f123868f", 1_669_178, 0),
    "Omer Yurtseven": ("omer-yurtseven", "8ec08c570265e499fcebe01757ff3c2cb358bc41348e24f2d3ef51086d686506", 1_489_065, 0),
    "P.J. Tucker": ("pj-tucker", "399b3027087442a73b28654f041257a476b49da1ab3b5e3a2afedcd6ff2545b1", 7_000_000, 0),
    "Tyler Herro": ("tyler-herro", "c9c8c89604c606b85b2f4f54206a2e1ea410aafe0551f73b74ff3155a50ae894", 4_004_280, 5_000),
    "Udonis Haslem": ("udonis-haslem", "7a579ba3f7337e125c3a7a7ee5bacbe664594f26d95a8b858dbb84f613f94fa8", 1_669_178, 0),
    "Victor Oladipo": ("victor-oladipo", "547af40bea58b8328733161e33513c3777290ea1e26d23eb94b1bf23b682094f", 1_669_178, 0),
}
RYAN_SHA = "35eec540023471addd02b490ba1acdb5b4fae0c75dd7e8b36b12a2ef854c21c5"
OUTGOING_2020_21 = {
    "Andre Iguodala": ("andre-iguodala", "16665da2f0b0c9a019b06438fbfe9cbbb492f0afb48a0f74d2d9c3a6375fe334"),
    "Goran Dragic": ("goran-dragic", "d5b06f1944ee505de917453118bae3bd9c93242dfaecb4b305161e7791f6a363"),
    "Kendrick Nunn": ("kendrick-nunn", "17d19c85ec8078149812d3de132512c2d71d026ad1c45f0e5b2f4c9e841ec5c2"),
    "Nemanja Bjelica": ("nemanja-bjelica", "412656464ae9e0ba9cd98c8e886accfe82e00cf34bb9603daeded15c716775a5"),
    "Precious Achiuwa": ("precious-achiuwa", "2d81394654d1afb10dc0259fa84fc9c5f92fb55d395f8b2801aa4625a3f53f9e"),
    "Trevor Ariza": ("trevor-ariza", "8e0ec5936754c9e3325325527f50f0ef7ad9645e1d7c95a400ec2fc5baa4a0c4"),
}
# Public 2020-21 reported performance-bonus maxima of Miami's 15 named
# prior-season standard players. Dedmon's waived $300k row belongs to a
# different old contract; Miami's later $432,890 row has no bonus.
PAST_MIA_BONUS_MAX = {"Bam Adebayo": 74_050, "Tyler Herro": 100_000, "Victor Oladipo": 250_000}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_sha(path: Path) -> str:
    return digest(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def load_rows() -> tuple[dict, dict, dict]:
    assert normalized_sha(PARENT) == PARENT_SHA, "parent changed"
    assert digest(CBA.read_bytes()) == CBA_SHA, "CBA changed"
    with fitz.open(CBA) as doc:
        for page, expected_sha in CBA_PAGE_TEXT_SHA.items():
            text = doc[page - 1].get_text().replace("\r\n", "\n").replace("\r", "\n")
            assert digest(text.encode("utf-8")) == expected_sha, f"CBA page {page} changed"
        assert "Two-Way Player Salaries shall be excluded from Team Salary" in " ".join(doc[215].get_text().split())
        assert "all Performance Bonuses excluded" in " ".join(doc[239].get_text().split())
        assert "exclude Free Agent Amounts" in " ".join(doc[239].get_text().split())
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    assert set(parent["MIA_roster_handoff"]["opening_2021_10_25_standard"]) == set(ROWS)
    assert parent["MIA_roster_handoff"]["opening_2021_10_25_two_way"] == ["Caleb Martin", "Marcus Garrett"]
    assert parent["apron_legal_scope"]["2021_22_reported_apron_usd"] == APRON
    assert parent["selected_atom"]["lowry_public_comparator_usd_by_season"][0] == 26_984_128

    observed = {}
    sources = {}
    for name, (slug, expected_sha, cap, likely) in ROWS.items():
        raw = (RAW_DIR / f"{slug}.html").read_bytes()
        assert digest(raw) == expected_sha, f"physical salary source changed: {name}"
        soup = BeautifulSoup(raw, "html.parser")
        candidates = []
        for tr in soup.find_all("tr"):
            cells = [x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
            if cells and cells[0].startswith("2021-22") and len(cells) == 8:
                if cells[3] == f"${cap:,}" and cells[6] == f"${likely:,}" and cells[7] == "$0":
                    candidates.append(cells)
        assert len(candidates) == 1, f"missing or ambiguous contracted salary row: {name}"
        observed[name] = {"public_cap_hit_usd": cap, "reported_likely_usd": likely,
                          "reported_unlikely_usd": 0, "source_row": candidates[0]}
        sources[name] = {"url": f"https://www.salaryswish.com/players/{slug}",
                         "cache_path": str(RAW_DIR / f"{slug}.html"), "raw_sha256": expected_sha}
    raw = (RAW_DIR / "ryan-anderson.html").read_bytes()
    assert digest(raw) == RYAN_SHA
    soup = BeautifulSoup(raw, "html.parser")
    assert any("2021-22" in tr.get_text(" ", strip=True) and "$5,214,583" in tr.get_text(" ", strip=True)
               for tr in soup.find_all("tr"))
    sources["Ryan Anderson"] = {"url": "https://www.salaryswish.com/players/ryan-anderson",
                                 "cache_path": str(RAW_DIR / "ryan-anderson.html"), "raw_sha256": RYAN_SHA}
    # Bound, but never erase, the S2 prior-year bonus liability. The Miami
    # source roster has 9 surviving/renewed players and 6 outgoing players.
    prior_names = {"Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala",
                   "Dewayne Dedmon", "Duncan Robinson", "Gabe Vincent", "Max Strus",
                   "Victor Oladipo"} | set(OUTGOING_2020_21)
    assert len(prior_names) == parent["MIA_roster_handoff"]["S2_standard_count"] == 15
    prior_bonus = {}
    for name in sorted(prior_names):
        if name in OUTGOING_2020_21:
            slug, expected_sha = OUTGOING_2020_21[name]
            raw = (RAW_DIR / f"{slug}.html").read_bytes()
            assert digest(raw) == expected_sha, f"outgoing prior physical source changed: {name}"
            sources[name + "_2020_21"] = {"url": f"https://www.salaryswish.com/players/{slug}",
                                          "cache_path": str(RAW_DIR / f"{slug}.html"), "raw_sha256": expected_sha}
        else:
            slug = ROWS[name][0]
            raw = (RAW_DIR / f"{slug}.html").read_bytes()
        matches = []
        for tr in BeautifulSoup(raw, "html.parser").find_all("tr"):
            cells = [x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
            if cells and cells[0] in {"2020-21", "2020-21 Max"} and len(cells) == 8:
                matches.append(cells)
        assert matches, f"no 2020-21 source row: {name}"
        max_bonus = max(int(c[6].replace("$", "").replace(",", "")) +
                        int(c[7].replace("$", "").replace(",", "")) for c in matches)
        assert max_bonus == PAST_MIA_BONUS_MAX.get(name, 0), f"prior bonus changed: {name}"
        prior_bonus[name] = {"reported_2020_21_bonus_upper_usd": max_bonus,
                             "cash_was_actually_earned_certified": False,
                             "apron_2021_22_automatic_carry": False}
    assert sum(x["reported_2020_21_bonus_upper_usd"] for x in prior_bonus.values()) == 424_050
    return observed, sources, prior_bonus


def build() -> dict:
    rows, sources, prior_bonus = load_rows()
    # Bind helper returns to reviewed physical rows; summed cap hits do not
    # protect current bonus components or prior-year earned-cost bounds.
    assert set(rows) == set(ROWS), "Returned current Miami names changed"
    for name, (slug, raw_pin, cap, likely) in ROWS.items():
        raw_path = RAW_DIR / f"{slug}.html"
        assert digest(raw_path.read_bytes()) == raw_pin, "Returned raw source changed"
        candidates = []
        for tr in BeautifulSoup(raw_path.read_bytes(), "html.parser").find_all("tr"):
            cells = [x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
            if len(cells) == 8 and cells[0].startswith("2021-22") and cells[3] == f"${cap:,}" and cells[6] == f"${likely:,}" and cells[7] == "$0": candidates.append(cells)
        assert len(candidates) == 1 and rows[name] == {"public_cap_hit_usd": cap, "reported_likely_usd": likely, "reported_unlikely_usd": 0, "source_row": candidates[0]}, "Returned named cap/bonus differs from physical public row: " + name
    prior_names = {"Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala", "Dewayne Dedmon", "Duncan Robinson", "Gabe Vincent", "Max Strus", "Victor Oladipo"} | set(OUTGOING_2020_21)
    assert set(prior_bonus) == prior_names, "Returned prior liability names changed"
    for name in prior_names:
        assert prior_bonus[name] == {"reported_2020_21_bonus_upper_usd": PAST_MIA_BONUS_MAX.get(name, 0), "cash_was_actually_earned_certified": False, "apron_2021_22_automatic_carry": False}, "Returned prior earned-cost bound differs from reviewed source: " + name
    expected_sources = {name: {"url": f"https://www.salaryswish.com/players/{meta[0]}", "cache_path": str(RAW_DIR / f"{meta[0]}.html"), "raw_sha256": meta[1]} for name, meta in ROWS.items()}
    expected_sources["Ryan Anderson"] = {"url": "https://www.salaryswish.com/players/ryan-anderson", "cache_path": str(RAW_DIR / "ryan-anderson.html"), "raw_sha256": RYAN_SHA}
    expected_sources.update({name + "_2020_21": {"url": f"https://www.salaryswish.com/players/{meta[0]}", "cache_path": str(RAW_DIR / f"{meta[0]}.html"), "raw_sha256": meta[1]} for name, meta in OUTGOING_2020_21.items()})
    assert sources == expected_sources, "Returned source locators changed"
    live = sum(rows[n]["public_cap_hit_usd"] for n in ["Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala"])
    lowry = rows["Kyle Lowry"]["public_cap_hit_usd"]
    other = sum(v["public_cap_hit_usd"] for n, v in rows.items() if n not in {"Jimmy Butler", "Bam Adebayo", "Tyler Herro", "KZ Okpala", "Kyle Lowry"})
    dead = 5_214_584
    zero_one_service_uplift = 1_669_178 - rows["Omer Yurtseven"]["public_cap_hit_usd"]
    public_adjusted = live + lowry + other + dead + zero_one_service_uplift
    assert (live, lowry, other, dead, zero_one_service_uplift, public_adjusted) == (
        69_906_601, 26_984_128, 34_154_133, 5_214_584, 180_113, 136_439_559)
    assert APRON - public_adjusted == 6_562_441
    return {
        "schema": "MIAMI_2021_SELECTED_APRON_CLOSURE_V1",
        "status": "SELECTED_FICTIONAL_PUBLIC_TERMS_APRON_WITNESS_NOT_PRIVATE_NBA_CERTIFICATE",
        "parent_sha256": PARENT_SHA,
        "source_sha256": {str(PARENT.relative_to(ROOT)).replace("\\", "/"): PARENT_SHA, "tools/build_miami_2021_selected_apron_closure.py": normalized_sha(Path(__file__))},
        "cba_raw_sha256": CBA_SHA,
        "cba_page_text_sha256": {str(k): v for k, v in CBA_PAGE_TEXT_SHA.items()},
        "source_hashes": sources,
        "public_contract_rows": rows,
        "S2_prior_2020_21_named_bonus_bounds": prior_bonus,
        "six_category_apron_witness": {
            "surviving_original_standard_cap_hits_usd": live,
            "incoming_lowry_public_first_year_usd": lowry,
            "other_nine_standard_cap_hits_usd": other,
            "ryan_anderson_prior_stretch_conservative_usd": dead,
            "two_way_apron_increment_usd": 0,
            "zero_one_year_minimum_apron_adjustment_usd": zero_one_service_uplift,
            "reported_salary_plus_known_adjustments_usd": public_adjusted,
            "reported_apron_usd": APRON,
            "slack_before_any_extra_unreported_obligation_usd": APRON - public_adjusted,
        },
        "selected_fictional_gamma_family": {
            "new_unreported_salary_or_bonus_clauses": "NONE_SELECTED; all 14 standard UPCs retain the individually reported 2021-22 price/bonus rows",
            "prior_2020_21_earned_salary_or_bonus": "PRESERVED_IN_PRIOR_SALARY_CAP_YEAR; no retroactive deletion; no 2021-22 extra charge inferred without a continuing clause",
            "S2_named_prior_year_bonus_upper_usd": 424_050,
            "S2_reported_prior_year_delta_vs_historical_possible_interval_usd": [-424_050, 424_050],
            "S2_bonus_interval_applies_to_2020_21_not_extra_2021_22_charge": True,
            "S2_altered_result_apron_delta_usd": 0,
            "delta_reason": "Article VII 6(m)(3)(ii)(A) adds all performance bonuses, earned or unearned, to adjusted Team Salary. The only reported 2021-22 bonus in these 14 rows is Herro's $5,000, already inside his $4,004,280 cap hit. Changed S2 achievement is not treated as proof of a different 2021-22 contract clause.",
            "uncounted_unsigned_free_agent_holds": "Excluded by Article VII 6(m)(3)(ii)(D); no outstanding Miami QO or first-refusal notice selected for an unsigned former player",
            "new_prior_year_grievance_resolution_added_to_2021_22": "NONE_SELECTED; Article VII 4(a)(1)(iii) would add any such actual resolution to Team Salary, so this is a fictional route condition rather than proof of historical absence",
            "unused_exception_or_incomplete_roster_hold": "Excluded by Article VII 6(m)(3)(ii)(F)-(G); 14 signed standard places and one open place",
            "draft_tender": "NONE; parent has zero Miami-owned 2021 picks",
            "two_way_cash_paid_zero_claim": False,
            "private_original_gamma_exact_certified": False,
            "any_extra_unreported_obligation_must_fit_slack_usd": APRON - public_adjusted,
        },
        "selected_route_feasible_under_reported_contract_family": True,
        "selected_MIA_apron_legal_family_complete": True,
        "Toronto_four_date_legal_handoff": "SELECTED_LOWRY_ATOM_PLUS_NAMED_MIA_PUBLIC_TERMS; Toronto membership/roles may execute conditionally, separate opponent health and NBA game results unselected",
        "actual_NBA_approval_or_contract_receipt_certified": False,
        "whole_2021_22_MIA_or_TOR_season_complete": False,
        "author_lock": False,
        "manuscript_allowed": False,
    }


def validate(packet: dict) -> None:
    expected = build()
    assert packet == expected, "packet differs from physical source-bound build"


def render(p: dict) -> str:
    c = p["six_category_apron_witness"]
    return "\n".join([
        "# Miami 2021–22 선택 원자거래 하드캡 여유 증인",
        "",
        "2021-10-25 명명 14 표준계약과 2 양방향 계약을 전제로 하는 **가상 선택 계약 가족**이다. 개별 선수 계약의 공개 보도 금액을 재산술했으며 NBA 비공개 장부·동의서 인증은 아니다.",
        "",
        "| 조정 Team Salary 항목 | USD |",
        "|---|---:|",
        f"| 기존 4인 | {c['surviving_original_standard_cap_hits_usd']:,} |",
        f"| Lowry 첫해 | {c['incoming_lowry_public_first_year_usd']:,} |",
        f"| 나머지 9인 | {c['other_nine_standard_cap_hits_usd']:,} |",
        f"| Ryan Anderson 잔존 보장액 보수값 | {c['ryan_anderson_prior_stretch_conservative_usd']:,} |",
        f"| 0·1년차 최소계약 apron 조정 | {c['zero_one_year_minimum_apron_adjustment_usd']:,} |",
        f"| 합계 | {c['reported_salary_plus_known_adjustments_usd']:,} |",
        f"| 보고 apron | {c['reported_apron_usd']:,} |",
        f"| 추가 미보고 부담을 수용할 여유 | {c['slack_before_any_extra_unreported_obligation_usd']:,} |",
        "",
        "Herro의 공개 likely bonus $5,000은 cap hit에 이미 포함된다. 2017 CBA Article VII §6(m)(3)(ii)(A)는 성취 여부에 관계없이 모든 performance bonus를 apron용 Team Salary에 넣는다. 따라서 2020–21의 다른 경기 결과 자체를 2021–22 보너스 $0 수령이라고 주장하지 않는다. 원래 얻은 전년도 급여·보너스는 보존하고 새해로 자동 중복 계상하지 않는다.",
        "전년도 Miami 명명 15인의 공개 2020–21 성과 보너스 상단은 Bam $74,050 + Herro $100,000 + Oladipo $250,000 = $424,050이다. 변경 세계에서 실제 벌었는지는 미인증이고, 원역사와의 차이는 −$424,050~+$424,050 범위를 넘기지 않는다. 이 금액은 전년도 급여 귀속으로 보존하며 2021–22 apron에 별도 재기입하지 않는다.",
        "",
        "이 가상 가족은 공개된 14개 계약 조건 외 추가 미보고 보너스·보장·서명을 채택하지 않는다. Ryan Anderson의 $5,214,583/$5,214,584 공개 차이는 높은 값을 사용했다. 남은 한 표준 자리는 계약을 체결한 것으로 만들지 않는다. 일반 미서명 FA 보류액·미사용 예외·미완성 명단 보류액은 CBA §6(m)(3)에서 제외되며, 미서명 선수의 QO/우선거절통지와 픽 Required Tender는 별도 예외다. 이 가족에서는 해당 예외를 새로 발행하지 않는다.",
        "",
        "토론토 4경기의 Lowry·Dragic·Achiuwa 소속 충돌은 선택된 원자거래와 이 비용 가족 아래에서 해소 가능하다. 상대 선수 건강, 토론토 계약의 별도 전수검문, 경기 결과·출전분은 이 문서가 인증하지 않는다.",
        "",
        "## 원자료",
        "",
        "- [2017 NBA CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf): PDF 216 Article VII §4(j), 240–241 §6(m)(3), 286 §12(f)(2).",
        "- [2021–22 NBA 공식 cap/tax 발표](https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/); apron $143,002,000은 [SalarySwish 보고값](https://www.salaryswish.com/salary-cap).",
        "- 각 선수의 2021–22 계약행은 JSON의 `source_hashes`에 URL·회수 원문 SHA와 함께 기록했다.",
        "",
        "원고·전체 시즌·실제 NBA 승인·새 작가잠금: 모두 0.",
        "",
    ])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    packet = build()
    validate(packet)
    data = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    md = render(packet)
    if args.write:
        OUTPUT.write_text(data, encoding="utf-8")
        REPORT.write_text(md, encoding="utf-8")
    if args.check:
        assert OUTPUT.read_text(encoding="utf-8") == data
        assert REPORT.read_text(encoding="utf-8") == md
    print(f"Miami selected apron witness: {packet['six_category_apron_witness']['slack_before_any_extra_unreported_obligation_usd']:,} USD; check={args.check}")


if __name__ == "__main__":
    main()
