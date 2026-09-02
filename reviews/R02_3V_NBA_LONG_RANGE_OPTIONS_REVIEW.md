# R02-3V NBA Long-Range Options Independent Review

- 기준일: 2026-09-02
- 대상: `design/NBA_LONG_RANGE_CAREER_OPTIONS.md` 및 관련 상태·게이트 수정
- 최종 판정: `PASS_FOR_AUTHOR_SELECTION / NOT_CANON`
- 원고 게이트: `CLOSED`

## 1차 검토 판정

초안은 `REVISE_BEFORE_AUTHOR_SELECTION`이었다.

| 등급 | 발견 | 조치 |
|---|---|---|
| BLOCKER | 2021 ECF·Huerter/Murray/Collins 거래·감독 교체를 접촉 뒤에도 고정 역사처럼 사용 | 전부 `ACTUAL_HISTORY_REFERENCE / CONDITIONAL_BRANCH`로 하향 |
| HIGH | 3·4년차 옵션 행사·QO·RFA·중형 계약을 자동 경로처럼 사용 | rookie-scale 구조와 실제 행사 결정을 분리하고 모든 계약 결과를 조건부로 변경 |
| HIGH | Chicago #4를 실제 Top 3 보존 때문에 추천 | 보존 논리를 제거하고 순번·팀 보드·의료·신체 적합이 독립적으로 #4를 설명할 때만 유효하도록 변경 |
| HIGH | 2029~31 우승·2034~36 은퇴 창을 공통 불변값으로 사용 | 비교용 후보 시간창으로 하향, 별도 작가 선택·인과 계산 HOLD |
| HIGH | C안과 Chicago안이 계산 전에 과도하게 우세 | `CALCULATION_PENDING_LEAN`으로 하향 |
| HIGH | 실제 역사 훼손 등급을 원장 없이 단정 | 노출 기간·접촉 사건을 표시하고 나비효과 등급은 `UNSCORED`로 변경 |
| MEDIUM | NBA 75~85% 목표의 수치 검산 장치 부재 | G13에 예상 회차·구간 비율·NBA 내부 비율 검산과 범위 초과 FAIL 추가 |
| MEDIUM | 결말 동료 3-Act가 이름만 세 구간으로 충족될 위험 | `3개 Act × 상호 비용 사건 × 비가역적 관계 상태 변화` 원장 요구 |
| MEDIUM | 재분할 뒤 낡아질 `Act 10` 고정 참조 | `최종 Act`로 변경 |

## 재검토

위 조치 반영 뒤 남은 BLOCKER는 없다.

- 정확한 장기 팀·계약액·라이벌 순번·우승 연도·은퇴 연도·결말 동료는 잠기지 않았다.
- C안과 Chicago안은 작가가 비교할 수 있는 잠정 선호일 뿐 정본이 아니다.
- E0/제목 게이트 분리, G04·G13 상태 수정, G16 최종 전체 검수 정의는 기존 정본과 충돌하지 않는다.
- `PROJECT_FREEZE v0.25 PARTIAL`, `manuscript_allowed: false`, 원고 게이트 `CLOSED`를 유지한다.

## 선택 뒤 재개 조건

1. O-11A·O-11B 작가 선택을 기록한다.
2. R09에서 2018-20 승패·순위·로터리·픽 소유권을 닫는다.
3. 선택 팀의 분·점유율·계약·밀려난 실존 선수 경로를 계산한다.
4. 결말 동료 3-Act 원장과 NBA 75~85% 회차 검산을 통과한다.
5. 그 뒤에만 `canon/CAREER_TIMELINE.md`와 PROJECT_FREEZE 승격을 검토한다.
