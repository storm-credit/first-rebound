"""Coby's 2019-scale ordinary QO function; no season branch or signing selection."""
from __future__ import annotations
import argparse, hashlib, json, re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
import fitz
import build_chicago_2022_rookie_rfa_qo_family as pure

ROOT=Path(__file__).resolve().parents[1]
SELF='tools/build_coby_2023_ordinary_qo_function.py'
OUT='research/COBY_2023_ORDINARY_QO_FUNCTION_2026_10_07.json'
MD=OUT[:-5]+'.md'
PRIMARY='research/COBY_2023_QO_PRIMARY_INPUT_2026_10_07.json'
PINS={PRIMARY:'ee2c866fb0a098c1d09f43f2288b9df27f0d20db2c4630e99353fba95612eb2e','tools/build_chicago_2022_rookie_rfa_qo_family.py':'8ec5d15b04069d300f5b7bd5a70459f757c23a297ca966145045689d66a8cc2b'}
FIXED_ROWS={7:(4422600,4643900,4864800,270,341),15:(2737600,2874500,3011400,533,398)}

def need(value,message):
    if not value:raise ValueError(message)
def text(p):return p.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def sha(p):return hashlib.sha256(text(p).encode()).hexdigest()
def read(root,p):return json.loads(text(root/p))
def checked_primary(root):
    for p,h in PINS.items():need(sha(root/p)==h,'Pinned input changed: '+p)
    d=read(root,PRIMARY)
    need(d==json.loads(text(root/PRIMARY)),'Returned primary differs from physical source')
    need(d['facts']['canon_Coby_2019_CHI_pick']==7,'Coby original pick changed')
    src=d['facts']['NBA_authored_scale_mirror'];cache=Path(src['cache_path'])
    need(hashlib.sha256(cache.read_bytes()).hexdigest()==src['raw_sha256'],'2019 scale raw changed')
    with fitz.open(cache) as pdf:page=pdf[src['table_page']-1].get_text()
    need(hashlib.sha256(page.replace('\r\n','\n').replace('\r','\n').encode()).hexdigest()==src['table_normalized_fitz_sha256'],'2019 scale page changed')
    pattern=r'(?m)^\s*(\d+)\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+([\d,]+\.\d)\s+(\d+\.\d)%\s+(\d+\.\d)%'
    allrows={int(k):tuple([int(Decimal(v.replace(',',''))*1000)for v in(a,b,c)]+[int(Decimal(f)*10),int(Decimal(q)*10)])for k,a,b,c,f,q in re.findall(pattern,page)}
    need(set(allrows)==set(range(1,31)),'2019 scale missing picks')
    rows={k:allrows[k]for k in FIXED_ROWS}
    need(rows==FIXED_ROWS and rows=={int(k):tuple(v)for k,v in d['facts']['relevant_rows'].items()},'2019 named scale meaning differs')
    cba=d['facts']['2017_CBA'];p=Path(cba['cache_path'])
    need(hashlib.sha256(p.read_bytes()).hexdigest()==cba['raw_sha256'],'2017 CBA raw changed')
    with fitz.open(p)as pdf:
        for n,h in cba['normalized_fitz_page_sha256'].items():
            body=pdf[int(n)-1].get_text().replace('\r\n','\n').replace('\r','\n')
            need(hashlib.sha256(body.encode()).hexdigest()==h,'CBA page changed: '+n)
    return d,rows

def ordinary_qo(third_year_components,starter_criteria_met,root=ROOT):
    need(type(starter_criteria_met)is bool,'Explicit starter branch required')
    _,rows=checked_primary(root)
    return pure.result(rows[7],third_year_components,starter_criteria_met,rows)

def starter_test(*,third_year_starts,third_year_credited_minutes,fourth_year_starts,fourth_year_credited_minutes):
    # Fraction allows credited partial minutes; bool and nonfinite/negative inputs are rejected.
    values=(third_year_starts,third_year_credited_minutes,fourth_year_starts,fourth_year_credited_minutes)
    need(all(type(v)in(int,Fraction) and v>=0 for v in values),'Nonnegative exact credited statistics required')
    need(type(third_year_starts)is int and type(fourth_year_starts)is int,'Starts must be integer')
    need(third_year_starts<=82 and fourth_year_starts<=82,'Starts exceed the season domain')
    return fourth_year_starts>=41 or fourth_year_credited_minutes>=2000 or third_year_starts+fourth_year_starts>=82 or third_year_credited_minutes+fourth_year_credited_minutes>=4000

def build(root=ROOT):
    d,rows=checked_primary(root);row=rows[7];s=row[2]
    corners=[('BASE80',(Fraction(4*s,5),0,0)),('BASE120',(Fraction(6*s,5),0,0)),('BASE80_LIKELY40',(Fraction(4*s,5),Fraction(2*s,5),0)),('BASE80_UNLIKELY40',(Fraction(4*s,5),0,Fraction(2*s,5)))]
    witnesses=[dict(starter=st,corner=name,third_year_components=[pure.rat(Fraction(v))for v in vec],ordinary_QO=pure.result(row,vec,st,rows))for st in(False,True)for name,vec in corners]
    own=pure.own_upper(row);_,anchor=pure.anchor(rows[15])
    need(pure.anchor(row)[0]==Fraction(6213821202,625)and pure.anchor(rows[15])[0]==Fraction(48403752957,6250),'Reference arithmetic differs')
    return dict(id='COBY_2023_ORDINARY_QO_FUNCTION_2026_10_07',status='DEFINED_TWO_BRANCH_COMPONENT_FUNCTION_NOT_EXECUTED',baseline_main='5d8b057f057f7611531868296035d20b9b449729',source_sha256={**PINS,SELF:sha(root/SELF)},primary_support=d['facts'],
        policy=dict(player='Coby White',team='CHI',original_salary_cap_year='2019-20',original_pick=7,ordinary_issue_deadline='2023-06-29',applicable_issue_law='2017_CBA',acceptance_open_through='2023-10-01',original_third_year_component_family='80pct base floor; nonnegative likely/unlikely; total<=120pct original2019scale; original terms retained',fourth_year_components='each third-year component times1.270',own_QO_components='each fourth-year component times1.341',nonstarter='Lesser legal whole offer: own components or original2019 rank15 at120pct base only; no elementwise bonus cancellation',starter='Own pick7 components; rank9 rule for later picks does not apply',QO_is_FAhold=False,original_2018_or_actual_2023_salary_copied=False),
        rational_function_corner_witnesses=witnesses,continuous_family_coverage='Exact scalar multiplication across the admitted three-component simplex; corners display boundary witnesses. Lesser whole-package alternatives retained.',
        conservative_integer_USD_cost_screens=dict(starter_own=own,nonstarter=min(own,anchor),all_branches=max(own,min(own,anchor)),not_actual_NBA_rounding_or_contract_cents=True),
        credited_statistics_interface=dict(regular_seasons=['2021-22','2022-23'],starter='GS4>=41 OR MIN4>=2000 OR GS3+GS4>=82 OR MIN3+MIN4>=4000',regulation_only_minutes_are_not_full_credited_totals=True,first_unordered_lineup_is_not_official_game_start=True,postseason_not_counted=True,alternate_credited_totals=None),
        handoff=['Join two chosen regular-season credited totals, including any separately chosen OT and explicit starts. Existing regulation results alone do not certify CBA statistics.','Issue valid fictional ordinary one-year fully protected base QO byJune29 under2017law, retain original bonus/rights; issuance is not acceptance.','Join offer/acceptance or Bird re-signing and normal/apron/FA/QO/FRN costs in named FY23 roster; July1 newCBA does not retroactively alter June29.'],
        certification=dict(starter_branch_selected=False,QO_issued=False,player_acceptance_selected=False,exact_contract_or_rounding_certified=False,independent_review_completed=False,whole_FY23_or_macro3=False,new_author_lock=False,manuscript_allowed=False,freeze='v0.30 PARTIAL',design_gate='CLOSED'))

def markdown(v):
    q=v['conservative_integer_USD_cost_screens']
    return '\n'.join(['# Coby2023 ordinary QO의 실행 가능한 성분 함수','','[기존 원 입력](COBY_2023_QO_PRIMARY_INPUT_2026_10_07.md)의 NBA 작성2019 표·2017 CBA 원cache를 직접 읽고, 이미 검문된2017 순수 성분 계산만 재사용했다. 다른 선수 계약 생성기·이전 전체 장부를 재실행하지 않았다.2018 표를 Coby에게 복사하지 않는다.','','사실: Chicago 원2019순위7. 추론: third→fourth 각성분×1.270, fourth→QO 각성분×1.341. starter면 자기7순위 성분; nonstarter면 자기 성분 offer와 원2019순위15의120% base-only offer 중 적법한 작은 패키지다. bonus를 항목별로 삭제하거나7순위에9순위 규칙을 적용하지 않는다.','',f"법적 가족의 보수 정수달러 비용 상한: starter {q['starter_own']:,}; nonstarter {q['nonstarter']:,}. 연속80–120% 성분 가족을 보존하며8개 모서리는 표시 증인이다. 이는 실제 UPC/법정센트/리그반올림 인증이 아니다.",'','두 정규시즌의 credited starts/minutes를 받는 함수가 준비됐다. 출전 시작은 unordered 첫블록이나 active명단만으로 확정하지 않으며, 정규시간만의 분은 선택되지 않은 OT를 포함한 공식 총분이 아니다. postseason은 제외한다. 미래 통계로 branch를 미리 선택하지 않았다.','','발행은2017법의2023June29 기한, 1년/기본급100%보호·유효 팀서명 전달·Oct1까지 수락 가능 조건을 갖는다. July1 새 CBA와 구분하며 FAhold/QO/FRN은 서로 다르다. 이 함수 정의만으로 발행·선수수락·가격·전체FY23·새 작가확정을 선택하지 않았다. 후속 실제 장부에서 소비한다.','','v0.30 PARTIAL·설계/원고 CLOSED·원고0.',''])

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();v=build()
    if a.write:(ROOT/OUT).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/MD).write_text(markdown(v),encoding='utf-8')
    if a.check:need(read(ROOT,OUT)==v,'Saved function changed');need(text(ROOT/MD)==markdown(v),'Saved explanation changed')
    print(json.dumps(v['conservative_integer_USD_cost_screens']))
if __name__=='__main__':main()
