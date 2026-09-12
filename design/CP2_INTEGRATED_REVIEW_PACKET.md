# CP2 통합 검토 패킷 — 2021 잠정 결산부터 은퇴까지

- 상태: `PROVISIONAL_REVIEWABLE_PACKET / NOT_DESIGN_COMPLETE`.
- 기준: PR #167 main `8bd0cc8a9aefeda72e4683a35bceba646f3a50a2`.
- 사용자 자동 후속 지시와 [CP2 절차 승인](../canon/CHICAGO_2020_21_CP2_APPROVAL.json)에 따라 작성했다. 최종 정본 승격·집필 허가는 포함하지 않는다.

## 지금 한 번에 검토할 수 있는 연결

| 범위 | 추천 또는 검증된 조건부 결과 | 단일 상세 권위 |
|---|---|---|
| 2020–21 | K1 Chicago31–41·L2 WAS 승리/IND 패배 | [K](../simulation/CHICAGO_2020_21_SEASON_RECOMMENDATION.md), [L](../simulation/CHICAGO_2020_21_EXECUTION_CLOSEOUT.md) |
| 2021 추첨 | 사전 게시 후 첫 결과 CHA/HOU/ORL/OKC; CHI10·39, MIN7·36 원소유 순번 | [잠정 추첨](../simulation/NBA_2021_PROVISIONAL_DRAFT.md) |
| 2021–23 | G1A 코어 유지·Caruso·Theis 이탈, E2 직접 RFA4년 $98.56m 예산 | [G1 예산/분 배분](../simulation/CHICAGO_2021_23_CONTINUATION.md) |
| 장기 | H2 2026 실패→2028 CHI–MIN 재대결→2035 은퇴 기능, RC1 LaMelo | [장기 패킷](CHICAGO_MINNESOTA_LONG_CAREER_PACKET.md) |
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
| D2 | 2021 선수 보드·실제 계약 | 바뀐 top4부터 보드/소유권, CHI10·39와 백업C 취득·예외 순서 | G1A의 자리·예산 범위 사용 |
| D3 | 2022–23 실제 분·성적·픽/계약 | 실제 가용성·연장·RFA·팀 재정과 전체 경로 | E2와 48재정조건으로 비용 비교 |
| D4 | 2023 대표팀·병역·새 CBA | 기존 범위 게이트 재개 조건에 따른 사실 조사와 전 경기 인과 | H2/NM1 조건부, 불성립 시 공백 분기 |
| D5 | 장기 시즌·수상·동료 잔류 | H2/RC1/AW2의 전력·계약·상대·가용성 연결과 선택 | 역할·실패·종료 기능표 사용 |
| D6 | G11 참고작 합성 | 10작품+예비3·4플랫폼·실제 회차 독서와 기능 비교 | 하우스 스타일 기초 규칙만 사용 |
| D7 | 확정 회차 기능표·실제 Context Pack | 선행 사건 채택 후 회차별 상태 변화와 이력 | 현재42 Sub-Act·2설계 샘플만 검증 |
| D8 | 전체 독립 검수·작가 승인 | 완성본의 독립 검토와 G17 명시 승인 | 자체 점검과 근거 패킷 제공 |

`D1~D8`은 새 승인 게이트가 아니라 기존 미완료 항목의 사용 지점 색인이다. 자동 계속 승인을 철회하거나 CP2를 다시 묻지 않는다. 개별 미확보 필드 수가 큰 작업 수와 같지 않으며, 진행 중 포함 남은 큰 작업은6개다.

## 유지되는 경계

`PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 세계관 v1.0·최종 통합 완료로 표시하지 않는다. 780개 회차 기능표를 자동 복제해 완성 수를 부풀리지 않는다.
