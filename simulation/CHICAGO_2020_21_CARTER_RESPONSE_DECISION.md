# Carter 공백 대안 — O-15F6D

- 상태: `BOUNDED_RESPONSE_AUDIT_COMPLETE / CONDITIONAL_29_OF_29 / ACTUAL_INJURIES_HOLD`
- 입력: O-15F6C의 Carter 단독 결장 29조건
- 기준 main: `aabceef75b3be615856f07cdd4b1cbd73263b8c5` (PR #136)
- 원고: `CLOSED / manuscript_allowed: false`

## 결과와 권고

| 정책 | 조합 성립 | 남은 실패 | 변화 |
|---|---:|---:|---|
| O-15F6C 원래 정책 | 17/29 | 12 | 비교 기준, 재계산하지 않음 |
| 센터 한 명 선발 | 20/29 | 9 | 두 센터 선발 시 Young 한 자리를 가드/윙으로 이전 |
| 위 정책 + Theis 비상 상한 30분 | 24/29 | 5 | 해당 입력에 Theis가 있을 때만 상한 확대 |
| 위 정책 + Young 비상 상한 30분 | 24/29 | 5 | 추가 해결 날짜 없음 |
| 위 정책 + Felicio 비상 상한 18분 | 29/29 | 0 | 실제 출전 또는 Coach's Decision DNP 근거가 있는 날만 후보 추가 |

**총괄 권고:** 원래 정책으로 되는 날은 유지한다. 안 되는 날에 선발 중첩을 먼저 줄이고, 그래도 부족하면 Theis 비상 분을 검토한다. Theis가 입력에 없는 다섯 조건은 Young·Felicio 조합을 별도 저효율 위험 분기로 보존한다. 모든 날 Theis 30분·Felicio 18분을 주는 주전 재편이 아니다. Young 상한 확대만으로 새로 해결되는 날이 없으므로 독립적인 추가 해결책으로 세지 않는다.

새 정책 4개 × 29날짜 = **116개 독립 시험**이다. 같은 시즌의 116경기가 아니며 Carter가 29경기 결장한다는 설정도 아니다. 앞선 LaMelo 3개 실패는 이 감사로 해결되지 않는다.

## 선발·분 정책

센터 둘이 선발일 때 Young의 선발 한 자리를 같은 날 입력의 Temple→Satoransky→Coby→Green→Valentine→Porter→Arcidiacono→Dotson→Mokoka 순에서 처음 가능한 선수에게 넘긴다. 원래 선발인 선수는 제외한다. 나머지 선발과 주인공·LaMelo·Porter·LaVine의 분을 고정한다. 선발 조합에는 3분을 배정할 수 있어야 한다.

Theis 30분 정책은 기존 `실제 분+6분` 상한도 대체하는 비상 가정이다. 의학적 안전 시간이나 코치의 실제 결정이 아니다. Young은 기존 상한과 30분 중 큰 값을 쓴다. 따라서 05-15의 기존 30:03은 30:00으로 줄이지 않는다. Felicio는 기존 상한과 18분 중 큰 값을 쓰며 새 DNP 후보의 하한은 0이다. 모든 다른 하한·상한은 선행 감사와 같다. 선수의 등록·건강 상태를 기록 행 하나로 확정하지 않는다.

5인 조합, 최소 한 센터·볼 운반자·윙, 동시 최대 2빅, 총 48분을 유지한다. 조합은 순서 없는 존재 증명이다. 선수별 절대 변경량 합은 Carter의 빠진 시간과 같아 불필요한 추가 분 이전 없이 공백을 채웠음을 확인했다. 여러 동률 해 중 한 증명이며 전술 최적해가 아니다.

## 남았던 다섯 조건의 근거

| 날짜 | 상대 | Felicio 실제 원장 | 마지막 정책의 센터 분 증명 |
|---|---|---|---|
| 03-27 | SAS | 실제 출전 1:46 | Young 30:00 + Felicio 18:00 |
| 04-06 | IND | 실제 출전 1:21 | Young 30:00 + Felicio 18:00 |
| 05-09 | DET | DNP - Coach's Decision | Young 30:00 + Felicio 18:00 |
| 05-13 | TOR | DNP - Coach's Decision | Young 30:00 + Felicio 18:00 |
| 05-15 | BKN | 실제 출전 2:50 | Young 30:03 + Felicio 18:00 |

출전/DNP 근거는 기존 `CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv`의 공식 NBA box-score 수집 행이다. 이번에 공식 PDF 재접근은 실패했으며 PDF를 새로 열람했다고 주장하지 않는다. CSV의 출처 링크와 SHA-256을 보존한다. Theis 행 부재에는 새 부상 진단을 붙이지 않는다. Felicio가 원자료에 없거나 Coach's Decision 이외 이유면 새로운 후보로 추가하지 않는다.

**대가:** Felicio 18분은 이전의 짧은 출전·DNP와 상당히 다른 역할이다. Carter의 공격·수비 생산성을 그대로 옮길 수 없다. Young의 센터 부담, 공격 공간, 파울과 매치업 비용을 후반 생산성 입력에서 다룬다. 29/29 분 성립을 전력 유지·무패·건강 보장으로 승격하지 않는다.

## 종료와 다음 작업

Carter 단독 공백의 분 존재 증명은 이 범위에서 종료한다. 새 실제 가용성 근거 또는 역할 상한 변경이 없는 한 다시 같은 29조건을 돌리지 않는다. 다음은 LaMelo의 남은 세 조건, 후반 실제/가정 가용성 구분, 상대 원장과 생산성 입력이다. 원래 all-active 조건과 결장 스트레스를 섞어 한 시즌으로 합산하지 않는다.

기계 원장: `CHICAGO_2020_21_CARTER_RESPONSES.json`.

검증: `python tools/audit_chicago_2020_21_carter_responses.py` (표준 라이브러리).

재생성: 같은 명령에 `--write` (scipy 필요).
