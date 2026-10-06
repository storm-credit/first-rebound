"""Public GSW dated apron cost intervals and finite residual thresholds; G1 unselected."""
from pathlib import Path
from copy import deepcopy
import argparse, hashlib, json, re
import fitz
from bs4 import BeautifulSoup
import build_gsw_g1_matching_hardcap_scope as matching
ROOT = Path(__file__).resolve().parents[1]
BASELINE = "47e5c806b8fdfe3f85a1bffdc629037a220d3863"
SELF = "tools/build_gsw_g1_remaining_apron_costs.py"
OUT = ROOT / "research/GSW_G1_REMAINING_APRON_COSTS_2026_10_07.json"
MD = OUT.with_suffix(".md")
CACHE = Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-gsw-apron-cost-20261007")
PINS = {'stephen-curry': '0f66e365b031f9e2721849477b1c1439193387e087bb45d70b2345ba4ff40239', 'draymond-green': 'eab1f1ab48037c6390dfdcc0182bf464647e6a9d6e428ec3f01b6cd8813143e0', 'klay-thompson': '69b9edd9b333c9c1b603174db8debf91a88f42cf362373d73f419b2a36715915', 'kevon-looney': 'd9ad5791c089578c52cb4165bfe3c8c5b9e9123605a06d7453a2cbdd8046cffe', 'shaun-livingston': 'cbb20eacbd61040a8db67232a093613f3305a4a13055fc1fb3f1eb8d6174a66b', 'willie-cauley-stein': '533ed9fad32fe56553c57fdf40273651218803c76b25fa0d203c18386e376fe3', 'alec-burks': '88a3cc3b11c15e90f5cad02185e63dbfd537fe748d25a80bd1a06f450327bbbf', 'glenn-robinsoniii': 'a4dd70f4732078d4dc645d28b8826183c2fcdf9408b7006e34d0c2847e876e50', 'eric-paschall': '78b6d048ba86735f2ab4bb1f928d2d4dc21d029e0d0d92c5c327ffcc824d1f4b', 'jordan-poole': '1d02175c65378b288780ca21183de56e23889c2f53a875084f32baf9830fc1fc', 'alen-smailagic': 'df89b672eff0fe29b517fafc37b0a1d0bce7d919a7e0750ab826696bb640503c', 'damion-lee': 'b50ca7844ccc4233b5f3c6ee0d9b0e5ce1b5406d10eb10992418fb3e59db7625', 'marquese-chriss': 'a9aa849dc80f7ddc054e3e8b43b0d147d8318f3733c55760dc165a5f8a8c42f3', 'alfonzo-mckinnie': 'f03154192589e8a55c2c3fc87d216cd07abe98dcb6b4fc1cd21ab0642915b402'}
UPSTREAM_PINS = {'research/GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.json': '4cbff2683a696271321637564b61c2563e17eb10757e1ffeb6691876a28bbf7e', 'tools/build_gsw_g1_matching_hardcap_scope.py': '62f90e5c66ac9f3462762399ccd969ef0e7484cc7120a62fb9411ecab268fb90'}
FAILURE_PINS = {"glenn-robinson.html":"24413809092f83d4adce46cd308d216b021a945c43998291aa4ca3c8e09e15b5","julian-washburn.html":"4d92300a3e8423fb040ef83dbbab92f9b77648d3e54080b013a884eb3175c939","WASHBURN_OFFICIAL.html":"b4794b0a58ac1af2647a04170821001f04e1351b3df9e3a32c45c5654a5d4f0c"}
CBA_PAGES = [27,28,31,200,202,203,216,240,241,254,286,289,303,313]
TABLE_INDEX = {"glenn-robinsoniii":1,"damion-lee":1,"marquese-chriss":1}

def norm(p): return p.read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n")
def sha(p): return hashlib.sha256(norm(p).encode()).hexdigest()
def money(s):
    m=re.search(r"\$([\d,]+)",s)
    if not m: raise ValueError("money cell missing")
    return int(m.group(1).replace(",",""))
def rows(raw):
    s=BeautifulSoup(raw,"html.parser"); ans=[]
    for t in s.find_all("table"):
        rs=[[c.get_text(" ",strip=True) for c in tr.find_all(["td","th"])] for tr in t.find_all("tr")]
        if rs and rs[0][:4]==["Season","Option","Option Used","Cap Hit"]:
            ans.extend(row for row in rs[1:] if row and row[0].startswith("2019-20"))
    return ans

def build():
    for f,h in UPSTREAM_PINS.items():
        if sha(ROOT/f)!=h: raise ValueError("reviewed upstream changed: "+f)
    u=json.loads(norm(ROOT/next(iter(UPSTREAM_PINS))))
    matching.validate(u) # includes full original operating reconstruction
    if u["candidate_selected"] or u["whole_financial_pass"]: raise ValueError("candidate authority changed")
    source, observed={},{}
    failed_raw={}
    for name,h in FAILURE_PINS.items():
        f=CACHE/name;b=f.read_bytes()
        if hashlib.sha256(b).hexdigest()!=h:raise ValueError("failed cache changed: "+name)
        if name!="WASHBURN_OFFICIAL.html" and rows(b):raise ValueError("missing-contract failure changed")
        failed_raw[name]={"cache_path":str(f),"raw_sha256":h,"bytes":len(b),"adopted_as_contract_evidence":False}
    for slug,h in PINS.items():
        p=CACHE/(slug+".html") if slug!="alfonzo-mckinnie" else Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-cleveland-cost-2026-10-06/alfonzo-mckinnie.html")
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=h: raise ValueError("raw contract changed: "+slug)
        rr=rows(raw); i=TABLE_INDEX.get(slug,0)
        row=rr[i]
        if len(row)<8: raise ValueError("contract schema missing")
        observed[slug]={"cap_hit":money(row[3]),"base":money(row[4]),"protected":money(row[5]),"likely":money(row[6]),"unlikely":money(row[7]),"source_table_index_among_2019_rows":i,"source_row":row,"all_2019_contract_rows":rr}
        txt=BeautifulSoup(raw,"html.parser").get_text(" ",strip=True)
        source[slug]={"url":"https://www.salaryswish.com/players/"+slug,"cache_path":str(p),"raw_sha256":h,"bytes":len(raw),"text_sha256":hashlib.sha256(txt.encode()).hexdigest(),"extraction":"BeautifulSoup html.parser get_text(' ',strip=True), UTF8","authority_type":"PUBLISHER_OWN_COMPILED_PUBLIC_CONTRACT_INPUT_NOT_LEAGUE_MEMO","collection_kind":"REUSED_PRIOR_CACHE" if slug=="alfonzo-mckinnie" else "DIRECT_HTTP200_BODY_COLLECTED_2026_10_07","origin_current_season_status_used":False}
    if any(v["likely"] or v["unlikely"] for v in observed.values()): raise ValueError("reported incentive input changed")
    o=u["observed_original_contract_inputs"]
    cap=lambda s:observed[s]["cap_hit"]
    floor=cap("alec-burks")
    if floor!=1620564 or cap("glenn-robinsoniii")!=floor: raise ValueError("one-year minimum cost source changed")
    # Draft rookies signed while exclusive rights remain are not Free Agents under I1(cc),(ggg).
    # Therefore VII12(f)(2)(ii) FA floor does not automatically uplift these second-round salaries.
    if cap("eric-paschall")!=898310 or cap("alen-smailagic")!=898310: raise ValueError("draft rookie inputs changed")
    living=observed["shaun-livingston"]
    soup=BeautifulSoup((CACHE/"shaun-livingston.html").read_bytes(),"html.parser")
    deadtables=[t for t in soup.find_all("table") if t.get_text(" ",strip=True).startswith("SEASON BASE SALARY CAP HIT") and "2019-20" in t.get_text()]
    if len(deadtables)!=1: raise ValueError("Livingston dead source ambiguous")
    dr=[[c.get_text(" ",strip=True) for c in tr.find_all(["td","th"])] for tr in deadtables[0].find_all("tr")]
    dead=money(next(row for row in dr if row and row[0]=="2019-20")[2])
    if dead!=666667: raise ValueError("Livingston dated dead row changed")
    july=[
        ("Stephen Curry",cap("stephen-curry"),cap("stephen-curry"),"existing contract"),
        ("Draymond Green",cap("draymond-green"),cap("draymond-green"),"existing contract; later extension does not retroactively replace current year"),
        ("D'Angelo Russell",o["RUSSELL"]["cap_hit"],o["RUSSELL"]["cap_hit"],"completed original July7 S&T preserved"),
        ("Omari Spellman",o["SPELLMAN"]["cap_hit"],o["SPELLMAN"]["cap_hit"],"completed original July8 assignment preserved"),
        ("Willie Cauley-Stein",cap("willie-cauley-stein"),cap("willie-cauley-stein"),"official guide July8 contract"),
        ("Alfonzo McKinnie",cap("alfonzo-mckinnie"),cap("alfonzo-mckinnie"),"live standard salary; zero protection does not erase active salary"),
        ("Shaun Livingston",dead,living["cap_hit"],"guide waiverJuly10 vs SS contract waiverJuly8/dead-tableJuly10: full active maximum preserves disagreement"),
        ("Jordan Poole",0,cap("jordan-poole"),"guideJuly11 vs SSJuly4; unsigned required tender or early contract up to preserved nominal salary"),
        ("Eric Paschall",0,cap("eric-paschall"),"guideJuly11 vs SSJuly7; exclusive second-round draft right, not automatic FA floor"),
        ("Alen Smailagic",0,cap("alen-smailagic"),"guideJuly11 vs SSJuly8; exclusive second-round draft right, not automatic FA floor"),
        ("Glenn Robinson III",0,cap("glenn-robinsoniii"),"guideJuly10 vs SSJuly8; veteran minimum team Salary, not full player cash")]
    feb=[(name,v,v,why) for name,v,why in [
        ("Stephen Curry",cap("stephen-curry"),"existing contract"),
        ("Draymond Green",cap("draymond-green"),"original 2015 term still current"),
        ("Klay Thompson",cap("klay-thompson"),"signedJuly10; inactive player still counts"),
        ("Kevon Looney",cap("kevon-looney"),"public nominal row; not league memo or whole bonus certificate"),
        ("D'Angelo Russell",o["RUSSELL"]["cap_hit"],"G1 outgoing"),
        ("Omari Spellman",o["SPELLMAN"]["cap_hit"],"G1 outgoing"),
        ("Jordan Poole",cap("jordan-poole"),"rookie scale contract"),
        ("Eric Paschall",cap("eric-paschall"),"Draft Rookie exclusive-right contract, FA floor not applicable"),
        ("Alen Smailagic",cap("alen-smailagic"),"Draft Rookie exclusive-right contract, FA floor not applicable"),
        ("Damion Lee",cap("damion-lee"),"Jan15 standard contract after original TW; observed prorated nominal row"),
        ("Alec Burks",cap("alec-burks"),"VII3(f) reimbursed minimum Salary; source basecash2320044 distinct"),
        ("Glenn Robinson III",cap("glenn-robinsoniii"),"VII3(f) reimbursed minimum Salary; source basecash1882867 distinct"),
        ("Shaun Livingston",dead,"original declared stretch dead row, no candidate new stretch choice")]]
    # Original zero-protected Chriss waivedJan7; full prewaiver cap charge is a conservative upper.
    # Do not guess exact earned fraction, setoff or waived after-tax subtotal.
    feb.append(("Marquese Chriss original standard waived Jan7",0,cap("marquese-chriss"),"paid/payable current charge retained; source unprotected; no blind zero dead charge"))
    def vector(items): return [{"name":n,"lower":lo,"upper":hi,"basis":why} for n,lo,hi,why in items]
    jlo,jhi=sum(x[1] for x in july),sum(x[2] for x in july)
    flo,fhi=sum(x[1] for x in feb),sum(x[2] for x in feb)
    H=[u["numeric_dual_matching_witness"]["h_pre_salary_lower"],u["numeric_dual_matching_witness"]["h_post_salary_plus_unlikely_upper"]]
    A=o["CAP"]["apron"]
    R,S,W=[o[k]["cap_hit"] for k in ["RUSSELL","SPELLMAN","WIGGINS"]]
    PHI=cap("alec-burks")+cap("glenn-robinsoniii")
    states=[]
    for label,blo,bhi,h,removed in [
        ("2019-07-08 after named guide transactions",jlo,jhi,H,[]),
        ("2020-02-06 before both named trades",flo,fhi,H,[]),
        ("2020-02-06 after G1 before PHI",flo-R-S+W,fhi-R-S+W,[0,0],["Russell","Spellman","Hutchison"]),
        ("2020-02-06 after PHI before G1",flo-PHI,fhi-PHI,H,["Burks","RobinsonIII"]),
        ("2020-02-06 after both named trades",flo-R-S+W-PHI,fhi-R-S+W-PHI,[0,0],["Russell","Spellman","Hutchison","Burks","RobinsonIII"])]:
        states.append({"state":label,"remaining_B_range":[blo,bhi],"H_apron_range":h,"known_plus_H_range":[blo+h[0],bhi+h[1]],"nonnegative_residual_X_max_for_sufficient_whole_declared_state":A-bhi-h[1],"removed_from_GSW_current_salary":removed,"formula":"B_public_upper + H_upper + X_state <= apron; X_state bound must be supported, not silently zero"})
    cba=Path(u["existing_cba_direct_read"]["cache_path"]) if "cache_path" in u["existing_cba_direct_read"] else Path("C:/Users/Storm Credit/AppData/Local/Temp/fr-2017-cba.pdf")
    b=cba.read_bytes();doc=fitz.open(cba)
    if hashlib.sha256(b).hexdigest()!=u["existing_cba_direct_read"]["raw_sha256"]:raise ValueError("CBA changed")
    guide=Path("C:/Users/Storm Credit/AppData/Local/Temp/first-rebound-gsw-hutchison-20261007/GSW_2324.pdf")
    if hashlib.sha256(guide.read_bytes()).hexdigest()!="1f229c48c478e78079a7c47ba1b9e0baa69f7867a1cfa8ff9c8185bca12dfd45":raise ValueError("official guide changed")
    gd=fitz.open(guide)
    return {"status":"DATED_PUBLIC_COST_INTERVALS_VALID_RESIDUAL_THRESHOLDS_G1_UNSELECTED_WHOLE_HARDCAP_HOLD", "baseline_main":BASELINE,"candidate":"G1","candidate_selected":False,
        "source_sha256":{**UPSTREAM_PINS,SELF:sha(ROOT/SELF)},"salary_public_sources":source,"historical_nominal_rows":observed,
        "legal_source":{"url":u["existing_cba_direct_read"]["url"],"cache_path":str(cba),"raw_sha256":hashlib.sha256(b).hexdigest(),"pdf_pages":CBA_PAGES,"page_text_normalized_lf_sha256":{str(n):hashlib.sha256(doc[n-1].get_text().replace("\r\n","\n").replace("\r","\n").encode()).hexdigest() for n in CBA_PAGES}},
        "official_date_source":{"url":"https://cdn.nba.com/teams/uploads/sites/1610612744/2023/12/2324-gsw-media-guide.pdf","cache_path":str(guide),"raw_sha256":hashlib.sha256(guide.read_bytes()).hexdigest(),"pdf_pages":[433],"page_text_normalized_lf_sha256":hashlib.sha256(gd[432].get_text().replace("\r\n","\n").replace("\r","\n").encode()).hexdigest()},
        "apron":A,"H_public_scale_envelope":u["scale_domain"],"July8_components_excluding_H":vector(july),"February6_pre_components_excluding_H":vector(feb),"dated_cost_states":states,
        "rules":{"A":"all likely/unlikely performance must count; table zero is source-family input, not complete unknown contract certification","B":"I1(cc),(ggg) excludes exclusive Draft Rookie from FA; VII12(f)(2)(ii) FA0/1YOS floor must not be applied to all rookies indiscriminately","C":"VII4(a)(1)(iii) grievance potential is residual, not unobserved zero","D":"UFA cap holds excluded including unsigned Klay/Looney July8; outstanding Cook/Bell RFA qualifying/first-refusal costs remain symbolic if not positively extinguished","E":"Poole unsigned tender and live contract mutually exclusive; range includes greater tender/current preserved salary; no double-add of cap hold and tender","F":"unused exceptions including Iggy TPE excluded from apron","G":"incomplete-roster holds excluded; does not erase actual standard salary","dead":"VII4(a)(1)(i) terminated paid/payable salary remains; original Livingston source dead666667 preserved, no new stretch election; Chriss upper includes full prewaiver1620564","minimum":"VII3(f) uses nonreimbursed team Salary rather than player cash; no apply to multi-year contract by analogy","TW":"VII4(j) excludes current TW salary; neither a later conversion nor future Feb7 Chriss/Bowman/JTA standard contract is imported into Feb6"},
        "residuals_to_close":{"2019-07-08":["outstanding Cook/Bell qualifying or first-refusal offers if still live", "any July8 acquired Washburn standard/TW cost not positively typed for this exact state", "any source-omitted bonus/grievance/camp protected or paid/payable amount"],"2020-02-06":["unlisted camp/terminated paid-payable contracts e.g. Marble/Harrison/JTA/Pippen/Cunningham/Zeisloft if any", "source-unlisted performance/signing/trade compensation and grievance adjustments", "public Looney15m total headline versus nominal table14464287 gap not silently assigned to any year"],"X_zero_selected":False,"X_actual_amount":None,"X_global_unchanged_across_trade_orders_certified":False,"exit":"A supported public upper bound on named residual or a complete permitted family witness below the computed threshold suffices; no private-ledger receipt is a new mandatory requirement"},
        "scope":{"two_dated_state_public_family_arithmetic":True,"all_intervening_capyear_states":False,"exact_operation_clocks":None,"G1_dual_matching_reopened":False,"actual_original_Evans_money_used":False,"actual_Chicago22_Hutchison_money_used":False,"new_financial_choice":False,"new_destination_selected":False,"actual_contract_or_acceptance_certificate":False,"full_registration_cleared":False,"whole_hardcap_pass":False,"whole_legal_pass":False,"REGISTER_promoted":False,"GSW_L2_objects_changed":False,"independent_review_completed":False,"Antigravity":"NOT_RUN","NotebookLM":"NOT_RUN","Claude":"NOT_RUN","manuscript_count":0},
        "source_failure_control":{"raw_failures":failed_raw,"glenn-robinson_wrong_slug":"HTTP200 Player not found; original cached body not adopted","julian-washburn_SS":"HTTP200 no 2019 contract row; no modern zero-YOS inference","WASHBURN_OFFICIAL_http":"HTTP403 cached461bytes, sha b4794b0a58ac1af2647a04170821001f04e1351b3df9e3a32c45c5654a5d4f0c; no cached official body claim; web first-party release observed independently but not used as exact currentcharge"},
        "progress_snapshot":{"scope":"PR438 main fixed snapshot, roadmap E6 current when task began","major_groups_remaining":6,"legal_PASS":11,"legal_HOLD":1,"F":"4/5","A":"0/3","K":"0/4","A01_final_functions":6,"A01_unassigned":30,"total_planned_slots":780,"total_unassigned":774,"actual_Context_Pack":0,"freeze":"v0.30 PARTIAL","design_gate":"CLOSED","manuscript_gate":"CLOSED","manuscript_count":0}}

def validate(obj):
    if obj!=build(): raise ValueError("full original source reconstruction differs")
    if obj["candidate_selected"] or obj["scope"]["whole_hardcap_pass"]:raise ValueError("authority escalation")
    return True

def markdown(x):
    out=["# GSW G1 날짜별 나머지 apron 비용 입력", "", "상태: **공개 비용 구간·잔여 임계값 검문 / G1 미선택 / 전체 하드캡 HOLD**. 기준 main `47e5c80` 고정. [현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md), [입력](GSW_G1_REMAINING_APRON_COSTS_2026_10_07.json), [기존 matching 범위](GSW_G1_DATED_MATCHING_AND_HARDCAP_SCOPE_2026_10_07.md).", "", "## 새로 확보한 범위", "", "SalarySwish 자체 계약표 신규13개와 기존 McKinnie 원캐시를 읽고 당시2019–20 행을 유형별로 연결했다. 이는 공개 편집 계약 입력이며 리그 계약원장 인증은 아니다. Looney 표시 기본급4,464,286과 후대/보도15m 총액의 차액을 임의로 해소하지 않는다. 날짜·옵션·보너스가 대체세계 작가확정이 된 것은 아니다.", "", "[2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) I1(cc)/(ggg),VII6(m)(3),12(f)(2)(ii)를 직접 읽었다. 독점협상권이 살아 있는 #41 Paschall/#39 Smailagic은 Free Agent가 아닌 Draft Rookie이므로 자유계약0/1년차의 2년차최저 상향을 일괄 적용하지 않는다. 현재공개금액은898,310씩이다. Burks/GRIII는 일년최저급여 환급 규칙으로 팀Salary1,620,564씩이며 선수 현금2,320,044/1,882,867과 다르다. Chriss는 FA 원계약의 방출 비용을 자동0으로 하지 않고 전체이전cap1,620,564를 상단에 남긴다.", "", "## 실제 비용 구간", "", "B는 Hutchison을 제외한 공개 연결 비용이다. X는 표/날짜 연결만으로 닫히지 않은 명명된 비용 잔여다. X=0이나 실제 계약수락을 선택하지 않았다.", "", "| 날짜·상태 | B 공개 구간 | H 상단 | 충분한 X 상단 |", "|---|---:|---:|---:|"]
    for s in x["dated_cost_states"]:out.append(f'| {s["state"]} | {s["remaining_B_range"][0]:,.0f}–{s["remaining_B_range"][1]:,.0f} | {s["H_apron_range"][1]:,.0f} | {s["nonnegative_residual_X_max_for_sufficient_whole_declared_state"]:,.0f} |')
    out += ["", "7/8은 guide와 공개 계약표의 Poole/Paschall/Smailagic/GRIII 서명 날짜 차이를 양쪽을 덮는0~현재표금액으로 처리한다. Livingston의 표기 waiver7/8과 guide7/10 차이도666,667~7,692,308으로 보존한다. 아직 미서명 Klay/Looney UFA hold는 apron 제외이며 살아 있는 RFA 제안은 X에 남긴다. 두 자료 날짜를 숨겨 동일 실행일로 인증하지 않는다.", "", "2/6는 Wiggins 원자거래와 같은날 PHI Burks/GRIII 거래의 양순서를 따로 계산했다. 정확 당일 접수순서는null이며 미래2/7 표준계약은 끌어오지 않는다. 표의 각 충분조건은 해당 상태의 X 상단이 지원될 때만 유효하고 모든상태X동일/전체시즌 비용을 인증하지 않는다.", "", "## 구체 남은 입력과 실패 제어", "", "7/8의 Cook/Bell 살아 있는 qualifying/first-refusal 제안, Washburn 당시계약유형, 기타 bonus/grievance/보호·지급액을 X로 이름 붙였다. 2/6의 camp/해제 잔여와 Looney 총액차이도 X이며 미확인=0 가정은 없다. 공개 상단 또는 허용 계약family 전체증인으로 각 임계값을 닫으면 충분하고 비공개 영수증의 회수를 영구필수 요건으로 만들지 않는다.", "", "Washburn 공개 계약페이지에는 당시 행이 없고 잘못된 Robinson slug는 Player not found였다. 공식Washburn release 원문 다운로드는403이라 cached본문 인증으로 채택하지 않았다. 현대 선수상태를 과거 계약으로 대입하지 않았다. raw14(신규13+재사용1)/SHA·CBA14쪽·guide433쪽 지문은JSON에 있고 원PDF지문은 불변이다.", "", "G1 선택·정확H계약비율·옵션·거래수락·전체금융/명단/법적PASS·중앙원장 승격·기존L2 변경0. 이 한정 검문에서 Antigravity/NotebookLM/Claude는 NOT_RUN이며 독립 검문은 pending이다.", "", "## 전체7행 진행표 (PR438/E6 입력 시점)", "", "| 번호 | 범위 | 상태 |", "|---|---|---|", "|1|2020 드래프트 연쇄|완료|", "|2|Chicago2020–21|법적11/12·F4/5·A0/3·K0/4, 시즌 미확정|", "|3|2021–23 거래·계약|승인방향 반영, 정확 실행 미완|", "|4|장기 커리어|선행 시즌 종료 대기|", "|5|결말·전체 구조|골격 완료, 전체 기능표 미완|", "|6|집필규격·Context Pack|A01기능6/잔여30, 전체780 중 미배정774, 실제Pack0|", "|7|통합·독립·작가 승인|미완|", "", "미완료 큰묶음 **6** · **v0.30 PARTIAL** · 설계/원고 **CLOSED** · 원고 **0**. 현행로드맵의 이후진전은 이 고정 입력시점 표보다 우선한다.", ""]
    return "\n".join(out)

def self_tests():
    x=build(); labels=[]
    for label,mut in [
      ("same-total donor cost corruption",lambda z:(z["February6_pre_components_excluding_H"][0].update(lower=z["February6_pre_components_excluding_H"][0]["lower"]+1,upper=z["February6_pre_components_excluding_H"][0]["upper"]+1),z["February6_pre_components_excluding_H"][1].update(lower=z["February6_pre_components_excluding_H"][1]["lower"]-1,upper=z["February6_pre_components_excluding_H"][1]["upper"]-1))),
      ("missing residual falsely zero",lambda z:z["residuals_to_close"].update(X_zero_selected=True)),
      ("wrong FA floor on exclusive draft rookie",lambda z:z["historical_nominal_rows"]["eric-paschall"].update(cap_hit=1620564)),
      ("whole authority escalation",lambda z:z["scope"].update(whole_hardcap_pass=True))]:
        y=deepcopy(x);mut(y)
        try:validate(y)
        except ValueError:labels.append(label)
        else:raise AssertionError("corruption accepted: "+label)
    return labels

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");p.add_argument("--self-test",action="store_true");a=p.parse_args()
    x=build()
    if a.self_test:print(json.dumps({"rejected":self_tests()},ensure_ascii=False))
    if a.check:
        validate(json.loads(norm(OUT)))
        if norm(MD)!=markdown(x):raise ValueError("MD stale")
        print("PASS dated costs/source reconstruction/scope")
    else:
        OUT.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");MD.write_text(markdown(x),encoding="utf-8");print("WROTE",OUT.name)
