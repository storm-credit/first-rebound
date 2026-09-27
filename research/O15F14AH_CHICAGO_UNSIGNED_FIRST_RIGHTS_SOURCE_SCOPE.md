# O-15F14-AH — Chicago 미서명 1라운드 권리와 거래 연혁의 누락 범위

- 기준 `main` `e50a41b`, 조회일 2026-09-28, 적용일 2021-03-25.
- 판정 `NAMED_2006_2020_RIGHTS_SCREEN / COMPLETE_RIGHTS_INVENTORY_HOLD`.
- 구분: NBA·구단의 실제 지명/계약·거래는 **FACT**; 선택 세계에서 원역사 선행 사건 유지와 추가 보류액 0은 **CONDITIONAL / NOT PROVEN**; 새 작가확정은 없다.

## 1. 먼저 적용 규칙

[2017 NBA–NBPA CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) Article VII §4(e)(1), 인쇄 186쪽은 팀이 보유한 **미서명 1라운드** 권리를 해당 신인 급여표의 120%로 Team Salary에 넣는다. 선수 계약 서명·권리 상실/양도 때까지 이어지되, §4(e)(2)는 비NBA 구단 계약의 정규시즌 중 제외와 다음 7월 1일 재진입을, §4(e)(3)은 팀·선수의 서면 신고에 따른 해당 cap year 제외를 각각 규정한다. 따라서 “해외 스태시 권리 보유”와 “3월 25일 양의 cap hold”는 같은 말이 아니다. 반대로 이름이 표에 없다는 이유만으로 권리나 hold가 0이라고 볼 수도 없다.

## 2. 구단 공식 가이드에서 확인한 일부 1라운드 권리 줄

[Chicago 공식 2022–23 미디어 가이드](https://chibullsdigital.com/mediaGuide/2022_ChicagoBulls_MG_NBA_HI.pdf)의 **PDF 361쪽 / 인쇄 359쪽** `DRAFT HISTORY / 2006–2022`, **PDF 394–401쪽 / 인쇄 392–399쪽** 거래 연혁을 대조했다. PDF를 직접 다운로드해 텍스트 추출했고 2019·2020쪽은 렌더링으로 누락·날짜 줄을 확인했다.

| 구간 | 원역사 지명·취득/송출 중 주목할 1R 권리 | 2021-03-25 비용 해석 |
|---|---|---|
| 2006–10 | 2006 드래프트 직후 **미서명 지명권** #4 Tyrus Thomas·#13 Thabo Sefolosha를 취득했고 이후 두 선수는 NBA 계약·출전 경로에 들어갔다. 2010 #17 Kevin Seraphin 권리는 Washington으로 양도 | 이 세 이름은 2021-03-25 Chicago의 **미서명** 권리로 재계상할 수 없다. 이는 해당 기간 전체 권리 전수가 아니라 특정 취득·양도 사건의 확인이다. |
| 2011–16 | 2011 #23 Nikola Mirotić 취득 후 [2014-07-18 Chicago 계약 공지](https://www.nba.com/bulls/news/bulls-sign-forward-nikola-mirotic); 2014 #11 Doug McDermott 취득 후 가이드의 2014-07-21 계약; #16 Nurkić·#19 Harris는 Denver에 양도. 2012 Teague, 2013 Snell, 2015 Portis, 2016 Valentine은 NBA 계약·출전 경로 | 이 확인된 지명/취득 줄의 과거 미서명 1R hold는 2021 거래일에 새로 더하지 않는다. |
| 2017–20 | 2017 #7 Markkanen 취득 후 [2017-07-05 Chicago 계약](https://www.nba.com/bulls/news/bulls-sign-lauri-markkanen), 2018 #7 Carter·#22 Hutchison, 2019 #7 White, 2020 #4 Williams는 원역사 계약·출전. 2020 #44 Simonović는 **2라운드** | 선택 세계의 2018 #22 주인공 정확 순번은 HOLD이나 그는 1R 표준계약·2020–21 실제 출전 경로다. 2020 #4 LaMelo의 승인된 급여 슬롯도 [기존 상한](../simulation/CHICAGO_2020_21_TAX_BOUND.md)에 반영했다. 과거 두 사람의 unsigned hold를 같은 급여에 중복 추가하지 않는다. |

위 표는 **지명/취득한 현대 이름들의 양수 중복을 막는 화면**이다. Chicago가 모든 시기의 1라운드 권리를 빠짐없이 보유/포기했다는 거래일 원장은 아니다. 오래된 권리, PDF의 누락 사건, §4(e)(2) 해외 계약 만료·§4(e)(3) 서면 선택, 선택 세계 선행 거래 변형은 따로 확인해야 한다. 따라서 `UNSIGNED_FIRSTS` 전체와 R은 `null`이다.

## 3. 공식 가이드만으로 0건을 선언할 수 없는 반례

가이드의 **PDF 399쪽 / 인쇄 397쪽** 2019-01-22 행은 Carmelo Anthony·현금 수취와 Tadija Dragićević 권리 송출을 기록하지만, 같은 거래에서 받은 **Jon Diebler 권리**를 적지 않았다. [Chicago 당시 공식 거래 공지](https://www.nba.com/bulls/news/bulls-complete-trade-rockets-0)는 Diebler 권리 수취를 명시하고, [NBA 거래 추적](https://www.nba.com/2018-19-trade-tracker)은 그가 2011년 **51순위, 2라운드**였음을 표시한다. Diebler에게 §4(e)의 1라운드 120% hold를 적용할 수는 없다. 다만 이 누락은 가이드의 `ALL-TIME TRANSACTIONS`가 **권리 종류까지 완전한 팀 cap/asset ledger는 아님**을 실제로 보여준다.

따라서 [AF 거래 직전 TPE 화면](O15F14AF_CHICAGO_PREDEADLINE_EXCEPTION_ORIGIN.md)의 2020년 `Traded` 행 0건은 가이드에서 찾은 범위로만 읽어야 한다. 실제 선수 계약 송출이 있었는지는 [NBA 2019–20 거래 추적](https://www.nba.com/2019-20-trade-tracker), [NBA 2020 오프시즌 이동표](https://www.nba.com/news/nba-player-movement-2020-offseason)와 추가 교차 확인한다. Diebler 사례 자체는 2라운드 권리 거래로서 새 Chicago TPE나 미서명 1라운드 비용을 만들지 않는다.

## 남는 입력과 게이트

필요한 것은 2021-03-25 시점 **보유 1R 권리의 전수 목록** 또는 그와 동등한 선행 취득/양도·서명/권리소멸·비NBA계약/서면선택 증인이다. 현 공식 가이드와 NBA 이동표만으로는 전체 부재를 인증하지 않는다. `UNSIGNED_FIRSTS=null`, F1과 전체 F1~F5 `0/5`, A1~A3 `0/3`, 네 K `0/4`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED` 유지.

검토: Codex 직접 출처 대조와 PDF 시각 확인 `SELF_REVIEW`; Claude CLI의 [문서 단독 반증](../reviews/R01_O15F14AH_RIGHTS_SOURCE_SCOPE_REBUTTAL.md)을 받아 범위 명칭과 Markkanen 계약일을 바로잡았다. Claude가 PDF·CBA·NBA 원문을 독립 조회한 것은 아니다. Anti-Gravity·NotebookLM·source-blind는 이 증인에서 `NOT_RUN`.
