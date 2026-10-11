"""Build a finite episode allocation recommendation; no final/ACTUAL authority."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='design/THREEPEAT_CURRENT_40_FUNCTION_SCENE_BLUEPRINTS_2026_10_12.json'
SCOPE='control/CURRENT_SELECTED_THREEPEAT_BY_2025_MAIN_STORY_SCOPE_2026_10_09.json'
PI22='simulation/NBA_2021_22_STANDINGS_PLAYIN_AND_2022_RIGHTS.json'
PHI22='simulation/CHICAGO_PHI_2022_FIRST_ROUND.json'
TITLE23='simulation/THREEPEAT_2023_FIRST_TITLE_USED_ROUTE_2026_10_09.json'
SEL23='canon/DELEGATED_THREEPEAT_2023_FIRST_TITLE_USED_ROUTE_SELECTION_2026_10_09.json'
LATE='canon/DELEGATED_THREEPEAT_2024_25_USED_ROUTES_AND_FINAL_COURTS_SELECTION_2026_10_09.json'
EAST='simulation/THREEPEAT_2024_25_SIX_EAST_USED_COURT_JOIN_2026_10_09.json'
LAST='simulation/THREEPEAT_2025_SHARED_FINAL_COURT_AND_LAST_ATTACK_PREPARATION_2026_10_09.json'
REC='design/EARLY_REWARD_B_RECOGNITION_ROSTER_CANDIDATES_2026_10_12.json'
ALLOCATION='design/THREEPEAT_51_EPISODE_DENSITY_ALLOCATION_2026_10_12.json'
BLUEPRINT='design/THREEPEAT_51_PREPARED_EPISODE_BLUEPRINTS_2026_10_12.json'
MD=ALLOCATION.replace('.json','.md')
REVIEW='reviews/THREEPEAT_51_EPISODE_DENSITY_ALLOCATION_2026_10_12_CODEX_CHECK.json'
NLM='reviews/THREEPEAT_51_DENSITY_NOTEBOOKLM_ANALYSIS_2026_10_12.json'
VILL='simulation/LC1_VILLANOVA_2017_2018_USED_ROLE_AND_TITLE_BRIDGE_IMPLEMENTATION_2026_10_09.json'
C01='research/THREEPEAT_C01_PUBLIC_AND_DUTY_USED_CALENDAR_PREPARATION_2026_10_09.json'

# Splits name different existing state transitions, not a quota of scenes.
# title, window, action/choice, newly incurred cost, resulting state
SPLITS={
4:[('떠날 이유를 내 질문으로','2015 방향 선택→프렙 준비',
    '전달된 경쟁 구조를 자기 부족과 대조하고 학점 질문을 나누어 준비 의사를 전한다.',
    '국내의 익숙한 승부와 쉬운 관계 안에 남는 선택을 내려놓는다.',
    '미답을 숨기지 않은 준비 의사가 생긴다. 이동 자격은 별도 기관 절차다.'),
   ('미답을 안고 새 환경에 도착','기존 기관 순서 뒤2016년3월 프렙 도착',
    '이미 선택된 이동 경로를 별도 기관 순서 뒤 수행하고 생활 영어와 학업 준비가 다름을 직접 만난다.',
    '익숙한 환경과 관계에서 떨어져 기존에 고른 이동의 비용을 실제로 겪는다. 새 비용·허가 날짜는 추가하지 않는다.',
    '프렙에 도착했다. 학업 지원과 코트 역할은 아직 스스로 수행해야 한다.')],
9:[('좁은 자리로 토너먼트에 남기','2018년3월25일 TT 사용창',
    '승인된 좁은 도움·박스아웃·연결 역할을 토너먼트에서 수행한다. 자기 쇼케이스를 위해 역할을 늘리지 않는다.',
    '좁은 역할 안에서 자기 공격 과시를 포기한다. 앞 기능의 두 리바운드 포기는 다시 차감하지 않는다.',
    '우승으로 가는 경기에 자기 몫이 남았다. 아직 준결승·결승 결과는 모른다.'),
   ('우승팀 안의 내 몫','2018년3월31일 Kansas→4월2일 Michigan 종료 뒤',
    '같은 좁은 역할로 동료의 독립 마무리에 참여하고 종료 뒤 우승에서 자신의 기여만 확인한다.',
    '팀 우승을 개인 스타 인정으로 전부 가져오지 않는다.',
    '2018 NCAA 우승과 제한된 개인 역할이 함께 남는다. NBA 평가는 별도다.')],
10:[('평가에 숨기지 않는 공격','4월2일 뒤→4월20일 early entry→5월17일 가상 평가',
     '약점이 드러나는 평가 과제를 내놓고 막힌 공격도 숨기지 않는다.',
     '공격 한계가 노출되고 쉬운 장점만 내보일 길을 포기한다.',
     '자기 한계를 포함한 평가 자료가 있다. Chicago의 판단은 아직 모른다.'),
    ('Chicago 앞의 좁은 수정','2018년6월8일 선택된 Chicago workout',
     '앞 평가에서 본 한계를 현재 허용 과제와 대조하고 이번 과제 안에서만 수정한다.',
     '준비 시간을 좁은 과제에 쓴다. 앞 평가를 지우거나 사적 스카우트 의견을 만들어내지 않는다.',
     'Chicago에 보여 준 과제는 끝났다.22순위 지명은 이후 공개 사건이다.')],
14:[('개발 무대에서 드러낼 것','2019년1월7일 배정→1월11·12일 GL',
     '별도 개발 배정에서 자기 마무리와 수비·연결 오류를 함께 시험한다.',
     '기존GL52분·이동·준비를 쓰고 해당NBA85분은 동료에게 간다.',
     '개발 무대의 성취와 오류가 남았다. NBA 복귀는 별도 절차다.'),
    ('돌아와도 다른 속도','1월14일 대면 복귀→1월15일 NBA',
     '허용된 복귀 뒤 NBA의 위치 오차를 다시 확인하고 필요한 과제를 좁힌다.',
     '복귀 뒤 불편한 위치 과제를 수행한다. 앞에서 반환한NBA85분은 다시 차감하지 않는다.',
     '복귀는 이루어졌지만 NBA 속도에서의 안정성은 아직 부족하다.')],
15:[('열린 내 공격, 닫힌 약한 손','2019–20 기존 약한 손 과제의 첫 사용',
     '열린 공격은 직접 끝내고 약한 손의 첫 벽에서는 Coby·Satoransky에게 일찍 넘긴다.',
     '직접 쓴 시도는 당일 동료의 기회를 쓰고 이양하면 자기 종료 기회를 잃는다.',
     '공격 조건과 포기 조건이 갈린다. 반복 가능한 전면 창조는 아니다.'),
    ('늘어난 역할과 다른 성장','라이벌 공개2019년11월28일·2020년3월10일 표본 이후',
     '앞의 한계와 현재 공격 역할을 함께 확인하고 공개된 라이벌의 다른 성장 비용을 짧게 대조한다.',
     '라이벌의 동료 분·터치 비용과 자기 한계를 지우지 않는다. 취소된 NCAA가 잃은 시간을 돌려주지 않는다.',
     '2년차 공격 기대 역할은 늘었다. 정확22–43/21–44 기록·MIP는 이 비교로 선택되지 않는다.')],
18:[('새 조합의 자기 몫','2021 승인된Theis·Green 합류 뒤',
     '전달받은 수비·연결·리바운드 과제와 자기 공격 창을 조합 안에서 준비한다.',
     '조합 준비에 시간을 쓰고 새 동료의 보완 노동을 자신의 지위 보상으로 가져오지 않는다.',
     '새 조합의 분담이 생겼다. 생존전 결과는 아직 일어나지 않았다.'),
    ('Washington 한 문턱','2021년5월18일 Washington 원정 종료 뒤',
     '선택된 역할을 수행하고 동료 공 확보·승리 뒤 다음 진입을 확인한다.',
     '이 경기의 기회·역할 노동을 쓴다. 승리 전체의 원인을 자기 포제션으로 독점하지 않는다.',
     '선택된Washington 승리로Indiana 문턱에 들어간다. 본선은 보장되지 않는다.')],
21:[('내 첫 동작과 조기 도움','2021–22 제한 라이브 사용, 선발투표 종료 전',
     '열린 첫 동작은 직접 공격하고 조기 도움에는 일찍 반환·재배치한다.',
     '공격의 시간·동료 시도 비용과 틀리거나 늦는 반환을 남긴다.',
     '4년차의 공격 역할이 선다. 한 번의 수정은 항상 맞는 카운터가 아니다.'),
    ('인정받고 싶은 역할의 비교','Jan22투표종료·Jan27선발발표·Feb3리저브발표의 분리된 비교창',
     '스타 인정을 목표로 자기 공격 책임을 동료의 시작·마무리 기여와 비교한다. 자기 준비와 역할 안의 선택만 한다.',
     '자기 득점순으로LM/LV의 독립 역할을 지울 수 없다. 아직 공개되지 않은 표나 결과를 이용할 수 없다.',
     '공격 성취와 공식 인정의 차이가 남는다. 발표 승패·선정명단을 쓰는 장면은 미선택이며 이 배치가 선정 결과를 부여하지 않는다.'),
    ('52승 뒤에도 필요한 생존전','정규 종료 뒤52–30/E7→2022년4월12일MIA전',
     '이미 끝난 정규 결과와 전달된 자기 역할을 가지고MIA 생존전에 들어가, 경기 종료 뒤 본선 진입만 확인한다.',
     '52승이 자동 진출권이 아니며 생존전 역할 노동과 기회를 따로 쓴다. 정규2624분과 플레이인 분을 합치지 않는다.',
     '선택된CHI 홈MIA 승리→PO7→PHI1라운드. 점수·개인 박스·B의 단독 승리 원인은 추가하지 않는다.')],
22:[('PHI의 첫 벽을 다시 만나기','2022년4월16·18·21·23일G1–4',
     '실전의 좋은 공격과 막힌 공격을 함께 드러내고 다음 허용 역할을 수행한다.',
     '앞 네 경기의 승패·공격 시간은 돌려받을 수 없다.',
     'G4까지의 끝난 경기만 알고G5에 들어간다. 시리즈 최종 승자는 아직 모른다.'),
    ('일곱 경기 뒤 내놓는 실패','2022년4월25·28·30일G5–7 종료 뒤',
     '탈락 뒤 좋은 공격과 실패를 함께 평가 자료로 남긴다.',
     '진출 기회를 잃고 실패를 숨겨 권한을 더 요구할 길도 포기한다.',
     'Apr30 PHI4–3CHI 탈락. 정규 역할 성취는 사라지지 않으며 계약은 별도다.')],
24:[('반환 뒤에도 남는 책임','2022–23 개막 이후 기존 첫 수정 가족',
     '첫 반환 차단 뒤 안전 재전개·짧은 창조·무볼 재참여를 같은 역할 비용 안에서 잇는다.',
     '첫 판단 오류의 시간과 동료 시작권 일부를 쓴다.',
     '좋은 재전개가 생겨도 약한 손과 재진입의 오류가 남는다.'),
    ('같은 한계를 안고 본선으로','같은 시즌 후행3phase 역할→2023년4월9일정규 종료',
     '다른 시점의 한계와 역할을 함께 준비하고 종료 뒤 선택된52–30/E6로PO에 진입한다.',
     'LM/LV 시작권의 비용을 유지한다. B득점 증가를2023점수 보너스로 다시 더하지 않는다.',
     '현재 선택된2023 PHI 경로에 들어간다. 미래 우승은 아직 모른다.')],
26:[('되돌아온 마지막 한 경기','2023년4월25·27일PHI G5–6 종료 뒤',
     '앞선 경기에서 한 행동·실패를 지고 다음 허용 역할을 수행한다.',
     'G5/G6의 기회를 이미 썼다. 이전2022패배는 환불되지 않는다.',
     'G6 종료 뒤에만 현재 시리즈 상태를 알고G7에 들어간다.'),
    ('2022 패배의 한정 회수','2023년4월29일PHI G7 종료 뒤',
     '선택된짧은롤·LM 재진입·LV 반대편 마무리의 공동 기능을 수행한다.',
     'P36분/Duarte14→10의 기존 비용과 동료의 독립 판단을 유지한다.',
     'CHI4–3PHI 진출. 정확 개인박스·새 마지막 슛은 만들지 않는다.')],
30:[('UTA 앞의 서로 다른 해답','2023년6월1·4·7·9일Finals G1–4',
     'P의 짧은 창조·LM 시작·Mark팝·Carter스크린·LV마무리를 같은 코트에서 역할별로 수행한다.',
     '예전100초루틴이 우승 자격증이 아니며 동료의 독립 역할 비용을 쓴다.',
     'G4까지의 끝난 상태만 안다. 아직 첫 우승은 이루어지지 않았다.'),
    ('처음 우승한 다섯 사람','2023년6월12·15일Finals G5–6 종료 뒤',
     '상대와 동료의 독립 판단을 남기고 종료 뒤 첫 우승의 자기 몫만 확인한다.',
     '공동 역할과 자기 공격·이양 선택의 비용을 지우지 않는다.',
     'June15 CHI4–2UTA 첫 우승. MVP/FMVP는 미선택이고2025최종수신 기능은 여기서 쓰지 않는다.')],
34:[('넘긴 뒤 비워 둔 자리','2024년6월6일DEN Finals G1의2770–2788초',
     'Carter의 확보·전진 뒤P가LM에 이양하고 오른쪽레인을 비운다. LM은 자기 시작을 고른다.',
     '자기 첫 운반과 쉬운 안쪽 진입을 포기한다. 동료의 보완 이동은 공짜가 아니다.',
     '18초의 공동 학습 창은 진행 중이다. 이 창에는 슛·점수·우승을 배정하지 않는다.'),
    ('학습과 다른 날의 두 번째 우승','2024년6월20일DEN Finals G6 종료 뒤',
     '별도선택 시리즈 종료에서 우승을 확인한다. June6의 이미 본 행동은 필요할 때만 한정 회수한다.',
     '자기 첫 소유와 동료 역할 비용을 유지하고, 한 학습 창을 시리즈 전체 승리 원인으로 쓰지 않는다.',
     'June20 CHI4–2DEN 두 번째 우승. 추가 개인상은 부여하지 않는다.')],
}

REASONS={4:'준비 의사와 기관 이후 도착은 다른 상태다.',9:'좁은 토너먼트 역할과 실제 우승 종료를 분리한다.',
10:'앞 평가와Chicago의 별도 과제는 시점·판단 주체가 다르다.',14:'GL52/NBA85 비용과NBA복귀 뒤 오류를 같은 성취로 쓰지 않는다.',
15:'첫 공격 조건과 후행 성장/라이벌 공개 비교의 취득 시점이 다르다.',18:'새 조합 준비와 생존전의 실제 진입을 분리한다.',
21:'공격 선택·인정 비교·정규 종료 뒤MIA진입은 다른 압력이다.',22:'첫 네 경기의 미래 불확실성과 탈락 뒤 평가를 분리한다.',
24:'첫 수정과 후행 정규 종료를 한 번 성공한 성장으로 합치지 않는다.',26:'G6 종료와G7 공동 역할 회수는 다른 상태다.',
30:'G4까지의 불확실성과June15첫 우승은 같은 장면 지식이 아니다.',34:'June6학습을June20우승으로 옮기지 않는다.'}

def norm(path):return path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode('utf-8')
def sha(path):return hashlib.sha256(norm(ROOT/path)).hexdigest()
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def ref(path,pointer=''):return {'path':path,'source_sha256':sha(path),'json_pointer':pointer}
def enc(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

def make():
    parent=read(BASE); original=parent['individual_function_designs']; episodes=[]; edits=[]
    for i,row in enumerate(original,1):
        if 35<=i<=39:continue
        if i==40:
            # Two omitted transitions consume already selected sources. No new
            # winner, medical event, private consultation or transaction.
            episodes += [
                {'unit_id':'M09','category':'NBA','function_ids':['CURRENT_2025_EAST_ENTRY'],
                 'title':'다시 같은 벽을 지나',
                 'timeline_window':'2025년4월19일MIA→5월15일BKN→5월31일PHI 종료',
                 'entry_state':'두 번째 우승 뒤2025의 새 사용 역할·상대 경로는 다시 수행해야 한다.',
                 'action_choice':'선택된MIA/BKN/PHI 사용창에서LM시작·P/LV윙 간격·Mark팝·Carter롤의 상대 대응과 비용을 본다. 완료된 경기만 다음 진입에 사용한다.',
                 'durable_cost':'BKN/PHI 사용창의 기존15초 위치 교환은 해당 벤치와코어의 이른/늦은 역할 비용이다. 분·급여·승리 원인을 새로 추가하지 않는다.',
                 'state_change':'선택된MIA4–1/BKN4–2/PHI4–3 뒤MIN Finals에 진입한다. MIN최종 우승 결과는 아직 모른다.',
                 'source_refs':[ref(LATE,'/selected_seasons/1'),ref(LATE,'/selected_six_East_partial_used_courts'),ref(EAST)],
                 'unresolved_used_dependencies':[], 'new_major_canon_choice':False},
                {'unit_id':'M09','category':'NBA','function_ids':['CURRENT_2025_G7_KNOWLEDGE_ENTRY'],
                 'title':'마지막 한 경기에서 알 수 있는 것',
                 'timeline_window':'2025년6월19일G6종료 뒤→6월22일G7의 현재 역할·마지막 공격 전',
                 'entry_state':'앞 여섯 경기 뒤 시리즈3–3이며G7 최종 결과는 아직 없다.',
                 'action_choice':'2022PHI탈락·2023PHIG7·June6_2024에서 자기가 이미 본 행동만 현재 자기 과제와 대조한다. 다른 선수의 선택과 아직 닫히지 않은 결과를 통제하려 하지 않는다.',
                 'durable_cost':'자기 역할과 동료 시작권의 비용을 현재 과제에 남긴다. 새 회고 사건·훈련·과거 득점은 추가하지 않는다.',
                 'state_change':'현재G7에서 맡을 역할과 알 수 없는 결과가 구별된다. 마지막 공의 독립 선택은 아직 일어나지 않았다.',
                 'source_refs':[ref(LATE,'/selected_seasons/1/selected_used_series/3'),ref(LATE,'/selected_2024_DEN_first_defense'),ref(LAST,'/learning_usepoint_and_information_boundaries')],
                 'unresolved_used_dependencies':[], 'new_major_canon_choice':False},
                {'unit_id':'M09','category':'NBA','function_ids':[f'FC{k:03}' for k in range(35,40)],
                 'title':'마지막 공을 동료가 끝내다', 'timeline_window':'2025년6월22일G7 MIN점유23.6초→CHI리바운드21.6초→릴리스0.2→혼·검토·공개 종료',
                 'entry_state':'현재CHI108–109MIN, 남은23.6초는MIN Rival의공/샷클록2.6이다. P는드리블과Towns접근만본다. 슛실패·CHI리바운드·마지막수신자·승리는아직모른다.',
                 'action_choice':'현재라이벌릴리스와보이는리바운드길에대응한다. 미스를본뒤공을확보한주가지에서만전진·닫힌직접공격·첫이양·반환·재참여·최종이양을잇는다. P는자기이양을선택하며LM의슛선택과성공을미리알거나보장하지않는다.',
                 'durable_cost':'P의 최종 슛·통제권 포기, LM의독립 슛 책임, LV/Mark/Carter의 무볼·박스아웃·중간소유 비용을 각각 남긴다.',
                 'state_change':'LM유효2점의검토 뒤공개CHI110–109MIN/시리즈4–3/삼연패. P결승득점0·새개인상0.',
                 'source_refs':[ref(BASE,f'/individual_function_designs/{k-1}') for k in range(35,40)]+[ref(LATE,'/selected_2025_last_attack'),ref(LAST,'/individual_choices_and_visible_costs')],
                 'unresolved_used_dependencies':[], 'new_major_canon_choice':False},
            ]
            edits.append({'operation':'MERGE','function_ids':[f'FC{k:03}' for k in range(35,40)],'old_rows':5,'new_rows':1,'reason':'최종회차에겹쳐쓰이는다섯기능이다. 라이벌수비는선택된MIN23.6초부터, CHI점유는21.6초부터다. 각기능을독립된새점유나여러회차의새사건으로반복하지않는다.'})
            edits.append({'operation':'RESTORE_SELECTED_TRANSITION','added_rows':2,'reason':'이미 선택된2025 East 진입과G7 이전 지식 경계를 보강한다. 새 승패·기관 판정·훈련을 만들지 않는다.'})
        parts=SPLITS.get(i)
        if parts:
            edits.append({'operation':'SPLIT','function_ids':[row['function_cluster_id']],'old_rows':1,'new_rows':len(parts),'reason':REASONS[i]})
        else:parts=[(row['title'],row['timeline_window'],row['action_choice'],row['durable_cost'],row['state_change'])]
        for j,(title,window,action,cost,state) in enumerate(parts,1):
            entry=row['entry_state'] if j==1 else parts[j-2][4]
            sources=copy.deepcopy(row['source_refs'])
            if i==21:sources.append(ref(REC))
            if i==21 and j==3:sources.append(ref(PI22,'/playin_games/0'))
            if i==22:sources.append(ref(PHI22,'/selected_series'))
            if i in (26,30):sources += [ref(TITLE23,f'/selected_CHI_series_preparation/{0 if i==26 else 3}'),ref(SEL23)]
            if i==33:sources += [ref(LATE,'/selected_six_East_partial_used_courts'),ref(EAST)]
            episodes.append({'unit_id':row['unit_id'],'category':row['category'],'function_ids':[row['function_cluster_id']],
                             'part':j,'parts':len(parts),'title':title,'timeline_window':window,
                             'entry_state':entry,'action_choice':action,'durable_cost':cost,'state_change':state,
                             'source_refs':sources,'unresolved_used_dependencies':copy.deepcopy(row['used_dependencies_remaining']),
                             'new_major_canon_choice':False})
    assert len(episodes)==51
    episodes[9]['entry_state']='선발 승격 없이 후순위로 맡은 제한 역할이 있다. 아직 끝나지 않은 시즌의 최종34GP·323분은 이 진입에서 알 수 없다.'
    episodes[9]['author_only_season_budget']={'GP':34,'GS':0,'minutes':323,'classification':'CONDITIONAL_SEASON_AGGREGATE_NOT_DATED_BOXES_OR_POV_KNOWLEDGE','source_ref':ref(VILL,'/selected_season_role_cost_family/selected_point')}
    episodes[9]['source_refs'].append(ref(VILL,'/selected_season_role_cost_family'))
    episodes[10]['source_refs'].append(ref(VILL,'/current_selected_title_bridge'))
    episodes[28]['entry_state']='정규시즌 종료 뒤52–30/E7과CHI 홈MIA 생존전의 자기 역할을 확인했다. 아직MIA전 결과와 본선 진출은 모른다.'
    episodes[35]['entry_state']='4월22일G4 종료 뒤CHI–PHI는2–2다. 원정G5가 눈앞에 있지만6·7차전의 승패나G7 개최는 아직 확정되지 않았다.'
    episodes[35]['state_change']='4월25일G5 승리 뒤3–2,4월27일G6 패배 뒤3–3을 차례로 확인했다. 이제야4월29일G7에 진입한다.'
    episodes[44]['timeline_window']='2023–24 첫 방어 준비→2024년4월20일ATL→5월19일BOS→6월1일MIL 종료, DEN Finals 이전'
    episodes[44]['state_change']='각 종료 뒤에만ATL4–1/BOS4–3/MIL4–2를 알고DEN Finals에 들어간다. June6 학습과June20 우승은 아직 겪지 않았다.'
    episodes[44]['source_refs'].append(ref(LATE,'/selected_seasons/0/selected_used_series'))
    episodes[27]['action_choice']='스타로 인정받고 싶은 욕구는 남기되, 자기 공격 책임과 LM/LV의 독립 기여를 비교하고 자기 준비만 고른다. Jan22 종료 전44경기 입력과 Jan27 발표 전47·Feb3 발표 전50의 서로 다른 공개창을 구별한다. 기대 평균·미공개 표·미선택 발표 결과는 자기 지식으로 쓰지 않는다.'
    episodes[46]['entry_state']='June6에 직접 본 이양·레인 비우기의 첫 소유 포기와 동료 보완 비용이 남는다. 그것이 시리즈 전체 승리 원인은 아니다. 현재는 별도June20 G6의 종료 확인이다.'
    episodes[48]['current_source_priority']='June6_2024 사용은 LATE의 selected_2024_DEN_first_defense를 따른다. LAST의 예전 L2024DEN_HOLD는 출생 이력으로 보존하며 현재 성공 사용을 다시 HOLD로 덮지 않는다.'
    episodes[49]['actor_cost_separation']={'P':'최종 직접 슛과 통제권을 넘긴다. LM의 성공을 사전에 알지 못한다.', 'LM':'독립적으로 읽고 릴리스하며 자기 슛의 성공·실패 책임을 진다.', 'LV_Mark_Carter':'선택된 무볼·박스아웃·중간 소유 비용을 유지한다. 마지막 득점자로 바꾸지 않는다.'}
    for i,e in enumerate(episodes,1):
        e.update(proposed_episode=i,status='PREPARED_EPISODE_ALLOCATION_NOT_FINAL_LOCK',personal_award_use_mode='NOT_USED')
        e['next_entry_state']=episodes[i]['entry_state'] if i<len(episodes) else None
        e['editorial_directions_are_dialogue']=False
    # These are named planned access checkpoints, not private vote receipts,
    # institutional approvals or newly invented seconds.
    checkpoints={
      10:[('2018-03-25 before selected TT use','현재 받은 제한 과제만; 최종 시즌합계·준결승·결승 결과 미취득'),('2018-03-25 TT use completed','실제로 수행한 스위치·박스아웃·동료 공 확보만; 우승 미취득')],
      11:[('2018-03-31 Kansas completed','끝난 준결승의 진행·자기 역할만; Michigan 결과 미취득'),('2018-04-02 Michigan completed','끝난 결승과팀 우승·동료의 공개 마무리; 조건부323분을 실제개인박스로 확정하지 않음')],
      28:[('2022-01-22 fan close','종료 전44경기 창만; 후행47/50경기와미공개표 미취득'),('2022-01-27 starter announcement window','그날까지47경기 창; 실제 선택된 새선발명단 없음'),('2022-02-03 reserve announcement upper bound','그날까지50경기 창; 감독 제출마감·새리저브명단 미확정')],
      29:[('2022 regular season completed','52–30/E7·생존전 상대/자기 과제 확인; 본선진출 미취득'),('2022-04-12 MIA completed','CHI승리/PO7/PHI진입 확인; 점수·개인박스·승리단독원인 미부여')],
      36:[('2023-04-22 PHI G4 completed','2–2; G7개최 미확정'),('2023-04-25 PHI G5 completed','3–2; G6·G7결과 미취득'),('2023-04-27 PHI G6 completed','3–3; G7진입확정,승패 미취득')],
      43:[('after 2023 title and separately selected summer ports','자기 자료·질문 전달만; 대표팀명단·보험·입국·구단 허가 미취득')],
      44:[('conditional September private preparation','사적 과제의 자기 선택만; 공적 금메달·편입·실제여행 미선택'),('conditional October return','실제 가용성C01보류; 사적 준비가NBA복귀허가를 생성하지 않음')],
      45:[('2024-04-30 ATL completed','4–1; BOS·MIL·DEN결과 미취득'),('2024-05-19 BOS completed','4–3; MIL·DEN결과 미취득'),('2024-06-01 MIL completed','4–2; DEN진입만, June6/20미취득')],
      46:[('2024-06-06 elapsed2770','Carter리바운드/새24초; 미래18초끝·점수 미취득'),('2024-06-06 elapsed2772','Carter선택전진패스와P수신'),('2024-06-06 elapsed2775','P이양·LM수신/독립시작·SC19'),('2024-06-06 elapsed2778','P오른쪽레인비움; 동료이동 보이는 범위만'),('2024-06-06 elapsed2788','진행중/슛·점수 미배정; June20우승 미취득')],
      47:[('2024-06-20 DEN G6 completed','별도종료4–2/우승 확인; June6첫소유포기비용기억,개인상 미부여')],
      49:[('2025-06-19 Finals G6 completed','3–3; 끝난2022/23·June6_2024 자기경험만'),('2025-06-22 G7 before final possession','현재받은역할; Rival미래실패·LM미래득점·최종수신 확정 미취득')],
      50:[('2025-06-22 remaining23.6 MIN possession','Rival의공·드리블/Towns접근·샷클록2.6만; 미래미스·CHI획득 미취득'),('2025-06-22 remaining22.7 Rival release','릴리스와골대쪽공/동료박스아웃; 아직슛실패 미취득'),('2025-06-22 remaining22.0 rim miss','림에맞아튀는공; 아직CHI수비리바운드확보 미취득'),('2025-06-22 remaining21.6 rebound','CHI108–109MIN·P수비리바운드·SCoff'),('2025-06-22 remaining16.6 frontcourt','실제전진·보이는수비·닫힌직접공격만'),('2025-06-22 firstfeed return reentry finalpass','LM첫수신/Carter반환/P재참여/최종이양의현재관찰; 정확중간초 새로 부여하지 않음'),('2025-06-22 remaining0.2 release','LM자기릴리스 관찰; 유효2점·최종승리 미확정'),('2025-06-22 horn and valid-shot review completed','유효2점/추가시간없음의선택가상판정 뒤에만110–109·4–3·삼연패확인'),('2025-06-22 public end and visible nod','상호보이는고개행동만; 동료의속마음·미래보증 미취득')],
      51:[('2035-06-18 service end','서비스종료만; UPC만료와같다는추론 금지'),('2035-06-19 separately permitted guest','별도자발적권한/후배의보이는준비; 본인NBA서비스연장 없음'),('2035-06-20 public retirement','전날본행동만기억; 후배생각/미래직업 미취득,실사용C01의무가용보류')]
    }
    for ep,points in checkpoints.items():
        episodes[ep-1]['named_acquisition_checkpoints']=[{'order':n,'source_clock_label':label,'available_knowledge_limit':limit,'status':'SOURCE_JOINED_ACCESS_DESIGN_NOT_ACTUAL_RECEIPT'} for n,(label,limit) in enumerate(points,1)]
    for ep in (43,44,51):episodes[ep-1]['source_refs'].append(ref(C01,'/finite_remaining_ports'))
    ownership={f'FC{i:03}':[e['proposed_episode'] for e in episodes if f'FC{i:03}' in e['function_ids']] for i in range(1,41)}
    promises=[]
    for p in parent['five_promise_consumption']:
        current=copy.deepcopy(p)
        current['episode_roles']={k:sorted({ep for fc in ids for ep in ownership[fc]}) for k,ids in p['current_function_ids'].items()}
        current['actual_prose_payoff_verified']=False;promises.append(current)
    pins={path:sha(path) for path in [BASE,SCOPE,PI22,PHI22,TITLE23,SEL23,LATE,EAST,LAST,REC,NLM,VILL,C01]}
    allocation={'id':'THREEPEAT_51_EPISODE_DENSITY_ALLOCATION_2026_10_12','producer_id':'root_codex',
                'baseline_main':'098e8f170a9e4ea0503dff576811807a79fd7e6d',
                'status':'COMPLETE_51_ROW_EDITORIAL_RECOMMENDATION_NOT_FINAL_N_LOCK',
                'authority_boundary':'기존 짧은 본편·B 방향의 편집 준비. 정확N51은 작가 선택이나 독립 수락으로 기록하지 않는다.',
                'source_sha256':pins,'scope_ref':ref(SCOPE),'recommended_episode_count':51,'main_episode_count':50,
                'brief_epilogue_count':1,'final_episode_count_locked':None,
                'derivation':{'original_clusters':40,'split_added_rows':13,'merged_removed_rows':4,'restored_existing_transition_rows':2,
                              'arithmetic':'40+13-4+2=51','ratio_driven_padding':False,'old111_or40_used_as_final_N':False},
                'episodes':episodes,'density_edits':edits,'function_ownership':ownership,'five_promise_episode_consumption':promises,
                'unit_counts':dict(Counter(e['unit_id'] for e in episodes)),
                'category_counts':dict(Counter(e['category'] for e in episodes)),
                'draft_counting_policy':'NBA_DRAFT counted in recommendation diagnostic only; final selected policy source not issued',
                'recognition_announcement_scene_outcomes_selected':False,
                'semantic_review_risks':['50main episodes is an editorial recommendation; no prose length/render or commercial pacing proof',
                                         '2025progression is compressed to three episodes; independent narrative-density review required',
                                         'FC021 recognition scene details remain prepared; actual award announcement cannot be written without selected result',
                                         'C01 used-calendar availability remains pending; conditional scene is not institutional completion'],
                'gates':{'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False,'actual_blueprint_authority_count':0,'actual_pack_count':0},
                'tools_this_pass':{'Codex':'LOCAL_READ_EDIT_CHECK','Antigravity':'NOT_RUN','NotebookLM':'SELF_AUTHORED_PROPOSAL_SOURCE_REGISTERED_AND_CITED_ANALYSIS_RECOVERED','Claude':'NOT_RUN','independent_agent':'NOT_RUN'},
                'notebooklm_analysis_ref':ref(NLM),
                'access_repair_baseline_main':'568870cfbc3d7736cda2fcb5d47e9c6d1cd74e56',
                'access_repair_scope':{'repaired_episodes':[10,29,36,45],'named_checkpoint_episodes':sorted(checkpoints),'new_event_or_choice_selected':False},
                'access_repair_precedence':'Current episode entry/state and acquisition checkpoints override unsplit parent actor-knowledge wording. Parent outcome/aggregate and original bytes remain unchanged.',
                'tools_access_repair':{'Codex':'DIRECT_READ_SEMANTIC_REPAIR_AND_LOCAL_CHECK','Antigravity':'NOT_RUN','NotebookLM':'NOT_RUN_ON_REPAIRED_GENERATION','Claude':'NOT_RUN','independent_agent':'NOT_RUN'},
                'unfinished_major_groups':4,'unfinished_through_group6':3}
    bps=[]
    for e in episodes:
        bp=copy.deepcopy(e);bp['status']='INDIVIDUAL_PREPARED_EPISODE_BLUEPRINT_NOT_ACTUAL_VERIFIED'
        bp['unit_question']='지금 허용된 자기 선택이 동료의 역할·이미 쓴 비용을 남긴 채 무엇을 바꾸는가.'
        bp['reader_question']=e['next_entry_state'] or '물러난 뒤에도 후배의 다음 행동이 남는가.'
        bp['physical_state']='기존 선택된 가용 조건만 사용; 새 부상·피로·진단·의료 판정 추가0'
        bp['relationship_state']='동료·상대의 자기 판단을 남긴다. 사실로 확인되지 않은 속마음·비리를 추가하지 않는다.'
        bp['basketball_goal']=e['action_choice']
        bp['forbidden_changes']='승패·지명·UPC·계약·수상·사용달력의 미선택 또는 다른 세대를 자동 변경하지 않는다.'
        bp['primary_devices']=['OWN_CHOICE','COACTOR_COST']
        bp['setup_to_plant']='현재 진입의 남은 부담을 이번 선택에 필요한 만큼만 둔다.'
        bp['payoff_to_consume']='앞의 이미 취득한 행동을 현재 선택에서만 회수한다. 결과 전 미래를 알지 않는다.'
        bp['claims']=[{'text':e[k],'status':'AUTHOR_MODELED_DESIGN','temporal_kind':'CURRENT_PLAN' if k=='action_choice' else 'OBSERVED_EVENT','source_refs':copy.deepcopy(e['source_refs'])} for k in ('entry_state','action_choice','state_change')]
        bp['information_boundary']={'status':'RELATIVE_ACCESS_PREPARED_NOT_SELECTED_SCENE_ACCESS_LOCK','pov_character':'PROTAGONIST',
            'clock_basis':'회차 내 상대 순서; 서로 다른날/경기 종료는timeline_window의 순서를 따른다.',
            'scene_segments':[{'segment_id':f'S{k+1}','scene_order':k+1,'pov_character':'PROTAGONIST','known_claim_indexes':[k]} for k in range(3)],
            'access_witnesses':[{'segment_id':f'S{k+1}','owner':'PROTAGONIST','scene_order':k+1,'acquired_order':k+1,
                                'event_order':k+1 if k!=1 else None,'knowledge_kind':bp['claims'][k]['temporal_kind'],
                                'claim_indexes':[k],'access_method':'자기 선택 계획' if k==1 else '참여·이미 받은 본인 과제·끝난 공개 상태; 작가 모델 숫자는 인물 지식으로 쓰지 않는다.'} for k in range(3)],
            'clock_order_checked_locally':True,'prose_access_verified':False}
        bps.append(bp)
    bundle={'id':'THREEPEAT_51_PREPARED_EPISODE_BLUEPRINTS_2026_10_12','producer_id':'root_codex',
            'status':'COMPLETE_PREPARED_51_EPISODE_BUNDLE_NOT_ACTUAL_AUTHORITY','allocation_ref':{'path':ALLOCATION,'source_sha256':hashlib.sha256(enc(allocation)).hexdigest(),'json_pointer':''},
            'prepared_episode_blueprints':bps,'final_N_locked':False,'independent_acceptance':False,
            'gates':copy.deepcopy(allocation['gates'])}
    return allocation,bundle

def validate(a,b):
    assert a['recommended_episode_count']==len(a['episodes'])==len(b['prepared_episode_blueprints'])==51
    assert a['final_episode_count_locked'] is None and not b['final_N_locked']
    assert a['gates']==b['gates']=={'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False,'actual_blueprint_authority_count':0,'actual_pack_count':0}
    assert not b['independent_acceptance']
    receipt=read(NLM)
    assert receipt['query_status']=='success' and receipt['sources_used']==receipt['registered_source_ids']
    assert set(receipt['citation_source_ids'])==set(receipt['registered_source_ids'])
    assert list(a['function_ownership'])==[f'FC{i:03}' for i in range(1,41)]
    assert all(v for v in a['function_ownership'].values())
    assert [e['proposed_episode'] for e in a['episodes']]==list(range(1,52))
    assert a['unit_counts']=={'M01':3,'M02':5,'M03':6,'M04':6,'M05':5,'M06':6,'M07':11,'M08':5,'M09':3,'EPI':1}
    assert a['category_counts']=={'PRE_NBA':11,'NBA_DRAFT':3,'NBA':36,'POST_NBA':1}
    assert [a['function_ownership'][f'FC{i:03}'] for i in range(35,40)]==[[50]]*5
    assert a['function_ownership']['FC040']==[51]
    for path,h in a['source_sha256'].items():assert sha(path)==h,('stale source',path)
    for i,(e,bp) in enumerate(zip(a['episodes'],b['prepared_episode_blueprints'])):
        assert e['status']=='PREPARED_EPISODE_ALLOCATION_NOT_FINAL_LOCK'
        assert bp['status']=='INDIVIDUAL_PREPARED_EPISODE_BLUEPRINT_NOT_ACTUAL_VERIFIED'
        assert e['personal_award_use_mode']=='NOT_USED' and bp['personal_award_use_mode']=='NOT_USED'
        assert all(e[k]==bp[k] for k in e if k!='status')
        assert e['next_entry_state']==(a['episodes'][i+1]['entry_state'] if i<50 else None)
        assert all(e[k] for k in ('entry_state','action_choice','durable_cost','state_change','timeline_window'))
        assert len(bp['primary_devices'])<=2
        for source in e['source_refs']:
            assert sha(source['path'])==source['source_sha256'];value=read(source['path'])
            for t in source['json_pointer'].split('/')[1:]:
                t=t.replace('~1','/').replace('~0','~');value=value[int(t)] if isinstance(value,list) else value[t]
        for w in bp['information_boundary']['access_witnesses']:
            assert w['acquired_order']<=w['scene_order']
            if w['knowledge_kind']=='OBSERVED_EVENT':assert w['event_order']<=w['acquired_order']
    # Required entry that compressed40 omitted; do not make 52wins automatic qualification.
    pi=[e for e in a['episodes'] if 'CHI 홈MIA 승리' in e['state_change']]
    assert len(pi)==1 and any(r['path']==PI22 and r['json_pointer']=='/playin_games/0' for r in pi[0]['source_refs'])
    pi_source=read(PI22)['playin_games'][0]; assert (pi_source['date'],pi_source['home'],pi_source['away'],pi_source['winner'])==('2022-04-12','CHI','MIA','CHI')
    last=a['episodes'][49]; assert '108–109' in last['entry_state'] and '110–109' not in last['entry_state']
    assert '110–109' in last['state_change']
    assert [e['proposed_episode'] for e in a['episodes'] if e['unresolved_used_dependencies']]==[43,44,51]
    assert '6월6일' in a['episodes'][45]['timeline_window'] and '6월20일' in a['episodes'][46]['timeline_window']
    assert '34GP' not in a['episodes'][9]['entry_state'].split('아직')[0]
    assert a['episodes'][9]['author_only_season_budget']['classification']=='CONDITIONAL_SEASON_AGGREGATE_NOT_DATED_BOXES_OR_POV_KNOWLEDGE'
    assert '정규시즌 종료 뒤52–30/E7' in a['episodes'][28]['entry_state']
    assert 'G7 개최는 아직 확정되지 않았다' in a['episodes'][35]['entry_state']
    assert 'G6 패배 뒤3–3' in a['episodes'][35]['state_change']
    assert 'June20_2024 CHI4–2DEN' not in a['episodes'][44]['state_change']
    assert '우승은 아직 겪지 않았다' in a['episodes'][44]['state_change']
    learning=read(LATE)['selected_2024_DEN_first_defense']['new_successor_current_learning_selected']
    assert [x['elapsed'] for x in learning['events']]==[2770,2772,2775,2778] and learning['window_elapsed_seconds']==[2770,2788]
    assert [x['order'] for x in a['episodes'][49]['named_acquisition_checkpoints']]==list(range(1,10))
    assert '유효2점·최종승리 미확정' in a['episodes'][49]['named_acquisition_checkpoints'][6]['available_knowledge_limit']
    assert '남은23.6초는MIN Rival의공/샷클록2.6' in last['entry_state']
    events=read(LAST)['last_attack_candidate']['live_events']
    assert [e['remaining_game_seconds'] for e in events[:4]]==[23.6,22.7,22.0,21.6]
    profiled=[e for e in a['episodes'] if 'named_acquisition_checkpoints' in e]
    assert len(profiled)==13 and sum(len(e['named_acquisition_checkpoints']) for e in profiled)==38
    phi=read(TITLE23)['selected_CHI_series_preparation'][0]['games']
    assert [(g['date'],g['selected_winner']) for g in phi[3:6]]==[('2023-04-22','CHI'),('2023-04-25','CHI'),('2023-04-27','PHI')]
    late=read(LATE)['selected_seasons'][0]['selected_used_series']
    assert [s['games'][-1]['date'] for s in late[:3]]==['2024-04-30','2024-05-19','2024-06-01']

def render(a):
    lines=['# 현재 본편50회+후일담1회 밀도 배치 권고','',
           '**51행을 실제 작성한 편집 권고안이다. 최종N LOCK·작가선택·독립수락이 아니다.** 원고0·ACTUAL Blueprint/Pack0·v0.30 PARTIAL/CLOSED.','',
           '## 수의 근거','',
           '40기능에서 다른 날짜·다른 압력의 선택을13행 더 나누고, 2025 마지막회차의겹치는5기능은1회로합쳐4행을줄였다. 라이벌수비는선택된MIN점유23.6초부터, CHI마지막점유는21.6초부터다. 이미선택된2025 East진입·G7지식경계2행을복원해 `40+13−4+2=51`이다. 경기별·계약서별·연간후일담별로나누거나비율을맞추려NBA장면을늘리지않았다.','',
           '비율 진단: PRE11 / NBA_DRAFT3 / NBA36 / POST1. draft포함39/51=76.47%, NBA만36/51=70.59%. EPI는POST이며 최종 정책 선택 자료는 발급하지 않았다.','',
           '## 회차별 배치','',
           '|권고 회차|막|제목|사용 기능|바뀐 상태|','|---|---|---|---|---|']
    for e in a['episodes']:
        lines.append('|'+ '|'.join([str(e['proposed_episode']),e['unit_id'],e['title'],','.join(e['function_ids']),e['state_change'].replace('|','/')])+'|')
    lines += ['','## 개별 행동·비용·진입','']
    for e in a['episodes']:
        lines += [f"### 권고{e['proposed_episode']:02} · {e['title']}",'',
                  f"- 시간·진입: {e['timeline_window']} / {e['entry_state']}",f"- 행동·선택: {e['action_choice']}",
                  f"- 남는 비용: {e['durable_cost']}",f"- 다음 진입: {e['next_entry_state'] or '후배의 다음 행동으로 닫는다.'}",
                  '- 사용 의존성: '+(','.join(e['unresolved_used_dependencies']) or '이 배치 단계에서 추가 없음; 전체 입력의 선택·독립수락은 후행'),'']
    lines += ['## 중요한 경계','',
              '- 권고28의 인정 비교는44/47/50경기 입력을 날짜별로 분리한다. 선정 발표 결과는 미선택이고 작가 기대값을 선수의 실제평균으로 인용하지 않는다.',
              '- 권고29는2022Apr12 MIA생존전,30부터PHI다. 정규52승이 본선 자동 진입을 뜻하지 않는다.',
              '- 권고46 June6학습은슛/점수 없는18초,47 June20우승은다른 경기다.',
              '- 권고48의2025East 일부 접촉은선택된15초 창만 소비한다. 전체시리즈의 유일승리원인·추가교체·부상을 만들지 않는다.',
              '- 권고49는끝난6경기의3–3만 안다.50의LM최종득점은자기리바운드·이양뒤 검토/종료에서만 안다.',
              '- 다섯 약속의설치·변주·회수를권고회차로재연결했다.50/51의기능소비는본문회수완료가 아니다.',
              '- C01의권고43/44/51은사용날가용이보류다.개인상NOT_USED를허가/서비스달력의대체로쓰지 않는다.','',
              '## 검증·남은 일','',
              '51배치와51개별Blueprint를대조하고설계12출처핀+분석영수증1핀/원40기능소비/10막순서/진입·비용·다음상태/정보취득순서를검사했다.동일생산자의Codex검사로신규독립검수는아니다.','',
              'NotebookLM은이편집권고안의첫세대본문을새source로등록하고인용답을회수했다.자기작성설계의구조분석이며NBA원전검증이나독립수락은아니다.인정욕구삭제권고는거부하고정보창만분리했고,June6→June20기존비용연결과P/LM마지막비용구분을보강했다.원입력해시·답·수락범위는별도영수증에보존한다.','',
              '후속 직접 검사에서 권고10의 미완료 시즌34GP/323분 선인지, 권고36의2–2시점G7확정, 권고45의DEN진입 전June20우승 소비를 발견해 수리했다. 권고29는 정규 종료 뒤52–30/E7을 확인한 진입으로 명확히 했다. 최종 합계는 작가용 조건부 예산으로 분리하고13회차의38취득 체크포인트를 날짜/현재 시계에 붙였다. 마지막회차는원선택전체시계의23.6/22.7/22.0을복원해CHI점유획득을미리알지않는다. 기존6반례·NLM첫세대 분석의 검증 한계도 기록한다.','',
              '원고분량·상업적리듬이입증되지않았다.특히2025진행3회와인정비교의서사밀도는현재출처를받은독립의미검수대상이다.권고51을고정분량으로맞추기위해회상·설명·같은21.6초를늘리지않는다.','',
              '다음: 이51행의독립적인의미·정보접근검수와현재역사/사용달력연결,필요하면권고배치수리→최종N/개별권위발급→실제Pack컴파일.','',
              '|번호|작업|상태|','|---|---|---|','|1|드래프트연쇄|완료|','|2|Chicago2020–21|기존선택시즌완료|',
              '|3|거래·계약|완료|','|4|커리어·B|인정비교/대표팀달력남음|','|5|구조|51행배치권고·전체역사/최종N미LOCK|',
              '|6|규격·Pack|51개별Blueprint준비·실제권위/Pack미완료|','|7|통합·독립·작가승인|미완료|','',
              '미완료4개·6번까지3개.신규NotebookLM등록·구조분석1회;Antigravity/Claude/하위agent/독립0·일정0·원고0.','']
    return '\n'.join(lines).encode('utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--refresh-untracked',action='store_true');parser.add_argument('--refresh-owned',action='store_true');parser.add_argument('--expected-hashes-file');args=parser.parse_args()
    expected=read(args.expected_hashes_file) if args.refresh_owned and args.expected_hashes_file else {}
    a,b=make();validate(a,b);rejected=[]
    def both(x,y,index,key,value):
        x['episodes'][index][key]=value;y['prepared_episode_blueprints'][index][key]=value
    for label,mutate in [
        ('MIA_ENTRY_OMITTED',lambda x,y:both(x,y,28,'state_change','52승으로바로PHI에진입한다.')),
        ('SAME_FINAL_CLOCK_REPLAY',lambda x,y:x['function_ownership']['FC035'].append(49)),
        ('LM_FUTURE_SCORE_AT_ENTRY',lambda x,y:both(x,y,49,'entry_state','CHI110–109MIN을이미안다.')),
        ('KNOWLEDGE_ACQUIRED_AFTER_USE',lambda x,y:y['prepared_episode_blueprints'][49]['information_boundary']['access_witnesses'][0].update(acquired_order=4)),
        ('FALSE_FINAL_N_LOCK',lambda x,y:x.update(final_episode_count_locked=51)),
        ('FALSE_ACTUAL_BLUEPRINT',lambda x,y:y['prepared_episode_blueprints'][0].update(status='ACTUAL_VERIFIED')),
        ('SEASON_TOTAL_AS_EARLY_KNOWLEDGE',lambda x,y:both(x,y,9,'entry_state','34GP·323분을이미안다.')),
        ('MIA_RESULT_BEFORE_ENTRY',lambda x,y:both(x,y,28,'entry_state','Feb3에MIA승리와본선진출을안다.')),
        ('G7_KNOWN_AT_TWO_TWO',lambda x,y:both(x,y,35,'entry_state','2–2에서G7개최와최종승리를안다.')),
        ('TITLE_BEFORE_JUNE6',lambda x,y:both(x,y,44,'state_change','June20_2024 CHI4–2DEN 우승을이미안다.')),
        ('LM_WIN_AT_RELEASE',lambda x,y:(x['episodes'][49]['named_acquisition_checkpoints'][6].update(available_knowledge_limit='릴리스순간최종승리를확신한다.'),y['prepared_episode_blueprints'][49]['named_acquisition_checkpoints'][6].update(available_knowledge_limit='릴리스순간최종승리를확신한다.'))),
        ('RIVAL_MISS_KNOWN_BEFORE_RELEASE',lambda x,y:both(x,y,49,'entry_state','현재108–109지만Rival미스와P의다음리바운드를미리안다.')),
    ]:
        x,y=copy.deepcopy(a),copy.deepcopy(b);mutate(x,y)
        try:validate(x,y)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('false pass '+label)
    files={ALLOCATION:enc(a),BLUEPRINT:enc(b),MD:render(a)}
    review={'id':'THREEPEAT_51_EPISODE_DENSITY_ALLOCATION_2026_10_12_CODEX_CHECK',
            'status':'LOCAL_SOURCE_COVERAGE_AND_ACCESS_CHECK_NOT_INDEPENDENT_ACCEPTANCE','producer_id':'root_codex',
            'input_source_sha256':a['source_sha256'],'recommended_episodes':51,'prepared_individual_blueprints':51,
            'rejected_counterexamples':rejected,'whole_history_or_final_N_accepted':False,'independent_review_completed':False,
            'actual_Blueprints':0,'actual_Packs':0,'output_LF_SHA256':{p:hashlib.sha256(c).hexdigest() for p,c in files.items()}}
    files[REVIEW]=enc(review)
    for p,data in files.items():
        path=ROOT/p
        if args.check:assert path.is_file() and norm(path)==data,('mismatch',p)
        elif path.exists() and norm(path)!=data:
            tracked=subprocess.run(['git','ls-files','--error-unmatch','--',p],cwd=ROOT,capture_output=True)
            if tracked.returncode==0:
                assert args.refresh_owned and expected.get(p)==sha(p),('refuse unverified tracked overwrite',p)
            else:assert args.refresh_untracked,('refuse untracked overwrite',p)
            prior=path.read_bytes();backup=ROOT/'Temp'/'density51_preserved_first_generation'/f'{path.name}.{hashlib.sha256(prior).hexdigest()}'
            backup.parent.mkdir(parents=True,exist_ok=True)
            if not backup.exists():backup.write_bytes(prior)
            path.write_bytes(data)
        elif path.exists():assert norm(path)==data,('refuse overwrite',p)
        else:path.write_bytes(data)
    print(json.dumps({'mode':'check' if args.check else 'write','allocation_rows':51,'prepared_blueprints':51,'source_pins':len(a['source_sha256']),'rejected':rejected,'final_N_LOCK':False,'Pack':0}))

if __name__=='__main__':main()
