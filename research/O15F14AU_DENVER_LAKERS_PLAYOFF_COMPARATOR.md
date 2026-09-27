# O-15F14-AU — Denver–Lakers 2021 조건부 1라운드의 관측 범위

- 판정: `HISTORICAL_MATCHUP_AND_OPENERS_OBSERVED / K1_L2_SERIES_HEALTH_MINUTES_SCORE_HOLD`.
- 경로: [K1/F038+L2 대진](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)의 **조건부** Denver 3번–Lakers 6번 첫 라운드. 작가가 확정한 사건은 McGee–Hartenstein 거래 생략과 Gordon A의 Nnaji Orlando 이동·Bey Denver 잔류다. 대진·건강·시리즈 결과는 작가확정이 아니다.
- 출처 등급: 아래 세 경기의 NBA **공식 최종 경기책 첫 장**을 직접 확인했다. 원역사 사실과 대체 세계 가정을 분리한다.

## 원역사 세 시점 비교

| NBA 경기책 | Denver 관측 | Lakers 관측 | 허용되는 용도 |
|---|---|---|---|
| [5/3 DEN @ LAL 정규시즌](https://statsdmz.nba.com/pdfs/20210503/20210503_DENLAL_book.pdf) | 89–93 패. McGee **12:24=744초**, Nnaji `Inactive / Left Ankle Sprain`; Murray `Inactive / Left ACL Surgery`, Barton·Monte Morris도 `Inactive / Right Hamstring Strain` | James `Inactive / Right Ankle Sprain`, Schröder `Inactive / Health and Safety Protocols`; Davis **33:06** | 실제 맞대결의 점수·명단·분 비교. 플레이오프 승패 기준선 아님 |
| [5/22 POR @ DEN 원역사 1라운드 1차전](https://statsdmz.nba.com/pdfs/20210522/20210522_PORDEN_book.pdf) | McGee·Nnaji 모두 **DNP / Coach's decision**. Murray ACL 수술, Barton 햄스트링, Dozier 오른쪽 내전근 문제로 `Inactive`; Morris **21:59** 출전 | 상대가 Portland이므로 Lakers 명단/전술 관측 없음 | Denver의 원역사 플레이오프 개막 가용성 **비교**. 새 Lakers 상대 기용 결정 아님 |
| [5/23 LAL @ PHX 원역사 1라운드 1차전](https://statsdmz.nba.com/pdfs/20210523/20210523_LALPHX_book.pdf) | 상대가 Phoenix이므로 Denver 명단/전술 관측 없음 | James **36:04**, Davis **38:48**, Schröder **34:08**, Drummond **19:05**, Horton-Tucker **7:05** 출전; Gasol **DNP / 감독 선택** | Lakers의 원역사 플레이오프 개막 가용성 **비교**. 새 Denver 상대 분/득점 아님 |

**사실:** 5/3 맞대결에서 빠진 James·Schröder는 원역사 5/23 플레이오프 개막 경기에 출전했다. 5/3의 Lakers 93–89 승리와 [F5 정규시즌 국소 치환](O15F14Q_DENVER_MCGEE_NONTRADE_F5_SCREEN.md)의 McGee `744초`→Hartenstein `744초`는 같은 날·같은 원역사 결장을 전제로 한 계산이다. 후자의 조건부 홈 점수차는 RAPTOR `+4.40518408`, BPM `+4.09807281`로 두 방법 모두 Lakers 방향이다. 이 값은 **단일 정규시즌 경기의 국소 민감도**이며, James·Schröder가 출전하는 플레이오프 상대 전력이나 4~7경기 결과를 검증하지 않는다.

**선택 경로의 명단 차이:** 작가가 선택한 거래/이동에 따르면 대체 Denver에는 McGee·Nnaji가 없고 Hartenstein·Bey가 남는다. 5/22 원역사 McGee·Nnaji의 DNP는 새 상대·새 명단에서 Hartenstein·Bey DNP의 근거가 아니다. 원역사 Cleveland의 Hartenstein 뇌진탕/결장도 [별도 인과 검문](O15F14AP_DENVER_HARTENSTEIN_HEALTH_CAUSALITY.md)에 따라 Denver 의료 장부로 복사하지 않는다.

[후속 AV 판독 교정](O15F14AV_DEN_LAL_OPENING_MINUTE_TEMPLATES.md)은 위 5/23 `7:05`가 Horton-Tucker의 분이며 Gasol은 감독 선택 DNP임을 PDF 첫 장에서 확인했다. 두 팀의 **서로 다른 원역사 개막 경기** 240분씩을 명시적 후보 입력으로만 연결했고, 대체 세계의 5대5 시간축·승패는 만들지 않았다.

[2월 동일 상대 맞대결 검문](O15F14AW_DEN_LAL_HARTENSTEIN_HEAD_TO_HEAD_PRECEDENT.md)은 Hartenstein의 원역사 Denver 선수 시절 Lakers 상대 `10:11`·`3:04` 출전 선례를 확인했다. 그러나 그 두 박스에는 대체 Draft에서 Dallas로 간 Hampton의 Denver 분도 들어 있다. 2/14 Davis의 선행 건병증과 경기 중 재악화 역시 A1의 별도 인과 사건이다. 원역사 두 승패를 5월 조건부 시리즈로 상속하지 않는다.

**추론/후보:** 새 시리즈의 첫 경기 날짜, 양 팀의 실제 가용 선수, 선발과 교대, 경기별 240분·5인조, 슛/포제션, 승자와 시리즈 길이는 전부 `UNKNOWN`이다. 원역사 5/22 Denver와 5/23 Lakers의 가용성은 **초기 비교 후보**로만 사용할 수 있다. 별도 인과 근거 없이 이를 대체 세계 1차전 건강·기용으로 확정하지 않는다. 원역사 Denver–Portland 6경기·Denver–Phoenix 4경기의 출전 시계도 [대진 보정](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)의 실제 DEN–LAL 분 원장에 이월하지 않는다.

**다음 정확 검문:** (1) 2021년 5월 대체 Denver/Lakers 각 선수의 등록·건강·가용성 달력을 구성하고, (2) McGee/Nnaji 이탈·Hartenstein/Bey 잔류를 Denver 경기별 5인조와 팀 240분에 반영하고, (3) Lakers의 James/Davis/Schröder 및 센터군을 상대 전력으로 반영해 시리즈 4~7경기 승패를 **후보별**로 검산하고, (4) Phoenix–Portland 승자와 2라운드 상대·일정·후속 계약 영향을 연결한다. 날짜·점수·건강을 임의로 확정하지 않는다. Cleveland Varejão C1/C2, F1~F4와 A1/A3도 별도 열린 입력이다.

**도구 분리:** Antigravity CLI는 5/3 NBA 박스 본문 수집 요청이 45초 print timeout·`response=""`여서 Evidence Pack **0건**. NotebookLM CLI는 공식 5/3 경기책 한 파일을 비정본 작업실 출처 `70328aad-7ab8-4858-beca-7f27216d317d`로 추가하고 그 출처만 질의했다. 점수·McGee 분·양 팀 inactive·Davis 분을 원문과 일치하게 반환했다. Codex는 5/3·5/22·5/23 공식 경기책을 직접 대조하고 저장소 F5 JSON의 744초·점수차를 확인했다. NotebookLM은 **같은 5/3 원문** 분석이므로 독립 원자료 증가로 세지 않는다. Claude/source-blind 처분은 [별도 검토 기록](../reviews/R01_O15F14AU_DEN_LAL_BASELINE_REBUTTAL.md)에 둔다.

**게이트:** F5·A1/A3·K_METHOD_EVENTS `HOLD`; F1~F5 `0/5`, A1~A3 `0/3`, 네 K `0/4`. 7개 매크로 1완료·1진행·5대기, 미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 금지.
