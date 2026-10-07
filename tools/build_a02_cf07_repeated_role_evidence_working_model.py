"""Build bounded prep role evidence and coach referral for A02-CF07."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import build_a02_e6_final_episode_function as previous_builder


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path('design/A02_CF07_REPEATED_ROLE_EVIDENCE_WORKING_MODEL_2026_10_07.json')
MARKDOWN = Path('design/A02_CF07_REPEATED_ROLE_EVIDENCE_WORKING_MODEL_2026_10_07.md')
SOURCES = (
    'tools/build_a02_cf07_repeated_role_evidence_working_model.py',
    str(previous_builder.OUTPUT).replace('\\', '/'),
    'design/A02_PREP_CONDITIONAL_FUNCTIONS.json',
    'design/CP2_ACT_SUBACT_PACKET.json',
    'canon/TALENT_BQ_MODEL.md',
    'canon/CHARACTER_RESPONSIBILITY_ARC.md',
    'canon/STORY_BIBLE.md',
    'research/COLLEGE_EXIT_PACKET.md',
    'research/TIMELINE_ELIGIBILITY_LEDGER.md',
    'canon/PROJECT_FREEZE.md',
    'C:/Users/Storm Credit/Desktop/Novel/novel-writing-skills/skills/writing/SKILL.md',
)
CF07_PINS = {
    'dominant_function': '반복 수행을 평가 근거로 남기기',
    'cause': '수정할 과제를 알고 수행을 이어 가는 가운데 기존 프렙 추천·실전 평가 경로가 열린다',
    'pressure': '한 번의 워크아웃 과시가 지속 수행과 학업 준비를 대신할 수 없다',
    'choice': '리바운드·수비·전환의 맡은 역할을 반복 수행하며 평가에 보일 근거를 쌓는다',
    'direct_cost': '눈에 띄는 단기 개인 과시의 기회를 줄이며 맡은 역할의 안정성에 시간을 쓴다',
    'changed_state': '자신이 평가에 보일 수 있는 후보 근거가 단일 하이라이트보다 반복된 역할 수행으로 넓어진다',
    'next': 'A02-CF08',
    'next_dependency': '농구 평가와 별개로 학업·시험 준비도 이어 가야 한다',
}


def sha(raw):
    return hashlib.sha256(raw.decode('utf-8-sig').replace('\r\n', '\n')
                           .replace('\r', '\n').encode('utf-8')).hexdigest()


def load(root, path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def build(root=ROOT):
    previous = load(root, previous_builder.OUTPUT)
    candidates = load(root, 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json')
    structure = load(root, 'design/CP2_ACT_SUBACT_PACKET.json')
    college = (root / 'research/COLLEGE_EXIT_PACKET.md').read_text(encoding='utf-8-sig')
    bq = (root / 'canon/TALENT_BQ_MODEL.md').read_text(encoding='utf-8-sig')
    assert not previous_builder.validate(previous, root=root), 'A02 E6 source stale'
    assert previous['episode_function_id'] == 'A02-EF-006'
    assert (previous['final_function_order'], previous['planned_allocation_slot']) == (15, 42)
    assert previous['next_unit']['candidate_id'] == 'A02-CF07'
    assert previous['next_unit']['candidate_is_executed_here'] is False
    assert previous['next_unit']['recommendation_or_actual_evaluation_verified_here'] is False
    assert previous['whole_A02_S2_exit_certified'] is False
    assert previous['manuscript_allowed'] is False
    cf07 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF07')
    assert cf07['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf07['evidence_class'] == 'CANDIDATE'
    assert cf07['selected_event'] is False and cf07['author_locked'] is False
    assert cf07['subact'] == 'A02-S3'
    for key, expected in CF07_PINS.items():
        assert cf07[key] == expected, f'A02-CF07 source {key} changed'
    assert cf07['entry_state'] == '훈련이 막연한 반복에서 자기 실패에 대응하는 과제로 좁혀진다'
    cf08 = next(f for f in candidates['functions'] if f['id'] == 'A02-CF08')
    assert cf08['status'] == 'CONDITIONAL_CAUSAL_FUNCTION_UNIT_NOT_EPISODE'
    assert cf08['selected_event'] is False and cf08['author_locked'] is False
    s3 = next(s for s in structure['subacts'] if s['id'] == 'A02-S3')
    assert s3['status'] == 'CP2_PROVISIONAL_FUNCTION_ONLY'
    assert '가상 프렙 감독이 2016년 봄의 신체·수비 영상과 학점 감사표를 Villanova 스태프에 전달' in college
    assert '허용된 평가 기간의 뉴잉글랜드 경기에서 보조 코치가 실전 확인' in college
    assert '가상 프렙의 정식 교명·교과목명·졸업 요구학점' in college
    assert '실패/제약 노출 → 원인 해석 → 코칭·훈련 → 반복 비용 → 경기 검증 → 상대의 새 카운터' in bq
    hashes = {p: sha((Path(p) if Path(p).is_absolute() else root / p).read_bytes())
              for p in SOURCES}
    return {
        'schema': 'A02_CF07_REPEATED_ROLE_EVIDENCE_WORKING_MODEL_V1',
        'status': 'ROUTINE_PREP_ROLE_EVIDENCE_AND_COACH_REFERRAL_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED',
        'authority_scope': 'LOCKED_FICTIONAL_PREP_REFERRAL_ROUTE_NOT_VILLANOVA_EVALUATION_OR_OFFER',
        'source_function': 'A02-CF07', 'target_subact': 'A02-S3',
        'prior_A02_E6_exact_full_exit': previous['exit_state'],
        'entry_state': previous['exit_state'],
        'candidate_entry_summary_is_exact_projection': False,
        'single_function': '한 번의 개인 과시를 택하지 않고 감독이 허용한 가상 프렙 훈련에서 리바운드 위치·담당 수비 복귀·전환 연결의 제한 역할을 거듭 보이며, 직접 받은 감독 피드백과 기관별 권한을 거친 예비 자료 전달로 평가 후보 근거를 남긴다',
        'practice_evidence': {
            'classification': 'ROUTINE_FICTIONAL_DESIGN',
            'fictional_coach_authorized_group_practice_and_recording': True,
            'observed_role_scope': ['리바운드 전에 맡은 상대의 위치를 확인하고 박스아웃한다',
                                    '공이 코너로 돌아오면 앞서 배운 복귀 시작 단서를 시도한다',
                                    '자기 득점 시도 대신 확보된 공을 동료에게 연결한 뒤 측면 통로로 달려 다음 패스를 받을 위치를 찾는다'],
            'repeated_in_bounded_practice': True,
            'official_game_score_or_minutes_certified': False,
            'single_practice_proves_stable_game_role': False,
            'individual_real_school_record_certified': False,
        },
        'institutional_handoff': {
            'classification': 'LOCKED_ROUTE_FICTIONAL_IMPLEMENTATION',
            'prep_coach_observes_and_gives_direct_limited_feedback': True,
            'academic_office_creates_preliminary_credit_gap_audit': True,
            'preliminary_audit_is_final_transcript_or_NCAA_eligibility': False,
            'fictional_student_guardian_recruiting_release_checked_before_external_send': True,
            'prep_coach_forwards_authorized_spring_role_clip_and_office_audit_for_review': True,
            'college_receipt_or_reaction_observed': False,
            'college_live_game_evaluation_or_offer_executed_here': False,
            'prep_coach_certifies_school_credit_or_NCAA_eligibility': False,
        },
        'event_steps': [
            {'id': 'R1', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'choice_options': ['자기 득점·개인 기술 장면을 먼저 요구한다', '허용된 훈련의 맡은 리바운드·수비·전환 일을 반복한다'],
             'selected_choice': '허용된 훈련의 맡은 리바운드·수비·전환 일을 반복한다',
             'action': '감독이 허용하고 기록하는 한정 단체 훈련의 여러 차례 공 전환에서 주인공은 맡은 상대를 먼저 막고, 코너 복귀 시작 단서를 시험하며, 공을 잡으면 개인 득점 시도 대신 동료에게 연결한 뒤 측면 통로로 달려 다음 패스를 받을 위치를 찾는다',
             'observable_result': '같은 세 역할을 다시 시도한 장면이 남지만, 실제 경기 분·점수·안정된 성공률은 정해지지 않는다',
             'not_claimed': '팀 공식 명단·특정 실전 경기 승패·완성된 수비·대학 평가'},
            {'id': 'R2', 'classification': 'ROUTINE_FICTIONAL_DESIGN',
             'action': '감독은 주인공에게 그 기록에서 볼 수 있는 제한 역할과 아직 확인되지 않은 경기 안정성을 직접 구분해 말하고, 단일 개인 하이라이트가 아니라 반복한 맡은 일의 후보 자료로 보겠다고 알린다',
             'observable_result': '주인공에게 직접 전달된 피드백과 추천 의사가 생기지만 감독의 대학 입학·학점 인증 권한은 생기지 않는다',
             'not_claimed': '감독 내면·Villanova 스태프 반응·장학금 약속'},
            {'id': 'R3', 'classification': 'LOCKED_ROUTE_FICTIONAL_IMPLEMENTATION',
             'action': '학교 학업담당은 이전 기록의 범주별 빈칸을 표시한 예비 학점 감사표를 만들어 주인공에게 그 빈칸 범주를 보여 준다. 학교가 가상 학생·보호자 자료공개 절차를 확인한 뒤 프렙 감독은 허용된 봄 훈련 영상과 그 감사표를 Villanova 쪽 검토 요청 자료로 전달한다',
             'observable_result': '자료를 보낸 학교 측 행위까지만 확인된다. Villanova의 수신·판단·실전 평가·오퍼나 학생의 최종 자격은 확인되지 않는다',
             'not_claimed': '실제 사람·학교 문서 발급 사실·정확 서명·대학 결정'},
        ],
        'partial_order': ['A02 E6 full exit < 2016 spring scoped practice R1 < direct coach feedback R2 < preliminary academic office audit and fictional release check < school-side packet send R3 < later college evaluation not executed'],
        'direct_present_cost': '허용된 단체 훈련에서 자기 득점 시도를 앞세우는 대신 반복해서 맡은 수비·리바운드·전환에 시간을 쓰고, 즉시 돋보이는 결과를 요구할 선택을 미룬다. 실제 오퍼를 포기했다는 뜻은 아니다.',
        'selected_design_exit_state': '주인공은 가상 프렙 감독이 허용한 봄 단체 훈련에서 리바운드 위치·코너 복귀 시작·전환 연결의 제한 역할을 거듭 시도했다. 감독은 직접 본 역할과 아직 미검증인 경기 안정성을 구분해 피드백했고, 학교 학업담당의 예비 감사표와 허용 영상을 학교 측 권한으로 검토 요청에 보냈다. 대학의 수신·실전 평가·오퍼·학업 자격은 아직 확인되지 않았다.',
        'reader_question_at_end': '보낸 제한 자료와 이후 실제 경기 수행 사이에서, 학업 준비까지 별도로 이어 갈 수 있는가',
        'next_candidate': {'id': 'A02-CF08', 'status': 'CONDITIONAL_NOT_EXECUTED',
                           'academic_study_or_exam_preparation_executed_here': False},
        'information_access': {
            'style': 'S1_PROTAGONIST_CLOSE_THIRD_SELECTED_GLOBALLY',
            'protagonist_may_know': ['자신이 수행한 제한 훈련 역할', '감독이 직접 말한 피드백·학교 측 자료 전달 안내', '학업담당이 본인에게 보여 준 예비 과목 범주 빈칸'],
            'not_available_without_access': ['감독·대학 평가자의 내면', 'Villanova 실제 수신·판단', '비공개 입학 심사', '최종 학점·NCAA 자격'],
            'individual_scene_pov_verified': False, 'exact_dialogue': None,
        },
        'unassigned_details': {'fictional_school_or_staff_name': None, 'exact_spring_date': None,
                               'practice_opponent_or_teammate_identity': None,
                               'published_clip_or_personal_file_path': None,
                               'course_ids_or_credit_values': None,
                               'score_or_minutes': None, 'recruiter_identity_or_reply': None,
                               'roster_or_game_status': None},
        'source_rev_convention': 'SHA256_UTF8_BOM_REMOVED_CRLF_CR_TO_LF',
        'source_rev_sha256': hashes,
        'verification_limits': [
            'The existing selected route includes spring prep coach material transfer; this model gives it bounded fictional school-side actions, not proof of real Villanova receipt.',
            'A school academic officer authors only a preliminary category gap audit; coach cannot certify credits, graduation or NCAA eligibility.',
            'Fictional release and recording permissions are institutional design assumptions, not actual personal consents or 2016 real-school records.',
            'Repeated attempts in one scoped practice are candidate evidence, not stable live-game success or later college evaluation.',
            'CF08 study and exam preparation, actual offer, whole A02-S3 and G13 remain unexecuted or unverified.',
            'The working model passed independent source, access and meaning review; a separate final-function review is required before promotion.',
        ],
        'actual_verified_blueprint_created': False,
        'final_episode_function_added': 0,
        'whole_A02_S3_exit_certified': False, 'whole_g13_complete': False,
        'whole_g14_complete': False, 'actual_context_packs': 0,
        'author_locked': False, 'new_author_decisions': 0,
        'manuscript_count': 0, 'manuscript_allowed': False,
        'design_gate': 'CLOSED',
    }


def render(data):
    return '\n'.join([
        '# A02 CF07: 제한 역할의 반복 증거와 학교 측 검토 요청', '',
        '**상태:** `ROUTINE_PREP_ROLE_EVIDENCE_AND_COACH_REFERRAL_DESIGN_SELECTED_INDEPENDENTLY_REVIEWED`. 기존 가상 프렙 추천 경로의 봄 영상·초기 학점 감사표 전달을 제한적으로 구현하고 독립 원천·접근·의미 검문을 통과했다. 실제 대학의 수신·평가·오퍼를 인증하지 않으며 별도 기능 검문 전 기능 수는 늘리지 않는다.', '',
        '## 보이는 역할과 권한', '',
        f"- 정확한 진입: {data['entry_state']}",
        f"- 기능: {data['single_function']}",
        f"- R1: {data['event_steps'][0]['action']} → {data['event_steps'][0]['observable_result']}",
        f"- R2: {data['event_steps'][1]['action']} → {data['event_steps'][1]['observable_result']}",
        f"- R3: {data['event_steps'][2]['action']} → {data['event_steps'][2]['observable_result']}",
        f"- 비용: {data['direct_present_cost']}",
        f"- 국소 출구: {data['selected_design_exit_state']}",
        f"- 다음 질문: {data['reader_question_at_end']}", '',
        '## 증거 한계', '',
        '- 학교 학업담당이 예비 학점 빈칸표를 만들고 감독은 허용된 훈련 자료를 전달한다. 감독은 학점·NCAA 자격을 인증하지 못한다. 본인·보호자 공개 절차는 가상기관 설계 조건이며 실제 인물의 문서나 동의를 인증하지 않는다.',
        '- 한정 단체 훈련의 반복 장면은 실전 안정성이나 Villanova의 수신·실전 평가·장학금·입학 결정을 뜻하지 않는다. CF08 학업·시험 준비와 전체 S3/G13도 미실행이다.',
        '- 최종 기능·Context Pack·원고0, 게이트 `CLOSED`, `manuscript_allowed:false`.', '',
    ])


def validate(data, root=ROOT):
    try:
        expected = build(root)
    except (AssertionError, KeyError, StopIteration, OSError, TypeError) as exc:
        return [f'source construction: {exc}']
    return [] if data == expected else ['record differs from source-bound CF07 working model']


def self_test(data):
    mutations = [
        ('claim college receipt', lambda d: d['institutional_handoff'].update(college_receipt_or_reaction_observed=True)),
        ('claim college evaluation', lambda d: d['institutional_handoff'].update(college_live_game_evaluation_or_offer_executed_here=True)),
        ('coach certifies credits', lambda d: d['institutional_handoff'].update(prep_coach_certifies_school_credit_or_NCAA_eligibility=True)),
        ('promote preliminary audit', lambda d: d['institutional_handoff'].update(preliminary_audit_is_final_transcript_or_NCAA_eligibility=True)),
        ('claim stable game role', lambda d: d['practice_evidence'].update(single_practice_proves_stable_game_role=True)),
        ('claim actual game stats', lambda d: d['practice_evidence'].update(official_game_score_or_minutes_certified=True)),
        ('execute CF08 studies', lambda d: d['next_candidate'].update(academic_study_or_exam_preparation_executed_here=True)),
        ('claim full S3', lambda d: d.update(whole_A02_S3_exit_certified=True)),
        ('promote function', lambda d: d.update(final_episode_function_added=1)),
        ('authorize manuscript', lambda d: d.update(manuscript_allowed=True)),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(data)
        mutate(changed)
        assert validate(changed), name
    original_load = load
    for name, key, value in [
        ('same-ID offer choice', 'choice', '한 번의 하이라이트로 대학 장학금과 입학을 확정한다'),
        ('same-ID actual evaluation state', 'changed_state', 'Villanova 실전 평가에서 주전 자리와 장학금을 얻는다'),
        ('same-ID invisible cost', 'direct_cost', '이미 받은 오퍼를 포기하고 부상으로 시즌을 잃는다'),
    ]:
        def changed_load(root, path):
            source = original_load(root, path)
            if path == 'design/A02_PREP_CONDITIONAL_FUNCTIONS.json':
                source = copy.deepcopy(source)
                next(f for f in source['functions'] if f['id'] == 'A02-CF07')[key] = value
            return source
        with patch(__name__ + '.load', side_effect=changed_load):
            assert validate(data), name
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
                      'negative_controls': tested, 'current': not errors, 'errors': errors},
                     ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
