# Design Gate

```yaml
status: CLOSED
manuscript_allowed: false
authority: this_file
last_reviewed: 2026-09-09
```

## 절대 규칙

상태가 `OPEN`으로 명시적으로 변경되기 전에는 프롤로그, 본편, 에필로그, 시험 장면을 작성하지 않는다. “한 장면만”, “문체 테스트”, “홍보용 맛보기”도 원고에 포함된다.

## OPEN 수용 기준

아래 항목이 모두 `PASS`이고 미해결 `BLOCKER/HOLD`가 0개일 때만 열 수 있다.

| 게이트 | 요구 산출물 | 현재 |
|---|---|---|
| G00E 시대 패키지 | 시작·프렙·NCAA·드래프트 시대 | PASS — 2018 E0·2017-18 Villanova LOCK |
| G00T 정식 제목 | 정식 제목과 표기 규칙 | HOLD |
| G01 핵심 정본 | 장르·질문·성장축·결말 기능 | PARTIAL_PASS |
| G02 인물 정본 | 주인공·주요 인물·관계·욕망·결핍·권한 | FOUNDATION_PASS — 무목표·게임·출석, 동갑 라이벌, 입문 3단 동기, 책임 성장 5단계 잠금. 조연·학교 권한·세부 사건 HOLD |
| G03 신체/기술 모델 | 키 성장·포지션·훈련·부상 한계 | FOUNDATION_PASS — 천재성/BQ와 라이벌 ACL·단계별 복귀 안전선 잠금. 주인공 연도별 신체·개별 의료 수치 HOLD |
| G04 한국 농구 세계 | 선택 시대의 학교·대회·스카우팅·문화 | FOUNDATION_PARTIAL — 2015 입문·같은 고교·미국행 인과 LOCK, 교명·개별 대회/권한 HOLD |
| G05 미국 프렙 세계 | 입학·비자·학사·리크루팅·생활 | FOUNDATION_PASS — 가상 뉴잉글랜드 보딩 프렙·2016년 3월 편입·2017년 5~6월 조기졸업 구조 LOCK. 교명·개별 학점 감사 HOLD |
| G06 NCAA 세계 | 선택 시대의 자격·규정·일정·리크루팅 | FOUNDATION_PASS / COLLEGE_SCOPE_COMPLETE / RIVAL_COLLEGE_SCOPE_COMPLETE — 주인공 Villanova 역할과 라이벌 Gonzaga 0경기 레드셔츠·WCC 우승 기능 LOCK. 양쪽 개별 인증·counter·정확 기록 HOLD |
| G07 NBA 세계 | 선택 드래프트의 CBA·로스터·계약·미디어 | FOUNDATION_PASS / CHICAGO_LANDING_REOPENED / COMMERCIAL_RELATIONSHIP_FOUNDATION_COMPLETE — Chicago 원클럽·라이벌 Minnesota #1·2020 picks 1~60과 rookie-scale 방향 LOCK. 주인공 2018 정확 순번·관계·Riller 계약 HOLD |
| G08 역사 기준선 | 시즌별 고정 사건과 검증 출처 | FOUNDATION_PARTIAL — 2018/2023 대표팀·병역 일정 기준선 완료, 전체 시즌 기준선 R09 대기 |
| G09 인과 시뮬레이션 | 접촉 사건·파급 사건·대안 결과 | PROTOCOL_PASS / CHICAGO_2020_21_PREDEADLINE_OUTCOME_PASS / LOW_COST_CENTER_DIRECTION_LOCKED / O15F5_BOARD_PASS — Atlanta 원장은 폐기 분기 증거로 보존. Chicago 2018-20 donor·생산성 범위와 2019/20 lottery·2020 picks 1~60, 2020-21 opening 15+2·마감일 전 역할·생산성·19~21승 중심 범위 통과. Vučević 패키지 거부·저비용 센터 우선 작가 승인, Theis·Green 3팀 5인 A PRIMARY_LEAN. exact 거래·박스·승수·부상·Riller 계약 HOLD |
| G10 결말/주제 | 장면 기능·인물 선택·대가·잔상 | DRAFT |
| G11 하우스 스타일 | 단일 문체 규약과 합법적 참고작 기능 합성 | NOT_STARTED |
| G12 서사 장치 | 장치 예산·복선/회수 원장·Hoffman Unity | FRAMEWORK_PASS / ASSIGNMENTS_BLOCKED |
| G13 전체 구조 | 모든 Act/Sub-Act/회차 기능표 | NBA_LONG_RANGE_RECALCULATION — 15~25% 전사 / 75~85% NBA, Chicago 원클럽·라이벌 Minnesota #1 LOCK. 정확 시즌·결말 동료 HOLD |
| G14 Context Pack | 활성 장치 필드·샘플·무결성 검사 | PARTIAL |
| G15 통합/견인력 검수 | Unity 및 연재 견인력 기준 통과 | NOT_STARTED |
| G16 독립 검수 | 완성된 전체 설계의 맹점·모순·정의 누락 검토 | FINAL_WHOLE_DESIGN_REVIEW_NOT_STARTED — 구간별 독립 검토 이력은 존재 |
| G17 사용자 승인 | 설계 100% 완료에 대한 명시 승인 | NOT_STARTED |

## 개방 절차

1. 모든 게이트의 증거 링크를 붙인다.
2. 독립 검수자는 정본·요구·제약만 받아 재검사한다.
3. `PROJECT_STATE.md`의 열린 위험과 HOLD가 0인지 확인한다.
4. 사용자가 설계 완료와 집필 전환을 명시적으로 승인한다.
5. 별도 커밋/PR에서만 `status: OPEN`, `manuscript_allowed: true`로 바꾼다.

설계 작업자가 편의를 위해 스스로 열 수 없다.

## O-15F6 최신 판정 — 2026-09-09

G09의 O-15F5 A는 `AUTHOR_APPROVED_PLAYER_ROUTE`로 갱신됐다. 후반 29경기 실제 기준선과 조건부 분·선발 용량은 통과했지만 거래 세부·가용성·5인 조합·상대 roster·생산성·승패는 HOLD다. G09 전체 PASS 및 원고 개방으로 확대하지 않는다. 다음 O-15F6B.

## O-15F6D 최신 판정 — 2026-09-09

G09는 `POSTDEADLINE_CONDITIONAL_CAPACITY_AND_CARTER_RESPONSE_PASS / O15F7_INPUTS_NEXT`다. 위 O-15F6의 다음 O-15F6B 포인터는 과거 기록이다. 116개 Carter 대응 시험에서 비상 정책을 포함한 29/29 분 증명을 얻었으나 실제 부상·거래 세부·상대 변화·생산성·승패는 미확정이다. 세계관 완성까지 진행 중인 시즌 원장을 포함해 큰 작업 6개가 남는다. G11·G15·G16 최종 검수·G17을 완료로 바꾸지 않는다.

## O-15F7 최신 판정 — 2026-09-09

G09는 `POSTDEADLINE_OBSERVATION_AND_CHICAGO_BOX_INPUT_PASS / O15F8_IMPACT_INPUTS_NEXT`다. 실제 양 팀815행·cutoff300명·조건부174박스 입력과 LaMelo 잔여3조건 대응이 통과했다. 상대7팀10경기 변경 분은 미배정이며 나머지19경기도 리그 전체 무영향 FINAL이 아니다. 정확 부상·거래 조항·양 팀 impact·승패 및 최종72경기 정본은 HOLD다. 위 과거 포인터를 최신 완료 상태로 오인하지 않는다.
