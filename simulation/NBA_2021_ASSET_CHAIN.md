# O-15F14-L — Boston 예외·Fournier 픽의 출처 연결

- 기준 main: PR #159 / `11d488d3ae6afdf9c9d26dca44d2733e5b522e28`.
- 상태: **Boston 픽 출처·예외 사용 보도·Denver 선행 종료 보도 회수 / 정확 실행·시즌 채택 HOLD**.
- 사실 권위: `research/NBA_2021_L_ASSET_CHAIN_SOURCES.json`. 산술/분기 권위: 동명JSON.

## 1. Fournier의2025 픽은 승인된 Bane 거래에서 이어진다

[Boston의 Bane 거래 공지](https://www.nba.com/celtics/news/pressrelease/celtics-complete-three-team-trade-grizzlies-trail-blazers)는 Memphis 자체2025년2R 취득을 명시한다. 공지UTC는2020-11-21 03:00, 동부 날짜는11/20이다. 기존 `2020_DRAFT_RJ_HAMPTON_RELANDING_BOARD.md`의 Bane30 목적 거래 승인을 재사용한다. 새 드래프트 경로를 제안하지 않는다.

| 자산 단계 | 연결 결과 | 경계 |
|---|---|---|
| 2020 Bane30 권리 거래 | MEM2025 2R → BOS | 해당 연도 자산 출처를 구단본문에서 회수 |
| 2021 Fournier 대가 | BOS/MEM2025 중 뒤 순번 → ORL | 기존2차거래장부 조건; 전체 원계약 미확보 |
| 같은2025 묶음의 나머지 | 앞 순번은 BOS에 남는 구조 | 다른 의무가 없다는 조건; 전 자산 우선권 인증 아님 |
| 별도 두 번째 대가 | BOS2027 2R → ORL | 기존 보고; 전체 보호·우선권 검증은 별도 |

[Boston의 Fournier 공지](https://www.nba.com/celtics/news/pressrelease/celtics-acquire-evan-fournier)도 Teague와미래2R두장 교환을 확인한다. 기존Orlando 공지와 일치하지만 이Boston 공지는 정확 픽연도나TPE금액을 명시하지 않는다. 기존 [Fournier 거래 장부](https://www.salaryswish.com/trades/players/evan-fournier)의 최종2025 순번/선수 결과는 복사하지 않는다.

`less favorable`는 숫자가 더 큰 뒤 지명이다. 예시 BOS60/MEM31이면ORL에BOS60, 반대면MEM60이다. 이는 선택 규칙의 시험이며 미래성적·동률추첨·최종순번이 아니다. 아직 순번이 없으면 결과는null이다. 서로 같은 최종순번을 입력하거나1R순번을 넣으면 거부한다. 동률승수를 최종순번으로 대신하지 않는다.

## 2. TPE 사용과11.05m 잔액의 의미

[동시대 CBS 보도](https://www.cbsnews.com/boston/news/celtics-evan-fournier-trade-magic-nba-trade-deadline/)는 Fournier 수취에TPE를사용했고 잔액을약11m으로 설명한다. [HoopsRumors의2021 오프시즌 장부](https://www.hoopsrumors.com/2021/07/2021-nba-offseason-preview-boston-celtics.html)에는 **$11,050,000** 예외가 있다. HTML의 발행7/8·수정7/26을 기록했다. 목록 자체가 예외 원선수를 명명하지 않으므로 Hayward와의 연결에는 기존28.5m근거와사용보도를 함께 사용한다.

| 기존28.5m 예외에 넣는 Fournier 시험값 | 다른 사용0일 때 잔액 | 후대11.05m와 산술 일치 |
|---:|---:|---|
| $17,000,000 | $11,500,000 | 아니오 |
| $17,150,000 | $11,350,000 | 아니오 |
| $17,450,000 | $11,050,000 | 예 |

이 표는 기존L의3조건을 다시 연결한 것이며 새3조건으로 부풀리지 않는다. **새로 확보한 것은 외부 잔액 목록과 실제사용 보도**다. 동일예외이며 다른사용이없었다고 가정할 때 차액$17.45m이 도출되지만, 이것을3/25의정확Fournier charge로확정하지 않는다. 후대스냅샷에서역산한일치와거래당일원장확인은다르다. 이 자료로 기본급17m·거래요약17.15m·계약장부cap17.45m의 차이 원인까지 증명하지도 않는다.

Teague를같은공식거래로보냈다는이유로 `Fournier−Teague` 순액만 기존TPE에사용한 것으로계산하지않는다. 기존3조건은Fournier수취액전체를시험한다. 예외가생겼다는사실, 사용액, 다른예외와의합산, 팀급여·세금은별개다. Boston예외가Orlando생성예외와같은것도아니다. 정확새세계예외잔액은null을유지한다.

## 3. Denver 선행1R의 미전달 종료 보도를 회수했다

[Basketball Insiders의 미래픽 보도](https://www.basketballinsiders.com/news/assessing-future-draft-capital/)는 선행DEN1R의2023~25 top14 보호와 **2025·2026 DEN2R 전환**을 명시한다. 페이지는2021-10-15 갱신 표시이며3/25 서명 원계약으로 취급하지 않는다. 이전L의종료null은당시미확보이력이고, 이제 `REPORTED_TERMINAL_CONVERSION` 필드를 후속 권위로 제공한다. 대체세계에서 정확조항을채택했다는뜻은아니다.

| 시험 경로 | 선행 의무의 보고 조건상 결과 | Gordon에 넘길 처리 |
|---|---|---|
| 2023 최종15~30 | 2023 1R 전달 | 기존조건부Y+2의2025부터 검토 |
| 2023 보호,2024 최종15~30 | 2024 1R 전달 | 같은조건부2026부터 검토 |
| 2023·24 보호,2025 최종15~30 | 2025 1R 전달 | 같은조건부2027부터 검토 |
| 2023~25 모두1~14 | 보고상2025·2026 2R전환 | Gordon의연결/종료원문없으므로null |

경계14는보호,15는전달이다. 미래결과가아직없으면그해에서멈춘다. 소설의2023~27성적을새로정하거나실제전달연도를복사하지않았다. 전환되는2R도실제보유·기존처분·우선권과결합해야하므로자동인도확정은아니다.

[동시대 Gordon 보도](https://www.hoopsrumors.com/2021/03/nuggets-magic-nearing-aaron-gordon-trade.html)는2025~27 top5를재확인했지만그이후종료나선행전환과의연결문구는없다. 특히 **선행의2025·26 2R전환을Gordon의종료조항으로복사하지않는다.** 전체Stepien·자산가용성인증도아니다. 승인된Nnaji24 대가방향을실제Hampton으로되돌리지않는다.

## 4. 후속 입력과 남은 마지막 구분

이번에좁힌항목은MEM2025의출처, Boston예외사용/후대잔액일치, Denver선행미전달전환이다. 같은항목을전량재조사하지않는다. Chicago의R한도$5,609,972와15명급여는이전PR159권위그대로유지한다.

남은사실은R실제구성·Boston당일charge/예외우선권·Gordon후행의정확연결과종료·후속등록charge다. 공개보도회수를실행완료로올리지않고, 미확보원문을작가선택으로대체하지않는다. K1·L2·Hall행정사건은기존추천패킷으로남기며이미승인한방향은재질문하지않는다. 새경기점검목록은추가하지않았다.

신규검증6개PASS·JSON재현·diff검사통과. **자체검토 NOT_INDEPENDENT**. 네K묶음전체종료0, author_locked=false·season_selected=false·원고false·v0.30 PARTIAL·설계/원고CLOSED 유지.


### 최신 회수 범위 연결

[실행 조항 후속](NBA_2021_EXECUTION_RESOLUTION.md)에서 해당 미확보 이력의 후속 근거를 제공한다. 이 문서/JSON의 당시 계산을 소급 변경하지 않는다. 최신 잔여 필드는 [채택 준비 색인](CHICAGO_2020_21_ADOPTION_READINESS.md)에 통합했다. 전체 정확 실행·시즌은 여전히 HOLD다.
