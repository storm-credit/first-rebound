"""Produce CLOSED-gate design samples and validate cross-document CP2 boundaries.

No scenes, actual episode packs, canon promotion, or new season simulation.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import build_a01_e1_final_episode_function as e1_function
import build_a01_e2_final_episode_function as e2_function
import build_a01_e3_final_episode_function as e3_function
import build_a01_e4_final_episode_function as e4_function
import build_a01_e5_final_episode_function as e5_function
import build_a01_e6_final_episode_function as e6_function
import build_a01_e7_final_episode_function as e7_function
import build_a01_e8_final_episode_function as e8_function
import build_a01_e9_final_episode_function as e9_function
import build_a02_e1_final_episode_function as a02_e1_function
import build_a02_e2_final_episode_function as a02_e2_function
import build_a02_e3_final_episode_function as a02_e3_function
import build_a02_e4_final_episode_function as a02_e4_function
import build_a02_e5_final_episode_function as a02_e5_function
import build_a02_e6_final_episode_function as a02_e6_function
import build_a02_e7_final_episode_function as a02_e7_function
import build_a02_e8_final_episode_function as a02_e8_function
import build_a02_e9_final_episode_function as a02_e9_function
import build_a02_e10_final_episode_function as a02_e10_function

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = '171b46b'
STRUCTURE = 'design/CP2_ACT_SUBACT_PACKET.json'
CAREER = 'design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.json'
PROMISES = 'design/CP2_PROMISE_LEDGER.json'
PACKS = 'context-packs/CP2_DESIGN_VALIDATION_SAMPLES.json'
REPORT = 'reviews/O15G2_INTEGRITY_REPORT.json'


def validate_final_functions(structure, root=ROOT):
    """Count reviewed functional assignments; never infer completion from slots."""
    errors, records = [], []
    paths = structure.get('final_episode_function_paths', [])
    declared = structure.get('final_episode_functions_completed', 0)
    if (type(declared) is not int or declared < 0 or not isinstance(paths, list)
            or any(not isinstance(path, str) for path in paths)):
        return ['invalid final function registry'], []
    if len(paths) != len(set(paths)):
        errors.append('duplicate final function path')
    known = {str(e1_function.OUTPUT).replace('\\', '/'): e1_function.validate,
             str(e2_function.OUTPUT).replace('\\', '/'): e2_function.validate,
             str(e3_function.OUTPUT).replace('\\', '/'): e3_function.validate,
             str(e4_function.OUTPUT).replace('\\', '/'): e4_function.validate,
             str(e5_function.OUTPUT).replace('\\', '/'): e5_function.validate,
             str(e6_function.OUTPUT).replace('\\', '/'): e6_function.validate,
             str(e7_function.OUTPUT).replace('\\', '/'): e7_function.validate,
             str(e8_function.OUTPUT).replace('\\', '/'): e8_function.validate,
             str(e9_function.OUTPUT).replace('\\', '/'): e9_function.validate,
             str(a02_e1_function.OUTPUT).replace('\\', '/'): a02_e1_function.validate,
             str(a02_e2_function.OUTPUT).replace('\\', '/'): a02_e2_function.validate,
             str(a02_e3_function.OUTPUT).replace('\\', '/'): a02_e3_function.validate,
             str(a02_e4_function.OUTPUT).replace('\\', '/'): a02_e4_function.validate,
             str(a02_e5_function.OUTPUT).replace('\\', '/'): a02_e5_function.validate,
             str(a02_e6_function.OUTPUT).replace('\\', '/'): a02_e6_function.validate,
             str(a02_e7_function.OUTPUT).replace('\\', '/'): a02_e7_function.validate,
             str(a02_e8_function.OUTPUT).replace('\\', '/'): a02_e8_function.validate,
             str(a02_e9_function.OUTPUT).replace('\\', '/'): a02_e9_function.validate,
             str(a02_e10_function.OUTPUT).replace('\\', '/'): a02_e10_function.validate}
    for path in paths:
        if path not in known:
            errors.append('unreviewed final function path: ' + str(path))
            continue
        try:
            data = load(path, root)
            check_errors = known[path](data, root=root)
            errors.extend(path + ': ' + e for e in check_errors)
            if not check_errors:
                records.append(data)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(path + ': ' + str(exc))
    if declared != len(records):
        errors.append('final function count differs from verified assignments')
    slots = [r['planned_allocation_slot'] for r in records]
    orders = [r['final_function_order'] for r in records]
    if len(slots) != len(set(slots)) or sorted(orders) != list(range(1, len(records) + 1)):
        errors.append('final function allocation/order collision')
    return errors, records


def load(path, root=ROOT):
    return json.loads((root / path).read_text(encoding='utf-8'))


def sha(path, root=ROOT):
    # Git may check out the same text with CRLF on Windows and LF elsewhere.
    return hashlib.sha256((root / path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def validate_design(structure, career, promises, root=ROOT):
    errors = []
    for name, data in [('structure', structure), ('career', career), ('promises', promises)]:
        if data.get('author_locked') is not False or data.get('manuscript_allowed') is not False:
            errors.append(name + ': promotion forbidden')
    if career.get('season_selected') is not False or career.get('exact_execution_cleared') is not False:
        errors.append('career: factual or season promotion forbidden')
    acts = structure['acts']
    subacts = structure['subacts']
    act_by_id = {a['id']: a for a in acts}
    sub_by_id = {s['id']: s for s in subacts}
    if len(act_by_id) != len(acts) or len(sub_by_id) != len(subacts):
        errors.append('duplicate design IDs')
    cursor = 1
    for a in acts:
        if (a['allocation_start'], a['allocation_end']) != (cursor, cursor + a['planned_units'] - 1):
            errors.append(a['id'] + ': allocation discontinuity')
        cursor += a['planned_units']
        if not 1 <= len(a['methods']) <= 2:
            errors.append(a['id'] + ': method budget')
        alloc = a['NBA_content_allocation']
        if a['category'] == 'NBA' and (not alloc or sum(alloc.values()) != a['planned_units']):
            errors.append(a['id'] + ': NBA allocation mismatch')
        if not any(s['parent_act'] == a['id'] for s in subacts):
            errors.append(a['id'] + ': missing subacts')
    total = sum(a['planned_units'] for a in acts)
    nba = sum(a['planned_units'] for a in acts if a['category'] == 'NBA')
    if total != structure['total_planned_units'] or not .75 <= nba / total <= .85:
        errors.append('global allocation / NBA share')
    if structure.get('planned_episode_outlines_completed') != 0:
        errors.append('slots cannot become finished episode outlines')
    function_errors, _ = validate_final_functions(structure, root)
    errors.extend(function_errors)
    for s in subacts:
        if s['parent_act'] not in act_by_id:
            errors.append(s['id'] + ': unknown parent')
        required = ['entry_state', 'goal', 'pressure', 'choice', 'cost', 'exit_state',
                    'primary_device', 'institutional_constraint', 'relationship_in_play',
                    'basketball_question', 'irreversible_choice']
        if any(not isinstance(s.get(k), str) or not s[k].strip() for k in required):
            errors.append(s['id'] + ': missing function field')
        if set(s.get('time_and_place', {})) != {'window', 'place_scope'} or not s.get('continuity_checks'):
            errors.append(s['id'] + ': missing scope / continuity fields')
        if s.get('secondary_device') is not None and not isinstance(s['secondary_device'], str):
            errors.append(s['id'] + ': secondary device budget')
        if s.get('manuscript_allowed') is not False:
            errors.append(s['id'] + ': manuscript permission')
        for path in s['research_dependencies']:
            if not (root / path).is_file():
                errors.append(s['id'] + ': missing dependency ' + path)
    if len(promises['global_primary']) > 2 or len(promises['promises']) > 5:
        errors.append('global promise budget')
    if len(promises['false_victory_candidates']) > 3 or promises['macguffin_count'] > 1:
        errors.append('false victory / MacGuffin budget')
    for p in promises['promises']:
        refs = [p['plant'], *p['variations'], p['payoff']]
        if any(r not in sub_by_id for r in refs):
            errors.append(p['id'] + ': dangling promise reference')
        if p['status'] != 'PLANNED':
            errors.append(p['id'] + ': payoff not written or approved')
    relationship = next(p for p in promises['promises'] if p['id'] == 'P3')
    prior = [relationship['plant'], *relationship['variations']]
    if len({r.split('-')[0] for r in prior}) < 3:
        errors.append('final receiver: fewer than three prior Acts')
    seasons = career['seasons']
    years = [int(s['season'][:4]) for s in seasons]
    if years != list(range(2018, 2035)):
        errors.append('career season continuity')
    for s, year in zip(seasons, years):
        if s['protagonist_NBA_year'] != year - 2017 or s['age_during_calendar_year'] != year - 1999:
            errors.append(s['season'] + ': age/year mismatch')
        if any(s[k] is not None for k in ['team_wins', 'individual_stats', 'awards']):
            errors.append(s['season'] + ': proposed targets promoted into results')
    if career['protagonist_one_club'] != 'CHI' or career['rival_initial_team'] != 'MIN':
        errors.append('approved team direction changed')
    if career['rival_lifetime_one_club_author_locked'] is not False:
        errors.append('rival lifetime team not approved')
    for key in ['options', 'receiver_options', 'award_budget_options']:
        if len(career[key]) != 4:
            errors.append(key + ': four alternatives required')
    return errors


def make_samples(root=ROOT):
    structure = load(STRUCTURE, root)
    promises = load(PROMISES, root)
    configs = [
        ('CP2-A06-S3', 'A06-S3', '위임 선택된 K1/L2와 사전 기록된 M 추첨의 실행 경계 확인',
         ['simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json',
          'simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json',
          'simulation/NBA_2021_PROVISIONAL_DRAFT.json',
          'canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json',
          'canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json',
          'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json',
          'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json',
          'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json',
          'canon/DELEGATED_2021_BRACKET_DRAW_DECISION.json'],
         [dict(claim='CHI 31–41은 위임 선택 K1의 S2 유한 실행 결과이며 실제 박스 인증은 아님', status='AUTHOR_MODELED_DESIGN',
               source_paths=['simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json']),
          dict(claim='L2 WAS 승리/IND 패배는 위임 선택의 S2 유한 실행이며 실제 박스 인증은 아님', status='AUTHOR_MODELED_DESIGN',
               source_paths=['simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json', 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json']),
          dict(claim='사전 게시 뒤 첫 추첨에서 CHI10·39, MIN7·36 원소유 순번',
               status='AUTHOR_MODELED_DESIGN',
               source_paths=['simulation/NBA_2021_PROVISIONAL_DRAFT.json', 'canon/DELEGATED_2021_BRACKET_DRAW_DECISION.json'])],
         ['K1', 'L2', 'M_DRAW'], '사실 검증자',
         ['F4 Hall 5/9 재계약 생략·F5 McGee 거래 및 Cleveland Varejão 5월 복귀계약 생략은 작가 선택; S2 유한 건강·명단·법적범위 실행 완료/실제 임상·접수·사적charge는 미인증',
          'Markkanen M1은 2021 여름 후행 선택이며 2020–21 결과의 소급 증거가 아님',
          'G1A 여름 주 경로 선택도 2020–21 결과나 Caruso 계약 실행의 소급 증거가 아님',
          '전체 60픽의 현재 소유 구단과 선수 지명']),
        ('CP2-A13-S3', 'A13-S3', '결말 기능과 RC1의 선행 상호 비용 연결 확인',
         [CAREER, 'design/ENDING_THEME.md',
          'canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json',
          'canon/CHICAGO_2021_M1_OFFSEASON_A_DECISION.json'],
         [dict(claim='결말 기능은 수비→리바운드→직접 전진→유리한 동료에게 패스→동료 결승 득점',
               status='CANON_FUNCTION', source_paths=['design/ENDING_THEME.md'])],
         [], '주인공 밀착 3인칭 후보 — 설계 시점만',
         ['M1 계약 제안은 2024–25 종료; 2028 Markkanen 소속·잔류는 미확정',
          'G1A 선택은 2028 Caruso·Green 소속이나 실제 계약 수락을 확정하지 않음',
          '2028 대진·수취인 RC1은 새 창작 추천', '점수·남은 시간·패스 각도·잔류·건강'])]
    out = []
    for pid, sid, function, extra, facts, events, pov, holds in configs:
        s = next(s for s in structure['subacts'] if s['id'] == sid)
        a = next(a for a in structure['acts'] if a['id'] == s['parent_act'])
        refs = list(dict.fromkeys(['canon/PROJECT_FREEZE.md', 'canon/CAREER_TIMELINE.md',
             'control/DESIGN_GATE.md',
             'canon/CHICAGO_2020_21_D1_S2_STANDARD_DECISION.json',
             'control/CHICAGO_2020_21_D1_S2_PROTOCOL.md',
             STRUCTURE, PROMISES, 'design/HOUSE_STYLE_FOUNDATION.md',
             'research/STYLE_REFERENCE_ACCESS.md', 'research/STYLE_READING_OBSERVATIONS.json',
             'research/STYLE_FUNCTION_COMPARISON.md',
             'research/G11_CORE_EXTENSION_2026_10_02.json',
             'research/G11_CORE_EXTENSION_2026_10_02.md',
             'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.json',
             'research/G11_SGRADE_COMMON_MINIMUM_2026_10_02.md',
             'research/G11_BUSINESS_COMMON_MINIMUM_2026_10_02.json',
             'research/G11_BUSINESS_COMMON_MINIMUM_2026_10_02.md',
             'research/G11_EXTRA_COMMON_MINIMUM_2026_10_02.json',
             'research/G11_EXTRA_COMMON_MINIMUM_2026_10_02.md',
             'research/G11_ORV_VISUAL_MINIMUM_2026_10_02.json',
             'research/G11_ORV_VISUAL_MINIMUM_2026_10_02.md',
             'research/G11_FIELD_VISUAL_MINIMUM_2026_10_02.json',
             'research/G11_FIELD_VISUAL_MINIMUM_2026_10_02.md',
             'research/G11_KAKAO_SCOPED_MINIMUM_2026_10_02.json',
             'research/G11_KAKAO_SCOPED_MINIMUM_2026_10_02.md',
             'research/G11_MUNPIA_REMAINING_MINIMUM_2026_10_02.json',
             'research/G11_MUNPIA_REMAINING_MINIMUM_2026_10_02.md',
             'research/G11_TEN_WORK_SYNTHESIS_2026_10_02.json',
             'research/G11_TEN_WORK_SYNTHESIS_2026_10_02.md',
             'research/G11_RIDI_STRUCTURAL_MEASUREMENTS_2026_10_01.json',
             'research/G11_POPULARITY_PROVENANCE_2026_10_01.json',
             'research/G11_RECORDED_FUNCTION_CODING_2026_10_01.json',
             'research/G11_RIDI_CONTEXTUAL_VOICE_PILOT_2026_10_01.json',
             'research/G11_RIDI_CONTEXTUAL_VOICE_FIRST_FIVE_2026_10_01.json',
             'research/G11_RIDI_OPENING_BOUNDARY_COMPONENT_2026_10_01.json',
             'research/G11_RIDI_FUNCTION_SEQUENCE_FIRST_FIVE_2026_10_01.json',
             'research/G11_RIDI_INFORMATION_DELIVERY_FIRST_FIVE_2026_10_01.json',
             'research/G11_INFORMATION_DELIVERY_CROSS_WORK_SELECTED_2026_10_01.md',
             'research/G11_RIDI_BUSINESS_FIRST_FIVE_COMPONENTS_2026_10_01.json',
             'research/G11_RIDI_BUSINESS_FIRST_FIVE_COMPONENTS_2026_10_01.md',
             'research/G11_JOARA_EXTRA_FIRST_FIVE_COMPONENTS_2026_10_01.json',
             'research/G11_JOARA_EXTRA_FIRST_FIVE_COMPONENTS_2026_10_01.md',
             'research/G11_COMPONENT_PROGRESS_2026_10_01.json',
             'research/G11_THREE_WORK_RANGES_2026_10_01.json',
             'research/G11_THREE_WORK_RANGES_2026_10_01.md',
             'research/G11_MUNPIA_FIELD_VISUAL_FUNCTIONS_2026_10_01.json',
             'research/G11_MUNPIA_FIELD_VISUAL_FUNCTIONS_2026_10_01.md',
             'research/D1_ORLANDO_CALENDAR_SOURCES_2026_10_02.json',
             'simulation/ORLANDO_2020_21_SELECTED_DAILY_REGISTRATION.json',
             'research/D1_ORLANDO_DAILY_REGISTRATION_WITNESS_2026_10_02.md'] + extra))
        active = [p['id'] for p in promises['promises'] if sid in [p['plant'], *p['variations'], p['payoff']]]
        out.append(dict(
            pack_id=pid, target_episode_or_design_unit=sid,
            purpose='DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK', generated_at='2026-10-02',
            source_commit=BASE_COMMIT,
            source_revision='MAIN_BASE_PLUS_REVIEWED_CONTENT_HASHES',
            source_revision_note='source_commit는 기반 커밋. 새 설계 파일은 같은 커밋에 포함됐다는 뜻이 아니며 아래 개별 해시가 실제 내용을 고정한다.',
            canon_version='PROJECT_FREEZE v0.30 PARTIAL', timeline_window=s['window'],
            pov_character=pov, entry_state=s['entry_state'], episode_function=function,
            act_question=a['question'], subact_question=s['goal'],
            primary_narrative_device=s['primary_device'], secondary_device_optional=s['secondary_device'],
            active_setup=active, payoff_or_defer='설계 기능 검증만; 실제 회수·원고 없음',
            reader_expected_question=a['question'], do_not_explain_device=True,
            allowed_facts=[f['claim'] for f in facts], fact_evidence=facts,
            information_boundary=dict(
                mode='DESIGN_REVIEW_NO_IN_WORLD_ACCESS',
                reviewer_loaded_claim_indexes=list(range(len(facts))),
                story_known_claim_indexes=[], scene_segments=[], access_witnesses=[],
                relative_time_references=[], exact_scene_date=None,
                pov_author_locked=False, narrative_access_status='HOLD'),
            fact_status='CLAIM_LEVEL_STATUS_IN_FACT_EVIDENCE',
            decision_boundaries=[
                'F4/F5 및 Cleveland C2 선택 방향은 정확 시즌·의료·등록 PASS가 아니다',
                'M1 제안·수락 방향은 2021 여름 사건이며 2028 잔류나 전체 계약 실행 PASS가 아니다',
                'G1A 여름 주 경로 선택은 선수별 수락·SQ1·시즌 결과 PASS가 아니다'],
            required_historical_events=events, relationship_state=s['relationship_in_play'],
            physical_state='HOLD — 개별 날짜의 신체·건강 확정 없음',
            basketball_constraints=s['institutional_constraint'], promises_to_pay=active,
            hold_fields=holds,
            forbidden_moves=['원고/대사 생성', 'HOLD를 실제 사실로 전환', '미승인 시즌/수상 잠금',
                             '타인의 속마음·권한 밖 정보 부여', '과거 Atlanta 착지를 현행 적용'],
            exit_state_required=s['exit_state'], source_links=refs,
            source_content_sha256={p: sha(p, root) for p in refs},
            integrity_status='CONTENT_HASH_PINNED_DESIGN_ONLY', manuscript_allowed=False,
            author_locked=False))
    return dict(stage='O-15G2', samples=out, actual_episode_packs=0,
                manuscript_allowed=False, author_locked=False)


def assess_observed_access(witness):
    """Check a supplied past-observation clock, never authenticate a story claim."""
    if witness.get('claim_kind') != 'PAST_OBSERVED_EVENT':
        return 'HOLD'
    values = [witness.get(k) for k in ('event_on', 'acquired_on', 'segment_on')]
    if any(not isinstance(v, str) for v in values):
        return 'HOLD'
    try:
        event_on, acquired_on, segment_on = [date.fromisoformat(v) for v in values]
    except ValueError:
        return 'HOLD'
    if not event_on <= acquired_on <= segment_on:
        return 'FAIL'
    if (witness.get('access_route') not in {'DIRECT_OBSERVATION', 'PUBLIC_RECORD', 'DIRECT_REPORT'}
            or not witness.get('holder_id') or not witness.get('source_path')
            or witness.get('source_verified') is not True):
        return 'HOLD'
    return 'SUPPLIED_CLOCK_REPRODUCTION_PASS_NOT_NARRATIVE_CLEARANCE'


def validate_information_boundary(sample):
    errors = []
    b = sample.get('information_boundary', {})
    if (b.get('mode') != 'DESIGN_REVIEW_NO_IN_WORLD_ACCESS'
            or b.get('narrative_access_status') != 'HOLD'
            or b.get('pov_author_locked') is not False
            or b.get('exact_scene_date') is not None):
        errors.append('design review cannot grant POV/date/narrative access')
    if b.get('reviewer_loaded_claim_indexes') != list(range(len(sample.get('fact_evidence', [])))):
        errors.append('reviewer claim mapping mismatch')
    for key in ('story_known_claim_indexes', 'scene_segments', 'access_witnesses', 'relative_time_references'):
        if b.get(key) != []:
            errors.append('in-world input requires locked scene/POV; ' + key)
    return errors


def validate_samples(data, root=ROOT):
    errors = []
    if (data.get('actual_episode_packs') != 0 or data.get('manuscript_allowed') is not False
            or data.get('author_locked') is not False):
        errors.append('sample promoted into manuscript pack')
    expected = make_samples(root)
    actual_samples = data.get('samples', [])
    expected_by_id = {p['pack_id']: p for p in expected['samples']}
    if {k: v for k, v in data.items() if k != 'samples'} != {k: v for k, v in expected.items() if k != 'samples'}:
        errors.append('sample root differs from generated design-only root')
    if len(actual_samples) != len(expected_by_id) or {p.get('pack_id') for p in actual_samples} != set(expected_by_id):
        errors.append('sample IDs differ from generated set')
    for p in actual_samples:
        pid = p.get('pack_id', '<missing pack_id>')
        errors.extend(pid + ': ' + e for e in validate_information_boundary(p))
        if (p.get('purpose') != 'DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK'
                or p.get('manuscript_allowed') is not False or p.get('author_locked') is not False):
            errors.append(pid + ': purpose or author lock')
        if len(p.get('decision_boundaries', [])) != 3:
            errors.append(pid + ': missing author-decision boundary')
        links = p.get('source_links', [])
        hashes = p.get('source_content_sha256', {})
        if len(links) != len(set(links)):
            errors.append(pid + ': duplicate source link')
        if set(links) != set(hashes):
            errors.append(pid + ': source hash coverage')
        evidence = p.get('fact_evidence', [])
        if len(evidence) != len(p.get('allowed_facts', [])) or [e.get('claim') for e in evidence] != p.get('allowed_facts', []):
            errors.append(pid + ': claim evidence coverage')
        for i, e in enumerate(evidence):
            if e.get('status') == 'AUTHOR_MODELED_DESIGN':
                authority_path = ('canon/DELEGATED_2021_BRACKET_DRAW_DECISION.json'
                                  if i == 2 else 'canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json')
                if pid != 'CP2-A06-S3' or i > 2 or authority_path not in e.get('source_paths', []):
                    errors.append(pid + ': delegated claim missing scoped authority')
            if e.get('status') not in {'CANON_FUNCTION', 'CANDIDATE', 'CONDITIONAL_RESULT', 'AUTHOR_MODELED_DESIGN'}:
                errors.append(pid + ': invalid or promoted claim status')
            paths = e.get('source_paths', [])
            if not paths or len(paths) != len(set(paths)) or any(path not in hashes for path in paths):
                errors.append(pid + ': claim source not hash-pinned')
        generated = expected_by_id.get(pid)
        if generated is not None:
            body = {k: v for k, v in p.items() if k != 'source_content_sha256'}
            generated_body = {k: v for k, v in generated.items() if k != 'source_content_sha256'}
            if body != generated_body:
                errors.append(pid + ': content differs from generated design sample')
        for path, expected_hash in hashes.items():
            if not (root / path).is_file() or sha(path, root) != expected_hash:
                errors.append(pid + ': STALE ' + path)
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='Check existing samples; do not regenerate stale hashes')
    args = ap.parse_args()
    a, c, p = load(STRUCTURE), load(CAREER), load(PROMISES)
    errors = validate_design(a, c, p)
    _, final_functions = validate_final_functions(a)
    samples = load(PACKS) if args.check else make_samples()
    errors += validate_samples(samples)
    alloc = {k: sum((x['NBA_content_allocation'] or {}).get(k, 0) for x in a['acts'])
             for k in ['regular', 'postseason', 'offseason', 'national_team']}
    report = dict(PASS=not errors, scope='STRUCTURE_CONTENT_AND_SAMPLE_SEMANTICS',
                  acts=len(a['acts']), subacts=len(a['subacts']), planned_units=a['total_planned_units'],
                  episode_outlines_completed=0, NBA_content_allocation=alloc,
                  final_episode_functions_completed=len(final_functions),
                  assigned_function_slots=len(final_functions),
                  unassigned_planned_slots=a['total_planned_units'] - len(final_functions),
                  career_seasons=len(c['seasons']), design_samples=len(samples['samples']),
                  independent_review=False, final_design_complete=False,
                  manuscript_allowed=False, errors=errors)
    if not args.check and not errors:
        for path, data in [(PACKS, samples), (REPORT, report)]:
            (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
