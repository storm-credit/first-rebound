# Design Gate

```yaml
status: CLOSED
manuscript_allowed: false
authority: this_file
last_reviewed: 2026-08-28
```

## 절대 규칙

상태가 `OPEN`으로 명시적으로 변경되기 전에는 프롤로그, 본편, 에필로그, 시험 장면을 작성하지 않는다. “한 장면만”, “문체 테스트”, “홍보용 맛보기”도 원고에 포함된다.

## OPEN 수용 기준

아래 항목이 모두 `PASS`이고 미해결 `BLOCKER/HOLD`가 0개일 때만 열 수 있다.

| 게이트 | 요구 산출물 | 현재 |
|---|---|---|
| G00 시대/제목 | 시작·프렙·NCAA·드래프트 시대 패키지와 정식 제목 | PARTIAL — 2018 E0·2017-18 Villanova 선택, 제목 HOLD |
| G01 핵심 정본 | 장르·질문·성장축·결말 기능 | PARTIAL_PASS |
| G02 인물 정본 | 주인공·주요 인물·관계·욕망·결핍·권한 | FOUNDATION_PASS — 무목표·게임·출석, 동갑 라이벌, 입문 3단 동기, 책임 성장 5단계 잠금. 조연·학교 권한·세부 사건 HOLD |
| G03 신체/기술 모델 | 키 성장·포지션·훈련·부상 한계 | FOUNDATION_PASS — 천재성/BQ 잠금, 연도별 신체·부상 HOLD |
| G04 한국 농구 세계 | 선택 시대의 학교·대회·스카우팅·문화 | BLOCKED_BY_G00 |
| G05 미국 프렙 세계 | 입학·비자·학사·리크루팅·생활 | FOUNDATION — 2017 졸업 필요, 정확한 학교·학점 HOLD |
| G06 NCAA 세계 | 선택 시대의 자격·규정·일정·리크루팅 | FOUNDATION — Villanova·2018 우승 LOCK, 초기 자격·로테이션 HOLD |
| G07 NBA 세계 | 선택 드래프트의 CBA·로스터·계약·미디어 | BLOCKED_BY_G00 |
| G08 역사 기준선 | 시즌별 고정 사건과 검증 출처 | BLOCKED_BY_G00 |
| G09 인과 시뮬레이션 | 접촉 사건·파급 사건·대안 결과 | NOT_STARTED |
| G10 결말/주제 | 장면 기능·인물 선택·대가·잔상 | DRAFT |
| G11 하우스 스타일 | 단일 문체 규약과 합법적 참고작 기능 합성 | NOT_STARTED |
| G12 서사 장치 | 장치 예산·복선/회수 원장·Hoffman Unity | FRAMEWORK_PASS / ASSIGNMENTS_BLOCKED |
| G13 전체 구조 | 모든 Act/Sub-Act/회차 기능표 | BLOCKED_BY_G00 |
| G14 Context Pack | 활성 장치 필드·샘플·무결성 검사 | PARTIAL |
| G15 통합/견인력 검수 | Unity 및 연재 견인력 기준 통과 | NOT_STARTED |
| G16 독립 검수 | 맹점·모순·정의 누락 검토 | NOT_STARTED |
| G17 사용자 승인 | 설계 100% 완료에 대한 명시 승인 | NOT_STARTED |

## 개방 절차

1. 모든 게이트의 증거 링크를 붙인다.
2. 독립 검수자는 정본·요구·제약만 받아 재검사한다.
3. `PROJECT_STATE.md`의 열린 위험과 HOLD가 0인지 확인한다.
4. 사용자가 설계 완료와 집필 전환을 명시적으로 승인한다.
5. 별도 커밋/PR에서만 `status: OPEN`, `manuscript_allowed: true`로 바꾼다.

설계 작업자가 편의를 위해 스스로 열 수 없다.
