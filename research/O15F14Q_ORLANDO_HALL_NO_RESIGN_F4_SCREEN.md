# O-15F14-Q — Orlando 5월 Hall 재계약 생략 경로 선별

- 상태: `F4_FEASIBILITY_WITNESS / AUTHOR_DIRECTION_SELECTED / EXACT_EXECUTION_HOLD`.
- 후속 선택: [작가 응답](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)은 이 경로를 선택했다. 아래 표의 선별 계산 자체는 선택 전 후보 출력이며 건강·최종 시즌 PASS로 승격하지 않는다.
- 기준: 기존 K1 LOW_MINUTES 분·역할, Orlando 등록 원장, R1 상대 평점 및 K1의 두 평점법. 계산은 [`screen_orlando_hall_no_resign.py`](../tools/screen_orlando_hall_no_resign.py)와 [결과 JSON](../simulation/ORLANDO_2020_21_HALL_NO_RESIGN_SCREEN.json)에서 재현한다.
- 이 문서는 K1·L2의 정본 변경이나 F4 PASS가 아니다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`를 유지한다.

## 사실과 후보 경계

| 분류 | 내용 |
|---|---|
| 사실 | [Orlando 등록 원장](../simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.md)의 유지 경로에서는 5월 9·11·13·14·16일 일반계약이 16명이고 추가 1자리가 필요하다. Hall의 5월 9일 실제 재계약은 [구단 공지](https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509)에 근거한다. |
| 추론 | 이 대체 명단에서 **5월 9일 Hall 재계약만 생략**하면 다섯 경기의 일반계약 수가 각각 15명, 투웨이가 2명이 된다. 4월의 Hall 계약·출전은 그대로 둔다. |
| 후보 | Hall의 기존 다섯 경기 분을 Bamba·Wagner·Vučević·Nnaji 중 가용한 선수에게 재배정한다. 신규 부상·리그 hardship 승인·무급 계약은 가정하지 않는다. |
| 작가 확정 | 5월 9일 Hall 재계약 생략 방향만 확정. 선수별 건강·정확 분·최종 시즌은 미확정. |

## 다섯 경기 검산

기존 Hall 분 외 모든 선수의 분을 고정하고, 남은 빅맨의 기존 분을 줄이지 않았다. 상한은 Vučević/Wagner 각 36분, Bamba 30분, Nnaji 16분이며 선발 5명 동시 출전 3분과 각 경기 240 팀분을 지켰다. 기존 역할 검사에 통과하는 다섯 명 조합의 시간 분해를 결과 JSON에 기록했다. 상한은 후보 선별용 작업 가정이며 건강 허용치의 사실 확인이 아니다.

| 경기 | 빠지는 Hall 분 | 재배정 대상·분 | BPM 후보 홈 점수차 범위 |
|---|---:|---|---:|
| 5/9 ORL–MIN | 16.72 | Bamba 4.66, Wagner 12.05 | −34.13 ~ −30.46 |
| 5/11 MIL–ORL | 17.05 | Wagner 8.42, Vučević 0.63, Nnaji 8.00 | +8.67 ~ +12.41 |
| 5/13 ATL–ORL | 20.67 | Wagner 14.60, Nnaji 6.07 | +19.34 ~ +23.87 |
| 5/14 PHI–ORL | 7.40 | Bamba 4.38, Wagner 3.02 | +22.66 ~ +24.28 |
| 5/16 PHI–ORL | 25.08 | Bamba 7.08, Wagner 18.00 | +7.00 ~ +12.50 |

표의 반올림 분은 합계가 0.01분 다를 수 있다. 정확 초와 분해는 JSON을 따른다. RAPTOR와 BPM의 **10개 경기·방법 비교에서 승자 방향 반전은 0건**이다. BPM의 Hall 평점 공백은 리그 관측 범위로 처리했고, 5월 14일 연전 피로 변화를 반영했다. 이는 승패 방향의 국소 스트레스 검사다. 실제 경기 결과, 선수 건강, 효율, 앞선 일정의 누적 변화를 증명하지 않는다.

## F4 판정과 다음 연결

선택된 경로에서는 Hall 추가 일반계약 자리와 그 재계약 비용, 대체 세계의 hardship 신청·허가 사건이 **필요하지 않다**. 대신 다섯 경기의 선수별 분·체력 및 경기 결과를 검토해야 한다. Hall을 남기는 이전 경로에는 [D1 종료 묶음](../simulation/CHICAGO_2020_21_D1_CLOSEOUT_BATCH.md)의 A1 건강·A2 행정 조건이 적용됐었다. 두 경로를 합쳐 필요조건을 지우지 않는다.

F1~F3·F5의 정확 실행, F4 후보 채택, A1~A3 및 네 K 묶음이 열려 있으므로 D1은 여전히 `OPEN`이다. 이 선별에서 전체 F PASS는 `0/5`, A 최종 채택은 `0/3`, K 종료는 `0/4`다.
