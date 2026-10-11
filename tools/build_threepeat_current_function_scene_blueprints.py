"""Prepare individual scene designs; never issue final-N, ACTUAL or Pack authority."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'design/THREEPEAT_BY_2025_EPISODE_FUNCTION_COMPRESSION_2026_10_09.json'
SCOPE = 'control/CURRENT_SELECTED_THREEPEAT_BY_2025_MAIN_STORY_SCOPE_2026_10_09.json'
B = 'canon/EARLY_REWARD_B_AUTHOR_SELECTION_2026_10_11.json'
ROLES = 'simulation/EARLY_REWARD_B_CURRENT_FULL_ROLE_INPUTS_2026_10_12.json'
IMPACT = 'simulation/EARLY_REWARD_B_JOINT_RESULT_RESPONSE_2026_10_12.json'
RECOG = 'design/EARLY_REWARD_B_RECOGNITION_ROSTER_CANDIDATES_2026_10_12.json'
LATE = 'canon/DELEGATED_THREEPEAT_2024_25_USED_ROUTES_AND_FINAL_COURTS_SELECTION_2026_10_09.json'
EPI = 'canon/DELEGATED_THREEPEAT_BRIEF_EPILOGUE_PREPARATION_ACCEPTANCE_2026_10_09.json'
ADAPTER = 'design/BASKETBALL_SCENE_RESEARCH_APPLICATION_2026_10_09.json'
OUT = 'design/THREEPEAT_CURRENT_40_FUNCTION_SCENE_BLUEPRINTS_2026_10_12.json'
MD = OUT.replace('.json', '.md')
REVIEW = 'reviews/THREEPEAT_CURRENT_40_FUNCTION_SCENE_BLUEPRINTS_2026_10_12_CODEX_CHECK.json'

# Individual editorial work. These are visible questions and switch conditions,
# not newly certified plays, coach motives, medical events or actual prose.
NOTES = [
 ('동갑이 먼저 도착한 자리와 자기 늦은 발을 본다.', '신체 차이보다 위치 선점·기술·판단을 구별한다.', '처음 받은 과제 안에서 끝까지 참여하되 무리한 만회 동작을 새로 추가하지 않는다.', '동갑의 선택을 주인공을 가르치기 위한 호의로 바꾸지 않는다.', '자존심 때문에 들어온 사람이 실패 뒤에도 남는 첫 이유.'),
 ('자기 아웃렛 뒤 동료가 끝낸 득점과 뒤의 박스아웃 실패를 함께 본다.', '공 확보와 자리 확보는 별개 과제다.', '공을 확보하면 연결하고, 뒤 과제에서는 먼저 위치를 확인한다.', '수신자의 마무리 판단은 수신자에게 남긴다.', '한 번은 필요한 사람이 되었지만 같은 성공을 반복할 수는 없다.'),
 ('자기가 맡은 공 준비 뒤 동료가 남은 몫만 하는 것을 본다.', '생활 전체가 개선됐다는 평가 대신 이 한 번의 노동 분담을 관찰한다.', '추가 게임을 시작하지 않고 이번 준비에 간다.', '동료의 남은 노동은 여전히 존재한다.', '칭찬이 없어도 다시 오는 행동이 첫 보상보다 오래 남는다.'),
 ('전달받은 경쟁 조건과 아직 답이 없는 학점 질문을 구별한다.', '생활 영어·학업 기록·경쟁 수준을 한 능력으로 합치지 않는다.', '준비 의사를 전하되 감독의 추천을 학교의 허가로 읽지 않는다.', '감독과 학교 담당자의 권한을 분리한다.', '미답을 숨기지 않은 이동 선택; 도착은 별도 절차 뒤다.'),
 ('자기가 요청한 도움 시간에 늦었다는 사실을 본다.', '수면 지연과 도움 접근 실패를 낮은 지능·담당자의 악의로 바꾸지 않는다.', '잃은 지원은 돌려받지 않고 다음 의무 순서부터 바꾼다.', '담당자의 이미 배정된 시간도 유한하다.', '다음 하루는 고칠 수 있지만 전날 도움은 사라졌다.'),
 ('골밑에 시선이 남아 두 번 늦게 돌아온 자신의 위치를 본다.', '출발 단서 부족·판단 지연·실행 지연을 구별한다.', '패스 시작을 단서로 시험하고 단서가 안 보이면 다시 위치부터 확인한다.', '코치의 설명은 허용된 영상과 과제 범위에서만 사용한다.', '쉬운 골밑 만족 대신 불편한 윙 과제를 선택한다.'),
 ('계속 수행한 제한 역할과 학교가 전달한 평가를 구별한다.', '추천·오퍼·졸업·Eligibility Center 자격을 각각 다른 결과로 둔다.', '자기 공부와 역할을 계속하고 기관 판정의 미답은 미답으로 남긴다.', '학교는 평가를 보낼 수 있으나 대학·기관의 판정을 대신하지 않는다.', '기다림만이 아니라 수행할 자기 몫이 생긴다.'),
 ('대학에서 맡은 좁은 도움·박스아웃 과제를 본다.', '리바운드 두 번을 쫓지 않는 비용과 선발권 부재를 구별한다.', '맡은 과제 안에서 움직이고 추가 공 추격이 맡은 자리를 비우면 중단한다.', '자기가 남겨 둔 공간에서 동료도 자기 과제를 한다.', '강팀에 들어갔다는 보상과 자기 자리가 작다는 압력이 함께 선다.'),
 ('우승이 끝난 뒤 자신이 수행한 연결과 동료들의 마무리를 돌아본다.', '팀 우승·자기 역할·개인 스타 인정은 다른 성취다.', '우승의 자기 몫을 좁게 남기고 개인 쇼케이스로 확대하지 않는다.', '동료의 득점·판단을 주인공의 지시 결과로 독점하지 않는다.', '첫 큰 우승 안에 자신의 기여가 있다.'),
 ('평가 과제에서 공격이 닫힌 자신의 동작을 본다.', '시도 실패와 스카우트의 비공개 평가를 분리한다.', '막힌 동작도 내놓고 수정은 이번 과제에 한정한다.', '평가자는 자기 기준이 있으나 속마음을 서술하지 않는다.', '드래프트 평가가 약점을 숨기는 자리가 아니다.'),
 ('CHI22 지명과 자기에게 전달된 계약·여름 일정만 안다.', '2018 대표팀 자리가 자신의 소유였다는 전제를 만들지 않는다.', '선택된 신인 여름 경로를 수행하고 국가대표 미참가를 확정 박탈로 쓰지 않는다.', '구단의 계약 담당 권한과 선수의 수행을 분리한다.', 'NBA 입단 보상과 선발·대표팀 권한 부재가 함께 남는다.'),
 ('NBA에서 늦은 발과 열린 컷·전환의 자기 마무리 기회를 함께 본다.', '처음 열린 공격과 지속 가능한 자가 창출을 구별한다.', '열린 창은 직접 끝내고 도움수비가 길을 닫으면 짧은 연결로 바꾼다.', '자기 추가 시도가 그날 출전한 LaVine·Markkanen 또는 벤치의 기회를 쓴다.', '신인도 직접 득점하는 보상; 완성형 공격수 인정과 분리한다.'),
 ('이미 놓친 Dec7 시범 기회가 다른 선수에게 넘어간 것을 본다.', '직전의 공격 성취와 시간 약속 실패를 상쇄하지 않는다.', '지난 기회를 돌려 달라 하지 않고 다음 준비를 수행한다.', '기회를 받은 동료에게 반환 의무를 부여하지 않는다.', '득점할 줄 알아도 역할 기회는 잃을 수 있다.'),
 ('개발 무대와 복귀 뒤 각각 남은 위치 오류를 본다.', 'GL 과제·NBA 속도·팀 분 배분을 동일한 성공 지표로 쓰지 않는다.', '직접 마무리와 수비·연결을 함께 시험하되 복귀 자체를 실력 인증으로 읽지 않는다.', 'GL52분 동안 해당 NBA85분을 받은 동료의 기회를 지우지 않는다.', '개발 무대 성취는 있지만 NBA 자리 재획득은 따로 남는다.'),
 ('열린 2점 창과 약한 손 쪽 첫 벽을 구별한다.', '운반 권한·마무리 능력·수신자의 지원이 같은 문제는 아니다.', '열린 창은 자기 공격으로 끝내고 첫 벽은 Coby·Satoransky에게 일찍 넘긴다.', 'Coby·Satoransky의 운반과 마무리는 독립된 역할이다.', '2년차에는 자기 공격 보상이 커져도 막힌 경로는 남는다.'),
 ('LaMelo가 시작한 공격에서 자기 컷·숏롤 창과 LaVine의 마무리 자리를 본다.', '득점 증가를 주PG 권한 획득으로 해석하지 않는다.', '자기에게 열린 창은 직접 끝내고 LM의 시작과 동료 공간은 보존한다.', 'LM·LV·Mark·Carter 각자의 시작과 종료 공간을 남긴다.', '3년차에는 조합의 부속만이 아니라 제한된 자기 종료 역할이 선다.'),
 ('짧은 전진과 숏롤에서 도움수비가 들어오는 서로 다른 시점을 본다.', '정보 부족·첫 읽기 지연·패스 실행을 하나의 실패로 합치지 않는다.', '도움이 늦으면 직접 끝내고 일찍 길을 닫으면 첫 수신자에게 반환한다.', '반환 받은 동료가 다시 결정한다. 성공을 P의 예측 능력으로 독점하지 않는다.', '자기 공격과 이양 중 선택할 수 있지만 두 번째 읽기는 아직 부족하다.'),
 ('새 Theis·Green 조합에서 자신이 전달받은 수비·연결 과제를 본다.', '새 동료 합류와 자기 지위 상승을 구별한다.', '허용된 역할 안에서 공격 창을 쓰고 개인 과시 때문에 새 과제를 버리지 않는다.', 'Theis·Green의 노동과 동료 공 확보를 생존전 승리의 독립 기여로 둔다.', '자기 공격이 생존전에 기여해도 Washington 승리는 모두의 결과다.'),
 ('Indiana 패배 뒤 자신의 좋은 공격과 늦은 첫 패스를 함께 확인한다.', '시즌 탈락과 개인 성장의 증거를 양립시킨다.', '성취를 지우지 않고 다음 과제는 첫 패스 시점으로 좁힌다.', '팀 탈락을 한 선수의 실패나 구단의 보복으로 만들지 않는다.', '3년차의 공격 성장은 남고 플레이오프 진입은 놓친다.'),
 ('동료 역할 비용이 드는 제한 엘보 시험을 준비한다.', '요청·코치의 허용·실전 성공을 분리한다.', '좁은 첫 동작 시험을 요청하고 닫힌 길이면 반환까지 과제에 포함한다.', '코치가 허용하고 동료가 시작·받기 역할을 수행한다. P는 지시권을 갖지 않는다.', '4년차에는 자기 공격을 시험할 근거가 생겼다.'),
 ('안쪽 유지 수비와 캐치 전 조기 도움을 구별한다.', '자가 창출 실패와 다른 이양 시점 실패를 따로 본다.', '열린 첫 동작은 직접 공격하고 조기 도움에는 더 일찍 반환·재배치한다.', 'LaMelo의 주PG·LaVine의 주득점원 기여를 득점순으로 지우지 않는다.', '20점 기대 역할과 스타 인정 경쟁이 선다. 선정 결과는 아직 주어지지 않는다.'),
 ('PHI와의 일곱 경기에서 좋은 공격과 막힌 공격을 함께 남긴다.', '정규 역할 성장·한 시리즈 실패·계약 자격은 별개다.', '공격 성취도 실패도 평가 자료에 내놓는다.', '다른 선수의 판단을 P가 구제해야만 유효한 기여로 만들지 않는다.', '4년차는 스타 경쟁으로 전진했지만 Apr30 탈락은 그대로다.'),
 ('확대된 자기 공격이 동료의 시작·마무리 기회를 줄이는 것을 본다.', '역할 확대와 동료의 실력 저하를 혼동하지 않는다.', '자기 종료와 연결 중 보이는 창을 고르고 계약을 새로운 지시권으로 읽지 않는다.', 'LM/LV는 줄어든 터치 안에서도 스스로 선택한다.', '공격을 맡는 만큼 자신이 쓰는 동료의 몫도 보인다.'),
 ('짧은 창조·반환·재진입을 한 시즌에서 반복하며 약한 손의 실패도 본다.', '좋은 전개 하나와 연간 경기 결과를 분리한다.', '실패를 숨기지 않고 다음 공격의 첫 벽을 다시 읽는다.', '가드의 시작·윙 마무리·빅맨 공간은 각각 남는다.', '2023의52–30/E6은 현재 선택 결과이며 추가 B 점수 보너스가 아니다.'),
 ('PHI가 주는 첫 벽과 현재 허용된 자신의 역할을 본다.', '지난 시즌 실패 기억과 이번 상대 행동을 구별한다.', '이번 역할 안에서 공격하고 과거 복수 때문에 무리하게 운반하지 않는다.', 'P36분의 비용은 Duarte14→10이며 모든 동료의 성공을 대체하지 않는다.', 'G4 뒤2–2; 이전 패배가 자동으로 환불되지는 않는다.'),
 ('G5·G6·G7을 각각 끝난 뒤의 상태로만 겪는다.', '계획과 끝난 경기, 다음 경기 진입을 순서대로 분리한다.', '이미 끝난 경기의 부담을 지고 다음 허용 역할을 수행한다.', '승패 전체를 자기 마지막 슛으로 만들어 동료를 지우지 않는다.', 'CHI4–3PHI의 첫 회수; 정확 개인 박스·마지막 슛은 미설계다.'),
 ('BKN의 KD·Harden·Kyrie와 자신의 수비 담당 범위를 본다.', '자기 수비 기여와 다섯 사람의 수비를 합치지 않는다.', '자기 담당·인계를 수행하고 다른 담당의 공백을 없는 것으로 만들지 않는다.', '현재 사용 코트에 없는 Caruso를 구원 수비자로 호출하지 않는다.', 'CHI4–2BKN; 공격 성장만으로 모든 수비가 해결되지 않는다.'),
 ('MIL전 앞선 세 패배 뒤 현재2–3을 안다.', '한 번 성공한 읽기와 상대의 다음 대응을 구별한다.', '이번에 확인한 단서로 준비하고 항상 통하는 대응이라 선언하지 않는다.', '상대는 자신의 다음 선택을 할 수 있다.', '우승 방향이 정해져 있어도 인물에게는 남은 두 기회만 보인다.'),
 ('LM·Mark가 자신의 공을 받은 뒤 각각 선택하는 행동을 본다.', '자기 이양과 동료의 독립 판단을 구별한다.', '넘긴 뒤 무볼 책임을 수행하되 동료의 판단을 대신하지 않는다.', 'LM·Mark의 기여가 P의 명령 이행으로 환원되지 않는다.', 'CHI4–3MIL; 첫 우승 문턱까지 공동 책임이 남는다.'),
 ('UTA전에서 LM의 시작·Mark의 공간·Carter의 스크린·LV의 마무리를 본다.', '첫 우승과 개인 FMVP·MVP를 구별한다.', '자기 공격과 동료 종료를 보이는 창에 따라 선택한다.', '다섯 사람의 기여를 자신의 예측·지시로 독점하지 않는다.', 'June15_2023 CHI4–2UTA 첫 우승; 개인상은 부여하지 않는다.'),
 ('첫 우승 뒤 자신의 자료·질문을 공동 준비에 내놓는다.', '개인 준비·구단 승인·등록·보험의 결정권을 구별한다.', '자기 준비는 계속하되 기관 허가가 필요한 행위는 허가 전 수행으로 쓰지 않는다.', '스태프·프런트는 각자의 담당을 가지며 P에게 공적 결정권을 넘기지 않는다.', '우승 뒤에도 함께 준비할 시간과 권한은 자동 보상이 아니다.'),
 ('서로 다른 방식의 개인 준비를 공동 과제와 대조한다.', '사적 훈련 참여와 국가대표 등록·금메달·편입을 구별한다.', '개인 과제만 준비하고 공적 참가·병역 실행은 C01 달력 해소 전 보류한다.', '라이벌도 자신의 방식과 자기 시간 비용을 가진다.', '완전한 화해 없이도 다른 방식의 유효성을 볼 수 있다.'),
 ('첫 방어에서 LM/LV의 시작과 자신의 낮은 연결·무볼 위치를 본다.', 'P의 점유 감소와 동료의 추가 움직임 노동을 따로 남긴다.', '선택된 공동 코트 범위에서 시작을 넘기고 비운 수비 위치를 다시 읽는다.', '동료의 보완 한 걸음은 비용이며 P가 사라진 공백을 공짜로 메운 것이 아니다.', '2024의 공동 책임이 실제 선택 코트로 이어진다.'),
 ('DEN전에서 넘긴 뒤 자신의 무볼 첫 연결과 상대의 응답을 본다.', '한 창의 실행과 전체 시리즈 우승을 분리한다.', '선택된2024 공동 시계 안에서 첫 운반을 양보하고 다시 연결한다.', 'LM의 시작과 DEN의 대응 권리는 각각 유지한다.', 'June20_2024 CHI4–2DEN 두 번째 우승; 옛 실행대기를 현재 대기로 재사용하지 않는다.'),
 ('리바운드 뒤 자기 공 소유와 다음 사람의 전진 자리를 본다.', '공 확보와 계속 운반할 권리를 동일시하지 않는다.', '긴 운반의 기회를 포기하면 무볼로 다시 참여한다.', '다음 수신자는 자신의 전진을 고른다.', '공을 놓아도 공격에서 사라지지 않는다.'),
 ('MIN전에서 라이벌 외의 공간·담당 위협도 함께 본다.', '라이벌을 존중하는 것과 모든 공격을 봉쇄하는 것을 분리한다.', '선택 코트의 도움·자기 자리 비용을 읽고 전부 막았다고 결론짓지 않는다.', '라이벌은 MIN32분 SG, Towns34분 C; Edwards를 MIN 선수로 복사하지 않는다.', '라이벌 밖의 위협 때문에도 마지막 선택이 어려워진다.'),
 ('윙 전진이 닫힌 뒤 다른 수신자·위치를 본다.', '길이 닫힌 관찰과 상대의 숨은 의도를 분리한다.', '선택된 역할 안에서 다른 길로 바꾸고 새 전술 지시권을 만들지 않는다.', '다른 길의 수신자도 자기 선택을 가진다.', '막혔을 때의 재선택이 마지막 공격으로 이어진다.'),
 ('자기에게 열린 종료와 더 유리한 동료를 함께 본다.', '항상 패스하는 미덕과 실제 선택을 구별한다.', '자기 종료도 선택지에 두되 그 공·시간은 한 번만 쓸 수 있다.', '동료에게 넘긴 경우 동료의 판단과 결과 통제권을 남긴다.', '초반 직접 공격 보상을 없애지 않으면서 최종 이양의 비용을 세운다.'),
 ('2025G7에서 라이벌의 실패 뒤 자기 리바운드와21.6초·CHI108–109MIN 상태를 본다. LM의 결승 득점은 아직 일어나지 않았다.', '선택된 마지막 득점과 미래 우승·개인상 목록을 분리한다.', '자기 최종 슛·통제권을 내려놓고 마지막 무볼 책임을 수행한다.', 'LM의 결승 득점은 독립된 판단이다. P의 공로로 대체하지 않는다.', 'June22_2025 CHI110–109MIN 삼연패; 옛2028 16초/108–107을 복사하지 않는다.'),
 ('June19 guest에서 본 후배의 준비를 June20 공개 은퇴에서 기억한다.', '서비스 종료·별도 허용 guest·공개 은퇴를 서로 다른 행위로 둔다.', '한 번 순서를 보여 주고 물러나며 후배의 과제를 다시 통제하지 않는다.', '후배·스태프에게 자기 행동과 권한을 남긴다.', 'June18→19→20_2035 순서; 후배의 속마음·미래 커리어는 닫는다.'),
]

B_OVERRIDES = {
12: ('늦은 NBA 발과 열린 첫 공격', '좁은 임무에서 전환·컷·풋백의 열린 창을 직접 끝내고, 첫 도움수비가 닫으면 짧게 연결한다.', '직접 끝낼 창과 연결할 창을 구별한다.', '그날 출전한 동료의 시도 기회를 쓰며 좁은 수비 과제는 남는다.', '직접 공격 성취가 앞당겨진다. 신인상·올루키·고정 개인 박스는 부여하지 않는다.'),
14: ('개발 무대의 공격과 남은 오류', '개발 무대에서 자기 마무리도 시험하고 수비·연결 오류를 드러낸 뒤, NBA 복귀에서 위치 오차를 다시 본다.', '득점 과시만도 실패 숨기기도 택하지 않는다.', '기존GL52분·NBA85분 반환과 그날 동료 시도 비용을 구별한다.', '첫 공격 성취와 복귀 뒤 한계를 함께 남긴다.'),
15: ('열린 공격과 약한 손의 첫 벽', '열린 전환·컷의 자기 종료를 쓰되 약한 손의 첫 벽에서는 Coby·Satoransky에게 일찍 넘긴다.', '자기 공격을 할 수 있는 조건과 포기 조건을 함께 둔다.', '추가 자기 2점 시도는 실제 당일 동료 기회를 사용한다. 이양한 공격의 종료 기회는 돌려받지 않는다.', '2년차12PPG는 작가용 기대 역할이다. 개별 득점·MIP·정확21–44/22–43 선택을 자동 부여하지 않는다.'),
16: ('다섯 시작권과 내 종료 역할', 'LM 시작에 맞춘 컷·숏롤·전환에서 자기 마무리를 쓰고 LV·Mark·Carter의 공간을 남긴다.', '주PG 권한을 가져오지 않고 자기에게 열린 종료를 선택한다.', '자기 추가 시도는 LV/LM/Mark/Coby/Young의 당일 기회를 사용한다.', '3년차 공격 성취와 시작권 분담이 함께 선다. 다섯 사람이 P를 위한 보조자로 고정되지 않는다.'),
17: ('도움 도착 전 내 공격, 도착 뒤 반환', '짧은 전진과 숏롤의 도움 도착 시점을 구별해 열린 창을 직접 끝내거나 첫 수신자에게 반환한다.', '닫힌 공격을 자기 종료로 억지로 바꾸지 않는다.', '첫 읽기·반환 지연의 시간과 동료 기회 비용은 남는다.', '직접 공격 보상은 있지만 빠른 수비·두 번째 읽기는 미완성이다.'),
18: ('새 조합의 내 공격과 생존전', '새 수비·연결 과제를 수행하며 허용된 공격 창을 쓰고 Washington 원정에서 동료 공 확보를 본다.', '자기 공격 성취와 새 조합의 노동을 같이 남긴다.', '조합 준비의 시간과 동료의 독립 실행이 필요하다.', '기존Washington 승리는 유지하며 전체 승리를 자기 공격 하나로 설명하지 않는다.'),
19: ('성장한 공격도 넘지 못한 탈락', 'Indiana 패배 뒤 자기 공격 성취와 첫 패스·무볼 위치의 부족을 함께 추려 다음 과제를 정한다.', '공격 성취를 지우지도 탈락을 숨기지도 않는다.', '31–41 뒤 탈락·진출 기회 손실은 그대로 남는다.', '3년차 공격 성장과 팀 한계가 함께 다음 시즌의 압력으로 간다.'),
20: ('자기 공격의 다음 시험을 요청하다', '동료 역할 비용을 함께 설명해 제한 엘보 시험을 허용받고 첫 동작·자기 종료·닫힐 때 반환을 준비한다.', '자기 공격을 시험하되 공동 에이스 권한부터 요구하지 않는다.', '자기 첫 동작과 동료 시작·받기 준비의 시간 비용을 남긴다.', '허용된 시험이 생긴다. 새 선발권·실전 성공·개인상은 자동 발생하지 않는다.'),
21: ('직접 공격과 스타 인정 경쟁', '열린 첫 동작을 자기 공격으로 끝내고 조기 도움에는 반환·재배치한다. 인정 비교는 투표와 발표의 각 시점에서 사용 가능한 자료만 놓는다.', '공격 창이 닫히면 접으며, 공개되지 않은 표·발표 결과는 알 수 없는 것으로 남긴다.', 'LM의 주PG와 LV의 주득점원 역할·추가 시도 비용을 지우지 않는다.', '4년차20PPG 기대 역할과 인정 경쟁을 앞당긴다. 정확 올스타·All-NBA·MVP는 미선택이다.'),
22: ('스타 경쟁 뒤에도 남는 PHI 실패', 'PHI 일곱 경기 뒤 자기 좋은 공격·막힌 공격을 함께 평가 자료에 내놓는다.', '공격 성취와 실패를 함께 보여 준다.', 'Apr30_2022 탈락과 동료의 기여·부담은 남는다.', '고정 E2/CX1을 보존한다. 올스타 후보를 계약 HigherMax 인정으로 바꾸지 않는다.'),
}

def normalized(path):
    return path.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode('utf-8')

def digest(path):
    return hashlib.sha256(normalized(path)).hexdigest()

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def ref(path, pointer=''):
    return {'path': path, 'source_sha256': digest(ROOT / path), 'json_pointer': pointer}

def scene(sid, order, purpose, claim, method, event_order=None, kind='CURRENT_PLAN'):
    return {'segment_id': sid, 'relative_order': order, 'purpose': purpose,
            'claim': {'text': claim, 'status': 'CANON_FUNCTION_DESIGN', 'temporal_kind': kind},
            'access': {'owner': 'PROTAGONIST', 'scene_order': order,
                       'acquired_order': order, 'event_order': event_order,
                       'method': method},
            'design_only': True, 'prose_read_or_generated': False}

def make():
    base = load(BASE)
    rows = []
    assert len(base['episode_rows']) == len(NOTES) == 40
    for i, (original, note) in enumerate(zip(base['episode_rows'], NOTES), 1):
        obs, diagnosis, switch, coactor, reward = note
        title, action, choice, cost, result = [original[k] for k in ('title','action','choice','cost','result')]
        sources = [ref(BASE, f'/episode_rows/{i-1}'), ref(ADAPTER)]
        if i in B_OVERRIDES:
            title, action, choice, cost, result = B_OVERRIDES[i]
        if 12 <= i <= 22:
            sources += [ref(B,'/B'), ref(ROLES), ref(IMPACT,'/current_working_response'), ref(RECOG,'/year1_to_year3')]
        if i in (33,34):
            sources.append(ref(LATE,'/selected_2024_DEN_first_defense'))
            result = '현재 선택된2024 공동 코트·우승 경로를 사용한다. 두 번째 우승은June20_2024 CHI4–2DEN이며 개인상·정확 개인 박스는 미선택이다.'
            if i == 33:
                action = '현재 선택된2024 공동 코트에서 시작을 넘긴 뒤 자기 무볼 위치와 동료 보완 노동을 함께 확인한다.'
            else:
                sources.append(ref(LATE,'/selected_seasons/0/selected_used_series/3'))
                action = 'June6_2024 Finals G1의2770→2788초에서 Carter의 확보·전진, P의LM 이양·오른쪽 레인 비우기, LM의 독립 시작을 사용한다. 이 창에는 슛·점수를 추가하지 않는다. June20 G6의 우승 종료는 별도 후행 장면으로 둔다.'
                result = 'June6 공동 학습의18초에는 슛·점수 미배정. 별도June20_2024 Finals G6 뒤 CHI4–2DEN 두 번째 우승을 확인한다.'
        if 35 <= i <= 39:
            sources.append(ref(LATE,'/selected_2025_last_attack'))
            if i == 39:
                action = '현재 선택된June22_2025 최종 시계의 라이벌 실패→P 리바운드21.6→전방16.6→동료 반환→P 최종 패스→LM 자기 릴리스0.2→혼→유효2점 검토→공개 종료 순서를 그대로 사용한다.'
                result = 'June22_2025 CHI110–109MIN/시리즈4–3/삼연패. LM이 자기 판단으로 최종 득점하며 P는 자기 종료·통제권을 내려놓는다.'
            elif i == 36:
                result = 'MIN Finals 진출·사용 코트는 현재 별도 선택으로 해결됐다. 이 기능은 자기 도움과 다른 위협의 비용을 비교하며 라이벌 전체 봉쇄·완전 화해는 선택하지 않는다.'
            elif i == 37:
                result = '현재 선택된2025 합법 사용 코트·상대·날짜 안에서 경로 변경 기능을 준비한다. 새 전술·클러치 개인 성공을 추가하지 않는다.'
            elif i == 35:
                result = '현재 선택된2025 코트로 이어지는 통합 기능이다. 공 확보 뒤의 긴 운반과 재참여를 구별하며 모든 압박에서 자동 성공하지 않는다.'
        if i in (31,32,40):
            sources.append(ref(EPI))
        if i == 34:
            window = '2024년6월6일 DEN Finals G1 공동 학습2770–2788초→별도6월20일 Finals G6 우승 종료'
        elif i == 39:
            window = '2025년6월22일 MIN Finals G7의 현재 선택 최종 공격과 종료 이후'
        else:
            window = original['window']
        if i in (33,35,36,37,38):
            window = ('2023–24' if i == 33 else '2024–25') + ' 현재 선택된 사용 경로; 개별 정확 장면 배치는 최종N 단계에서 분리'
        # The viewpoint sees its own actions; source spreadsheets and season
        # projections remain editor-only, never silently enter a player's head.
        segments = [
            scene('S1', 1, '현재 문제·관찰', obs, '자기 참여·직접 보이는 위치 또는 이미 받은 본인 과제'),
            scene('S2', 2, '권한 안의 선택·전환', switch, 'S1 관찰을 바탕으로 자신의 선택을 한다'),
            scene('S3', 3, '남는 비용·다음 압력', coactor, '자기 포기·직접 보이는 동료 행동; 동료의 속마음은 접근하지 않는다'),
        ]
        if i == 26:
            segments = [scene(f'G{g}', j, '끝난 경기의 상태→다음 경기',
                              f'G{g}은 끝난 뒤에만 결과를 안다. 다음 경기 승패는 계획과 분리한다.',
                              '참여한 경기 종료·보이는 최종 상태', j, 'OBSERVED_EVENT')
                        for j, g in enumerate((5,6,7),1)]
        if i in (30,34,39):
            segments.append(scene('END',4,'현재 선택 경기 종료 확인',reward,
                                  '참여한 경기 종료 뒤 보이는 최종 상태; 미래 시즌은 모른다',4,'OBSERVED_EVENT'))
        if i == 40:
            segments = [
                scene('SERVICE_END',1,'서비스 종료와 guest 권한 분리',
                      'June18 서비스 종료와 June19 별도 허용 guest는 다른 행위다.',
                      '본인 서비스 종료·별도 허용 확인; C01 날짜 가용은 미해소'),
                scene('GUEST',2,'물러난 뒤 후배 실행',
                      'June19 준비 순서를 한 번 보여 준 뒤 후배의 독립 실행을 본다.',
                      '직접 관찰',2,'OBSERVED_EVENT'),
                scene('RETIRE',3,'은퇴에서 이미 본 행동만 기억',
                      'June20 공개 은퇴에서 June19에 본 준비를 기억한다. 후배의 미래는 모른다.',
                      '이전 직접 관찰의 기억',2,'OBSERVED_EVENT'),
            ]
            segments[-1]['access']['acquired_order'] = 2
        early = 12 <= i <= 22
        deps = ['C01_CALENDAR_USED_AVAILABILITY'] if i in (31,32,40) else []
        rows.append({
            'function_cluster_id': f'FC{i:03}', 'source_candidate_cluster': i,
            'final_episode': None, 'unit_id': original['unit'],
            'status': 'INDIVIDUAL_FUNCTION_SCENE_DESIGN_PREPARED_NOT_ACTUAL_BLUEPRINT_AUTHORITY',
            'title': title, 'category': 'POST_NBA' if i == 40 else original['category'],
            'timeline_window': window, 'entry_state': original['entry'],
            'episode_function': reward, 'action_choice': action + ' ' + choice,
            'durable_cost': cost, 'state_change': result,
            'next_entry_state': original['next_entry'],
            'observation_and_diagnosis': {'visible_observation': obs, 'competing_explanations': diagnosis,
                                        'new_cause_selected': False, 'medical_claim_added': False},
            'abort_or_switch_condition': switch, 'independent_coactor_contribution': coactor,
            'scene_specs': segments,
            'information_boundary': {
                'status': 'RELATIVE_ACCESS_PREPARATION_NOT_SELECTED_SCENE_ACCESS_LOCK',
                'pov_direction': 'PROTAGONIST_CLOSE_THIRD',
                'absolute_date_invented': False, 'clock_basis': '이 기능 내 상대 순서',
                'author_expected_stats_are_pov_facts': False,
                'season_result_known_before_game_end': False,
                'coach_vote_submission_deadline_certified': False,
                'forbidden': ['미래 결과·수상','타인의 비공개 의도','작가용 평점·Γ·모델 잔차','사적 임상 판단'],
            },
            'primary_devices': ['BOUNDED_OWN_ATTACK','SHARED_ROLE_COST'] if early else ['CHOICE_AND_DURABLE_COST'],
            'physical_state': '기존 선택된 가용·역할 범위만 사용; 새 부상·피로 수치·의료 소견 추가0',
            'relationship_state': coactor,
            'personal_award_use_mode': 'NOT_USED',
            'used_dependencies_remaining': deps,
            'source_refs': sources,
            'promise_roles': copy.deepcopy(original.get('promise_roles',[])),
            'final_density_review': '기능 수는 회차 수가 아니다. 복수 경기·기관 절차·발표 시점은 최종 배치에서 합치거나 나눈다.',
            'manuscript_allowed': False,
        })
        if i == 34:
            rows[-1]['scene_specs'][0]['date'] = '2024-06-06'
            rows[-1]['scene_specs'][1]['date'] = '2024-06-06'
            rows[-1]['scene_specs'][2]['date'] = '2024-06-06'
            rows[-1]['scene_specs'][-1]['date'] = '2024-06-20'
            rows[-1]['scene_specs'][-1]['claim']['text'] = 'June20_2024 G6가 끝난 뒤 CHI4–2DEN 두 번째 우승을 안다. June6 학습 창 자체에는 점수를 부여하지 않는다.'
    # Dedicated B recognition ports are editorial comparisons, not a fictional
    # news article, actual ballot receipt or a selected award outcome.
    rows[20]['recognition_ports'] = [{**copy.deepcopy(r),
                                    'source_ref': ref(RECOG,f'/date_context/{j}'),
                                    'claim_use': 'EDITOR_ONLY_EXPECTED_INPUT_NOT_CHARACTER_QUOTED_ACTUAL_STATS',
                                    'selected_award': False}
                                   for j,r in enumerate(load(RECOG)['date_context'])]
    rows[20]['recognition_options_ref'] = ref(RECOG,'/candidate_routes')
    rows[20]['recognition_selected_candidate'] = None
    promises = copy.deepcopy(base['five_promise_function_consumption'])
    for p in promises:
        p['current_function_ids'] = {k:[f'FC{n:03}' for n in p[k]]
                                     for k in ('plant_candidates','variation_candidates','payoff_candidates')}
        p['current_endpoint'] = '2035-06-19/20 conditional guest/retirement' if p['id'] in ('P2','P4') else '2025-06-22 selected final court'
        p['actual_prose_payoff_verified'] = False
    return {
        'id': 'THREEPEAT_CURRENT_40_FUNCTION_SCENE_BLUEPRINTS_2026_10_12',
        'baseline_main': '902c4d959cf95391d5100000d51eb786b48967b5',
        'producer_id': 'root_codex',
        'status': 'CURRENT_40_INDIVIDUAL_FUNCTION_SCENE_DESIGNS_PREPARED_NOT_FINAL_N_OR_ACTUAL_AUTHORITY',
        'scope_ref': ref(SCOPE), 'source_hash_method': 'UTF8_BOM_removed_LF_SHA256',
        'source_sha256': {p:digest(ROOT/p) for p in (BASE,SCOPE,B,ROLES,IMPACT,RECOG,LATE,EPI,ADAPTER)},
        'count': {'function_designs_prepared':40,'B_year1_to4_designs':11,
                  'final_episode_count_locked':None,'actual_blueprint_authorities_issued':0,
                  'actual_pack_count':0,'prose_read_or_revised':0},
        'category_diagnostic_only': {'counts':dict(Counter(r['category'] for r in rows)),
                                    'NBA_plus_draft': '30/40 = 75%', 'strict_NBA':'28/40 = 70%',
                                    'EPI_is_POST_NBA':True,'selected_final_policy':False,
                                    'function_ratio_is_final_episode_ratio':False},
        'individual_function_designs': rows, 'five_promise_consumption':promises,
        'current_priority': 'B own-attack and later selected courts override older birth-generation passing-only/pending wording in this preparation; original source bytes remain.',
        'external_2026_AG_fact_vs_2023_design': {
            '2026_official_gold_roster_includes_Lee_Hyunjung': True,
            'source':'https://www.korea.kr/news/policyNewsView.do?newsId=148972552',
            'read_date':'2026-10-12','individual_military_admission_verified':False,
            'current_mma_service_months':34,'current_mma_volunteer_hours':544,
            'mma_source':'https://www.mma.go.kr/navigation/contents.do?mc=mma0000758',
            'current_page_certifies_2023_individual_admission':False,
            'C01_2023_gold_or_admission_selected_by_question':False,
        },
        'tools_this_pass': {'Codex':'LOCAL_SOURCE_READ_EDIT_AND_CHECK', 'web':'KOREA_GOLD_ROSTER_AND_MMA_CURRENT_BODY_READ',
                            'Antigravity':'NOT_RUN','NotebookLM':'NOT_RUN','Claude':'NOT_RUN',
                            'independent_agent':'NOT_RUN','source_blind_review':'NOT_RUN'},
        'remaining':['C01 selected used-date availability','exact personal award remains NOT_USED unless chosen',
                     'final-N density allocation and episode numbering','whole selected-history exit lock',
                     'independent current input acceptance','individual ACTUAL Blueprint authority and Pack'],
        'gates': {'freeze':'v0.30 PARTIAL','design_gate':'CLOSED','manuscript_allowed':False},
        'unfinished_major_groups':4,'unfinished_through_group6':3,
    }

def validate(doc):
    assert doc['count']['final_episode_count_locked'] is None
    assert doc['count']['actual_blueprint_authorities_issued'] == doc['count']['actual_pack_count'] == 0
    for path, wanted in doc['source_sha256'].items():
        assert digest(ROOT/path) == wanted, ('stale source',path)
    rows = doc['individual_function_designs']
    assert [r['function_cluster_id'] for r in rows] == [f'FC{i:03}' for i in range(1,41)]
    assert list(dict.fromkeys(r['unit_id'] for r in rows)) == [f'M{i:02}' for i in range(1,10)] + ['EPI']
    for r in rows:
        assert r['final_episode'] is None and r['personal_award_use_mode']=='NOT_USED'
        assert 1 <= len(r['primary_devices']) <= 2
        assert all(r[k] for k in ('entry_state','action_choice','durable_cost','state_change','next_entry_state'))
        assert not r['information_boundary']['author_expected_stats_are_pov_facts']
        previous = 0
        for s in r['scene_specs']:
            access=s['access']; order=s['relative_order']
            assert order > previous and access['owner']=='PROTAGONIST'
            assert access['acquired_order'] <= order == access['scene_order']
            if s['claim']['temporal_kind']=='OBSERVED_EVENT':
                assert access['event_order'] <= access['acquired_order']
            previous=order
        for source in r['source_refs']:
            assert digest(ROOT/source['path'])==source['source_sha256']
            value=load(source['path'])
            for token in source['json_pointer'].split('/')[1:]:
                token=token.replace('~1','/').replace('~0','~')
                value=value[int(token)] if isinstance(value,list) else value[token]
    assert rows[39]['category']=='POST_NBA'
    assert Counter(r['category'] for r in rows)==Counter(PRE_NBA=9,NBA_DRAFT=2,NBA=28,POST_NBA=1)
    ports=rows[20]['recognition_ports']
    assert [(p['cutoff_exclusive'],p['CHI_games']) for p in ports]==[('2022-01-22',44),('2022-01-27',47),('2022-02-03',50)]
    assert all(not p['selected_award'] and p['same_day_games_excluded'] for p in ports)
    assert rows[20]['recognition_selected_candidate'] is None
    assert [i+1 for i,r in enumerate(rows) if r['used_dependencies_remaining']]==[31,32,40]
    assert 'June20_2024' in rows[33]['state_change']
    assert '110–109' in rows[38]['state_change']
    late=load(LATE)
    assert rows[33]['scene_specs'][0]['date']==late['selected_2024_DEN_first_defense']['use_date']
    assert rows[33]['scene_specs'][-1]['date']==late['selected_seasons'][0]['selected_used_series'][3]['games'][-1]['date']
    assert '108–109' in rows[38]['scene_specs'][0]['claim']['text']
    assert '110–109' not in rows[38]['scene_specs'][0]['claim']['text']

def render(doc):
    lines=['# 현재 9막·40기능의 개별 장면 Blueprint 준비','',
           '원고 없이 설계만 작성했다. 40은 기존 기능 묶음 수이며 최종 회차 N이 아니다. 개별 ACTUAL Blueprint·Pack 권한0, 원고0, v0.30 PARTIAL/CLOSED를 유지한다.','',
           '## 이번에 실제 바뀐 설계','',
           '- FC012–022: B안의 직접 공격·중단 조건·동료 시도 비용을11개 기능에 연결했다. 기대 평균은 작가용 입력이며 인물이 인용하는 확정 실적이 아니다.',
           '- FC033–039: 이미 선택된2024 DEN/2025 MIN 경로·최종LM 독립 득점을 소비한다. 옛 준비표의 미실행 문구를 현재 미선택으로 재사용하지 않는다.',
           '- FC031/032/040: 개인 준비·별도guest와 대표팀/병역의 공적 실행을 분리한다. C01 날짜 가용은 보류이며 금메달을 자동 선택하지 않는다.',
           '- 40기능의 진입·선택·비용·다음 압력과 상대정보 접근을 개별 작성했다. 복수 게임/발표를 품은 묶음은 최종 회차 밀도 배치에서 나눈다.','',
           '## 대표팀·병역 질문','',
           '[정부2026 금메달 명단](https://www.korea.kr/news/policyNewsView.do?newsId=148972552)에 이현중이 포함돼 있다. 개인 병무 편입 완료는 이 명단으로 확인되지 않는다. [현재 병무청 복무 안내](https://www.mma.go.kr/navigation/contents.do?mc=mma0000758)는34개월 해당 분야 복무·544시간 봉사를 설명한다. 이를 주인공2023의 참가·우승·편입 완료로 옮기지 않는다. 기존2023 권고 경로는 별도 선택·허가·당시 제도·사용 달력의 해결이 필요하다.','',
           '## 기능별 개별 설계','']
    for r in doc['individual_function_designs']:
        lines += [f"### {r['function_cluster_id']} · {r['unit_id']} · {r['title']}",'',
                  f"- 시간: {r['timeline_window']}",f"- 진입: {r['entry_state']}",
                  f"- 관찰/다른 설명: {r['observation_and_diagnosis']['visible_observation']} {r['observation_and_diagnosis']['competing_explanations']}",
                  f"- 행동·선택: {r['action_choice']}",f"- 포기·전환: {r['abort_or_switch_condition']}",
                  f"- 비용/동료 독립성: {r['durable_cost']} {r['independent_coactor_contribution']}",
                  f"- 바뀐 상태/독자 보상: {r['state_change']} {r['episode_function']}",
                  f"- 다음 진입: {r['next_entry_state']}",
                  '- 접근 순서: '+ ' → '.join(s['segment_id'] for s in r['scene_specs']),
                  '- 잔여 사용 의존성: '+(', '.join(r['used_dependencies_remaining']) or '이 기능 준비 단계에서 추가 없음; 최종N/현재 전체 입력 검수는 공통 후행'), '']
        if r.get('recognition_ports'):
            lines += ['선정 비교는Jan22미만44경기,Jan27미만47경기,Feb3미만50경기를 분리한다.50은 리저브 발표 전 상한이며 실제 코치 제출 마감 인증이 아니다. A/B/C/D와 실제 선정은 미선택이다.','']
    lines += ['## 분배·약속·끝맺음','',
              'LaMelo는 시작/최종독립득점, LaVine은 주득점원, Markkanen은 공간·자기 마무리, Carter는 스크린·리바운드, Coby/Satoransky는 운반, Theis/Green은 새 조합 노동을 가진다. 벤치의 분 비용과 슛 시도 비용을 이중 차감하지 않는다. P는 선수이며 스태프·프런트·국가대표 등록 담당의 권한을 갖지 않는다.','',
              '다섯 약속의 심기·변주·회수 대상 FC를 JSON에 연결했다. P1/P3/P5는 현재2025 최종 코트, P2/P4는 조건부2035 guest/은퇴로 연결한다. 본문 약속 회수·독자 견인력은 원고가 없으므로 검수 완료가 아니다.','',
              '기능 태그 진단은 PRE9/NBA_DRAFT2/NBA28/POST1이다. EPI를NBA로 세지 않는다. NBA+draft30/40=75%, NBA만28/40=70%이며 이는 최종 회차 비율 정책 선택이 아니다. 비율을 높이려고 경기나 설명을 늘리지 않는다.','',
              '## 검사와 도구','',
              '재현: `C:/Python314/python.exe -B -X utf8 tools/build_threepeat_current_function_scene_blueprints.py --check`',
              '현재9개 출처 핀·40개별 설계·정보 접근 순서·11 B 연결·3 인정 날짜·3 C01 의존성을 확인했다. 미래 지식/투표 컷 혼동/후일담 NBA 오분류 반례를 검사한다. 동일 생산자의 Codex 검사이며 신규 독립 검수는 아니다. Antigravity/NotebookLM/Claude/하위agent는 이번에 실행하지 않았다.','',
              '## 전체 진행','',
              '| 번호 | 작업 | 현황 |','|---|---|---|',
              '|1|2020 드래프트 연쇄|완료|','|2|Chicago2020–21|기존 선택 시즌 완료|',
              '|3|2021–23 거래·계약|완료|','|4|커리어·B안|영향·인정 후보 연결, C01 미해소|',
              '|5|결말·전체 구조|9막·현재코트 연결, 전체 역사LOCK/최종N 미완료|',
              '|6|집필 규격·Pack|독서110/110·40개별 기능 장면 설계 준비, 최종 회차 Blueprint/Pack 미완료|',
              '|7|통합·독립·작가 승인|미완료|','',
              '미완료 큰 작업4개,6번까지3개. 다음: 복수 사건을 품은 기능의 회차 밀도 배치와 사용 달력의 권위 연결; ACTUAL 입력·Pack는 필요한 선택/검수가 충족된 뒤 발급한다.','']
    return '\n'.join(lines).encode('utf-8')

def encode(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true')
    parser.add_argument('--refresh-untracked',action='store_true',help='Repair only these owned, not-yet-tracked generated drafts')
    args=parser.parse_args()
    doc=make(); validate(doc)
    rejected=[]
    for name, mutate in [
        ('FUTURE_OBSERVATION', lambda d:d['individual_function_designs'][39]['scene_specs'][2]['access'].update(acquired_order=4)),
        ('STARTER_BALLOT_FUTURE_50_GAMES', lambda d:d['individual_function_designs'][20]['recognition_ports'][0].update(CHI_games=50)),
        ('EPI_COUNTED_AS_NBA', lambda d:d['individual_function_designs'][39].update(category='NBA')),
        ('JUNE6_LEARNING_MOVED_TO_JUNE20', lambda d:d['individual_function_designs'][33]['scene_specs'][0].update(date='2024-06-20')),
        ('LM_SCORE_KNOWN_BEFORE_FINAL_PASS', lambda d:d['individual_function_designs'][38]['scene_specs'][0]['claim'].update(text='CHI110–109MIN을 이미 알고 최종 패스를 고른다.')),
    ]:
        wrong=copy.deepcopy(doc); mutate(wrong)
        try: validate(wrong)
        except AssertionError: rejected.append(name)
        else: raise AssertionError('False pass: '+name)
    outputs={OUT:encode(doc),MD:render(doc)}
    review={'id':'THREEPEAT_CURRENT_40_FUNCTION_SCENE_BLUEPRINTS_2026_10_12_CODEX_CHECK',
            'status':'LOCAL_CODEX_SOURCE_AND_ACCESS_CHECK_NOT_INDEPENDENT_ACCEPTANCE',
            'source_sha256':doc['source_sha256'],'source_pins':9,'function_scene_designs':40,
            'B_connected':11,'required_C01_preparation_holds':[31,32,40],
            'rejected_semantic_counterexamples':rejected,
            'output_LF_SHA256':{p:hashlib.sha256(b).hexdigest() for p,b in outputs.items()},
            'final_N':None,'actual_blueprint_authorities':0,'actual_packs':0,'independent_review_completed':False}
    outputs[REVIEW]=encode(review)
    for name,content in outputs.items():
        path=ROOT/name
        if args.check:
            assert path.is_file() and normalized(path)==content, ('output mismatch',name)
        else:
            path.parent.mkdir(exist_ok=True,parents=True)
            if path.exists():
                if normalized(path)!=content:
                    assert args.refresh_untracked, ('will not overwrite different bytes',name)
                    tracked=subprocess.run(['git','ls-files','--error-unmatch','--',name],cwd=ROOT,capture_output=True)
                    assert tracked.returncode==1, ('will not overwrite tracked artifact',name)
                    path.write_bytes(content)
            else:
                path.write_bytes(content)
    print(json.dumps({'mode':'check' if args.check else 'write','functions':40,'B':11,
                      'source_pins':9,'counterexamples_rejected':rejected,'ACTUAL':0,'Pack':0},ensure_ascii=False))

if __name__=='__main__':
    main()
