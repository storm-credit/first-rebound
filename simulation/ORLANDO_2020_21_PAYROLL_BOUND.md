# O-15F14-L Orlando 후반 급여·apron 범위

- 기준 main: `9ed8b288c2d664133efaace05f3bd3f37db3ba51` / PR #163.
- 판정: `LISTED_COMMITMENT_BOUND_NOT_COMPLETE_TEAM_CLEARANCE`.
- 권위: 동명 JSON, `research/ORLANDO_2020_21_PAYROLL_SOURCES.json`; 재현 `tools/build_orlando_2020_21_payroll_bound.py`.
- 범위: 2021-04-12~05-16. 같은 계약·거래 경로를 유지할 때의 누적 계약 부담이며 지급된 현금이나 시즌 전체 정확 장부가 아니다.

공개된 보너스, 앞선 계약 부담, 0~1년차 자유계약 선수의 apron 보정과 캠프 4명의 연간 기본급 전액 시험까지 더하면 최고 **$124,207,255**다. 당시 apron **$138,928,000**까지 **$14,720,745**가 남는다. Hall 5/9의 보고 charge 0을 적용하지 않고도 성립하는 조건부 계산이다. 아직 포함하지 못한 순증 부담 R_ORL이 이 한도 이내여야 한다. 실제 R_ORL과 전체 적법성은 미확정이다. [시즌별 한도표](https://www.salaryswish.com/salary-cap)

## 1. 기존 조건부 일반계약 13명

등록 장부의 13명과 이름을 전량 대조한다. Vučević·Aminu는 승인된 잔류 경로로 남기며 부상·0분을 이유로 계약을 지우지 않는다. 실제 Orlando 명단의 Carter·Porter·Hampton 급여를 추가하지 않는다. Anthony 15순위는 정본 유지이고, Nnaji는 실제 22순위 급여 대신 이미 계산하던 대체 24순위 120%·추가 보너스 없음 조건이다. 아래 공개 금액의 대체세계 이월 자체는 조건부다.

| 선수 | 2020–21 기본급 | 공개 보너스 전액 | 출처/조건 |
|---|---:|---:|---|
| Nikola Vucevic | $26,000,000 | $0 | [급여 이력](https://www.salaryswish.com/players/nikola-vucevic) |
| Al-Farouq Aminu | $9,720,900 | $0 | [급여 이력](https://www.salaryswish.com/players/alfarouq-aminu) |
| Terrence Ross | $13,500,000 | $1,000,000 | [급여 이력](https://www.salaryswish.com/players/terrence-ross) |
| Markelle Fultz | $12,288,697 | $0 | [급여 이력](https://www.salaryswish.com/players/markelle-fultz) |
| Jonathan Isaac | $7,362,566 | $0 | [급여 이력](https://www.salaryswish.com/players/jonathan-isaac) |
| Cole Anthony | $3,285,120 | $0 | [급여 이력](https://www.salaryswish.com/players/cole-anthony) |
| Mo Bamba | $5,969,040 | $0 | [급여 이력](https://www.salaryswish.com/players/mo-bamba) |
| James Ennis III | $3,300,000 | $0 | [급여 이력](https://www.salaryswish.com/players/james-ennisiii) |
| Michael Carter-Williams | $3,300,000 | $0 | [급여 이력](https://www.salaryswish.com/players/michael-carterwilliams) |
| Dwayne Bacon | $1,678,854 | $0 | [급여 이력](https://www.salaryswish.com/players/dwayne-bacon) |
| Chuma Okeke | $3,121,080 | $0 | [급여 이력](https://www.salaryswish.com/players/chuma-okeke) |
| Gary Harris | $19,160,714 | $2,533,333 | 기존 EXECUTION_TERMS 출처 LT_GARY_HARRIS |
| Zeke Nnaji | $2,193,480 | $0 | 기존 대체 24순위·120% 조건 |

기본급 **$110,880,451**, 알려진 보너스 **$3,533,333**. Fultz·Isaac의 다음 시즌 연장 급여, Ennis의 거절한 종전 옵션, Anthony의 2년차 급여를 현재 시즌에 넣지 않는다. Harris의 원자료는 기존 실행 조건 출처를 재사용한다. 명목 기본급은 거래일 발신·수신 charge와 같다고 인증하지 않는다.

## 2. 단기 계약 9건을 누적한다

PR #163의 Orlando 6계약을 읽고, Cannady 4/6 및 Franks 4/12·4/22의 3계약을 연결했다. 날짜는 기존 등록 장부·2020–21 거래 목록과 계약 이력을 대조했다. 보고 보수를 146일 기준으로 재현하며 10일 계약은 등록 해제일로 보수를 깎지 않는다. [Cannady 이력](https://www.salaryswish.com/players/devin-cannady), [Franks 이력](https://www.salaryswish.com/players/robert-franks), [거래 목록](https://www.basketball-reference.com/teams/ORL/2021_transactions.html)

| 계약 ID | 보수 기간 | 일반 최소급여 비용안 | apron 비용안 |
|---|---|---:|---:|
| CANNADY_APR06 | 04-06~04-15 | $61,528 | $110,998 |
| FRANKS_APR12 | 04-12~04-21 | $99,020 | $110,998 |
| HALL_APR13 | 04-13~04-22 | $99,020 | $110,998 |
| FRANKS_APR22 | 04-22~05-01 | $99,020 | $110,998 |
| HALL_APR23 | 04-23~05-02 | $99,020 | $110,998 |
| WAGNER_APR27 | 04-27~05-16 | $221,995 | $221,995 |
| BRAZDEIKIS_MAY02 | 05-02~05-11 | $99,020 | $110,998 |
| HALL_MAY09 | 05-09~05-16 | $79,216 | $88,798 |
| BRAZDEIKIS_MAY12 | 05-12~05-16 | $49,510 | $55,499 |

일반 비용 **$907,349**에 젊은 FA 보정 **$124,931**을 더해 apron 비용 **$1,032,280**이다. 원자료의 보고 cap hit와 이 계산은 같은 필드가 아니다. Cannady는 4/12 등록 해제 뒤 4/15까지, Franks 두 번째 계약은 4/26 해제 뒤 5/1까지, Hall 두 번째 계약은 5/1 해제 뒤 5/2까지 보수를 보존한다. Wagner의 20일 계약은 끝에서 한 번 반올림하므로 $221,995이며, 반올림한 10일 비용 두 배로 바꾸지 않는다.

2017 CBA VII 6(m)(3)은 해당 apron 계산에 모든 성과 보너스와 VII 12(f)(2)의 0~1년차 FA 최소급여 보정을 넣는다. 후자는 같은 보수 기간의 2년차 최저급여와 계약 Salary 중 큰 금액을 쓰며, 정규시즌 중 종료 시 보수에 비례한 조항도 포함한다. 이번 시험은 보장 보수 기간을 유지한 일반 최소급여 경로다. Hall hardship의 별도 0달러 제외 적용까지 검증한 것은 아니다. [CBA, 인쇄 214–216·259–260쪽](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)

## 3. 명단에서 빠진 기존 계약과 예외 이력

| 항목 | 이번 처리 | 경계 |
|---|---|---|
| Birch | 기존 계약 기본급 전액 $3,000,000 예산 | 보고 dead cap $2,586,036의 감액 이익은 미사용. Toronto 새 계약 금액은 미가산 |
| Teague | 이전 1년 최저급여 계약 charge $1,620,564 보존 | 총 보수 $2,564,753 및 Milwaukee 후속 계약을 중복 가산하지 않음 |
| Cannady·Franks·Teske·Dowtin 캠프 | 4명 연간 기본급 전액 합계 $4,140,627을 추가 시험 | 보고 보장액 0을 실제 charge 0으로 잠그지 않음. 전체 미확인 부담 상한도 아님 |
| Mozgov | 보도된 기존 리그 제외 경로가 유지되는 예산 | 2019년 3년 분산분 제외 승인 보도가 있어 분산액을 기계적으로 다시 더하지 않음. 정확 대체 장부는 별도 |
| 투웨이 계약 | 일반계약 급여에 합산하지 않음 | 일반계약 전환/새 계약은 따로 계산. 투웨이 명목 급여를 실제 시즌 현금으로 인증하지 않음 |

[Birch 이력](https://www.salaryswish.com/players/khem-birch), [Teague 이력](https://www.salaryswish.com/players/jeff-teague), [Teske 이력](https://www.salaryswish.com/players/jon-teske), [Dowtin 이력](https://www.salaryswish.com/players/jeff-dowtin), [Mozgov 제외 승인 보도](https://slamonline.com/nba/magic-granted-salary-cap-relief-for-timofey-mozgov/). Cannady·Franks는 앞 절의 이력과 같은 원자료다. 캠프 보수와 뒤의 새 단기 계약은 별도 계약이며 선수 이름이 같다고 한 줄을 삭제하지 않는다.

당시 MLE 사용 목록은 Ennis $3.3m와 Clark $2m, 합계 **$5.3m**이고 Carter-Williams는 **Early Bird**로 설명한다. Clark 이적 후에도 이미 사용한 MLE 기록은 남긴다. 이 기록과 비납세 MLE $9.258m의 단순 차액을 4월 가용 예외로 쓰지 않는다. 일할 감소·다른 사용 이력이 별도로 필요하다. $5.3m라는 금액만으로 실제 hard-cap 발동을 확정하지 않으며, 이번에는 발동 여부와 별개로 apron에 대조했다. [당시 MLE 사용 목록](https://www.hoopsrumors.com/2020/12/how-teams-are-using-202021-mid-level-exceptions.html)

## 4. 계약 체결일별 누적 예산

기본 13명·보너스·Birch/Teague 이전 계약 비용은 이 기간에 계속 포함한다. 단기 계약은 체결된 날부터 해당 계약 전체 보수를 포함하고 기간 종료 뒤에도 누적 부담에서 삭제하지 않는다. 5/12 이후 추가 입력이 없어 5/16까지 같은 최고값이다. 아래 첫 금액에도 캠프 외 잔여 미확인 항목은 포함되지 않았다.

| 기준일 | 열거한 비용 | 캠프 전액 시험 추가 | 추가 후 R_ORL 허용액 |
|---|---:|---:|---:|
| 2021-04-12 | $119,256,344 | $123,396,971 | $15,531,029 |
| 2021-04-13 | $119,367,342 | $123,507,969 | $15,420,031 |
| 2021-04-22 | $119,478,340 | $123,618,967 | $15,309,033 |
| 2021-04-23 | $119,589,338 | $123,729,965 | $15,198,035 |
| 2021-04-27 | $119,811,333 | $123,951,960 | $14,976,040 |
| 2021-05-02 | $119,922,331 | $124,062,958 | $14,865,042 |
| 2021-05-09 | $120,011,129 | $124,151,756 | $14,776,244 |
| 2021-05-12 | $120,066,628 | $124,207,255 | $14,720,745 |

`실제 apron 비용 ≤ 시험 예산 + R_ORL`이라는 이월 조건 아래 `R_ORL ≤ $14,720,745`이면 이번 기간의 한도 시험은 통과한다. R_ORL은 시험 예산에 아직 반영하지 않은 순증 조정의 한도 변수이며, 실제값은 `null`이다. 캠프 실제 비용이 시험액보다 작을 경우 그 차액을 다른 항목에 다시 쓸 수 있다고 미리 채택하지 않는다.

## 5. 닫힌 조사 범위와 남은 필드

이번에 회수한 범위는 ORL 13명 기본급·공개 보너스, 앞선 3단기 계약, Birch/Teague 보고 잔액과 전액 예산, 캠프 4건, MLE 사용 이력 및 해당 apron 보정이다. 이 값들의 재검색은 다음 단계의 선행 요건이 아니다. 잘못된 선수 URL이 반환한 공통 일반 페이지와 일반 급여 페이지로 이동한 archive 요청은 출처에서 제외했다.

정확한 팀 장부를 닫으려면 남은 이전 계약 조정·Exhibit 10 지급·대체 계약 비율/보너스·RFA 제안 및 1R Required Tender 등의 적용 필드를 확인해야 한다. CBA 6(m)(3)이 일반 FA 보류액·미사용 예외 보류액·빈자리 보류액 등을 제외하더라도 RFA 제안과 Required Tender 같은 예외는 남으므로, 모든 과거 권리를 0으로 처리하지 않는다. 이 정의는 **Chicago 거래 6(j) 비납세 검사로 옮겨 쓰지 않는다**. 그 원장의 R과 $5,609,972 한도는 별도다.

계약 비용 여유는 Hall 추가 1자리 5경기(5/9·11·13·14·16)의 허가가 아니다. `alternate_hardship_approved=false`, 실제 apron 적합성 `null`, 완전 항목 목록 검증 `false`다. 이전 3/25 거래·시즌 초 한도와 Boston/Denver 원장은 이번 기간 검사에 포함하지 않았다.

F4의 다음 순서는 Boston/Denver 후반 계약을 각각 승인된 명단과 누적 비용에 연결하고, 이 ORL의 잔여 필드와 함께 채택 준비 패킷에 반영하는 것이다. F1~F3/F5의 기존 정확 charge·픽 의무는 그대로 남는다. A1~A3 사건 선택 전에 필요한 사실을 작가의 임의 숫자로 채우지 않는다.

신규 5개·기존 등록 비용 5개 검사, JSON 재현·diff 검사 PASS. 자체검토 `NOT_INDEPENDENT`. 네 K 조건 묶음 전체 종료 0, K1/L2 미채택, `author_locked=false`, `season_selected=false`, `PROJECT_FREEZE v0.30 PARTIAL`·설계/원고 `CLOSED` 유지. 진행 중 포함 남은 큰 작업 6개.
