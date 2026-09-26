# O-15G15I — Aminu 명단 이탈과 2021–22 팀 샐러리 비용

- 기준 `main` `edf1730` (PR #192). [G15H의 날짜별 자리 증명](O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)에서 필요한 Aminu 이탈을 **명단 자리와 급여 부담의 서로 다른 질문**으로 나눈다. 이 문서는 새 방출·트레이드·재계약을 선택하지 않는다.
- 상태: `CBA_COST_BRANCH_ONLY / EXACT_SALARY_AND_EXECUTION_HOLD`. 2018 드래프트 Chicago 원클럽 방향이나 2020–21 T2를 다시 승인받지 않는다.

## 1. 적용 규칙과 실제 계약의 범위

2021–22에는 2017 CBA 체계가 적용된다. [NBA의 2021년 CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) `I.L Team Salary Rules`는 **계약 중인 선수의 급여와 방출 뒤에도 팀이 지급하는 보장급여**를 팀 샐러리의 주요 구성요소로 적는다. 같은 문서 `I.U Stretch`는 방출 후 **현금 지급 일정**의 자동 분산과 **샐러리캡 계산**의 선택적 stretch를 구분하며, 9월 1일 이후 방출의 당해 시즌 지급 일정과 장래 방출 선수 급여 15% 한계도 별도로 적는다. `I.T Termination Agreements`의 보호액 감액은 선수와 합의해야 하며 재영입 제한이 뒤따른다. `I.L`의 자유계약선수 금액과 권리 포기 규칙도 비영입 시 cap hold가 자동으로 0이 되지 않을 수 있음을 보여준다.

[NBA의 2021–22 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)는 샐러리캡 **$112.414m**, 사치세선 **$136.606m**, 팀 최소급여 **$101.173m**를 정한다. 이 숫자는 **리그 기준선**이지 대체 Orlando의 팀 샐러리, cap room, 세금 지위가 아니다.

원역사 Orlando는 [2019-07-06 Aminu와 계약](https://www.nba.com/magic/magic-sign-al-farouq-aminu-20190706)하고 [같은 날 Vučević와 재계약](https://www.nba.com/magic/orlando-magic-re-sign-nikola-vucevic)했다. 구단 발표는 **계약 조건을 비공개**로 했다. NBA.com의 당시 보도는 각각 [Aminu 3년·$29m](https://www.nba.com/30teams30days/2019/orl), [Vučević 4년·$100m](https://www.nba.com/news/report-nikola-vucevic-re-sign-magic)으로 전하지만, 이 **총액 보도만으로** 2021–22의 연봉·보호액·보너스·트레이드 계산액을 산출하지 않는다. T2에서 Vučević가 2020–21 잔여 기간 Orlando에 남는다고 승인됐으므로, 별도 후속 사건이 없다면 그의 기존 계약이 2021–22에도 Orlando에 이어진다는 것은 **조건부 추론**이다. 그해 잔류와 정확 급여는 작가확정이 아니다.

**Aminu 선수 옵션 선행 게이트:** 원역사 [2021 Chicago 드래프트 전 팀 프로필](https://www.nba.com/draft/2021/team-profiles/chicago-bulls)은 Aminu를 계약 중인 선수로 적는다. 당시 [옵션 결정 보도](https://www.hoopsrumors.com/2021/05/nba-player-option-decisions-for-202122.html)와 [계약 추적표](https://www.salaryswish.com/players/alfarouq-aminu)는 2021–22 **선수 옵션 행사**, 연봉 **$10,183,800**을 보고한다. 이 숫자는 두 비공식 계약 자료가 일치하는 **원역사 작업 추정치**이며 공식 구단 발표의 상세 금액은 아니다. [T2 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)은 Vučević의 2020–21 잔여 시즌만 명시한다. Aminu는 [Orlando 2020–21 등록 유지안](../simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.md)에 있으므로 **원역사 Chicago 패키지 이후 별도 이동이 없다는 조건에서만** 2021년 5월 Orlando 소속으로 시험한다. **그가 옵션을 행사했는지**를 먼저 분기해야 한다. 원역사의 Chicago 행사·마감일을 자동 복사하지 않는다. 아래 A~D의 방출/트레이드 분기는 모두 **Orlando가 해당 계약을 보유하고 옵션 행사 후 계약이 존재한다는 조건**이다. 옵션 미행사라면 2021–22 계약을 방출/트레이드할 수 없고 O15A/O15C의 표준 수는 각각 15/16으로 내려가지만, Orlando 자체 FA 권리·cap hold와 Aminu가 큰 보수의 옵션을 포기할 동기·다음 팀 계약을 별도로 증명해야 한다. 미행사를 편의상 기본값으로 삼지 않는다.

## 2. Aminu의 서로 배타적인 비용 분기

| 2021–22 후보 사건 | 10/16 표준 자리 영향 | 팀 샐러리·실존 선수 비용 | 실행 판정 |
|---|---|---|---|
| A. Orlando가 계속 보유 | G15E의 O15A **16**, O15C **17** 유지 | 기존 계약을 보유한다는 조건. 다른 실제 선수를 밀어낼 자리 사건이 필요 | `SLOT_FAIL` |
| B. 10/16 전에 Orlando가 waiver를 요청하고 명단 이탈을 완결 | O15A **15**, O15C **16**이라는 수량은 가능 | 방출이 **보호급여를 지우지 않는다**. 보호액·waiver claim·선수와의 감액 합의·cap stretch 선택·정확 비용은 미확인. 선수의 다음 행선지도 미정 | `NAMED_SLOT_ONLY / CAP_HOLD` |
| C. 10/16 전에 Aminu 계약을 다른 팀에 트레이드하고 표준 선수를 돌려받지 않음 | O15A **15**, O15C **16**이라는 수량은 가능 | 수취 팀의 cap room/예외·실제 수용 동기, Orlando가 내줄 수 있는 픽·현금 등의 보상, 팀별 급여 매칭·실행일과 대체 DeRozan 거래 파급이 전부 필요. [CBA 101의 트레이드 선수 예외](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) 공식은 팀 샐러리/세금 지위별로 다르므로 단독 합법 판정 불가 | `TRADE_MATCH_AND_COUNTERPARTY_HOLD` |
| D. 10/16 뒤 1/23 전에 별도 처분 | **10/16 초과 문제를 소급 해결하지 못함** | O15C의 [Lopez 비영입→개막 15명→Aminu 처분→Gravett 신규 계약](O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md) 예시에는 시간상 쓸 수 있으나, 각 계약·명단·급여 사건이 모두 필요 | `O15A_OPENING_FAIL / O15C_CONDITIONAL` |

`B`에서 waiver를 요청했다는 말만으로 해당 점검일의 명단 이탈을 확정하지 않는다. CBA 101 `VI.D`의 일반 waiver 기간은 48시간이고, [2017 CBA에 수록된 NBA By-Laws 5.04](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)는 **리그의 waiver 통지 뒤** 48시간을 청구 기간으로 규정한다. 정확 요청·리그 통지·통과/claim 시각을 별도 기록해야 한다. **자리 1개 확보 ≠ 그 선수의 급여 부담 제거 ≠ 새 계약을 맺을 cap room 확보**다. `C`에서도 무조건 무보상·무급여 트레이드가 가능한 것으로 쓰지 않는다.

Lopez는 [2021-08-06 원역사 외부 FA 영입](https://www.nba.com/magic/orlando-magic-sign-robin-lopez-nba-free-agent-contract-20210806)을 대체세계에서 **선택하지 않는** 경우이므로 Orlando의 그 신규 표준계약이 생기지 않는 조건이다. 반면 Moritz는 [2021-08-23 원역사 재계약](https://www.nba.com/magic/orlando-magic-re-sign-moritz-wagner-20210823)을 하지 않는 분기다. [NBA의 2021 드래프트 전 Orlando 팀 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 그를 **unrestricted FA**로 분류한다. 그가 Orlando의 자체 FA였던 만큼, 비재계약만으로 **FA 관련 팀 샐러리 금액까지 없어진다고 단정할 수 없다**. CBA 101 `I.L`의 기본 FA 금액을 제거하려면 권리 포기 등의 사건이 필요하다. 권리 유지·포기, 다른 팀 서명, 정확 cap hold와 선수 행선지를 확인해야 한다. 둘 다 명단·출전시간·선수 경로 비용이 남는다.

원역사의 [2021-08-11 DeRozan 사인앤트레이드](O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)는 Chicago가 Aminu를 보유한 경우에 성립했다. 이 분기들에서 그 원거래를 그대로 복사하지 않는다. **8월의 Chicago 거래/FA·픽 비용이 먼저 바뀌면 10월 Orlando의 수취 팀 시장도 바뀔 수 있다.** Aminu를 Orlando에서 방출하든 다른 팀으로 보내든, Chicago–Spurs의 상대·Young·픽·급여 구조는 별도 증명이 필요하다. [G15E의 4대5 치환](O15G15E_ORLANDO_STANDARD_SLOT_BRIDGE.md)은 원거래로 Orlando에 온 Carter/Porter와 원역사 전용 Hampton/Suggs/Franz를 공통 11명에서 제외하고 있으나, 다른 팀의 후속 선수·픽 경로는 아직 완결하지 않았다.

## 3. 도구 결과와 다음 검증

- Codex가 NBA 공식 CBA 101 `I.L`, `I.T`, `I.U`, `VI.D`와 NBA 2021–22 캡 발표를 직접 대조했다. 구단의 2019 계약 발표에는 세부 급여가 공개되지 않음을 확인했다.
- NotebookLM CLI는 위 CBA PDF 소스 `4e516c8c-d38b-4a27-8c70-1e05f8c5dced`와 캡 발표 소스 `605e9737-8fa5-42b1-9ca7-130873b289f1`만 지정한 질의 `deefcfcf-17d0-421f-905a-94d3e926d5a8`에서 방출 보장급여·현금/캡 stretch 차이·리그 수치를 인용했다. 두 소스에는 Aminu/Vučević의 정확 2021–22 급여가 없다고 답했다. Codex와 **같은 원문**이므로 독립 출처 수를 늘리지 않는다.
- Anti-Gravity CLI의 CBA PDF `read_url_content`는 60초 제한에서 도구 실행 중 멈춰 본문 출력이 없었다. 별도 [NBA 2021–22 캡 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)는 `read_url_content`→`view_file` 완료 기록과 최종 URL·제목·발행일·$112.414m/$136.606m을 반환했다(대화 `3e98de87-6343-4b7d-96f9-7cbbb10fe842`). Codex도 저장된 본문에서 두 수치를 직접 확인했다. **이 URL에 한해 NBA 직접 원문 판독 1건**이며 CBA PDF 판독이나 새 독립 출처 확보로 확대하지 않는다.

다음은 (1) Aminu의 **대체세계 선수 옵션 행사 여부와 개인 동기**, Vučević의 해당 시즌 계약 원문·보호액, (2) Orlando의 대체세계 날짜별 **전체 팀 샐러리와 세금 지위**, (3) B/C/D의 실제 상대·선수·픽·waiver 시각, (4) Moritz FA 권리·Lopez 후속 경로를 확보하는 것이다. 그 뒤에만 G15H의 `NAMED_SLOT_WITNESS_ONLY`를 `registration/cap` 심사로 넘긴다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16/G17 미완료, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, author/season/exact/manuscript false 유지.
