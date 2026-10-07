# 2018 Villanova–Texas Tech 공식 박스와 가상 11분 삽입

**범위:** NCAA East Regional Final 한 경기의 원자료와 가상 분 수지 증인. 원고·완성 대체세계 박스·실제 포제션 재구성은 아니다.

- 공식 기록: 2018-03-25 Villanova 71-59 Texas Tech, Villanova 200 player-minutes·양수 선수 8명·선발 5명·리바운드 51(선수 50+TEAM 1).
- 근거: [Villanova 공식 경기 박스](https://villanova.com/sports/mens-basketball/stats/2017-18/texas-tech/boxscore/2694), [Texas Tech 공식 경기책 PDF](https://texastech.com/documents/download/2018/3/25/Game37TexasTech_Villanova.pdf). 양쪽의 8명·분·득점·리바운드를 대조했다.

- 원자료는 저장소 밖 임시 캐시에 있다. 생성·검사 시 두 파일의 바이트 수와 SHA-256을 재확인하고, 공식 표에서 선수별 분·선발·득점·리바운드를 다시 추출한다. 경로·해시는 JSON `historical_official.source_documents`에 기록했다.

| 선수 | 공식 분 | 공식 선발 | 공식 득점 | 공식 리바운드 | 가상 분 차이 | 가상 작업 분 |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Jalen Brunson | 36 | 예 | 15 | 6 | -1 | 35 |
| Eric Paschall | 37 | 예 | 12 | 14 | +0 | 37 |
| Mikal Bridges | 30 | 예 | 12 | 5 | -3 | 27 |
| Omari Spellman | 26 | 예 | 11 | 6 | -3 | 23 |
| Phil Booth | 31 | 예 | 5 | 4 | -2 | 29 |
| Donte DiVincenzo | 26 | 아니오 | 12 | 8 | -2 | 24 |
| Dhamir Cosby-Roundtree | 12 | 아니오 | 4 | 7 | +0 | 12 |
| Collin Gillespie | 2 | 아니오 | 0 | 0 | +0 | 2 |
| FICTIONAL_PROTAGONIST | 0 | 아니오 | — | — | +11 | 11 |

- 실제 공식 양수 선수는 **8명**이고 가상 주인공을 넣은 작업본만 9명이다. 작업본 합계 200분, 기존 선발 5명 보존.
- Paschall 14리바운드·Cosby-Roundtree 7리바운드는 핵심 공로 보존 목표이며 두 선수의 분은 감축하지 않았다. 대체 사건·박스의 검증된 기록이라고 주장하지 않는다.
- 분 기증 선택은 Brunson 1, Bridges 3, Spellman 3, Booth 2, DiVincenzo 2분이다. 정확 교체 시점·5인조 시간표·PBP 연속성은 아직 검증하지 않았다.
- 공식 71–59는 역사 결과와 작품의 보존 목표다. 바뀐 분 아래 정확 득점·리바운드·승패를 기계적으로 재현했다는 뜻은 아니다.
- F03 Texas Tech 장면은 아직 실행하지 않았다. 앞 두 훈련 기능이 토너먼트에서 자동 성공을 보장하지 않으며 실제 상대·동료의 내면이나 실존 발언을 만들지 않는다.
- 40경기 전수·대표 기능3 상한 확대·새 대표 경기·원고는 없다. 전체 G13/G14·Pack 미완료, 설계/원고 게이트 `CLOSED`.
