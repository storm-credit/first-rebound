"""Produce CLOSED-gate design samples and validate cross-document CP2 boundaries.

No scenes, actual episode packs, canon promotion, or new season simulation.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = '8bd0cc8a9aefeda72e4683a35bceba646f3a50a2'
STRUCTURE = 'design/CP2_ACT_SUBACT_PACKET.json'
CAREER = 'design/CHICAGO_MINNESOTA_LONG_CAREER_PACKET.json'
PROMISES = 'design/CP2_PROMISE_LEDGER.json'
PACKS = 'context-packs/CP2_DESIGN_VALIDATION_SAMPLES.json'
REPORT = 'reviews/O15G2_INTEGRITY_REPORT.json'


def load(path, root=ROOT):
    return json.loads((root / path).read_text())


def sha(path, root=ROOT):
    return hashlib.sha256((root / path).read_bytes()).hexdigest()


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
        ('CP2-A06-S3', 'A06-S3', 'K1/L2와 사전 기록된 M 추첨의 잠정 연결 확인',
         ['simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.json',
          'simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.json',
          'simulation/NBA_2021_PROVISIONAL_DRAFT.json'],
         ['CHI 31–41은 K1 조건부 추천', 'L2는 WAS 승리/IND 패배의 사건안',
          '사전 게시 뒤 첫 추첨에서 CHI10·39, MIN7·36 원소유 순번'],
         ['K1', 'L2', 'M_DRAW'], '사실 검증자',
         ['정확 건강·등록·charge', '전체 60픽의 현재 소유 구단과 선수 지명']),
        ('CP2-A13-S3', 'A13-S3', '결말 기능과 RC1의 선행 상호 비용 연결 확인',
         [CAREER, 'design/ENDING_THEME.md'],
         ['결말 기능은 수비→리바운드→직접 전진→유리한 동료에게 패스→동료 결승 득점'],
         [], '주인공 밀착 3인칭 후보 — 설계 시점만',
         ['2028 대진·수취인 RC1은 새 창작 추천', '점수·남은 시간·패스 각도·잔류·건강'])]
    out = []
    for pid, sid, function, extra, facts, events, pov, holds in configs:
        s = next(s for s in structure['subacts'] if s['id'] == sid)
        a = next(a for a in structure['acts'] if a['id'] == s['parent_act'])
        refs = list(dict.fromkeys(['canon/PROJECT_FREEZE.md', 'canon/CAREER_TIMELINE.md',
             'control/DESIGN_GATE.md', STRUCTURE, PROMISES, 'design/HOUSE_STYLE_FOUNDATION.md',
             'research/STYLE_REFERENCE_ACCESS.md', 'research/STYLE_READING_OBSERVATIONS.json',
             'research/STYLE_FUNCTION_COMPARISON.md'] + extra))
        active = [p['id'] for p in promises['promises'] if sid in [p['plant'], *p['variations'], p['payoff']]]
        out.append(dict(
            pack_id=pid, target_episode_or_design_unit=sid,
            purpose='DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK', generated_at='2026-09-12',
            source_commit=BASE_COMMIT,
            source_revision='BASE_COMMIT_PLUS_REVIEWED_WORKTREE_HASHES',
            source_revision_note='source_commit는 기반 커밋. 새 설계 파일은 같은 커밋에 포함됐다는 뜻이 아니며 아래 개별 해시가 실제 내용을 고정한다.',
            canon_version='PROJECT_FREEZE v0.30 PARTIAL', timeline_window=s['window'],
            pov_character=pov, entry_state=s['entry_state'], episode_function=function,
            act_question=a['question'], subact_question=s['goal'],
            primary_narrative_device=s['primary_device'], secondary_device_optional=s['secondary_device'],
            active_setup=active, payoff_or_defer='설계 기능 검증만; 실제 회수·원고 없음',
            reader_expected_question=a['question'], do_not_explain_device=True,
            allowed_facts=facts, fact_status='CANON_FUNCTION_OR_EXPLICIT_CONDITIONAL_RESULT',
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


def validate_samples(data, root=ROOT):
    errors = []
    if data.get('actual_episode_packs') != 0 or data.get('manuscript_allowed') is not False:
        errors.append('sample promoted into manuscript pack')
    for p in data['samples']:
        if p['purpose'] != 'DESIGN_VALIDATION_ONLY_NOT_EPISODE_PACK' or p['manuscript_allowed'] is not False:
            errors.append(p['pack_id'] + ': purpose')
        if set(p['source_links']) != set(p['source_content_sha256']):
            errors.append(p['pack_id'] + ': source hash coverage')
        for path, expected in p['source_content_sha256'].items():
            if not (root / path).is_file() or sha(path, root) != expected:
                errors.append(p['pack_id'] + ': STALE ' + path)
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='Check existing samples; do not regenerate stale hashes')
    args = ap.parse_args()
    a, c, p = load(STRUCTURE), load(CAREER), load(PROMISES)
    errors = validate_design(a, c, p)
    samples = load(PACKS) if args.check else make_samples()
    errors += validate_samples(samples)
    alloc = {k: sum((x['NBA_content_allocation'] or {}).get(k, 0) for x in a['acts'])
             for k in ['regular', 'postseason', 'offseason', 'national_team']}
    report = dict(PASS=not errors, scope='STRUCTURE_AND_CONTENT_HASHES_ONLY',
                  acts=len(a['acts']), subacts=len(a['subacts']), planned_units=a['total_planned_units'],
                  episode_outlines_completed=0, NBA_content_allocation=alloc,
                  career_seasons=len(c['seasons']), design_samples=len(samples['samples']),
                  independent_review=False, final_design_complete=False,
                  manuscript_allowed=False, errors=errors)
    if not args.check and not errors:
        for path, data in [(PACKS, samples), (REPORT, report)]:
            (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
