# G14 집필 전 Pack 검증의 게이트 순환 수리

기준 main `aa8f9186e14f7bbf50d31a0d1ef3573844f2bee0` / PR432 뒤 연속 작업.
판정: **문서상 의존성 순환1개 수리 / G13·역사 잠금·G14 실제 Pack은 미완료 유지**.

## 발견한 실제 순환

[DESIGN_GATE](../control/DESIGN_GATE.md)는 G14 PASS를 OPEN의 선행조건으로 요구한다.
그런데 [Context Pack 규약](../context-packs/README.md)의 이전 문구는 CLOSED 동안 실제 Pack 생성 자체를 금지했다.
그 두 규칙을 함께 읽으면 `실제Pack→G14 PASS→G17→OPEN→실제Pack` 순환이 생겨6번을 끝낼 수 없다.
이는 이미10/4에 수리한 G13 기능표→G14 연결의 다른 문제이며 당시 수리를 반복하지 않았다.

## 최소 변경

집필 전 Pack **생성·검증**과 원고 입력으로 **사용**하는 시점을 분리했다.
전체 Act/Sub-Act/최종 회차 기능표와 역사 원장 잠금, 해당 구간 ACTUAL_VERIFIED Blueprint와 현행 Canon을 먼저 요구한다.
그 이후에는 CLOSED 상태에서 실제 Pack을 생성·검증해 G14를 검사할 수 있다.
G15/G16 전체 검수·G17 명시 승인·별도 개방 PR이 끝나기 전에는 원고 입력으로 사용할 수 없다.

```mermaid
flowchart LR
  A[전체 G13·역사 원장 잠금] --> B[검증 Blueprint·현행 Canon]
  B --> C[Pack 생성·G14 무결성 검증]
  C --> D[G15·G16 전체 검수]
  D --> E[G17 사용자 명시 승인]
  E --> F[별도 PR로 OPEN]
  F --> G[Pack 사용·원고 작성]
```

Pack 생성·G14 검사까지 게이트는 CLOSED이고 manuscript_allowed:false다.
이를 설계 게이트를 스스로 여는 행위나 미선택 사건의 승인으로 처리하지 않는다.
780개 Pack 전부 생성 등 새 수량조건을 추가하지 않았다.

## 현재성과 독립 검문

공통 novel-writing-skill §§13·14·22는 Context Pack을 Episode 앞의 컴파일 산출물로 두고
ACTUAL_VERIFIED Blueprint+Canon을 입력으로 요구한다. OPEN 선행조건은 없다.
독립 검수자가 현행 README·DESIGN_GATE·공통 스킬과10/4 수리를 직접 대조했고
잘못된 OPEN 선행 문구가 README 한 곳에만 있다는 전역 검색을 확인했다.
최종 실제 diff 독립 검문에서 G13/역사 원장/검증 Blueprint 선행과 G17 개방 권한 보존을 확인했다.
검수와 사용자 승인 표현을 분리하고 G14의 기존 활성 장치 필드·샘플 요구도 병기했다.
CP2/A01/DEN 재현 검사 모두 PASS이며, 실제 Pack0·최종 회차0·원고0이다.

README·게이트 현황의 출처 내용 변경에 따라 A01 경계 입력과 Denver 보조 증인의 지문을 재생성한다.
기존 CP2 설계샘플2도 현재 출처를 소비하여 재현한다. 이는 새 실제 Pack 생성이나 기존 후보의 승격이 아니다.
이 문서 수정에 새 NBA 사실 수집은 필요하지 않다. Antigravity·NotebookLM·Claude 신규 실행은 NOT_RUN이며
PR432의 호출을 이 수리의 새 실행으로 합산하지 않는다.

## 최종 상태

G13 최종 회차 기능0·역사 전체 잠금 미완료이므로 실제 Pack0이다.
법적10PASS/2HOLD·F법적3/5·A0/3·K0/4·최종시즌false, 원고0을 유지한다.
6번 완료 경로의 순환을 없앴고, 실제 남은 입력은 회차 기능표·역사 잠금·검증 Blueprint·POV/정보 접근이다.

| 큰 작업 | 상태 |
|---|---|
| 1 2020 드래프트 연쇄 | 완료 |
| 2 Chicago2020–21 | 작업 모델 완료 범위 보존; 법적2행·등록/예비 건강·최종 시즌 미완료 |
| 3 2021–23 거래·계약 | 승인 방향 반영; 정확 실행 미완료 |
| 4 장기 커리어 | 골격 완료; 중요 결과·후속 미완료 |
| 5 결말·구조 | 14막/42소막/780배분; 최종 회차 기능 미완료 |
| 6 집필 규격·Context Pack | 문체 규격 완료·G14 개방 순환 수리; 실제Pack0 |
| 7 통합·독립·작가 승인 | 전체 미완료 |

**미완료 큰 묶음6개. Freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.**
