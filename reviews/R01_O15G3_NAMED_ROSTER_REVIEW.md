# O-15G3 자체 검토 — 이름을 넣은 2021 조건부 명단

상태 `SELF_REVIEW / NOT_INDEPENDENT`. 세계관 완성·독립 검수·작가 승인 완료가 아니다.

## 변경과 결론

G1A의 다섯 빈자리를 Moody/Edwards/Bradley/Stanley/Valentine 후보로 교체했다. 10·39순위와 백업C는 각각 네 대안을 제공한다. 앞선 지명 보드와 계약 합의는 null/false이며 원래 G1·추첨 산출은 변경하지 않았다.

15일반계약 자리, 주인공 급여/Young 보너스 포함 네 센터240예산 조건, 드래프트 가용성32조건을 작성했다. 기본 추천 총액은 G1A보다 $856,688 낮다. 2022의 세 유지 조건을 모두 택할 때 예산 차이는 −$206,244다.

Valentine의 실제 보고 FA 금액을 유지하는 경우 Caruso NTMLE 분류의 추가 실제 금액 필요가30조건 모두0이 된다. 정상 cap·현금·apron 장부를 동일시하거나 실제 실행을 인증하지 않는다.

## 발견하고 보존한 반례

1. Dieng $4m는 Caruso 뒤 NTMLE 잔액과 단독 BAE보다 크며 예외 합산 금지다. 별도 cap 공간 경로는 불가능 판정하지 않았다.
2. 지명 독점권을 유지한 Draft Rookie와 Rookie Free Agent는 다르다. 0년차 FA 세금/apron 하한의 $743,920 추가는 반례에만 두고 새39순위 기본안에 합산하지 않았다.
3. Stanley의 실제 캠프 방출을 시즌 잔류로 복사하지 않았고, Valentine의 부분 보장/방출액을 연간 기본급으로 쓰지 않았다.
4. Sengun을 골랐을 때 Moody의 SF분을 자동 복사하지 않는다. 원래240분 표 치환은 능력·건강 검증이 아니다.
5. 실제 2021 지명 순번을 새 세계 가용성으로 간주하지 않는다. 후보 전원이 이미 지명됐으면 null이다.

## 검증 범위

`PYTHONPATH=tools python -m unittest tools/test_chicago_2021_named_roster.py -v`의5개 검사: 선행 지명 제외, 빈자리 교체/중복 거부, 예외 부족 반례, 15자리/240분/미확정 경계, FA 금액과 Draft Rookie 분류. JSON 재생성 및 diff 공백 검사도 수행한다. 원격 CI는 게시 때 별도로 확인하며 이 로컬 결과로 대신하지 않는다.

`author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`, `v0.30 PARTIAL`, 설계·원고 CLOSED. 신규 원고·정본 승격0. 진행 중 포함 남은 큰 작업6개.
