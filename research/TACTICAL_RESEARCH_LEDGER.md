# Tactical Research Ledger v0.1

- 기준일: 2026-08-27
- 상태 표기: `VERIFIED / PARTIAL / RESEARCH_HOLD / SIMULATED_FUTURE`
- 사실은 출처·적용일·대상 리그가 확인되어야 설계 정본으로 승격

## 원장 필드

| 필드 | 내용 |
|---|---|
| era/date | 적용 시즌과 날짜 |
| rules baseline | 샷클록·3점선·파울 등 공식 규칙 |
| dominant pressure | 당시 로스터와 공격/수비가 만드는 압력 |
| protagonist role | 주인공에게 요구되는 기능 |
| rival role | 라이벌에게 요구되는 기능 |
| counter | 상대의 대응과 재대응 |
| cost | 부상·파울·턴오버·출전·계약 비용 |
| evidence | 공식/1차 출처 |
| confidence/status | 확신도와 정본 승격 상태 |

## 확인된 규칙 기준선

| ID | 시즌/일자 | 사실 | 설계 영향 | 출처 | 상태 |
|---|---|---|---|---|---|
| T-001 | NCAA 2015-16부터 D-I | 남자 농구 공격 제한 시간이 35초에서 30초로 단축 | 2017-18 대학 구간은 이미 30초 기준 | [NCAA](https://www.ncaa.org/news/2015/6/8/shorter-shot-clock-other-changes-coming-to-college-hoops.aspx) | `VERIFIED` |
| T-002 | NCAA 2018-19 | 당시 남자 대학 3점선은 20피트 9인치 | 주인공 대학 시즌과 NBA 거리 전환을 분리 | [NCAA](https://www.ncaa.org/news/2018/5/23/committee-seeks-feedback-on-experimental-men-s-basketball-rules.aspx) | `VERIFIED` |
| T-003 | NCAA 2019-20부터 D-I | 남자 대학 3점선이 국제 거리 22피트 1과 3/4인치로 확대 | 라이벌 대학 시즌의 공간·슈팅 평가 변화 | [NCAA](https://www.ncaa.org/about/resources/media-center/news/men-s-basketball-3-point-line-extended-international-distance) | `VERIFIED` |
| T-004 | NBA 2018-19 | 공격 리바운드 등 특정 상황에서 샷클록을 14초로 리셋 | 주인공의 리바운드 직후 판단 속도가 루키 시즌부터 중요 | [NBA](https://www.nba.com/news/nba-board-governors-approves-rule-changes) | `VERIFIED` |
| T-005 | FIBA 기준 | FIBA는 NBA보다 먼저 특정 공격 리바운드 상황에 14초 리셋을 적용 | 국대 경험과 NBA 적응의 규칙 연결 가능 | [FIBA](https://www.fiba.basketball/en/news/nba-implements-fibas-14-second-shot-clock-rule) | `VERIFIED` |
| T-006 | NBA 2021-22 해석 | 비농구적 슈팅 동작에 대한 파울 판정 해석 강화 | 라이벌의 파울 유도형 득점이 자동 성장하지 않음 | [NBA Video Rulebook](https://videorulebook.nba.com/rule/non-basketball-moves/) | `PARTIAL` |
| T-007 | NBA 2022-23 | 전환 공격을 끊는 take foul에 강화된 벌칙 | 주인공의 리바운드→전환과 선행 패스 가치 상승 | [NBA](https://www.nba.com/news/nba-board-of-governors-approves-heightened-penalty-for-transition-take-foul) | `VERIFIED` |

## 다음 조사 큐

1. 2012-17 한국 고교농구의 수비 규정·대회 일정·대표 전술을 KBA/대회 기록으로 확인
2. 2016-18 미국 프렙/AAU의 학사·경기 규칙과 쇼케이스 구조 확인
3. 2017-18 NCAA 실제 팀별 전술은 선택 대학 후보가 나온 뒤 좁혀 조사
4. 2018-26 NBA 전술은 리그 전체 경향과 특정 팀 철학을 분리해 공식 트래킹·라인업 자료로 검증
5. 플레이오프 전술은 실제 시리즈를 그대로 복제하지 않고 문제-카운터 기능만 추출
