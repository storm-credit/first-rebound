# Chicago 2019 Simon 계약의 이월 범위

기준 main: `92d3db48d2ff8f4b4459dbb02554e061c2f261a1` (PR #419).
분류: **공개 원보도에 연결한 S2 국소 법적 추론**. Chicago 전체 R·이월 비용의 종료 증인이 아니다.

## 사실

- [Adam Zagoria의 2019-09-12 원보도](https://www.zagsblog.com/2019/09/12/chicago-bulls-to-sign-former-st-johns-guard-justin-simon/)는 리그 취재원에 근거해 Justin Simon의 Exhibit10 계약을 명시한다. 동일 본문의 September13 업데이트는 실제 서명을 확인한다. 계약서·리그 접수증과 구분한다.
- NBA 공개 movement의 `Waive 1021066`은 Chicago가 Simon을 2019-10-19 방출한 사건이다. [기존 21행 자료](CHICAGO_2019_ROOM_RETROSPECTIVE_FLOW_2026_10_05.json)의 원행을 대조한다.
- [Windy City 공식 November7 명단](https://windycity.gleague.nba.com/news/windy-city-bulls-announce-2019-20-opening-night-roster-for-teams-fourth-season)은 Simon·Callandret·Doyle·Shittu를 Affiliate Player로 분류한다. 이는 G League 명단 사실이며 NBA 계약 유형을 증명하지 않는다.
- [2017 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf) II§3(q), PDF42–44/인쇄20–22: Exhibit10은 1시즌·최소급여 계약이며, 해당 보너스 외 보너스를 허용하지 않는다. §3(g) 보호는 Two-Way 전환 경우 외에는 허용하지 않는다. Exhibit9를 함께 갖는 것은 가능하나 Simon의 실제 Exhibit9 보유를 추정하지 않는다.
- VII§7(d)(6)(A), PDF249–250/인쇄227–228: September1 이후 요청된 방출은 당해 시즌 Salary를 그대로 두고, 이후 계약 시즌분만 별도로 stretch한다. 프리시즌 요청에서도 당해/upcoming 시즌은 future-year stretch 대상에서 제외한다.
- VII§4(k), PDF217/인쇄195: Exhibit10 Bonus 자체는 Team Salary에서 제외된다.

## 추론: 어느 항목이 좁혀지는가

당시 보도된 Exhibit10 분류와 기존 October19 방출 경로를 유지하는 계약에 한정한다. 2017 조항의 적용을 전제로 한 공개 법률 추론이며, 2020 개정 전체를 인증했다는 뜻이 아니다. 이 계약은 2019–20 한 시즌이므로 **이 계약 자체의 2020–21 ordinary base = 0**이다. 당해 시즌분을 미래로 stretch하는 경로도 위 조항으로 제외된다. 실제 Exhibit10 Bonus는 지급 여부·액수와 별도로 Team Salary 제외 항목이다.

따라서 이 세 항목에 한정한 `[0, 0]`이 가능하다. 방출 사실만 보고 잔급 전체를 0으로 놓은 계산이 아니다. 2019–20 당해 부상 보상, 중재·후행 조정, 별도 신계약, Chicago 전체 기타 비용을 0으로 인증하지 않는다. 이들은 각자의 유한 공개 범위·적용 조항에서 검문해야 하며, 미공표 비용의 절대 부재 증명이나 비공개 원계약을 새로운 필수조건으로 추가하지 않는다.

## 남은 범위

2019 방출 6명 중 이 신규 자료로 계약 유형을 좁힌 사람은 Simon 1명이다. 나머지 Blakeney·Callandret·Deng·Doyle·Shittu의 계약 유형·기간·해당 carry는 이 자료만으로 닫히지 않는다. 다른 파일에서 확인한 항목을 다시 미확인으로 되돌리지 않으며, 이 자료의 신규 증명 범위를 뜻한다. 2020 방출 3명과 초기/예외 산입 등은 [기존 공개 흐름](CHICAGO_2019_ROOM_RETROSPECTIVE_FLOW_2026_10_05.json) 및 [S2 원장](../control/CHICAGO_2020_21_D1_S2_REGISTER.json)에서 이어 검문한다.

## 후보·작가확정·게이트

- 새 작가 선택 0. 승인 방향·정본 계약 경로 보존.
- 전체 R 상한은 null. `CHI_TEAM_SALARY`는 HOLD.
- 법적 2완료/10HOLD, F0/5·A0/3·K0/4, 시즌 실행 미확정.
- freeze v0.30 PARTIAL, 설계/원고 CLOSED, 원고 0.
- 원자료·페이지 지문과 정확 범위는 [JSON](CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json)에 보존한다.
