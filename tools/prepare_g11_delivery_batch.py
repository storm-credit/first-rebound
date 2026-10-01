"""Assemble already observed numbers and authored derivatives, not a new browser capture."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = 'research/G11_RIDI_INFORMATION_DELIVERY_FIRST_FIVE_2026_10_01'
prior = json.loads((ROOT / 'research/G11_RIDI_FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json').read_text(encoding='utf-8'))
# Literal query set selected after reading; not an entity recognizer or exhaustive terminology inventory.
rows = [
('라우치타스',23,1,22,1),('게이트석',6,1,23,57),('엘릭서',1,1,30,13),('포션',1,1,31,12),
('한유현',8,1,43,1),('양육자',31,1,49,5),('마지막 보답',2,1,50,12),('기간트 실드',1,1,96,1),
('푸른 버들잎',2,2,25,1),('드래곤 슬레이어',9,2,77,9),('인벤토리',2,2,91,28),('소원석',6,2,85,1),
('해연',4,3,7,3),('각성 브로커',6,3,12,8),('협회',5,3,20,78),('센터',2,4,25,30),
('한유진',2,3,66,6),('완벽한 양육자',12,3,70,9),('내 새끼가 최고',5,3,75,16),('정신력 업',1,4,16,0),
('민첩 업',1,4,17,0),('에밀리 스펜스',1,4,23,75),('헌터 자격증',1,4,28,4),('독 저항',2,4,43,0),
('저주 저항',2,4,44,0),('공포 저항',3,4,45,0),('라우치타스의 천적',3,4,46,0),('마지막 보은',4,4,95,0),
('우리 애가 이렇게나 잘났다',3,4,96,0),('될성부른 떡잎',6,4,97,0),('김성한',11,5,18,7),
('불굴의 육체',1,5,47,0),('재생력',1,5,48,0),('대지의 방패',2,5,49,0),('발 구르기',2,5,51,89),
('박예림',1,5,141,22),('명동역',1,5,142,30)]
terms = [dict(id=f'T{i+1:02}', literal=t, selected_literal_match_count=n,
              first_in_cohort=dict(chapter=c, raw_p_index=p, utf16_offset=o))
         for i,(t,n,c,p,o) in enumerate(rows)]
def case(cid, chapter, anchors, domain, state, summary, limit):
    return dict(id=cid, chapter=chapter, anchors=anchors, domain=domain,
                event_status=state, interpretation_status='INFERENCE',
                own_functional_paraphrase=summary, boundary=limit)
cases = [
case('C01',1,[22,23],'term_space_cause','INSTRUCTION',
     '도구를 건네며 출구의 위치·시간·일회 사용 조건을 제시한다.', '그 경로로 탈출한 사건은 아님.'),
case('C02',1,[30,31],'term_cause','REPORTED_LIMIT',
     '치료 자원 질문에 부재·효과 부족과 상처의 추가 조건을 답한다.', '치료 실험이나 객관적 의료 인증 아님.'),
case('C03',1,[96,97],'term_cause','OBSERVED_WITH_FORECAST',
     '기술 발화 뒤 몸을 둘러싼 빛을 보여 주고 강화된 방어를 예상한다.', '발현은 관측, 깨물림을 버틴 결과는 예측.'),
case('C04',1,[99,100],'space','OBSERVED',
     '벽 틈에서 걸어나오자 넓은 공동 반대쪽 적이 시야에 들어온다.', '이동·시야 연결이며 거리 수치/전체 지도는 없음.'),
case('C05',2,[16,20,25,26,27,31,34],'space_term_cause','OBSERVED_WITH_PAST_REPORT',
     '적의 돌진에 뛰어 회피하고 보이는 발판으로 더 높이 움직인다.', '과거 형제의 사용 설명을 현재 비행 기술 보유로 바꾸지 않음.'),
case('C06',2,[42,50,56],'space_cause','OBSERVED',
     '두 머리를 차례로 파괴한 뒤 남은 기존 부상까지 연결해 시야 상실·움직임 정지를 서술하고 거체 위에 앉는다.', '몸체 위 착석은 관측; 공격 전 과정의 좌표/포제션 재현 아님.'),
case('C07',2,[60,67],'cause','FORECAST_AND_CONJECTURE',
     '효과 종료 후 위험을 예상하고 던전 등급과 괴물의 불일치를 의문으로 제시한다.', '예상 사망·관리자 오류는 실행/확정 사실 아님.'),
case('C08',3,[12,17,18,20],'term_profession','PAST_AND_FUTURE_KNOWLEDGE_REPORT',
     '연락 기록의 직업명을 부정적 정의·거래 행태·제도 변화 전망으로 풀어 낸다.', '주인공이 현재 시점에 직접 검증한 거래/정책 시행 아님.'),
case('C09',3,[3,11,23],'space_cause','OBSERVED_AND_RECOGNITION',
     '낯선 침대의 감각과 휴대전화 날짜를 확인한 뒤 기억으로 건물 객실을 특정한다.', '확인·기억의 경로이며 객실로 이동하는 장면은 아님.'),
case('C10',4,[53,54,55,58,60,61],'term_cause','RULE_TO_ROLE_REASONING',
     '저항 효과 목록을 신체 방어·공격의 별도 필요에 대입해 본인과 상위 전투원의 효용을 비교한다.', '숫자 등급 나열만으로 실제 전투 성과가 확정되지 않음.'),
case('C11',4,[148,149,150],'space_cause','RULE_TO_ROLE_REASONING',
     '짧은 지속 시간과 입장 인원 제한을 보스전 전 지원 가능성에 대입한다.', '근접 필요는 인물의 운용 판단이며 실제 이동/최대 사거리 측정 아님.'),
case('C12',4,[23,164,166],'profession_expression','EXEMPLIFICATION_AND_THEORY',
     '치유 전문 인물과 농사·고객 응대 사례, 상황별 능력 가설을 설명에 사용한다.', '전문 직업의 현재 수행 장면·과학적 실제 법칙·직업 밀도 인증 아님.'),
case('C13',5,[15,26,31,38,69,82],'space_term_cause','OBSERVED_WITH_UNEXECUTED_ROUTE',
     '객실을 나서다 팔을 잡혀 제지되고 공포 저항의 한계를 판단한 뒤 돌아와 방을 돌고 침대에 앉는다.', '택시 10분은 이동 예상; 협회 도착/등록은 없음.'),
case('C14',5,[41,47,48,49,58,62],'term_cause','OBSERVED_TEST_AND_RULE_INFORMATION',
     '상대를 대상으로 능력을 확인하자 실패한 기술과 최적화 금지 조건, 다른 성장 가능성이 안내된다.', '정보 획득을 재각성/실패 기술 획득 성공으로 바꾸지 않음.'),
case('C15',5,[118,136,141,142],'space_profession_cause','ORDER_AND_PLAN_WITH_FUTURE_KNOWLEDGE',
     '전화 속 이사 준비 지시와 보호 계약 구상, 기억 속 후보 거주지를 분리한다.', '이사 완료·계약 체결·후보 방문/영입은 없음; 판타지 계약은 NBA CBA가 아님.'),
case('C16',4,[40,43,44,45,46,53,54,55,60],'expression','LIST_THEN_CONDITIONAL_REASONING',
     '효과 목록 뒤에 적용 조건과 본인에게 남는 제약을 붙이는 선정 사례다.', '목록 형식만으로 AI/번역/보고서체 판정이나 작품 전체 빈도 인증을 하지 않음.'),
case('C17',5,[31,38,58,62,69],'expression','INTENTION_OBSTRUCTION_INFORMATION_DECISION',
     '외출 전망·제지·불충분한 효과·실패 조건 확인을 거쳐 방으로 돌아가는 선정 사례다.', '장애와 판단 연결은 국소 관측; 독자 반응/공통 문체 효과의 인과 인증 아님.')]
records=[]
for r in prior['records']:
    m=r['first_capture']
    records.append(dict(chapter=r['chapter'], url=m['url'], document_title=m['document_title'],
        body_sha256=m['body_sha256'], body_utf16=m['body_utf16'], body_p_count=len(m['paragraph_meta']),
        second_capture=dict(body_sha256=m['body_sha256'], same_selected_literal_positions=True,
                            intervening_chapter=5 if r['chapter']==1 else r['chapter']-1)))
data=dict(schema_version=1, work=prior['work'], baseline_main='23f40cd', common_skill_commit='f3af0eb',
    raw_novel_text_retained=False, raw_novel_text_uploaded=False,
    readings_added=0, unique_readings_unchanged=95, unread_chapters_unchanged=15,
    component_chapters=5, remaining_component_chapters=45, component_denominator=50,
    components_share_same_chapters=True, whole_P3_completed_chapters=0,
    complete_entity_inventory=False, complete_term_inventory=False, complete_space_cause_inventory=False,
    professional_action_density=None, independent_original_semantic_review=False,
    universal_house_style_rule=False, author_locked=False, actual_episode_packs=0,
    manuscript_allowed=False, freeze='v0.30 PARTIAL', gate='CLOSED', G11_final=False,
    browser_capture_sequence=[1,2,3,4,5]*2, normalization='p.textContent: remove U200B-D/U2060/U2063/UFEFF, trim; exclude title p0/empty; join two LF',
    matching_unit='CASE_SENSITIVE_LITERAL_SUBSTRING_UTF16_WITHIN_NONEMPTY_BODY_P',
    aliases_or_coreferences_resolved=False, nested_matches_not_deduplicated=True,
    selected_literal_count=37, selected_literal_match_count=174,
    literal_count_is_distinct_entity_count=False, lexical_counts_are_density=False,
    selected_terms=terms, records=records, selected_cases=cases,
    exceptions=[dict(id='X01',term_ids=['T06','T18'],kind='NESTED_MATCH',
                     observation='긴 명칭 내부에도 짧은 명칭이 일치한다. 독립 언급으로 합산하지 않는다.'),
                dict(id='X02',term_ids=['T16'],kind='HOMOGRAPH_IN_COMPOUND',
                     observation='4화 p25의 시설과 p164의 고객 응대 직장에 같은 부분 문자열이 일치한다. 동일 기관으로 합치지 않는다.'),
                dict(id='X03',term_ids=['T07','T28'],kind='DIFFERENT_LITERAL_RELATED_LABEL',
                     observation='두 시점의 비슷한 효과명은 다른 문자열로 유지하며 오탈자/동일 엔티티를 자동 확정하지 않는다.')],
    candidate_questions=[
        '새 용어가 현재 행동·대상·판단의 어느 지점에서 필요해지는가?',
        '위치 단서→실제 이동→시야/접촉 결과가 연결되는가? 지시·계획·거리 예상과 구별했는가?',
        '규칙 설명→역할 제약→다음 판단이 연결되는가? 예측/인물 가설을 사건 결과로 바꾸지 않았는가?',
        '직업 사례와 현재 직업 수행을 구별했는가? 목록/추상 설명의 쓰임을 문맥으로 판단했는가?'],
    candidate_status='ONE_WORK_LOCAL_QUESTIONS_ONLY_CROSS_WORK_SYNTHESIS_HOLD')
# Same-source numeric metadata is a comparison baseline, not a new capture certification.
(ROOT/(P+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('37 selected literals / 174 substring matches / 17 selected cases / same 5 chapters')
