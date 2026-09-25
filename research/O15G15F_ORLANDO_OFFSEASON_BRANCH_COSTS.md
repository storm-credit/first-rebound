# O-15G15F — Orlando 2021 여름 명단·33번 픽 분기 비용

- 기준 `main` `4da3489` (PR #188). [G15E의 11+5 표준계약 시험](O15G15E_ORLANDO_STANDARD_SLOT_BRIDGE.md)에서 나온 **1명/2명 초과 반례**를 해소할 수 있는 사건을 비교한다. 실제 대체세계 계약·선수 이동·승패를 선택하지 않는다.
- 원역사 1차 자료: [ORL의 33번 Jason Preston 권리 양도](https://www.nba.com/magic/orlando-magic-acquire-future-second-round-pick-la-clippers-cash-considerations-20210729), [Lopez 영입](https://www.nba.com/magic/orlando-magic-sign-robin-lopez-nba-free-agent-contract-20210806), [Moritz Wagner 재계약](https://www.nba.com/magic/orlando-magic-re-sign-moritz-wagner-20210823), [구단 2022–23 미디어 가이드 거래 연표](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf) 인쇄 230–231쪽. E’Twaun Moore 영입 2021-09-09은 같은 연표에 있다. 기사·연표는 **원역사**다. 다른 세계의 팀 필요나 실제 계약 성사는 추론이다.

## 1. 33번 픽은 공짜가 아니다

원역사 Orlando는 2021-07-29 드래프트에서 33번 Jason Preston의 권리를 Clippers에 넘기고 **Detroit 경유 2026년 2라운드 픽과 현금**을 받았다. [G7 DB1 비교안](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)은 대신 Orlando가 33번으로 Herbert Jones를 뽑고, Jason Preston은 OKC 55번 후보로 내려간다. 이 비교안을 채택하면 ORL의 **원역사 2026년 픽/현금 유입을 함께 취소**해야 한다. Clippers가 33번 신인권을 얻지 못할 때의 잔여 선수 선택과 2026년 픽/현금의 대체 사용도 열린 파급이다. Herbert의 33번 지명 제안은 신인 계약 서명·표준 등록을 증명하지 않는다. 정확 현금액·픽 보호/귀속은 별도 감사 전 `HOLD`다.

## 2. 여름 계약의 선행 비용

| 원역사 사건 | 대체세계에서 유지할 때 | 채택하지 않을 때의 실존 선수·팀 비용 | 현재 판정 |
|---|---|---|---|
| 2021-08-06 Robin Lopez FA 영입 | Vučević·Bamba·Nnaji·Mobley에 Moritz까지 있을 수 있는 빅맨 층에 표준 자리 1개와 베테랑 역할 추가 | Lopez의 실제 ORL 계약·멘토/백업 경로가 사라진다. 새 팀/계약을 만들어 확정할 수 없음 | `BRANCH_HOLD` |
| 2021-08-23 Moritz Wagner FA 재계약 | 2020–21 말단 합류를 다음 시즌까지 잇지만, 센터/포워드 분 혼잡이 증가 | 그의 ORL 재계약 경로가 사라진다. Franz의 GSW 분기 때문에 형제 동팀이라는 원역사 경로는 이미 별도로 사라졌다. 2020–21 이미 수행한 경기를 지우지 않음 | `BRANCH_HOLD` |
| 2021-09-09 E’Twaun Moore FA 영입 | 경험 많은 가드 표준 자리 1개. G15B가 조건으로 쓰는 1/23 결장과 이전 시즌 깊이를 따로 감사 | 그의 실제 ORL 복귀 경로와 시즌 가드 깊이가 사라진다. Gravett 계약이 자동 승인되는 것은 아님 | `BRANCH_HOLD` |
| Vučević·Aminu 2021–22 계속 보유 | 각각 표준 자리 1개와 남은 급여/트레이드 기회비용. [T2 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)은 2020–21 잔여 시즌까지만 | 별도 이적·방출이면 거래상대, 급여/보상, G15B의 Vučević 센터 분을 다시 연결해야 함 | `2021_22_NOT_AUTHOR_LOCKED` |

## 3. G15E 수량 반례의 최소 사건 수

아래는 [G15E](O15G15E_ORLANDO_STANDARD_SLOT_BRIDGE.md)의 **공통 11명을 유지한 10/16형 시험**에서 출발한다. 원역사 1/23 실제 명단이나 대체세계 계약 수가 아니다. `-1`은 이름 있는 선수 한 명의 영입 취소·방출·이적 같은 **명시적 사건**을 뜻한다. 2021 여름의 거래/계약 날짜와 합법성은 미검증이다.

| 비교 경로 | 출발 수량 | 수량상 필요한 최소 비용 사건 | 240분 증명에 즉시 미치는 영향 |
|---|---:|---|---|
| O15A Herbert PG12 + Brazdeikis/Schofield 투웨이 유지 | 표준 16 | **-1**. 예: Lopez 비영입 또는 Moritz 비재계약 또는 Aminu 후속 처분. 한 사건의 실제 성립·급여·선수 대가는 각각 별도 | 셋은 G15B의 양수 분 대상이 아니어서 **분 산술만** 즉시 깨지지 않는다. Vučević 처분은 증명을 깨므로 동일한 -1 대체가 아님 |
| O15C Gravett PG12 표준계약 + 같은 투웨이 유지 | 표준 17 | **-2**. 예: Lopez 비영입+Moritz 비재계약, 또는 Lopez 비영입+Moore 비영입. 선수 두 명의 후속 경로·급여·로스터 인과 필요 | 제시한 두 조합의 이름은 G15B 양수 분 대상이 아니지만, 가드 층과 빅맨 깊이/기회가 달라져 기존 가용성·역할 비용 재검증 필요 |
| 한 자리만 줄이고 Gravett를 하드십으로 추가 | 표준 15 + 임시 경로 | 단순 15명 한도 외에 **2022-01-23 특정 결장·리그 예외 자격·유효 계약**을 증명해야 함 | 원역사 12월 두 차례 10일 계약만으로 1/23 출전 불가. 새 계약 사건 필요 |

Lopez·Moritz·Moore는 원역사 **실제 선수**이므로 수량 해결용 익명 방출 대상이 아니다. 특히 Moritz의 2020–21 말단 분과 Moore의 가드 보험 비용은 보존한다. O15A가 O15C보다 **표준 자리 한 칸을 덜 요구한다는 산술**까지만 유지한다. 작품성·농구 역할·급여를 합산한 우열은 아직 정하지 않는다. 만약 Herbert를 투웨이로 돌리려면 Brazdeikis/Schofield 2/2를 먼저 바꿔야 하므로 현재 두 240분 증명은 그대로 적용되지 않는다.

## 다음 종료 조건

1. Vučević의 2021–22 잔류/별도 이적과 Aminu 계약 처리에 대해 **한 분기씩** 실제 팀·급여·픽 비용을 적는다. 2020–21 T2를 2021–22 장기 잔류 승인으로 확대하지 않는다.
2. Herbert33을 쓰는 분기는 Clippers와 2026 Detroit 2라운드 픽/현금의 역방향 파급을 원장에 넣는다. 해당 지명·계약·등록은 여전히 조건부다.
3. O15A 또는 O15C의 날짜별 표준 15명/투웨이 2명/1월 23일 활동 15명과 의료를 선수별로 검증한다. 10/16형 수량 시연을 1/23 확정값으로 승격하지 않는다.

**사실/추론/후보/작가확정:** 위 원역사 거래일과 33번 보상은 사실. 2021–22 대체세계 선수 층의 과밀 및 16/17명은 명시된 조건 아래 추론. Lopez·Moritz·Moore 미영입/미재계약 조합은 비용을 드러내는 후보. 이 문서에서 새로 작가확정된 것은 없다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, 시즌/정확 실행 미선택, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다.
