# D1 공개 입력·자산 범위 후속 검수

2026-10-05 / 기준 main `b089d5f` (PR418). 추가 법적 PASS0. 이번에는 확인한 입력과 종료되지 않은 범위를 구분한다.

## Chicago: 원역사 room episode와 유한 공개 사건 구간

[입력 원장](../research/CHICAGO_2019_ROOM_RETROSPECTIVE_FLOW_2026_10_05.json). [NBC Rob Schaefer의 Yahoo 재게시 분석](https://sports.yahoo.com/bulls-realistically-improve-roster-during-191754446.html)을 직접 HTTP200으로 읽었다. 역사2019 cap-below와 Kornet RoomMLE 사용의 사후 설명이다. 본문 지문을 실제 캐시와 대조했다. 과거의 계획 보도보다 적용 경로를 보강하지만 정확 July7 charge/최초 episode 날짜를 인증하지 않는다. 13명 전망 부분합은 전체 상한으로 사용하지 않는다.

NBA 공식 전체 movement feed에서2019-07-08~2021-03-24의 Chicago 관여21행을 별도로 추출했다. Signing12/Waive9/Trade0이며 Vonleh 중복 후보2행을 삭제하지 않는다. 2019 방출6계약과2020 방출3계약이 carry 검문의 추가 cohort다. feed의 누락된 캠프 서명은 구단 가이드와 합집합으로 확인해야 한다. 이 유한 공개 구간 검문은 미공표 사건의 절대 부재를 새 필수요건으로 요구하지 않는다. 방출은 잔급0의 증거가 아니다.

공식2017 CBA VII6(g)(1)의 RoomMLE는 같은 cap year의 해당 조건을 충족한 선행 cap-below episode에 연결할 수 있다. 그 episode에서 BAE/Non-Tax MLE/Tax MLE에 not entitled이며 제안시 그 세 예외를 같은 해 이미 쓰지 않았다는 조건을 함께 기록했다. Kornet 서명일에서 최초 episode 날짜를 역산하지 않는다. VIII1(c)의 Year2/Year3 독립80~120% 경계도 직접 다시 확인했다. 명시적인 비율 연결은 Year3→Year4다. 같은 pick은 유지하되 Year2/Year3를 같은 비율로 강제해 세금 경계를 줄이지 않는다. 전체 R·carry Δ 상단은null이다.

## Denver: 보장액 공개점과 조건부 배분 두 경로

[보너스 조사 원장](../research/DEN_GORDON_CLARK_BONUS_SCREEN_2026_10_05.json)을 확장했다. [SalarySwish Gordon 2018 계약 이력](https://www.salaryswish.com/players/aaron-gordon)의 마지막 두 해 Base=Guaranteed를 직접 읽었다. 계약 전체95%와 기본급100%를 구분하고 후대3% kicker를 복사하지 않았다. 공개 Guaranteed 열은 lack-of-skill을 별도 명명하지 않으므로 법률 배분 연결의 조건을 명시했다.

보호100/100을 VII3(b)에 적용하고 earned 하한0을 유지하는 경로는 Gordon 현재연도 half + Clark넓은615k =3,205,909.125(센트 올림3,205,909.13)다. 기본급 절감2,579,436보다 넓으며 현재비용 종료 증인이 아니다.

[NBA Schuhmann 일정 분석](https://www.nba.com/news/how-rest-road-trips-and-other-factors-played-out-in-2021-22-schedule)의 실제146일 표와 [공식 시즌 FAQ](https://www.nba.com/news/nba-2020-21-season-faq)의 시작/종료일을 읽었다. 거래일을 잔여에 포함하면53일이다. trade remainingBase에도 같은 earned 일할 규칙이 적용된다는 연결을 별도로 검증하면 조건부 총상한2,339,462.97이 나오지만, UPC16(e)는 종료 보상 조항이므로 이 연결을 직접 인증하지 않았다. 지급일·earned·달력일수를 혼동하지 않는다. 두 Gamma와 DeltaOther 검증 상단은null이다. 조건부 숫자가 절감폭 안에 들어간다는 사실은 비용 PASS가 아니다.

## Boston: 자산 정체성과 전체 우선권을 구분

[픽 증인 JSON](../research/BOS_FOURNIER_2025_2027_ASSET_EQUIVALENCE_2026_10_05.json) / [설명](../research/BOS_FOURNIER_2025_2027_ASSET_EQUIVALENCE_2026_10_05.md). 기존 원문 회수 기록으로 Bane의 MEM2025 자체2R→BOS, Fournier의2025 뒤순번 및BOS2027 자산 정체성을 연결했다. 이번 새 원문 수집으로 중복 계수하지 않는다. 서로 다른 최종31~60 순번870쌍에서 뒤순번 규칙을 대조했다. 승수 동률의 추첨·실제 미래순번은null이다. June Kemba 앞순번 후속 후보를 March25 의무에 소급하지 않는다.

초기 감사의 한정 종료 가능은 **자산 정체성·선택함수**였다. 실제 S2의 두 branch는 전체 dated ownership/priority를 요구하므로 아직 완료가 아니다. 이를 실제 파일 준비 과정에서 정정하여 SUPPORTING_ONLY로 기록했다. 비공개 원계약 원본 자체를 새 필수조건으로 만들지 않으며 공개 선행 의무 연결이나 관련 법적 입력 동일성 증인으로 닫을 수 있다. TPE·전체 Boston 비용은HOLD다.

## 실제 검문과 역할

- Codex 자료수집: Chicago 원분석·공식flow 필터, Gordon 원계약 이력·CBA·공식달력 실제 접근. raw HTML 성공/HTTP403·색인·재게시 성격 구분.
- 독립 Codex: chi_salary_domain은 Denver/Boston, nba_legal_next는 Chicago/Boston 실제 파일을 교차검문해 한정 수용했다. 원수집자가 본인 수집을 다시 독립 검수로 세지 않는다. 발견한 CBA 보호 범주 위치 II3(e)→II3(g)를 원 PDF40과 대조해 수리했고 RoomMLE 세 예외 조건 누락도 원 PDF231 대조 후 보강했다. Gamma 조건부 숫자·53/146·픽870쌍·입력7지문이 일치했다. S2 재실행은 등록2 PASS/10 HOLD·F/A/K0이며 비교 출력 --check와 모든 S2 근거 경로가 일치했다.
- Antigravity/NotebookLM/Claude: 이번 입력 신규 실행 NOT_RUN. 직전 실행이나 단일 파생 분석을 이번 원본문 분석으로 재계수하지 않는다.
- 전체 source-blind/G16: 미완료.

기존 승인 방향만 재사용한다. 사실/공개 보도와 법률 추론·조건부 후보·작가확정을 구분하며 신규 작가선택0·원고0이다. freeze/gate 본문과 A01 원본은 이번에 변경하지 않는다.

| 큰묶음 | 현재 |
|---|---|
| 1 2020 드래프트 연쇄 | 완료 유지 |
| 2 Chicago2020–21 | 법적2완료/10HOLD·F0/5 A0/3 K0/4, 이번 추가 종료0 |
| 3 2021–23 거래·계약 | 승인M1/G1A 유지, 정확 실행 미완료 |
| 4 장기 커리어 | 17시즌 골격, 실행/주요 결과 미완료 |
| 5 결말·전체 구조 | 14막42소막780슬롯·A01국소Blueprint3, 최종 회차 기능0 |
| 6 집필 규격·Context Pack | 표본 기반 문체 규격 완료, 실제Pack0·전체 미완료 |
| 7 통합·독립·작가 승인 | 전체 미완료 |

미완료 큰묶음6. 다음은 Chicago2019 캠프 계약 분류/이월범위, Gordon skill 보호·trade-earned 연결 및 기타 비용 차액, Boston 선행 자산 의무와 당일TPE다. 설계/원고 CLOSED, freeze v0.30 PARTIAL을 유지한다.
