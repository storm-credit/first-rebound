# O-15G15G — Aminu의 2021 여름 경로와 DeRozan 거래 연쇄

- 기준 `main` `040cfa3` (PR #190). [G15F의 Orlando 표준 자리 초과](O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)와 Vučević/Aminu 후속 처분 빈칸 중 **Aminu가 2021-08-11에 어느 팀 소속인가**를 먼저 대조한다.
- 상태: `ORIGINAL_HISTORY_VERIFIED / ALTERNATE_CAUSAL_BRANCH_HOLD`. 새 거래·계약·등록·시즌을 선택하지 않는다.
- 원역사 공식 근거: [2021-03-25 Magic 발표](https://www.nba.com/magic/orlando-magic-acquire-wendell-carter-jr-otto-porter-jr-chicago-bulls-nikola-vucevic-al-farouq-aminu-trade-20210325), [2021-08-11 Bulls 발표](https://www.nba.com/bulls/news/bulls-acquire-demar-derozan), [NBA 2021 오프시즌 거래 원장](https://www.nba.com/news/2021-offseason-trade-tracker)의 `Bulls add DeRozan via sign-and-trade (Aug. 11)`, [2021-10-18 Spurs 방출 발표](https://www.nba.com/spurs/spurs-waive-al-farouq-aminu). NBA 거래 원장은 공개 본문을 직접 확인했고 NotebookLM 작업실에서도 URL 소스 ID `291dc747-80e1-40ca-99cc-b8e9f5aa889a`로 수집·출처 제한 분석했다. 같은 원문을 두 도구가 읽은 것이므로 독립 원자료 두 건으로 세지 않는다.

## 1. 원역사의 실제 의존 사슬

| 날짜 | 확인된 사건 | 대체세계로 복사할 때의 제약 |
|---|---|---|
| 2021-03-25 | Orlando가 Vučević·Aminu를 Chicago에 보내고 Carter Jr.·Porter Jr.·미래 1라운드 픽 2장을 받음 | 이 프로젝트의 T2는 Vučević를 **2020–21 잔여 시즌만** Orlando에 남긴다. 따라서 원역사 Chicago 패키지는 실행되지 않았고 Carter/Porter/두 픽도 자동 유입되지 않는다. |
| 2021-08-11 | 원역사 Chicago가 DeRozan을 받고 San Antonio에 **Aminu·Thaddeus Young·미래 1라운드 1장·2022 2라운드 1장·2025 2라운드 1장**을 보냄 | 3월에 Aminu가 Chicago로 오지 않았다면 8월 원거래의 선수 1명이 송출 명단에 없다. [G8 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md)는 Young을 유지하는 조건부 예산이므로 그 경로를 쓰면 원거래의 두 선수 모두 가용하지 않다. DeRozan 합류나 동일 픽 지출을 자동 채택할 수 없다. |
| 2021-10-18 | 원역사 San Antonio가 Aminu를 방출함 | 대체세계에서 Spurs가 8월에 Aminu를 받지 않았다면 이 방출 역시 발생한 것으로 복사할 수 없다. Aminu의 다른 팀 계약·방출·건강 상태는 별도 사건이 필요하다. |

NBA 거래 원장은 8월 픽의 **미래 1라운드**라고만 적는다. 특정 연도·보호·이연·계약 금액·급여 매칭은 이 원문만으로 확정하지 않는다. NotebookLM도 같은 경계를 반환했으며, 이는 출처 연결 분석이지 CBA 판정이 아니다.

## 2. G15F의 10/16형 자리 산술에 주는 영향

G15F의 공통 11명+대체 선수 5명/6명 시험을 **그대로 둔 조건**에서만 아래 한 칸 산술이 성립한다. 2022-01-23 실제 명단이나 활동 가능 증명이 아니다.

| Aminu 사건 후보 | O15A Herbert PG12 | O15C Gravett PG12 | 다음 확인 |
|---|---:|---:|---|
| 2021-10-16 전에 대체세계 Orlando에서 이적·방출 | 표준 16→15 | 표준 17→16 | 사건일·새 팀 또는 방출 비용·남은 보장급여/charge·실존 선수 경로. O15C에는 추가로 1명 비용 사건 필요 |
| 10/16에는 남고 그 뒤 이적·방출 | 10/16형 표준 16 유지 | 10/16형 표준 17 유지 | 개막 15명 규칙의 초과를 나중 사건으로 소급 해소할 수 없음. 1/23 숫자는 날짜별 재구성 필요 |
| 2021–22 계속 보유 | 표준 16 유지 | 표준 17 유지 | 역할·급여·등록 비용과 추가 자리 사건 필요. T2의 Vučević 잔류 기간을 자동 연장하지 않음 |

**필요한 분기 비교:** (A) Aminu를 Orlando가 2021–22에도 보유, (B) 10/16 전 이름 있는 별도 이적·방출, (C) 10/16 뒤 별도 처분. Chicago가 8/11 전에 다른 거래로 Aminu를 얻는 세부 경로까지 검토하려면 상대·보상·급여/픽·Young 처리와 Spurs 합의를 새로 증명해야 한다. 이 표의 A/B/C는 비용과 시간 경계를 드러내는 후보이며 선택안이 아니다.

Vučević도 별도 분기다. 2021–22에 Orlando가 그를 계속 보유하면 표준 자리·빅맨 분·급여가 남는다. 떠나면 이적 상대와 대가가 필요하고 [G15B의 Vučević 양수 센터 분](../simulation/CHICAGO_2021_22_G15B_REVIEW.md)을 다시 검산해야 한다. Aminu 한 명의 자리 해소가 Vučević 계약과 DeRozan 거래까지 해결하지 않는다.

## 3. 도구 판정과 다음 종료 조건

- Anti-Gravity CLI 절대 경로 실행은 확인됐으나 이번 PDF 직접 읽기는 headless `command` 권한 자동 거부, Bulls 기사 `read_url_content`는 `ACCESS_FAILED`였다. **Anti-Gravity가 독립 확보한 새 NBA Evidence Pack은 0건**이다. 권한 전체 자동 승인은 적용하지 않았다.
- NotebookLM CLI에서 Bulls/Spurs 개별 기사 URL 두 건은 추가 실패. NBA 공식 거래 원장 URL은 추가·원문 조회·해당 소스만 지정한 질의에 성공했다. 질의는 위 8/11 선수 2명·픽 3장을 올바르게 추출했다. 출처 ID `291dc747-80e1-40ca-99cc-b8e9f5aa889a`, 대화 ID `7aae2c2c-9b9c-4520-9166-69526e4269b0`.
- 다음에는 Aminu·Vučević의 **날짜별** 대체세계 계약 보유자와 처분 사건을 서로 배타적인 안으로 놓고, 해당 시점의 15 표준/2 투웨이·급여·픽·실존 선수 분을 검산한다. Chicago–Spurs DeRozan 재협상과 G8 Young 유지 조건을 따로 비교한다. 새 선수 이동이 작가확정되기 전에는 G15B의 1/23 Orlando 12분·G14의 ORL4 `ROLE_HOLD`를 풀지 않는다.

**사실/추론/후보/작가확정:** 위 원역사 세 거래·방출 및 8월 송출 자산은 사실. 원거래를 대체세계에 그대로 복사할 수 없다는 것은 현재 승인 방향과 비교한 인과 추론. A/B/C는 후보. 이 문서의 새 작가확정은 0건. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 시즌·정확 실행 미선택을 유지한다.
