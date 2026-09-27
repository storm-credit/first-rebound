# O-15F14-R — Fournier F2의 원거래 동일성 증명 경로

- 기준: `main` `e9e6771` / PR #273 병합 뒤. 범위는 F2의 **Boston–Orlando Fournier 거래**이며 F1 Chicago 3팀 거래·F3 Gordon·F4/F5 새 선택의 정확 종료가 아니다.
- 판정: `PRIMARY_TRANSACTION_ROUTE_RECOVERED / ALTERNATE_LEDGER_EQUIVALENCE_HOLD`. 실제 NBA가 승인한 사건과 대체 세계의 이름·계약·픽 경로를 분리한다. 이 문서는 F2 `PASS`가 아니다.

## 1. 공식 자료로 닫히는 원역사 사실

| 시점 | 공식 1차·리그 자료 | 확인되는 사실 | 넘겨 읽지 않을 것 |
|---|---|---|---|
| 2020 드래프트/11월 | [Boston 신인 평가](https://www.nba.com/celtics/news/sidebar/draft-111820-nesmith-pritchard-hope-impact-celtics-shooting-competitive-spirit), [Portland Bane 거래 발표](https://www.nba.com/blazers/news/2020/11/20/trail-blazers-acquire-enes-kanter) | Boston Nesmith14·Pritchard26, Bane30 권리→Memphis와 미래 2R 수취 | Memphis 2025 픽 외 모든 Boston 픽 의무·보호가 비었다는 증명은 아님 |
| 2020-11-30 | [Boston Teague·Thompson 서명](https://www.nba.com/celtics/news/pressrelease/celtics-sign-jeff-teague-tristan-thompson) | Teague는 Boston의 2020–21 계약 선수 | 구단 공지는 계약 금액을 공개하지 않음 |
| 2021-03-16 | [NBA의 거래예외 설명](https://www.nba.com/news/trade-exceptions-what-they-are-and-why-they-matter) | Hayward 출처 Boston 예외의 보도 명목액 `$28.5m`, 거래 마감 전 보유 | 정확 센트 단위 원장·당일 다른 사용분은 아님 |
| 2021-03-25/26 | [Boston Fournier 발표](https://www.nba.com/celtics/news/pressrelease/celtics-acquire-evan-fournier), [NBA 거래일 설명](https://www.nba.com/news/2021-nba-trade-deadline-notes-and-numbers) | 실제 Boston은 Teague·미래 2R 둘을 내고 Fournier를 받았으며 NBA는 Hayward 예외 사용을 명시 | 실제 승인이 **변경된 Orlando 장부의 승인**은 아님 |
| 같은 거래일 | [Boston Wagner·Kornet 발표](https://www.nba.com/celtics/news/pressrelease/celtics-acquire-moe-wagner-luke-kornet-3-team-trade) | Boston 쪽 실제 Theis·Green 유출, Wagner·Kornet 수취가 이미 승인 방향의 선수 네 명과 같다 | Washington/Chicago 쪽 대체 거래 전체가 원역사와 동일하지는 않음 |
| 2021-03-25~27 | [Orlando Fournier 발표](https://www.nba.com/magic/orlando-magic-acquire-two-future-second-round-draft-picks-boston-celtics-evan-fournier-trade-20210325), [NBA Teague 방출](https://www.nba.com/news/magic-waive-veteran-guard-jeff-teague) | Orlando는 Teague를 받되 출석시키지 않고 3/27 방출, 약 `$17m` 자체 TPE 취득 | 출석하지 않는다는 말은 3/25–27 **등록·급여 0**을 뜻하지 않음 |
| 2021-06-10 | [Orlando 후대 픽 설명](https://www.nba.com/magic/news/orlando-magic-have-great-opportunity-add-several-quality-players-through-draft-next-few-years-20210610) 검색 색인 | BOS/MEM 중 뒤 2025 2R과 BOS 2027 2R을 Orlando 보유 자산으로 열거 | 이 실행에서 본문은 HTML 셸/접근 불가. 검색 색인 확인이며 서명된 픽 원계약은 아님 |

위 거래일 NBA 설명은 원역사 TPE **사용 자체**의 1차 근거다. 선행 [자산 장부](../simulation/NBA_2021_ASSET_CHAIN.md)의 CBS 사용 보도와 후대 `$11.05m` 역산에만 기대지 않아도 된다. 그렇다고 대체 세계의 `$17.45m` 정확 charge나 예외 잔액을 새로 알게 된 것은 아니다.

### 3/21 공식 경기책으로 본 Orlando 출발 등록 수

[NBA 2021-03-21 ORL–BOS 공식 경기책 첫 장](https://statsdmz.nba.com/pdfs/20210321/20210321_ORLBOS_book.pdf)은 Orlando 출전/벤치 12명과 별도 inactive 5명을 함께 적는다. 전자 중 [Randle](https://www.nba.com/magic/news/magic-beat-knicks-behind-big-scoring-night-from-terrence-ross-tenacious-team-defense-20210217)·[Mané](https://www.nba.com/magic/orlando-magic-waive-karim-mane-20210413)는 구단 자료상 투웨이이므로 **일반 15 + 투웨이 2**의 3/21 관측 단면이다. 후속 [3/24 경기책·구단 거래 연혁 연결](O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md)은 3/24에도 일반 15 + 투웨이 2를 재관측하고, 3/25 전 별도 명단 거래가 구단 공개 연혁에 없음을 확인했다. 승인된 Gordon/Clark→Harris/Nnaji는 **2대2**, Fournier→Teague는 **1대1**이어서 대체 거래일 일반계약 자리 수가 15를 넘지 않고 Teague의 3/27 방출 뒤에는 14가 된다. 공개 등록 자리 산술은 통과했지만 정확 비용·거래 자격 인증은 아니다.

## 2. `원거래 동일성`을 F2 증명으로 쓰기 위한 조건

대체 세계에서 Boston의 거래일 입력을 원역사와 같게 유지하고, Orlando도 같은 Fournier 계약을 내보내며 같은 Teague 계약과 두 픽을 받는다면, **실제 승인된 거래 구조를 그대로 실행할 수 있다**는 증명 경로가 열린다. 이는 추론이다. 정확 비공개 센트 수치를 만들어 채우는 것보다 승인된 사건의 입력 동일성을 확인하는 방식이다.

현재 정본의 Boston Nesmith14·Pritchard26·Bane30 목적 거래와 Chicago Theis/Green 이동 방향은 위 **이름 붙은 입력**과 일치한다. 그러나 다음 불변 조건을 사건별로 모두 입증해야 F2 정확 실행을 닫을 수 있다.

1. Boston의 Hayward 예외 생성 이후 3/25까지 사용·만료·결합 금지 상태가 원거래와 같은지, Fournier 수취 전 다른 2020–21 계약/예외/픽 의무의 대체 변동이 없는지.
2. Fournier·Teague 계약 및 수취 전체 charge와 Boston의 hard-cap/apron 조건이 원거래와 같은지. [기존 Boston 급여 상한](../simulation/BOSTON_DENVER_2020_21_PAYROLL.md)의 `$5,381,195`는 미포함 `R_BOS`의 **조건부 여유**이지 원장 동일성 인증이 아니다.
3. BOS/MEM 2025 중 뒤 순번과 BOS 2027 2R의 **3/25 시점** 가용성·보호/우선권을 대체 세계의 Bane30 거래와 다른 픽 지출에 대조할 것. 6월 기사나 2025 최종 순번을 거래일 원계약으로 바꾸지 않는다.
4. [S의 공식 3/24 경기책·구단 거래 연혁](O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md)으로 3/25–27 **공개 등록 자리 수는 PASS**. 아직 Teague가 3/27 방출되기 전의 계약 부담과 잔여 보수, 거래 순서별 정확 Team Salary를 반영할 것.
5. Orlando가 원거래와 다른 Vučević 잔류·Gordon 대가 아래서 보내는 Fournier 거래가 CBA 수취/급여·hard-cap 조건을 만족하는지. [Orlando 4/12 이후 한도](../simulation/ORLANDO_2020_21_PAYROLL_BOUND.md)는 3/25–27 사건의 정확 장부가 아니다.

1~5를 만족하면 F2의 사적 리그 원장 숫자 대신 **동일 입력 + 원역사 공식 승인**을 실행 증명으로 사용할 수 있다. 하나라도 빠지면 여전히 `HOLD`다. 특히 Boston 네 선수의 동일성이 곧 Orlando 전체 동일성이라는 도약은 허용하지 않는다.

## 3. 다음 최소 실행

새 Fournier 결과를 다시 시뮬레이션하지 않는다. Orlando의 3/25–27 **자리 수는 S에서 닫았다**. 다음은 Teague 방출 전후의 날짜별 잔류 비용과 Vučević 잔류·Nnaji 수취를 넣은 거래일 한도, Boston의 11월 Bane 거래→3/25 예외 잔액/픽 의무에서 **변경된 입력만** 대조한다. 대조가 성립하면 F2 증명 경로를 재판정하고, 실패하면 달라진 입력·계약/픽 비용만 재계산한다. 2021 시즌·플레이인·추첨의 최종 작가 채택은 여전히 A3 이후다.

F 전체 PASS `0/5`, A 최종 채택 `0/3`, K 종료 `0/4`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.
