"""Select a source-limited A01-S3 comparison without inventing US acceptance.

The 2016 prep move is existing canon. A student's 2015 information lookup is
new routine fictional design, and a historical tournament bracket only proves
competition structure, not individual skill superiority or in-world access.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a01_e6_final_episode_function as e6


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A01_CF10_PREP_COMPARISON_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A01_CF10_PREP_COMPARISON_WORKING_MODEL_2026_10_07.md')
EVIDENCE = Path('research/A01_CF10_2015_PREP_COMPETITION_SOURCE_2026_10_07.json')
SOURCES = (
    'tools/build_a01_cf10_prep_comparison_working_model.py',
    'design/A01_E6_FINAL_EPISODE_FUNCTION.json',
    'design/A01_E4_FINAL_EPISODE_FUNCTION.json',
    'design/A01_E3_FINAL_EPISODE_FUNCTION.json',
    'design/A01_FIRST_TRIAL_BLUEPRINT.json',
    'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json',
    'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    str(EVIDENCE).replace('\\', '/'),
    'canon/STORY_BIBLE.md',
    'canon/CAREER_TIMELINE.md',
    'canon/PROJECT_FREEZE.md',
    'AGENTS.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF10_CHOICE_PIN = '익숙한 훈련 승부 시간을 다음 환경의 농구 정보 확인에 써서 자신의 기술 격차를 기준으로 국내와 미국 환경을 비교한다'


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, e6.OUTPUT)
    candidates = load(root, 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json')
    packet = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    evidence = load(root, EVIDENCE)
    trial = load(root, 'design/A01_FIRST_TRIAL_BLUEPRINT.json')
    contribution = load(root, 'design/A01_FIRST_CONTRIBUTION_BLUEPRINT.json')
    e4 = load(root, 'design/A01_E4_FINAL_EPISODE_FUNCTION.json')
    story = (root / 'canon/STORY_BIBLE.md').read_text(encoding='utf-8-sig')
    career = (root / 'canon/CAREER_TIMELINE.md').read_text(encoding='utf-8-sig')
    freeze = (root / 'canon/PROJECT_FREEZE.md').read_text(encoding='utf-8-sig')
    agents = (root / 'AGENTS.md').read_text(encoding='utf-8-sig')
    assert not e6.validate(previous, root=root), 'E6 source-current function is stale'
    assert previous['episode_function_id'] == 'A01-EF-006'
    assert previous['whole_g13_complete'] is False
    assert previous['next_unit']['candidate_id'] == 'A01-CF10'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    cf10 = next(f for f in candidates['functions'] if f['id'] == 'A01-CF10')
    assert cf10['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf10['selected_event'] is False
    assert cf10['evidence_class'] == 'CANDIDATE'
    assert cf10['author_locked'] is False
    assert cf10['subact'] == 'A01-S3'
    assert cf10['function'] == '미국 환경과 익숙한 우위의 비교'
    assert cf10['entry_state'] == e6.CF10_ENTRY_PIN
    assert cf10['cause'] == '국내 팀에 나올 이유가 생겼어도 라이벌과의 기술·판단 차이와 자기 부족이 남는다'
    assert cf10['pressure'] == '익숙한 신체 우위에 머물면 낯선 경쟁에서 부족을 드러낼 위험은 피할 수 있다'
    assert cf10['choice'] == CF10_CHOICE_PIN
    assert cf10['cost'] == '그 시간에 동갑과 바로 승부하며 얻을 재미와 익숙한 평가의 기회를 포기한다'
    assert cf10['changed_state'] == '미국행의 이유가 장소 자체의 성공 보상보다 배울 과제로 좁혀진다'
    assert cf10['next'] == 'A01-CF11'
    subact = next(s for s in packet['subacts'] if s['id'] == 'A01-S3')
    assert subact['window'] == '2015–2016.02'
    assert subact['title'] == '미국행의 이유'
    assert subact['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert subact['choice'] == '국내 신체 우위에 남는 길과 낯선 기술 경쟁에 들어가는 길을 비교하고 미국행 이유를 자기 과제로 정한다'
    assert trial['status'] == 'ACTUAL_VERIFIED'
    assert next(b for b in trial['beats'] if b['id'] == 'T2')['event'] == '첫 연습에서 같은 학년 엘리트 라이벌의 기술·판단·위치선정에 완패한다'
    assert contribution['status'] == 'ACTUAL_VERIFIED'
    assert next(b for b in contribution['beats'] if b['id'] == 'C2')['event'] == '본능적으로 낙하지점을 선점한 첫 유효 리바운드와 이어진 아웃렛이 팀 득점을 만든다'
    assert e4['episode_function_id'] == 'A01-EF-004'
    assert '상대가 자신과 바스켓 사이에 먼저 자리한' in e4['beats'][0]['observable_result']
    assert evidence['status'] == 'DIRECT_PRIMARY_ARCHIVE_READ_LIMITED_TO_COMPETITION_STRUCTURE'
    assert evidence['publisher'] == 'New England Preparatory School Athletic Council'
    assert evidence['official_archive_url'] == 'https://nepsac.org/tournaments/tournament-archives/'
    assert evidence['official_pdf_url'] == 'https://assets-rst7.rschooltoday.com/rst7files/uploads/sites/328/2022/08/09195536/2015-NEPSAC-Boys-Basketball-Tournament-Bracket-Class-AAA-AA-A-B-C-D.pdf'
    assert evidence['raw_pdf_sha256'] == '4e63b254fd4fc81653c6a174d50ad7efd4c47d6a3c2fadb71b3e54a0ec5b6367'
    assert evidence['pdf_pages'] == 6
    assert {x['id'] for x in evidence['observed_facts']} == {'NEP2015-1', 'NEP2015-2'}
    assert evidence['observed_facts'][0]['statement'] == '2015년 뉴잉글랜드 프렙 남자농구 토너먼트가 Class AAA·AA·A·B·C·D로 나뉘었고 전체 대진표에는 3월 4·6·7·8일 경기 일정이 기재돼 있다. 등급별 일정은 서로 다르다.'
    assert evidence['observed_facts'][1]['statement'] == '여섯 등급마다 별도 대진표가 있어 미국 프렙 농구가 단일팀 또는 단일 서열이 아닌 여러 경쟁 단위로 조직됐다는 비교 근거가 된다.'
    assert '당시 게시·검색 가능 시점은 별도로 인증하지 않는다.' in evidence['source_date_limit']
    assert '2015년 당시 주인공이 이 정확 PDF 또는 웹페이지를 실제 열람했다는 사실' in evidence['not_certified']
    assert '한 번의 성공은 완성된 기술이나 천재 인증' in story
    assert '주인공은 한국 고1 뒤 2016년 3월 가상 뉴잉글랜드 보딩 프렙으로 이동한다.' in story
    assert '2016.03 | 가상 뉴잉글랜드 보딩 프렙 중도 편입' in career
    assert '주인공의 미국 학교는 실존 명문고가 아니라 **가상 뉴잉글랜드 소규모 보딩 프렙**' in freeze
    assert 'Escalate only a consequential author choice' in agents
    return {
        'schema': 'A01_CF10_PREP_COMPARISON_WORKING_MODEL_V1',
        'status': 'ROUTINE_COMPARISON_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'EXISTING_US_PREP_DIRECTION_WITH_NEW_FICTIONAL_INFORMATION_ACTION_NOT_NEW_AUTHOR_LOCK',
        'source_function': 'A01-CF10', 'target_subact': 'A01-S3',
        'entry_state': previous['exit_state'],
        'prior_S2_whole_subact_exit_certified': False,
        'S3_full_entry_or_exit_certified': False,
        'existing_locked_route': '한국 고1 후 2016년 3월 가상 뉴잉글랜드 소규모 보딩 프렙 편입 방향',
        'route_reapproval_required': False,
        'routine_choice_versus_locked_fact': {
            'locked_fact': 'The protagonist later moves to a fictional New England boarding prep in March 2016.',
            'new_design_choice': 'Use familiar contest time to examine a public 2015 multi-class prep tournament structure and compare it with personally observed Korean skill limits.',
            'new_author_lock': False,
            'actual_prep_admission_selected': False,
        },
        'competition_source': {
            'research_path': str(EVIDENCE).replace('\\', '/'),
            'official_archive_url': evidence['official_archive_url'],
            'official_pdf_url': evidence['official_pdf_url'],
            'source_classification': 'PRIMARY_2015_COMPETITION_STRUCTURE_ONLY',
            'observed_class_count': 6,
            'named_school_is_protagonist_school': False,
            'US_individual_skill_superiority_proved': False,
            'exact_2022_archive_url_viewed_in_2015_certified': False,
            'in_world_receipt_of_public_structure_selected_as_fiction': True,
        },
        'fictional_information_delivery': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN_NOT_HISTORICAL_DOCUMENT_ACCESS_PROOF',
            'deliverer': '기존 한국 고교 감독',
            'language': '한국어',
            'medium': '대진 구조만 간추린 한 장의 가상 안내',
            'content_scope': '2015 대회 종료 뒤 확인 가능한 여섯 등급·별도 대진 구조',
            'coach_knowledge_or_US_school_authority_historically_certified': False,
            'exact_official_pdf_or_2022_URL_seen_by_character': False,
            'application_or_athletic_offer_promised': False,
        },
        'relative_time_window': {
            'after_E6_exit': True,
            'after_2015_NEPSAC_final_date': '2015-03-08',
            'no_later_than': '2016-02',
            'exact_day_or_Korean_semester_position': None,
            'window_selected_as_fictional_sequence_not_dated_source_fact': True,
        },
        'personal_comparison_inputs': [
            {'id': 'T2', 'classification': 'AUTHOR_LOCKED_OBSERVED_KOREAN_RESULT',
             'observation': '동갑 라이벌에게 기술·판단·위치선정으로 완패했다',
             'not_inferred': '미국 선수와의 경기 결과'},
            {'id': 'C2', 'classification': 'AUTHOR_LOCKED_OBSERVED_KOREAN_RESULT',
             'observation': '한 번 본능적 리바운드·아웃렛으로 팀 득점에 기여했다',
             'not_inferred': '반복 가능한 완성 기술'},
            {'id': 'L1', 'classification': 'ROUTINE_FICTIONAL_DESIGN_OBSERVED_IN_E4',
             'observation': '첫 박스아웃 시도에서 상대가 바스켓 쪽 자리를 먼저 확보했고 자기 발 위치를 바꾸지 못했다',
             'not_inferred': '이전 C2 리바운드에도 같은 결함이 있었다는 소급'},
        ],
        'single_function': '익숙한 국내 즉시 승부 대신 다음 환경의 경쟁 구조와 자기 미완성 수행을 같은 시간에 대조해 미국행의 배울 이유를 좁힌다',
        'immediate_desire_in_this_function': '동갑에게 드러난 판단·위치 부족을 낯선 경쟁에서도 반복하지 않도록 배울 과제를 알고 싶다',
        'event_steps': [
            {'id': 'Q1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
                'choice_options': ['동갑과 바로 승부하는 익숙한 훈련 시간을 쓴다', '그 시간을 공개된 2015 프렙 대회 구조 확인에 쓴다'],
             'selected_choice': '그 시간을 공개된 2015 프렙 대회 구조 확인에 쓴다',
             'action': '익숙한 즉시 승부의 한 기회를 미루고, 기존 한국 고교 감독이 2015 대회 종료 뒤의 여섯 등급·별도 대진 구조만 한국어로 간추려 전달한 가상 안내를 확인한다',
             'observable_result': '전달된 대회 구조를 보되 개별 미국 선수의 기술이나 가상 프렙의 입학 가능성은 안내만으로 알 수 없다고 분리한다',
             'not_claimed': '원PDF나 2022 아카이브 URL을 2015에 열람·감독의 실제 미국학교 권한·미국 개인 선수 실력'},
            {'id': 'Q2', 'classification': 'ROUTINE_FICTIONAL_DESIGN_AND_EDITORIAL_INFERENCE',
             'action': '같은 승부 대체 시간 안에서 자기 T2 완패, C2 한 번의 기여, E4 위치 부족을 대조해 낯선 경쟁에서 확인하고 배울 과제로 위치·판단·패스의 반복성을 적는다',
             'observable_result': '미국이라는 장소가 성공을 보장해서가 아니라 아직 반복 증명하지 못한 과제를 시험할 환경을 찾는 이유로 비교를 좁힌다',
             'not_claimed': '미국선수기술우위 단정·새 스카우트 약속·학교 수락·훈련기술 완성'},
        ],
        'direct_present_cost': '동갑과 바로 승부하며 얻을 익숙한 평가·재미의 한 기회를 포기하고 그 동일한 시간을 한국어 대회 구조 안내 확인과 자기 T2/C2/E4 수행 대조 전체에 쓴다.',
        'selected_design_exit_state': '주인공은 미국 환경을 쉬운 성공 보상으로 보지 않고, 한 번의 기여 뒤에도 남은 위치·판단·패스 반복 과제를 낯선 경쟁에서 시험해 볼 이유로 좁혔다. 가상 프렙의 실제 입학·학업 승인과 S3 전체 선택은 아직 이 단위에서 실행되지 않았다.',
        'reader_question_at_end': '이 배울 이유를 실제 이동·학업 조건을 통과할 준비로 연결할 수 있는가',
        'next_candidate': {'id': 'A01-CF11', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'academic_transfer_conditions_not_resolved': True},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신의 T2/C2/E4 경험', '공개 대회 자료의 등급·대진 구조', '자기가 모르는 기술·입학 사항'],
            'not_available_without_access': ['실제 미국 선수의 개인 능력', '실존 학교의 비공개 평가', '가상 프렙의 입학 승인', '향후 미국 성공'],
            'exact_in_world_handout_text_or_delivery_day': None,
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'institutional_limits': {
            'fictional_school_name': None,
            'actual_application_or_acceptance_certified': False,
            'credit_transfer_visa_or_NCAA_eligibility_certified': False,
            'US_prep_training_or_roster_role_certified': False,
            'real_NEP_school_used_as_protagonist_school': False,
        },
        'unassigned_details': {
            'exact_day_or_Korean_semester_position': None,
            'exact_one_page_handout_text': None,
            'specific_real_school_or_player_viewed': None,
            'rival_scrimmage_result_or_reaction': None,
            'prep_academic_course_or_score': None,
            'travel_admission_or_visa_records': None,
        },
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
                              for p in SOURCES},
        'verification_limits': [
            'The 2015 bracket verifies competition organization, not player superiority or exact in-world internet access.',
            'The existing coach delivering a Korean one-page category summary is fictional design, not a historical knowledge or admissions guarantee.',
            'The comparison uses one foregone familiar contest opportunity for both Q1 source reading and Q2 self-comparison.',
            'The comparison action is new routine fictional design; the March 2016 move direction was already locked.',
            'S2 whole completion and S3 full entry/exit are not certified by this candidate unit.',
            'CF11 academic and transfer requirements remain unexecuted.',
            'Independent review accepted this limited model; source-current Blueprint and seventh function require separate validation.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_g13_complete': False, 'whole_g14_complete': False,
        'actual_context_packs': 0, 'author_locked': False,
        'new_author_decisions': 0, 'manuscript_count': 0,
        'manuscript_allowed': False, 'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A01 CF10 미국 환경 비교의 정보 범위', '',
        '**상태:** `ROUTINE_COMPARISON_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 미국 프렙 이동 방향은 기존 정본이며, 이 문서는 비교 행동만 가상 설계한다. 새 작가 잠금·최종 기능·원고가 아니다.', '',
        '## 입력과 비교', '',
        f"- E6 전체 종료 입력: {data['entry_state']}",
        f"- 기존 이동 방향: {data['existing_locked_route']}",
        '- 사실 원자료: [NEPSAC 2015 대진표](../research/A01_CF10_2015_PREP_COMPETITION_SOURCE_2026_10_07.md)는 여섯 등급의 경쟁 구조를 확인한다. 개별 기술 우위·가상학교 수락·2015 정확 웹주소 열람의 증거는 아니다.',
        '- 가상 전달 경로: 기존 한국 고교 감독이 대회 종료 2015-03-08 뒤부터 2016-02 이전의 한 준비창에 여섯 등급 구조만 한국어 한 장으로 간추려 전달한다. 실제 감독의 과거 지식·원PDF 직접열람·합격 보증은 아니다.',
        f"- Q1 선택: {data['event_steps'][0]['choice_options'][0]} / {data['event_steps'][0]['choice_options'][1]} 중 후자.",
        f"- Q1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- Q2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- 비용(한 기회의 Q1+Q2 전체): {data['direct_present_cost']}",
        f"- 출구: {data['selected_design_exit_state']}", '',
        '## 권위 경계', '',
        '- T2의 국내 라이벌 완패, C2의 한 번 기여, E4의 첫 박스아웃 부족만 자기 관측으로 옮긴다. 미국 선수 능력·가상 프렙 입학 가능성을 대진표에서 추론하지 않는다.',
        '- 기존 S2 전체 종료나 S3 전체 진입/종료를 이 자료만으로 인증하지 않는다. CF11 학업·이동 조건과 실제 학교·학점·비자·입학은 다음 과제다.',
        '- 국소 Blueprint/기능7 추가 0, 전체 G13/G14·실제 Context Pack·원고 미완료, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF10 working model']


def self_test(data):
    mutations = [
        ('false author lock', lambda d: d.update(author_locked=True)),
        ('false function7', lambda d: d.update(final_episode_function_added=1)),
        ('US superiority from bracket', lambda d: d['competition_source'].update(US_individual_skill_superiority_proved=True)),
        ('false 2015 exact URL access', lambda d: d['competition_source'].update(exact_2022_archive_url_viewed_in_2015_certified=True)),
        ('false school offer by coach', lambda d: d['fictional_information_delivery'].update(application_or_athletic_offer_promised=True)),
        ('remove post-tournament order', lambda d: d['relative_time_window'].update(after_2015_NEPSAC_final_date=None)),
        ('false school acceptance', lambda d: d['institutional_limits'].update(actual_application_or_acceptance_certified=True)),
        ('false S2 complete', lambda d: d.update(prior_S2_whole_subact_exit_certified=True)),
        ('execute CF11', lambda d: d['next_candidate'].update(academic_transfer_conditions_not_resolved=False)),
        ('false source SHA', lambda d: d['source_rev_sha256'].update({str(EVIDENCE): '0' * 64})),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        assert validate(candidate), name
    original_load = load
    for name, key, value in [
        ('same-ID US easy success', 'changed_state', '미국 학교 합격과 주전 성공을 이미 확인한다'),
        ('same-ID false injury cost', 'cost', '이동 전 라이벌과 충돌해 부상으로 은퇴한다'),
    ]:
        def changed_source(root, path):
            source = original_load(root, path)
            if path == 'design/A01_CONDITIONAL_EPISODE_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A01-CF10')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_source):
            assert validate(data), name
    def changed_primary(root, path):
        source = original_load(root, path)
        if path == EVIDENCE:
            source = copy.deepcopy(source)
            source['observed_facts'][1]['statement'] = '2015 미국 모든 선수는 주인공보다 기술이 뛰어나다'
        return source
    with patch(__name__ + '.load', side_effect=changed_primary):
        assert validate(data), 'primary structure-to-skill meaning reversal'
    return len(mutations) + 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()
    data = build()
    if args.write:
        (ROOT / OUTPUT).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (ROOT / MARKDOWN).write_text(render(data), encoding='utf-8')
    errors = validate(data)
    if args.check:
        saved = load(ROOT, OUTPUT)
        errors.extend(validate(saved))
        if (ROOT / MARKDOWN).read_text(encoding='utf-8-sig') != render(saved):
            errors.append('Markdown not synchronized')
    tested = self_test(data) if args.self_test else 0
    print(json.dumps({'status': data['status'], 'final_episode_function_added': 0,
                      'negative_controls': tested, 'current': not errors,
                      'errors': errors}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
