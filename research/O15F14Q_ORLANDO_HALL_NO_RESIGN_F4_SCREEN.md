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

### 5월 원역사 건강·출전 대조 (후속 검문)

| 경기 | 원역사 관측 | 선택 경로의 선별 분 | 판정 |
|---|---|---|---|
| 5/9 MIN | [NBA 원경기 기록](https://www.nba.com/magic/game/0022001022): Bamba 19:44, Wagner 24:25 출전 | Bamba 24.40, Wagner 27.27분 | 실제 출전 사실은 확인. 각각 약 +4.66, +2.85분의 대체 부하는 건강·코칭 `HOLD` |
| 5/11 @MIL | [NBA 경기 전 보고](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-11_08PM.pdf): Bamba `Out`, 비 COVID 질환 | Bamba 0, Wagner 36.00, Nnaji 16.00분 | Bamba의 원역사 결장과 선별안은 충돌하지 않음. Wagner/Nnaji 부하 `HOLD` |
| 5/13 @ATL | [NBA 경기 전 보고](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-13_05PM.pdf)와 [Orlando 구단 프리뷰](https://www.nba.com/magic/orlando-magic-atlanta-hawks-game-preview-story-20210513): Bamba `Questionable`, 비 COVID 질환 | Bamba 0, Wagner 36.00, Nnaji 14.07분 | `Questionable`을 `Out` 확정으로 바꾸지 않음. 미출전 선택과 다른 선수의 부하 `HOLD` |
| 5/14 @PHI | [NBA 경기 전 보고](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-14_05PM.pdf): Bamba `Questionable`; [Orlando 경기 후 보도](https://www.nba.com/magic/news/magic-lose-philly-first-two-games-against-76ers-finish-season-20210514): 앞선 두 경기 결장 뒤 복귀 출전 | Bamba 23.50, Wagner 19.52분 | 출전 가능성은 원역사로 뒷받침되나 추가 4.38분·연전 체력 `HOLD` |
| 5/16 @PHI | [NBA 최종 경기책](https://statsdmz.nba.com/pdfs/20210516/20210516_ORLPHI.pdf): Bamba 22:55, Wagner 34:38 출전 | Bamba 30.00, Wagner 29.55분 | Bamba의 추가 7.08분은 모델 상한에 맞춘 후보일 뿐 의료 허용치가 아님 |

위 대조는 원역사 **출전/상태의 증거**와 대체 세계 **선수별 분 후보**를 구분한다. 특히 Bamba의 5/11 원역사 `Out`을 무시해 빠진 Hall 분을 채우지 않았고, 5/13 `Questionable`을 대체 세계의 새 진단으로 변환하지 않았다. 다섯 경기의 5인조·240분 산술은 기존 JSON에서 통과했지만, Wagner의 5/11·13 각 36분 및 Bamba의 5/16 30분에 대한 대체 건강·체력·감독 선택은 확인되지 않았다. F4/A1·최종 시즌은 여전히 `HOLD`다.

[5/16 부하 민감도](O15F14AL_ORLANDO_HALL_FINAL_GAME_LOAD_BOUND.md)는 원역사 출전 상한을 적용해 Bamba `22:55`·Wagner `34:38`·Nnaji `10:00`의 다른 5인조 증인을 찾았다. 위 표와 원 JSON은 최초 선별 이력으로 유지한다. 새 증인도 대체 건강 허가나 전체 F4 PASS가 아니다.

## F4 판정과 다음 연결

선택된 경로에서는 Hall 추가 일반계약 자리와 그 재계약 비용, 대체 세계의 hardship 신청·허가 사건이 **필요하지 않다**. 대신 다섯 경기의 선수별 분·체력 및 경기 결과를 검토해야 한다. Hall을 남기는 이전 경로에는 [D1 종료 묶음](../simulation/CHICAGO_2020_21_D1_CLOSEOUT_BATCH.md)의 A1 건강·A2 행정 조건이 적용됐었다. 두 경로를 합쳐 필요조건을 지우지 않는다.

F1~F3·F5의 정확 실행, F4 후보 채택, A1~A3 및 네 K 묶음이 열려 있으므로 D1은 여전히 `OPEN`이다. 이 선별에서 전체 F PASS는 `0/5`, A 최종 채택은 `0/3`, K 종료는 `0/4`다.
