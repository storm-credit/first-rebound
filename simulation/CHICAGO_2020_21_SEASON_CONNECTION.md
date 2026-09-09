# O-15F10 전반 상대 조건부 입력과 72경기 연결

- 판정: `CONDITIONAL_72_GAME_CONNECTION_INPUT_PASS / SEASON_HOLD`
- 선행 main: `cf790094b732f443f86b4d0852735b9f8a0eb5d7` (O-15F9)
- 원고: `CLOSED`, `manuscript_allowed: false`

## 이번에 계산한 것

전반 43경기와 후반 29경기를 같은 점수차·분 영향 형식으로 연결했다. 전반은 양 팀 1,144행을 다시 대조했고, 드래프트·거래 입력이 바뀌는 **10팀 18경기**를 조건부 교체 벡터로 만들었다. 나머지25경기는 제한적 기준선 후보로 남겼다. Minnesota·Denver 연장전은 실제 팀 총초를 보존해 48분으로 잘라내지 않았다.

교체 벡터는 실제로 그 경기에서 뛴 선수의 초를 1:1로 옮기는 시작점이다. 예: Portland는 Trent→Evans, Charlotte는 LaMelo/Riller→Edwards/Terry, Detroit은 Hayes/Bey→Kira/Patrick, Washington은 Bonga→Trent. 0분인 선수를 추가 분의 증거로 쓰지 않는다. Jacob Evans·Fictional Rival처럼 정규시즌 비교 rate가 없는 선수는 계수를 남긴다.

## 시즌 산술 진단

아래는 상대를 실제 분으로 유지한 기준선 진단이다. 후반 변경 상대의 효과는 섞지 않고, 전반 18경기의 교체 벡터도 선택하지 않았다. 따라서 **정본 시즌 성적이 아니다.**

| 계열·prior | 72경기 진단 승수 | 의미 |
|---|---:|---|
| RAPTOR RS EB LOW | 19 | 하방 prior |
| RAPTOR RS EB BASE | 31 | 실제 상대·Chicago 영향만을 기계적으로 합친 값 |
| RAPTOR RS EB HIGH | 34 | 상방 stress |
| BPM 3/25 EB LOW | 20 | 소표본 수축 |
| BPM 3/25 EB BASE | 31 | 회고적 보정 |
| BPM 3/25 EB HIGH | 34 | 상방 stress |

표의 숫자는 전반 기존 원장의 상대 기준선과 후반 두 분 조건을 한 줄로 세어 본 것이다. 거래·가용성·상대 분·라이벌 능력·두 팀의 상호작용이 빠져 있으므로 19~34승의 최종 범위를 뜻하지 않는다. 실제로는 전반의 모든 변경 팀과 후반의 선택된 한 경로를 함께 넣어야 한다. 기존 19~21승은 선행 모형의 역사적 결과로 보존하며 새 산술표와 평균내지 않는다.

## 경로 일관성 규칙

- 한 시즌에서는 Portland의 Trent 부재를 1/5·1/30에 적용하면서 다른 날짜에 Trent를 다시 실제 Portland 선수로 복원할 수 없다.
- Washington·Charlotte·Detroit·New Orleans·Dallas의 드래프트 경로도 같은 규칙을 따른다. 날짜별로 유리한 선수만 골라 합산하지 않는다.
- Gordon A, Powell 잔류, Fournier, Hall 계약, 실제 가용성은 아직 각각 조건부다. Chicago A 승인만으로 이 사건들을 닫지 않는다.
- 후반 39개 상대 분 메뉴와 전반 18개 접촉은 모두 선택 전 입력이다. `selected=false`를 유지한다.

## 전반의 민감 지점

1월30일 Portland전은 선행 RAPTOR BASE에서 **+0.026809점**에 불과했다. Trent→Evans의 미정 rate가 0이 아니면 결과 방향이 달라질 수 있다. 1월5일 Portland도 Evans 18:36의 미정 계수가 있다. 2월24일 Minnesota는 Fictional Rival 계수와 Towns/Russell 공동창출 비용을 함께 정해야 한다. 이 세 날짜를 0능력으로 채우지 않는다.

전반 18경기 중 0분 접촉은 Denver·New Orleans 등에서 보인다. 0분은 새 선수의 0분을 증명하지 않으므로, 그 경기에는 실제 상대 분을 유지한 기준선만 저장했다. 분산된 연장 시간도 후속 점수차 계산에서 실제 값으로 유지한다.

## 다음 단계

O-15F10의 전반 관측·18경기 교체 벡터·72경기 기준선 진단은 완료했다. 다음 O-15F11은 전반 접전인 Portland·Golden State부터 상대 분 조합을 선택해 양 팀 점수차를 계산하고, 이후 다른 변경 팀을 같은 경로로 연결한다. 여기서 처음으로 시즌 단일 경로를 선택할 수 있지만, 거래·가용성 조건이 충돌하면 다시 `HOLD`로 둔다.

재현: `python tools/build_chicago_2020_21_season_connection.py`.
