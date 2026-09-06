# NBA Landing Scope Gate

```yaml
status: CHICAGO_LANDING_REOPENED
team: Chicago Bulls
draft_year: 2018
pick: HOLD_22_LEAN
contract: first-round NBA rookie-scale
deep_real_person_relationships_max: 3
rookie_representative_games_max: 2
primary_tactical_problems_max: 2
self_management_relapse_max: 1
manuscript_allowed: false
```

## v0.27 현행 범위

- Chicago 원클럽 프랜차이즈 팀 방향
- 주인공 동부·라이벌 서부 분리 방향
- 2018 NBA Draft 전체 22순위 최우선 후보, 정확 순번 HOLD
- 투웨이가 아닌 1라운드 NBA rookie-scale 계약
- 2018-19 NBA 본무대·Windy City 짧은 assignment 가능 구조
- 깊은 관계 최대 3명, 정확 인물 HOLD
- 핵심 전술 문제 2개: 비슈터 공간 복구, 약한 쪽 수비·전환 연결
- 자기관리 재발 1개: 아침 영상·컨디셔닝 지각으로 NBA 기회 상실
- G League가 징계가 아니라 후속 개발 배정이라는 권한 분리

## v0.28 드래프트 연쇄 상태

- Golden State 28 Hutchison: `TEAM_BOARD_PASS / DRAFT_NIGHT_PRIMARY_CANDIDATE / NOT_LOCKED`
- Portland 24: `SIMONS_KEEP_LEAN / HUTCHISON_CONTINGENCY_ONLY`
- Evans: Portland 37 `PRIMARY_LEAN`, Detroit 42·Orlando 43 대안
- Trent: Lakers 39 `PRIMARY_LEAN / PICK_TRADE_STRUCTURE_PASS`, Detroit 42 대안, Lakers 47 하한선
- Bonga 44 Washington `PRIMARY_LEAN`; Sanon 미지명/Olimpija `PRIMARY_LEAN`; San Antonio 49 LOW·Charlotte 55 대안; draft-board boundary `PASS`
- 2019 AD 거래: `CAP_MECHANICS_RESTORE_PASS / TRENT_WASHINGTON_CASCADE`; 2021 Powell 거래: `ORIGINAL_BLOCKED`

## v0.30 루키 donor·배정 상태

- 실제 Hutchison 894.6분 직접 슬롯과 시즌 종료 부상 뒤 33경기 donor를 분리한다.
- Chicago 루키 역할선: `73경기·11선발·1,274:02·17.45분 / PROVISIONAL_LOCK`
- 자기관리 후보: 2018-12-05 지각→12-07 약 10~12분 NBA 기회 상실. 벌금·정확 시각 HOLD
- Windy City 후보: 2019-01-07~13 standard-contract assignment, 01-11~12 홈 2경기·24~28분. 징계·투웨이 금지
- 같은 날짜 receiver 원장 PASS. 개인 박스·승수·대표 경기는 HOLD

## v0.29 거래 구조 감사 상태

- Hutchison 없는 2021 Chicago–Washington–Boston 최소 6인 거래: `CONDITIONAL_STRUCTURE_PASS / EVENT_HOLD`
- Washington Trent: `DEADLINE_KEEP_PRIMARY / RFA_PATH_PASS / EXACT_CONTRACT_HOLD`
- Portland Powell: `PORTLAND_NO_TRADE_PRIMARY / POWELL_DESTINATION_HOLD`
- 연도별 순서: 실제 사건 전수 대조, 변화 지점 심층 계산, 시즌 시간순 최종 확정
- O-15C3: 실제 2019 lottery 7순위·Coby White 지명 `AUTHOR_APPROVED / LOCKED`
- O-15C4: 실제 65경기·15,675:11·325선발 기준선과 2년차 BASE 1,395분 `PRECALC_RANGE_PASS`
- O-15C5: 65경기·18선발·1,395분과 경기별 15,675:11 보존 `PLAYER_GAME_CONSERVATION_PASS / PROVISIONAL_LOCK`
- 다음 실행: O-15C6 2년차 생산성 prior·경기 영향·2020 standings/lottery

## 닫기 조건

다음을 모두 통과할 때 첫 NBA 착지 범위를 다시 닫는다.

1. Villanova 저사용 선수가 22순위 후보가 되는 워크아웃·측정·팀 보드 근거.
2. Hutchison 이동과 2018 Draft 22~60 재판정. Lakers 내부 보드·Bonga/Sanon 팀보드·2019 AD·2021 Powell 거래까지 포함한다.
3. Chicago 2018-19 player-game donor·정확 루키 분·Windy City 배정.
4. Hoiberg→Boylen 체제의 역할과 자기관리 기회 상실 날짜.
5. 깊은 관계 세 명과 LaVine 공존 기능.

그 전에는 정확한 개인 기록·대표 경기·승패·2019 로터리를 정본화하지 않는다. v0.15 Atlanta 완료 범위는 삭제하지 않고 폐기 분기 증거로 보존한다.
