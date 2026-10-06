"""G1 public-contract matching interval and conditional apron delta; no choice/promotion."""
from pathlib import Path
from copy import deepcopy
from datetime import date
import argparse
import hashlib
import json
import re
import fitz
from bs4 import BeautifulSoup
import build_gsw_hutchison_operating_candidates as operating

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "b48fb829756fc8c9ee943a440a13a2b2d4426d08"
SELF = "tools/build_gsw_g1_matching_hardcap_scope.py"
OUT = ROOT / "research/GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json"
MD = OUT.with_suffix(".md")
CACHE = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-gsw-g1-matching-20261007")
REVIEWED_SHA = {'simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json': '8bf812b411ce61592d7221f91954479f596062cf7b501ca78292ebf9ce5e6a99', 'tools/build_gsw_hutchison_operating_candidates.py': '9fa244e5bfb8a745ebf2a48ca636eef13f095be947130ce97b39df63c8e6c7fa'}
HTML = {
    "WIGGINS": ("c938241967d082d8857303af95300ff9fc0dd0243ef971a06a78cff9132d39d3", "https://www.salaryswish.com/players/andrew-wiggins"),
    "RUSSELL": ("6b21519a6be3aeab265b5aab7fb4b0079f1d3fe92c78c53d9cfcb953a44d46ea", "https://www.salaryswish.com/players/dangelo-russell"),
    "SPELLMAN": ("21a830fae7ad38ec82a81ac8b575ce500f45a8861e30a03281bd6062db92342d", "https://www.salaryswish.com/players/omari-spellman"),
    "CAP": ("970ac166d62d09d052de1c8419d2c53288aed9af1d51c5b10db3c063e41340b4", "https://www.salaryswish.com/salary-cap"),
}
LEGAL_PAGES = [64, 65, 193, 233, 234, 235, 236, 240, 241, 248, 252, 253, 254, 255, 294, 295, 398, 399]


def normalized(p):
    return p.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def sha(p):
    return hashlib.sha256(normalized(p).encode("utf-8")).hexdigest()


def load(f):
    return json.loads(normalized(ROOT / f))


def dollars(cell):
    return int(re.search(r"\$([\d,]+)", cell).group(1).replace(",", ""))


def parse_contract(raw):
    soup = BeautifulSoup(raw, "html.parser")
    found = []
    for table in soup.find_all("table"):
        rows = [[td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])] for tr in table.find_all("tr")]
        if rows and rows[0][:4] == ["Season", "Option", "Option Used", "Cap Hit"]:
            for row in rows[1:]:
                if row and row[0].startswith("2019-20"):
                    found.append((row, rows))
    if len(found) != 1:
        raise ValueError("2019 contract row not unique")
    row, rows = found[0]
    return {"season_label":row[0], "cap_hit":dollars(row[3]), "base":dollars(row[4]), "protected":dollars(row[5]), "likely":dollars(row[6]), "unlikely":dollars(row[7]), "table_rows":[r for r in rows[1:] if r and re.match(r"20\d\d-\d\d", r[0])]}


def calculate(w, r, s, h_scale_lower, h_scale_upper):
    # The generous scale envelope contains the published #28 scale magnitude,
    # without declaring the one-decimal $000s display an exact contractual dollar.
    h_pre_lower = .8 * h_scale_lower
    h_post_upper = 1.2 * h_scale_upper  # includes ALL legally effective incoming bonus
    r_previous = next(dollars(row[3]) for row in r["prior_contract_rows"] if row[0].startswith("2018-19"))
    w_previous = next(dollars(row[3]) for row in w["table_rows"] if row[0].startswith("2018-19"))
    cap = 109140000
    r_bonus_ceiling = max(0, max(.25 * cap, 1.05 * r_previous) - r["cap_hit"] - r["unlikely"])
    w_bonus_ceiling = max(0, max(.25 * cap, 1.05 * w_previous) - w["cap_hit"] - w["unlikely"])
    gsw_out_lower = r["cap_hit"] + s["cap_hit"] + h_pre_lower
    gsw_in_upper = w["cap_hit"] + w_bonus_ceiling
    min_out = w["cap_hit"]
    min_in_upper = r["cap_hit"] + r_bonus_ceiling + s["cap_hit"] + h_post_upper
    return {
        "h_pre_salary_lower":h_pre_lower, "h_post_salary_plus_unlikely_upper":h_post_upper,
        "russell_current_bonus_headroom":r_bonus_ceiling, "wiggins_current_bonus_headroom":w_bonus_ceiling,
        "spellman_second_assignment_current_bonus":0,
        "gsw_outgoing_lower":gsw_out_lower, "gsw_incoming_upper":gsw_in_upper,
        "gsw_sufficient_matching_limit":1.25*gsw_out_lower+100000,
        "gsw_min_matching_slack":1.25*gsw_out_lower+100000-gsw_in_upper,
        "min_outgoing":min_out, "min_incoming_upper":min_in_upper,
        "min_sufficient_matching_limit":1.25*min_out+100000,
        "min_min_matching_slack":1.25*min_out+100000-min_in_upper,
        "gsw_trade_apron_delta_upper_if_other_costs_preserved":gsw_in_upper-gsw_out_lower,
    }


def build():
    for f, h in REVIEWED_SHA.items():
        if sha(ROOT/f) != h:
            raise ValueError("reviewed source changed: "+f)
    upstream = load("simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.json")
    operating.validate(upstream)  # full original-source reconstruction, not a freshly minted upstream SHA
    if upstream["recommendation"]["selected"] or upstream["authority"]["landing_author_locked"]:
        raise ValueError("G1 must remain an unselected candidate")
    observed, raw = {}, {}
    for key, (h, url) in HTML.items():
        p = CACHE/(key+".html")
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != h:
            raise ValueError("collected original HTML changed: "+key)
        soup = BeautifulSoup(b,"html.parser")
        text = soup.get_text(" ",strip=True)
        raw[key] = {"url":url, "cache_path":str(p), "raw_sha256":h, "bytes":len(b), "text_sha256":hashlib.sha256(text.encode()).hexdigest(), "extraction":"BeautifulSoup html.parser get_text(' ',strip=True), UTF8; raw HTML bytes unchanged", "authority_type":"PUBLISHER_OWN_COMPILED_PUBLIC_DATA_NOT_LEAGUE_CONTRACT_MEMO"}
        if key != "CAP":
            observed[key] = parse_contract(b)
        else:
            table = next(t for t in soup.find_all("table") if "2019-20" in t.get_text())
            rows = [[td.get_text(" ",strip=True) for td in tr.find_all(["td","th"])] for tr in table.find_all("tr")]
            row = next(row for row in rows if row and row[0]=="2019-20")
            observed["CAP"] = {"cap":dollars(row[4]), "tax":dollars(row[5]), "apron":dollars(row[6])}
    # Russell's previous-season rookie salary is independently parsed from its prior table.
    r_soup = BeautifulSoup((CACHE/"RUSSELL.html").read_bytes(),"html.parser")
    prior_rows = []
    for t in r_soup.find_all("table"):
        rows = [[td.get_text(" ",strip=True) for td in tr.find_all(["td","th"])] for tr in t.find_all("tr")]
        if rows and rows[0][:4] == ["Season","Option","Option Used","Cap Hit"] and any(row and row[0].startswith("2018-19") for row in rows):
            prior_rows.extend(row for row in rows[1:] if row and re.match(r"20\d\d-\d\d",row[0]))
    observed["RUSSELL"]["prior_contract_rows"] = prior_rows
    if {key:observed[key]["cap_hit"] for key in ["WIGGINS","RUSSELL","SPELLMAN"]} != {"WIGGINS":27504630, "RUSSELL":27285000, "SPELLMAN":1897800}:
        raise ValueError("historical salary anchors changed")
    if any(observed[key]["likely"] or observed[key]["unlikely"] for key in ["WIGGINS","RUSSELL","SPELLMAN"]):
        raise ValueError("preserved zero performance input family changed")
    cba = Path(upstream["raw_sources"]["CBA"]["cache_path"])
    doc = fitz.open(cba)
    cba_meta = {"url":upstream["raw_sources"]["CBA"]["url"], "raw_sha256":upstream["raw_sources"]["CBA"]["raw_sha256"], "pdf_pages":LEGAL_PAGES, "page_text_sha256":{str(page):hashlib.sha256(doc[page-1].get_text().replace("\r\n","\n").replace("\r","\n").encode()).hexdigest() for page in LEGAL_PAGES}}
    numeric = calculate(observed["WIGGINS"], observed["RUSSELL"], observed["SPELLMAN"],1000000,2000000)
    events = ["2019-07-07","2019-07-08","2019-07-10","2019-07-11","2019-07-17","2019-07-31","2019-08-03","2019-09-30","2019-10-07","2020-01-07","2020-01-15","2020-01-24","2020-02-06","2020-02-07","2020-02-08","2020-02-23","2020-02-27","2020-03-03","2020-03-05","2020-03-10"]
    return {
        "status":"G1_DUAL_MATCHING_SOURCE_BOUND_VALID_CONDITIONAL_HARDCAP_DELTA_WHOLE_COST_HOLD_ROOT_REVIEW_PENDING",
        "baseline_main":BASELINE, "candidate":"G1", "candidate_selected":False,
        "source_sha256":{**REVIEWED_SHA, SELF:sha(ROOT/SELF)},
        "raw_new_salary_sources":raw, "existing_cba_direct_read":cba_meta,
        "observed_original_contract_inputs":observed,
        "contract_source_scope":"Historical nominal contract components in publisher's own compilation; current modern player status and future careers are not candidate facts. No league memo certification.",
        "source_exclusions":{"SalarySwish_trade_sum":"NOT_USED: search trade summary reports original Evans as0 signingrights; aggregate is not a valid whole-player-salary witness", "ESPN2020":"HTTP403 raw cached; no retrieved salary-body evidence adopted"},
        "preserved_family":{"Russell_Wiggins_Spellman_public_nominal_contract_components":True, "original_Evans_salary_used":False, "original_Chicago22_Hutchison_salary_used":False, "original_Evans_MIN_NY_future_copied":False, "new_Hutchison_salary_percentage_selected":None, "third_fourth_options_selected":None, "post_assignment_Hutchison_bonus_or_salary_exact":None, "MIN_acceptance":None, "actual_contract_global_certification":False},
        "scale_domain":{"source":"NBA CBA1012018 ExhibitA PDF29 #28 secondyeardisplay1604.9 ($000s)", "published_reference":1604900, "conservative_source_magnitude_envelope":[1000000,2000000], "envelope_is_selected_salary":False, "envelope_is_exact_operative_scale":False, "all_salary_percentages":[.8,1.2], "unknown_trade_bonus_included_in_post_120_percent_ceiling":True, "future_option_dependence_does_not_bypass_current_year_ceiling":True, "no_precise_display_rounding_algorithm_assumed":True},
        "rule_connections":{"matching":"VII6(j)(1)(i),(iii) and6(j)(3):125%+100k is an available sufficient bound above/below tax and belowcap; simultaneous aggregate, no exceptions mixed", "current_guarantee":"VII6(j)(5)(ii):Feb6 is afterJan10, current base is fully protected for matching", "Hutchison_bonus":"VIII1(d):salary+unlikely including assignmentbonus automatically limited to120% of applicable scale", "Russell_Wiggins_bonus":"II7(f)(i):current bonus positive headroom max(0,max25%cap/105%prior salary-current salary-unlikely); both have0", "Spellman_bonus":"XXIV2(a)(i),(vi):original rookiecontract already traded ATL→GSW July8; this February assignment is not a second payable bonus", "allocation":"VII3(b)(1)(ii),(2):tradebonus allocated over current and remaining years by protected percentages, not arbitrary future-only assignment", "hardcap":"VII8(e)(1),6(m)(3):recipientS&T imposes apron in all subsequent capyear states with A-G adjustments"},
        "numeric_dual_matching_witness":numeric,
        "bonus_parameters_actual_values":None,
        "bonus_waiver_q_selected":False,
        "matching_bound_valid_for_all_h_salary_percentages_and_allowed_assignment_bonus_in_declared_source_domain":True,
        "matching_bound_whole_contract_or_transaction_certificate":False,
        "dates":{"candidate_trade":"2020-02-06", "Russell_signed_and_acquired":"2019-07-07", "Spellman_acquired":"2019-07-08", "Russell_days_since_acquisition":(date(2020,2,6)-date(2019,7,7)).days, "Spellman_days_since_acquisition":(date(2020,2,6)-date(2019,7,8)).days, "Hutchison_contract_family_start_season":"2018-19", "Hutchison_exact_signing_date":None, "aggregation_2month_and_signing3month_Dec15_Jan15_restrictions_have_elapsed_in_this_family":True, "new_excess_extension_6month_boundary":"2020-08-06", "actual_future_extension_selected":None},
        "hardcap_scope":{"reported_2019_apron":observed["CAP"]["apron"], "trigger_original_S_and_T":"2019-07-07", "pretrade_symbol":"B(t)=allother_GSW_apron_adjusted_cost_excluding_Hutchison", "pretrade_whole_scale_sufficient_othercost_upper":observed["CAP"]["apron"]-2400000, "pretrade_formula":"forall preG1 states t: B(t)+H_apron(t)<=A; H_apron<=1.2*s28<=2400000", "trade_delta_formula":"if unchanged other components and priorstate legal: outgoing R+S+H_apron replaced by incoming W; delta<=-2478170, so this trade cannot create a new apron breach", "after_trade_Hutchison_GSW_current_salary_removed":True, "outgoing_bonus_cash_and_annual_cash_limit_not_whole_certified":True, "posttrade_remaining_othercost_domain":None, "pretrade_Bt_source_complete":False, "known_guide_event_dates":events, "event_list_complete_private_transaction_registry":False, "all_cost_states_2019_to_actual_capyear_end_certified":False, "COVID_adjusted_next_capyear_boundary":None, "whole_hardcap_pass":False},
        "upstream_GSW_L2_objects_changed":False, "new_source_guessed_actual_money":False,
        "actual_registration_certified":False, "actual_medical_certified":False,
        "whole_financial_pass":False, "new_financial_selection":False,
        "whole_legal_pass":False, "new_destination_selected":False,
        "season_selected":False, "manuscript_allowed":False,
        "tools":{"Antigravity":"NOT_RUN_FOR_THIS_PACKET", "NotebookLM":"NOT_RUN_FOR_THIS_PACKET", "Claude":"NOT_RUN_FOR_THIS_PACKET", "independent_review":"PENDING"},
    }


def validate(d):
    if d != build():
        raise ValueError("original-source/current-rule reconstruction mismatch")
    n = d["numeric_dual_matching_witness"]
    if n["gsw_min_matching_slack"] < 0 or n["min_min_matching_slack"] < 0 or n["gsw_trade_apron_delta_upper_if_other_costs_preserved"] > 0:
        raise ValueError("declared domain violates sufficient bound")
    return {"gsw_min_matching_slack":n["gsw_min_matching_slack"], "min_min_matching_slack":n["min_min_matching_slack"], "conditional_gsw_apron_delta_upper":n["gsw_trade_apron_delta_upper_if_other_costs_preserved"], "whole_hardcap_pass":False, "candidate_selected":False}


def markdown(d):
    return """# GSW G1 날짜별 matching·하드캡 범위 검문

**G1 미선택 후보 / 양팀 공개입력 범위 matching 증인 / 전체 하드캡 HOLD / ROOT_REVIEW_PENDING**.
[원 후보](../simulation/GSW_HUTCHISON_2018_2021_OPERATING_CANDIDATES.md), [재현 입력](GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json), [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md).

## 새 원자료와 원계약 입력

원Warriors 공식 guide의 2019 S&T/Spellman 영입과2020 Wiggins 완료 사건을 기존 SHA로 연결했다. 구단 guide는 개별 급여 금액을 제시하지 않아 실제 부족한 원계약 숫자만 공개 작성자의 자체 표에서 회수했다. [Wiggins](https://www.salaryswish.com/players/andrew-wiggins) 2019–20 nominal27,504,630, [Russell](https://www.salaryswish.com/players/dangelo-russell)27,285,000, [Spellman](https://www.salaryswish.com/players/omari-spellman)1,897,800이다. 세 표의 해당시즌 likely/unlikely는0이며 이 공개 계약군을 보존하는 후보 범위다. 현대 선수 상태·후대 커리어·league private memo 인증은 가져오지 않았다.

SalarySwish 거래요약의 원Evans0/signingrights 표시는 전체 급여 증인으로 채택하지 않았다. 각 계약표를 따로 읽었으며 실제 Evans/Chicago22 Hutchison 금액의 대체복사0이다. ESPN salary 본문 요청은403으로 실패하여 근거0이다. 새 원자료는 계약표3+cap표1 rawHTML이며 원문/SHA/추출방식은 JSON에 있다.

## 표 정밀도와 전범위

[NBA2018 표](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) #28 두번째시즌 표시는1,604.9($000s)다. 이를 정확원장 값이나 새 계약%로 고정하지 않고, 그 공개 magnitude보다 훨씬 넓은 scale **$1m–$2m** 외부입력 envelope로 계산했다. 모든80–120%와 VIII1(d)의 current-year tradebonus 상한을 포함해 H outgoing하한800,000 / incoming salary+unlikely상한2,400,000이다. 향후 옵션으로 bonus기초가 늘어도 이번 current120% 상한을 넘을 수 없다. 정확H salary·%·bonus·옵션은null이다.

[2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF64–65 II7(f)에 따라 Russell의 현재 bonus양수여유는 max(0,max(25%cap,105%prior)-current)=0이다. Wiggins도 prior25,467,250×105%=26,740,612.5와25%cap27,285,000보다 current27,504,630이 커서 bonus양수여유0이다. 기존8% 인상 급여를 줄이거나 bonus가 없다는 비공개 부재증명을 요구한 것이 아니다. Spellman은 이미2019-07-08 최초 계약양도를 거쳤으므로 XXIV2(a)에 따른 원contract bonus를 다시 지급하는 가정을 넣지 않는다. VII3(b)로 current protectedyear를 건너뛰어 미래에만 bonus를 밀어놓을 수도 없다.

## 양팀 동시 매칭 증인

VII6(j)의125%+100,000은 납세/비납세/아래cap 구간 모두에서 사용할 수 있는 충분한 한도다. GSW는 Russell+Spellman+Hutchison을 동시 aggregate하며2개월 제한은 이미 경과했다. July7/8부터February6까지214/213일이다. S&T 최초거래의 BKN BYC를 이번GSW outgoing에 다시 적용하지 않는다. January10 이후 current base는 matching에서 전액 보호로 계산된다.

| 팀 | outgoing 하한/고정 | incoming 상한 | 충분 한도 | 최소 여유 |
|---|---:|---:|---:|---:|
|GSW|29,982,800|27,504,630|37,578,500|**10,073,870**|
|MIN|27,504,630|31,582,800|34,480,787.5|**2,897,987.5**|

이것은 선언된 공개 보존 계약군·넓은 신인scale입력에서의 모든 허용H%/bonus 매칭 증인이다. 실제 Minnesota 가치평가/수락·거래 전체·H 행선지·정확 계약을 선택하거나 인증한 것은 아니다. bonus면제 선택q0이며 새 금융 선택0이다. 초과 extension의6개월 제한과 일반 renegotiation eligibility를 구분했고 실제 후속 extension은null이다.

## 하드캡에서 실제 닫히는 것과 남는 것

VII8(e)와6(m)(3)의 apron은 원2019-07-07 S&T 이후 해당capyear의 모든 상태에 적용된다. 공개 cap표의2019 apron은138,928,000이다. **B(t)=H를 제외한 모든 apron-adjusted 비용**으로 두면 원G1이전 전체범위 충분조건은 B(t)≤136,528,000이다. A-G 조정·deadcost·incomingbonus·원거래 중간상태가 B(t)에 포함되어야 한다.

G1 원자거래 자체는 다른 비용을 보존하고 이전상태가 적법하다면 **apron delta≤−2,478,170**이다. 이 거래는 새로운 하드캡 초과를 만들지 않는다. 원Evans의 급여나 선수 수락을 이식하는 증명이 아니다. 이전모든B(t)의 실제 공개합계/구간은 아직없고, 거래후 다른 서명/방출/10일계약과COVID변경capyear말일까지 전체 비용도 미인증이다. 따라서 이 국소 비증가 관계로 whole hardcap을PASS시키지 않는다. annualcashlimit/지급 tradebonus cash도 별도 미인증이다.

다음 입력은 반복된 새 private receipt 요구가 아니라, guide가 보여준 유한 사건의 **GSW 나머지 비용구성·보호/성과 상단·날짜별 A-G 조정표**다. 각 후보의 수락·정확 자산 선택은 여전히 별도다. 현재 두GSW L2의8명·240분 객체 변경0이다.

재현: `python tools/build_gsw_g1_matching_hardcap_scope.py --check`.
상위 원후보를 source까지 전재구성 검문한 뒤 새 숫자를 계산한다. Antigravity/NotebookLM/Claude 이번범위NOT_RUN·독립PENDING이다. 중앙·원장·staging0.

## 7행 진행표 — 작성 시점 한정 복구

|번호|큰 묶음|현황|
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago2020–21|법적11/12·F4/5·A0/3·K0/4; 전체시즌 미완|
|3|2021–23 거래·계약|승인 방향 반영·정확 실행 미완|
|4|장기 커리어|선행 시즌 확정 대기|
|5|결말·전체 구조|골격 보존·전체 회차기능표 미완|
|6|집필 규격·Context Pack|E1/E2 기능2·A01잔여34·전체780 중 미배정778·실제Pack0|
|7|통합·독립·작가 승인|전체 게이트 미완|

**미완료 큰 묶음6 / v0.30 PARTIAL / 설계·원고 CLOSED / 원고0.** 이번 양팀 수식은 전체 금융/등록/정본 선택 완료가 아니다.
"""


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    d=build()
    result=validate(d)
    if a.self_test:
        changes=[("select_G1",lambda x:x.update(candidate_selected=True)),("incoming_bonus_doublecount_removed",lambda x:x["numeric_dual_matching_witness"].update(min_incoming_upper=29182800)),("matching_sign_flip",lambda x:x["numeric_dual_matching_witness"].update(min_min_matching_slack=-2897987.5)),("hardcap_delta_to_whole_pass",lambda x:x["hardcap_scope"].update(whole_hardcap_pass=True)),("same_sum_contract_change",lambda x:(x["observed_original_contract_inputs"]["RUSSELL"].update(cap_hit=27285100),x["observed_original_contract_inputs"]["SPELLMAN"].update(cap_hit=1897700))), ("Hutchison_exact120_selection",lambda x:x["preserved_family"].update(new_Hutchison_salary_percentage_selected=1.2))]
        for name,change in changes:
            bad=deepcopy(d)
            change(bad)
            try:
                validate(bad)
            except ValueError:
                continue
            raise ValueError("mutation falsely accepted:"+name)
        result["negative_rejected"]=[name for name,_ in changes]
    if a.check:
        validate(load(str(OUT.relative_to(ROOT)).replace("\\","/")))
        if normalized(MD)!=markdown(d):raise ValueError("MD stale")
    else:
        OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
        MD.write_text(markdown(d),encoding="utf-8",newline="\n")
    print(json.dumps({"status":d["status"],**result},ensure_ascii=False))


if __name__=="__main__":main()
