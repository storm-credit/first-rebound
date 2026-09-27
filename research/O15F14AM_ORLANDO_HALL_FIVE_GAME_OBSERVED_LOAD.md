# O-15F14-AM — Hall 미재계약 5경기 원경기 노출량 상한

- 상태: `F4_FIVE_GAME_LOAD_BOUND_LOCAL_PASS / HEALTH_AND_EXACT_SEASON_HOLD`.
- 재현: [`screen_orlando_hall_five_game_load.py`](../tools/screen_orlando_hall_five_game_load.py) → [5경기 JSON](../simulation/ORLANDO_2020_21_HALL_FIVE_GAME_LOAD_SCREEN.json). [최초 5경기 화면](O15F14Q_ORLANDO_HALL_NO_RESIGN_F4_SCREEN.md)과 [5/16 단독 민감도](O15F14AL_ORLANDO_HALL_FINAL_GAME_LOAD_BOUND.md)는 비교 이력으로 보존한다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, F1~F5 전체 PASS `0/5`, A1~A3 최종 채택 `0/3`, K 종료 `0/4`.

| 구분 | 판정 |
|---|---|
| 사실 | [원경기 분 데이터](../simulation/NBA_2020_21_FINAL859_MINUTES.json)의 5/9·11·13·14·16 Hall 출전과 Bamba/Wagner의 출전·미출전, [NBA 5/16 경기책](https://statsdmz.nba.com/pdfs/20210516/20210516_ORLPHI.pdf), [Bamba 당시 상태 출처 대조](O15F14Q_ORLANDO_HALL_NO_RESIGN_F4_SCREEN.md#5월-원역사-건강출전-대조-후속-검문)를 입력으로 쓴다. 5/11 Bamba 보고는 `Out`, 5/13은 `Questionable`이었고 K1 분 입력은 두 경기 모두 Bamba 0분이다. `Questionable`을 의학적 `Out`으로 바꾸지 않는다. |
| 추론 | 다른 K1 선수 분을 고정하고 Hall만 빼면, Bamba가 없는 두 경기에는 Vučević 36분·Nnaji 16분의 선별 상한을 모두 채워도 Wagner의 원경기 분보다 각각 3:03·6:40이 더 필요하다. 이는 **이 모델의 하한**이며 리그/의료 허용치가 아니다. |
| 후보 | Bamba는 원경기 출전 3경기의 분을 넘기지 않는다. Wagner는 5/9·14·16 원경기 분을 넘기지 않고 5/11·13만 위 하한만큼 늘린다. 나머지 Hall 분은 Vučević/Nnaji에게 배정한다. |
| 작가 확정 | Hall의 4월 두 계약과 앞선 출전은 보존하고 **5/9 신규 재계약은 생략**한다. 따라서 이 선택 경로의 5/9·11·13·14·16에는 Hall이 등록·출전하지 않는다. 아래 대체 분·건강·정확 승패는 미확정. |

| 경기 | Hall 제거 | Bamba 후보 | Wagner 후보 / 원경기 | Vučević 후보 | Nnaji 후보 | 추가 분 배정 |
|---|---:|---:|---:|---:|---:|---|
| 5/9 MIN | 16:43 | 19:44 | 24:25 / 24:25 | 30:00 | 15:31 | Wagner 9:12, Nnaji 7:31 |
| 5/11 @MIL | 17:03 | 결장 | 30:38 / 27:35 | 36:00 | 16:00 | Wagner 3:03, Vučević 6:00, Nnaji 8:00 |
| 5/13 @ATL | 20:40 | 미배정 | 28:04 / 21:24 | 36:00 | 16:00 | Wagner 6:40, Vučević 6:00, Nnaji 8:00 |
| 5/14 @PHI | 7:24 | 19:07 | 16:30 / 16:30 | 30:00 | 15:24 | Nnaji 7:24 |
| 5/16 @PHI | 25:05 | 22:55 | 34:38 / 34:38 | 30:00 | 10:00 | Wagner 23:05, Nnaji 2:00 |

표의 Nnaji·Vučević는 **대체 세계** 분이다. 두 선수의 원역사 Orlando 출전과 비교한 값이 아니다. Vučević 36분·Nnaji 16분은 [기존 F4 화면](O15F14Q_ORLANDO_HALL_NO_RESIGN_F4_SCREEN.md)의 **선별용 모델 상한**이며 실제 의료/계약 한도가 아니다. 코드가 Bamba 출전 세 날짜에는 원경기 `actual_seconds`를 상한으로 쓰고, 미출전 두 날짜에는 K1의 Bamba 0분을 보존한다. Hall 제거분은 각 행의 추가 분과 초 단위로 일치한다. 다섯 경기 모두 240 팀분·역할 유효 5인 조합·선발 동시 3분 증인을 얻었고 **5경기 × RAPTOR/BPM 두 방법 = 10개 국소 비교**의 승자 방향 반전은 0이다. K1의 연전 피로 계수 0.5와 경기 시계 2,880초 분모를 그대로 쓰며, 새 의료 추정치는 더하지 않는다. 평점 결과는 경기 득점이나 실제 경기 결과의 재현이 아니다.

이 상한 화면은 처음 선별의 5/11·13 Wagner 36분과 5/16 Bamba 30분 부담을 낮춘다. 대신 5/11·13의 Vučević 연속 36분과 Nnaji 연속 16분, 5/13→14 연전, Wagner의 두 경기 원경기 초과분이 남는다. 원역사 노출량은 실제 출전의 증거일 뿐 대체 세계의 건강·감독 승인·효율을 확정하지 않는다. 5경기 이전/이후 일정, Orlando 전체 계약비·후속 등록, 정확 시즌/추첨까지 이어야 F4/A1/A3를 재판정할 수 있다. 2번 종료 조건을 채우면 시간 간격 없이 3번 작업을 시작한다.
