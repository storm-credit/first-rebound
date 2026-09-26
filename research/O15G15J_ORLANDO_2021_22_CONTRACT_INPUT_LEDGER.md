# O-15G15J — Orlando 2021–22 계약 입력값의 출처와 날짜

- 시작점: `main` `6a0006f` / PR #193. [G15I의 옵션·명단·팀 샐러리 분기](O15G15I_AMINU_WAIVER_CAP_COST.md)를 이어 **금액을 넣을 수 있는 칸과 사건을 먼저 선택해야 하는 칸**을 구분한다.
- 상태: `HISTORICAL_CONTRACT_INPUTS_ONLY / ALTERNATE_TEAM_SALARY_HOLD`. 새 선수 옵션 행사, 방출, 트레이드, 계약 또는 시즌 결과를 확정하지 않는다.

## 1. 원역사 자료가 말하는 범위

| 필드 | 원역사 확인값과 출처 등급 | 대체 Orlando에 사용할 조건 |
|---|---|---|
| 2021–22 NBA 샐러리캡 / 세금선 | **$112,414,000 / $136,606,000**. [NBA 공식 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season) | 리그 전체에 적용하는 기준선이다. Orlando의 팀 샐러리나 cap room을 뜻하지 않는다. |
| Vučević 2019 계약의 2021–22 기본급 | **$24,000,000**. [SalarySwish의 2019 계약 연도별 표](https://www.salaryswish.com/players/nikola-vucevic)와 [Spotrac의 연도별 수령 표](https://www.spotrac.com/redirect/player/8067)가 일치하는 비공식 계약 추적값. [2019 NBA 보도](https://www.nba.com/news/report-nikola-vucevic-re-sign-magic)는 총액 4년/$100m까지만 전한다. | 승인된 T2는 **2020–21 잔여 기간** Orlando 잔류다. 2021–22에도 별도 거래·계약 변경 없이 잔류한다는 사건을 채택해야 Orlando 급여로 넣는다. 원역사 Chicago의 2021–22 소유를 복사하지 않는다. |
| Aminu 2021–22 선수 옵션 기본급 | **$10,183,800**. [SalarySwish의 계약·옵션·보호액 표](https://www.salaryswish.com/players/alfarouq-aminu)와 [당시 옵션 결정 보도](https://www.hoopsrumors.com/2021/05/nba-player-option-decisions-for-202122.html)의 비공식 값. 원역사에서 옵션은 2021-05-18 행사로 기록된다. | 대체세계에서는 그날 Orlando 소속이므로 **Orlando에서 옵션 행사 여부**와 선수 동기부터 별도 판정한다. 2019 계약서 원문이나 구단 공식 연도별 금액은 확보하지 못했다. |
| Lopez / Moritz 계약 | 원역사 Lopez **2021-08-06 영입**, Moritz **2021-08-23 재계약**. [Lopez 구단 발표](https://www.nba.com/magic/orlando-magic-sign-robin-lopez-nba-free-agent-contract-20210806), [Moritz 구단 발표](https://www.nba.com/magic/orlando-magic-re-sign-moritz-wagner-20210823)는 금액을 비공개로 한다. [NBA 2021 Orlando 드래프트 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 Moritz를 unrestricted FA로 분류한다. | Lopez 비영입이면 Orlando의 **신규 계약 비용**은 없지만 다른 팀 경로는 남는다. Moritz 비재계약은 자체 FA 관련 권리·cap hold의 포기/소멸 사건 없이 팀 샐러리 0이라고 쓸 수 없다. |

두 비공식 연봉의 단순 합은 **$34,183,800**이다. 이는 **Vučević의 2021–22 Orlando 잔류 + Aminu의 옵션 행사 및 Orlando 계약 보유**를 모두 가정한 **두 계약만의 후보 부분합**이다. 선수 2명 이외의 Orlando 급여·FA 금액·방출 보호액·신인 서명·예외 사용은 포함하지 않는다. 따라서 이 부분합으로 cap room, 사치세 여부, 거래 급여 매칭, 새 계약 가능성을 판정하지 않는다. 원역사 자료의 연도별 기본급이 대체세계의 확정 팀 샐러리 증명이라는 뜻도 아니다.

## 2. Aminu 한 자리의 날짜별 비용 분기

1. **옵션 행사 전:** 2021-05-18이라는 원역사 행사 날짜는 대체 Orlando의 자동 사건이 아니다. 옵션 미행사를 채택하면 $10,183,800 계약 자체가 2021–22에 발생하지 않지만, 자유계약선수 관련 팀 샐러리 금액과 그가 큰 옵션 보수를 포기할 동기·다음 계약이 미해결이다.
2. **옵션 행사 + 보유:** $10,183,800은 비공식 자료의 기본급 입력 후보. [G15I](O15G15I_AMINU_WAIVER_CAP_COST.md)의 10/16 O15A=16명·O15C=17명 자리 초과는 그대로다.
3. **옵션 행사 + 개막 전 방출:** waiver 완료 뒤 명단 자리 하나는 줄 수 있다. [2017 CBA 체계의 NBA CBA 101 `I.L Team Salary Rules`, `I.U Stretch`](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)에 따르면 지급할 보호급여는 팀 샐러리에 남고 cap stretch는 별도 선택이다. 실제 Spurs의 2021-10-18 방출에 대해 [SalarySwish](https://www.salaryswish.com/players/alfarouq-aminu)는 $10,183,800 dead cap을 기록하지만 **대체 Orlando의 방출 사건·보호액·감액 합의·set-off·stretch를 증명하지 않는다**. 조정·stretch가 없다는 조건 아래 두 계약의 후보 부분합도 **$34,183,800**으로 그대로다. 이는 전체 팀 샐러리 합계가 아니다.
4. **옵션 행사 + 개막 전 트레이드:** Aminu의 계약이 Orlando에서 나가면 위 두 선수의 남는 기본급 후보는 Vučević **$24,000,000**이다. 그러나 수취 팀의 수용·상대 선수/픽/현금·Orlando의 대가·급여 매칭·예외를 넣기 전에는 **Orlando 순급여 감소액**을 계산할 수 없다. Chicago의 실제 8월 DeRozan 사인앤트레이드 비용도 먼저 [G15G](O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)에서 다시 연결해야 한다.

## 3. 전체 팀 샐러리 계산을 막는 입력

| 날짜 점검 | 아직 필요한 행과 사건 | 지금 허용되는 판정 |
|---|---|---|
| 2021-05 옵션 시점 | Aminu의 대체 Orlando 옵션 통지·보호액·선수 동기 | `OPTION_DECISION_HOLD` |
| 2021-07/08 드래프트·FA·거래 | 대체 드래프트 픽/서명액, 기존 선수 계약 원장, 자유계약선수 금액·권리 포기, Chicago–Spurs 선행 거래, Lopez/Moritz 선택 | `DATE_LEDGER_HOLD` |
| 2021-10-16 개막 명단 점검 | G15H의 표준 15자리와 해당 날짜 전 Aminu waiver 통지/통과 또는 상대 이름 있는 거래, 모든 보호급여·예외·신규 서명 | `SLOT_WITNESS_ONLY / CAP_HOLD` |
| 2022-01-23 경기 가용성 | G15B 양수 출전자의 실제 서명·활동·의료, 뒤늦은 명단 사건의 당일 효력 | `ROLE_AND_REGISTRATION_HOLD` |

기준 [G15H 명단 증명](O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)의 O15A/O15C는 **조건부 자리 수**다. 실제 Orlando 2021–22 팀 급여표를 가져와 대체세계 급여로 붙이면 Vučević/Aminu의 원역사 이적, Carter/Porter 유입, 원역사 픽·신인 서명 등이 섞인다. 필요한 것은 선수별 `계약 소유 팀 / 사건일 / 2021–22 charge / 보장·방출 잔액 / FA hold 또는 포기 / 거래 유입·유출 / 서명 예외`를 날짜별로 다시 연결한 원장이다.

## 4. Research/Verification Layer v2의 이번 실행 범위

- **Codex 원문 대조:** NBA 공식 캡 발표와 CBA 101, 2019 구단/리그 발표, 2021 구단 영입 발표의 공개 범위를 확인하고 비공식 연도별 추적값은 `원역사 작업 추정치`로만 분류했다.
- **NotebookLM CLI:** 기존 공식 CBA PDF `4e516c8c-d38b-4a27-8c70-1e05f8c5dced`와 캡 발표 `605e9737-8fa5-42b1-9ca7-130873b289f1`만 지정한 새 질의 `5cf77ae9-bf25-4dc3-8617-f42bf79492af`에서 보호급여의 팀 샐러리 잔류와 cap/cash stretch 구분, 공식 기준선을 확인했다. 두 출처에 선수별 Orlando 급여는 없다고 답했다. Lopez/Moritz 구단 URL을 새 출처로 추가하려는 호출은 실패했다.
- **Anti-Gravity CLI:** 절대경로 `agy.exe`로 구단 발표 두 URL을 `read_url_content`에 요청했으나 본문 대신 JavaScript만 회수됐다고 반환했다. **두 발표의 Antigravity 직접 본문 판독은 실패**다. 이 결과를 Codex의 별도 원문 확인이나 NotebookLM 공식 자료와 합쳐 독립 원자료 여러 건으로 세지 않는다.
- **Claude 독립 반증 / source-blind:** Claude CLI에 읽기 전용 파일 검토와 도구 없는 문서 전달을 각각 시도했으나 두 호출 모두 2분 이상 응답 본문이 없어 중단했다. 이번 문서의 독립 반증은 `NOT_RUN`, 결과물 단독 검수도 `NOT_RUN`이다. G15I의 제한 검토 성공을 G15J 검수로 이월하지 않는다.

다음은 **대체 Orlando 2021년 5월 옵션 선택과 7–10월 선수별 계약·FA 권리·픽·예외 사건**을 날짜별로 연결하는 것이다. 출처가 없는 숫자는 null로 남긴다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16 독립 검수·G17 작가 승인 미완료, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, author/season/exact/manuscript false를 유지한다.
