# CP2 통합 검토 패킷 — 2021 잠정 결산부터 은퇴까지

- 상태: `PROVISIONAL_REVIEWABLE_PACKET / NOT_DESIGN_COMPLETE`.
- 기준: PR #167 main `8bd0cc8a9aefeda72e4683a35bceba646f3a50a2`.
- 사용자 자동 후속 지시와 [CP2 절차 승인](../canon/CHICAGO_2020_21_CP2_APPROVAL.json)에 따라 작성했다. 최종 정본 승격·집필 허가는 포함하지 않는다.

## 지금 한 번에 검토할 수 있는 연결

| 범위 | 추천 또는 검증된 조건부 결과 | 단일 상세 권위 |
|---|---|---|
| 2020–21 | K1 Chicago31–41·L2 WAS 승리/IND 패배 | [K](../simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.md), [L](../simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.md) |
| 2021 추첨 | 사전 게시 후 첫 결과 CHA/HOU/ORL/OKC; CHI10·39, MIN7·36 원소유 순번 | [잠정 추첨](../simulation/NBA_2021_PROVISIONAL_DRAFT.md) |
| 2021–23 | G1A/E2·G8 SQ1 취득 순서·CX1 Carter 연장 제안·2022 유지 조건 | [G8 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [G1 분 배분](../simulation/CHICAGO_2021_23_CONTINUATION.md) |
| 2021 후보 명단 | G7 DB1 CHI10 Duarte/39 Wieskamp 주 비교안; 15자리·G3 비용 유지 | [G7 전체 비교](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md), [G3 비용](../simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.md) |
| 장기 | H2 2026 실패→2028 CHI–MIN 재대결→2035 은퇴 기능, RC1 LaMelo; G9 기존 옵션·새 계약 비용 | [장기 패킷](CHICAGO_MINNESOTA_LONG_CAREER_PACKET.md), [장기 비용](../simulation/CHICAGO_LONG_CORE_CBA.md) |
| 우승/수상 | AW2의 CHI2028·2031 우승, P2027 MVP·2028/2031 FMVP 후보 | [기계 원장](CHICAGO_MINNESOTA_LONG_CAREER_PACKET.json) |
| 전체 구조 | 14 Act·42 Sub-Act·780 분량 슬롯, NBA81.54% | [Act](ACT_MAP.md), [Sub-Act](SUB_ACT_MAP.md), [5개 약속](CP2_PROMISE_LEDGER.json) |
| 문체 | S1 제한 3인칭 기초안·권한/동작/한국어 규칙 | [하우스 스타일](HOUSE_STYLE_FOUNDATION.md), [실제 독서 범위](../research/STYLE_REFERENCE_ACCESS.md) |
| 문맥 파생 | 설계 검증 샘플2개, 원문 해시로 STALE 감지 | [Context Pack](../context-packs/CP2_DESIGN_VALIDATION_SAMPLES.md) |

## 견인력·주제 자체 점검

1. 성장의 보상은 역할과 책임의 변화다. 전사에서 학교/입학, NCAA에서 소속, NBA 초반에서 출전 기회, 중반에서 공동 에이스, 정점에서 실패를 포함한 마지막 선택으로 달라진다.
2. 경기 외 비용이 성과를 제한한다. E2는 싼 계약 신화로 코어를 공짜 보존하지 않으며, 2026 새 계약은 벤치·분·LaVine의 역할을 다시 묻는다.
3. 라이벌은 주인공을 기다리는 인물이 아니다. 국내 잔류·ACL/학적·Gonzaga 복귀·MIN 창조 역할·2023 대표팀 협력·후대 독립 코어 판단이 별도다. 라이벌의 모든 수상·의료 경과를 주인공 곡선에 종속시키지 않는다.
4. 결말 동료 RC1은 A06·A08·A11·A12에 걸쳐 볼과 권한·실패·잔류 비용을 갖는다. 마지막 패스가 갑자기 등장한 선행 없는 교훈이 되지 않도록 P3가 연결한다.
5. A11 패배와 A12 탈락은 같은 실패의 반복으로 쓰지 않는다. 전자는 수비 선제 회전과 자기 슛 선택, 후자는 새 계약 뒤 팀 깊이와 동부 경쟁의 비용이다. 실제 시리즈가 이 차이를 증명하는지는 아직 미검증이다.
6. A14는 우승 트로피 목록 대신 주전 지위·분·계약·은퇴 뒤 준비의 전수로 종료한다. 15개 분량 슬롯은7시즌을 자세히 서술하겠다는 약속이 아니다.

위는 설계자의 자체 점검이다. 실제 독자 견인력·완성 원고 낭독·독립 검토 PASS가 아니다.

## 남은 작업의 닫힘 기준

새로운 경기 점검 목록을 무한히 늘리지 않는다. 기존 HOLD를 아래 사용 지점에 연결하고 동일 근거를 반복 수집하지 않는다.

| ID | 미완료 | 닫는 데 필요한 것 | 현재 가능한 후속 |
|---|---|---|---|
| D1 | 네 K 실행 묶음의 정확 사실/최종 채택 | [시즌 채택 준비](../simulation/CHICAGO_2020_21_ADOPTION_READINESS.md)의 기존 필드 회수·작가 선택 | K1/L2/M을 조건으로 설계 계속 |
| D2 | 2021 선수 보드·실제 계약 | 바뀐 top4부터 보드/소유권, CHI10·39와 백업C 취득·예외 순서 | [G7 60픽 비교](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)·G3 비용 사용, 최종 당일 거래/계약은 미완료 |
| D3 | 2022–23 실제 분·성적·픽/계약 | 실제 가용성·연장·RFA·팀 재정과 전체 경로 | G8의 QO·Carter/옵션·192재정조건으로 비용 비교 |
| D4 | 2023 대표팀·병역·새 CBA | 기존 범위 게이트 재개 조건에 따른 사실 조사와 전 경기 인과 | H2/NM1 조건부, 불성립 시 공백 분기 |
| D5 | 장기 시즌·수상·동료 잔류 | H2/RC1/AW2의 전력·계약·상대·가용성 연결과 선택 | 역할·실패·종료 기능표 사용 |
| D6 | G11 참고작 합성 | 10작품+예비3·4플랫폼·실제 회차 독서와 기능 비교 | 하우스 스타일 기초 규칙만 사용 |
| D7 | 확정 회차 기능표·실제 Context Pack | 선행 사건 채택 후 회차별 상태 변화와 이력 | 현재42 Sub-Act·2설계 샘플만 검증 |
| D8 | 전체 독립 검수·작가 승인 | 완성본의 독립 검토와 G17 명시 승인 | 자체 점검과 근거 패킷 제공 |

`D1~D8`은 새 승인 게이트가 아니라 기존 미완료 항목의 사용 지점 색인이다. 자동 계속 승인을 철회하거나 CP2를 다시 묻지 않는다. 개별 미확보 필드 수가 큰 작업 수와 같지 않으며, 진행 중 포함 남은 큰 작업은6개다.

## 유지되는 경계

`PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 세계관 v1.0·최종 통합 완료로 표시하지 않는다. 780개 회차 기능표를 자동 복제해 완성 수를 부풀리지 않는다.

## O-15G5 — 2021 픽 원소유·조건부 거래 연결

`simulation/NBA_2021_DRAFT_ASSETS.md` 및 동명 JSON은 네 거래 정책240행을 제공한다. AP1 Boston Kemba/Horford 교환 진행·NOP/MEM 교환 없음이 후속 추천이다. 순번 대신 원소유를 이동하므로 NOP/MEM 대안은9/17/40/49를 쓴다. Dallas 유래52의 현금 매각은 미실행, Lakers 유래53은 DET다. Fournier의 BOS/MEM2025 뒤 순번과 Kemba의 앞 순번을 분리하고,2023 Boston 수취의 중첩식을24순서로 검사했다. 미래 실제 순번/거래 적법성·최종60픽 지배권은 미확정이다.

G4 DB1의 Chicago10 Duarte 추천과 G3 급여를 유지한다. Chicago39 및15~60 지명은 다음 선수·목적 거래 비교 대상이다. 전체1완료·6진행/남은큰작업6개, 자체검토 NOT_INDEPENDENT, v0.30 PARTIAL·설계/원고 CLOSED 유지.

## O-15G6 — 1라운드 보유 선택 후속 비교

`simulation/NBA_2021_FIRST_ROUND_CONTINUATION.md` 및 동명 JSON은 G4 네 안/G5 AP1에15~30 비교64행을 추가한다. 전체120행은 추가 거래를 제한한 비교이며 최종 드래프트가 아니다. DB1~3은 HOU Sengun16 목적 거래 제안, DB4는 대상 부재로 이전 없음·OKC Ziaire16/MEM Bouknight17이다. 다른 당일 거래의 작가 거절이나 전체 구단 인사/의료 감사 완료로 해석하지 않는다. G3 급여·CHI10 Duarte 주 비교안은 유지하며39순위는31~38 이후에 판정한다.

DET/WAS의 별도 미래1R 보호·2R 전환과 선행연도 공백을 검사했다. 신규6개 PASS, 자체검토 NOT_INDEPENDENT. 전체1완료·6진행/남은큰작업6개, v0.30 PARTIAL·설계/원고 CLOSED 유지. 다음은2라운드 잔여 후보와39순위 연결 및 당일 거래 비교다.

## O-15G7 — 60픽 비교와 Chicago39 연결

`simulation/NBA_2021_FULL_DRAFT_COMPARISON.md` 및 동명 JSON은 G4/G5 AP1/G6에2라운드120행을 더한4안240행을 제공한다. DB1 Chicago10 Duarte·39 Wieskamp가 최신 주 비교안이다. G3의39후보는 NYK23 Ayo/UTA30 Thor/ORL33 Herbert/NOP34 Edwards로 먼저 소모된다. C39A~D 네 후속 후보와SAS44/TOR48 파급,15자리·G3 대비 예산차0을 연결했다.

60행 비교의 미판정0은 최종 드래프트 완료가 아니다. 당일 추가 거래·전체 등록·대체세계 대학 참가자 집합·의료/프런트 감사는 미완료다. 신규6검사 PASS·자체검토 NOT_INDEPENDENT. 전체1완료·6진행/남은큰작업6개, author/season/exact/manuscript false·v0.30 PARTIAL·설계/원고 CLOSED 유지. 다음은 Chicago의 이름 있는 취득/예외 순서와2022–23 계약 조건이다.

## O-15G8 — Chicago 취득 순서·2022 계약 조건

`simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md` 및 동명 JSON은 SQ1 NTMLE 유지 추천과세 대안,240조건을 제공한다. SQ3 Mark 먼저/Caruso cap 공간의 추가 normal cap 한도는 $11,369,971, SQ4는 $6,866,356이며 정확 R은 null이다. NTMLE 잔액 소멸과그해 hard-cap 유지를 분리했다.

P QO30쌍·Carter CX1~4(CX1 4년50m 제안 추천)·2022 유지192조건/방출잔액을 연결했다. G1A/E2/G7 10 Duarte·39 Wieskamp는 조건부 주 경로다. 신규7검사 PASS, 실제 계약/시즌·2022 지명·2023 시장은 미완료. 전체1완료·6진행/남은큰작업6개, NOT_INDEPENDENT·author/season/exact/manuscript false·v0.30 PARTIAL·설계/원고 CLOSED 유지.

## O-15G9 — 장기 핵심 선수 비용과 새 CBA 조건

`simulation/CHICAGO_LONG_CORE_CBA.md` 및 동명 JSON은 G2의 비율 목표를 실제 계약 기간에 대조한다. LM1 2023 LaMelo 5년 25→30% 연장 제안·BC1 P30/LaMelo25/LaVine 기존 옵션을 주 비교안으로 추천한다. 모두 미합의다. LaVine의 2026 옵션 $48,967,380을 18% 새 가격으로 낮춰 계산하지 않는다.

40비용 조건과44 CBA 표 조건을 연결했다. 실제2026 참고 cap에서 BC1 선수 예산 $205,210,600은 second 아래 $16,475,400이며, 미배정 예비비까지 포함한 계획 총액은 second보다 $20,700 크다. 예비비를 실제 charge로 판정하지 않는다. 동결 픽·수상 출전 기준·2023 전환 조항·2030 이후 규정 미확보를 구분했다. 신규8검사 PASS, 자체 검토 NOT_INDEPENDENT. 전체1완료·6진행/남은 큰 작업6개, author/season/exact/manuscript false·v0.30 PARTIAL·설계/원고 CLOSED 유지.
