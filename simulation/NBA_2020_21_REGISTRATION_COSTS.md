# O-15F14-L — 후반기 5명·9계약의 등록 비용

- 기준: PR #162, main `9bbcf7138ca86325f19ad4c85096bc0d7f663ead`, 2026-09-12.
- 판정: **PUBLIC_PAY_REPRODUCTION_PASS / TEAM_LIMITS_AND_HARDSHIP_HOLD**.
- 수치 권위: 동명 JSON. 출처 권위: `research/NBA_2020_21_REGISTRATION_COST_SOURCES.json`.
- 공개 계약 이력과 조건부 계산이다. `author_locked=false`, `season_selected=false`, v0.30 PARTIAL·설계/원고 CLOSED 유지.

## 1. 이번에 채운 금액

SalarySwish의 선수별 과거 계약 본문 5건을 확보했다. 현재 선수 요약의 서비스 연수를 소급하지 않고, 2020–21 진입 연수별 최저급여와 해당 계약의 급여를 대조했다. 금액은 2차 장부의 보고값이며 구단 공지가 공개한 계약서 금액이 아니다. 기존 공식 공지의 날짜·유형은 출처 ID로 연결한다.

| 선수 / 팀 | 계약 시작 | 이 시즌 보수 대상 일수 | 보고 급여 | 보고 cap hit | 보전 전제 |
|---|---|---:|---:|---:|---|
| Hall / ORL | 4/13 | 10 | $99,020 | $99,020 | 진입 1년 |
| Hall / ORL | 4/23 | 10 | $99,020 | $99,020 | 5/2 등록 해제와 보수 종료를 구분 |
| Hall / ORL | 5/9 | 8 | $79,216 | $0 | 당시 별도 제외 근거 미확보 |
| Wagner / ORL | 4/27 | 20 | $221,995 | $221,995 | 진입 2년 |
| Parker / BOS | 4/16 | 31 | $430,729 | $430,729 | **2년 계약**, 1년 계약 보전 미적용 |
| Rivers / DEN | 4/20 | 10 | $158,907 | $110,998 | 진입 8년, 1년 계약 보전 |
| Rivers / DEN | 4/30 | 17 | $270,142 | $188,696 | 같은 보전 규칙 |
| Brazdeikis / ORL | 5/2 | 10 | $99,020 | $99,020 | 진입 1년 |
| Brazdeikis / ORL | 5/12 | 5 | $49,510 | $49,510 | 같은 최저급여 |

각 행은 [Hall](https://www.salaryswish.com/players/donta-hall), [Wagner](https://www.salaryswish.com/players/moritz-wagner), [Parker](https://www.salaryswish.com/players/jabari-parker), [Rivers](https://www.salaryswish.com/players/austin-rivers), [Brazdeikis](https://www.salaryswish.com/players/ignas-brazdeikis)의 해당 시즌 계약 항목을 사용한다. 뒤 시즌 급여·보장 전환은 이번에 채택하지 않는다.

## 2. 일수와 보전 계산

[NBA 시즌 공지](https://official.nba.com/nba-announces-structure-and-format-for-2020-21-season/)의 12/22~5/16을 양끝 포함하면 146일이다. [당시 최저급여 표](https://www.hoopsrumors.com/2020/11/nba-minimum-salaries-for-202021.html)의 진입 1·2·6·8년 금액 $1,445,697 / $1,620,564 / $2,028,594 / $2,320,044를 사용했다. [당시 10일 계약 설명](https://www.hoopsrumors.com/2021/04/salaries-for-10-day-contracts-in-202021.html)도 146일 분모와 일치한다.

`연간 최저급여 × 계약 보수 대상 일수 ÷ 146`을 계약별 마지막 단계에서 달러 반올림했다. 10일 금액을 먼저 반올림한 뒤 두 배 하면 Wagner의 20일 금액과 $1 차이가 생기므로 그렇게 계산하지 않는다. 9개 급여 보고값의 재현 불일치는 0이다.

[2017 CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) I §1(ll), IV §6(g), VII §3(f)를 연결했다. 보전 대상인 Rivers는 진입 2년 최저급여의 같은 기간분을 팀 charge로 계산한다. Parker의 계약은 다음 시즌까지 포함하므로 해당 감액을 적용하지 않는다. II §9(e)의 계약 종료 처리와 공식 Hall 해제 공지를 함께 읽어, 등록 마지막 날을 계약 보수 일수로 바꾸지 않았다. 이 규칙은 Hall의 추가 등록 자리나 특별 급여 제외를 승인하지 않는다.

Hall 4/23 계약의 명목 10일은 5/2까지이고 공식 해제 사건은 5/2다. 따라서 기존 등록 장부의 5/1 종료 및 K의 5/2~5/8 0분을 유지하면서 10일치 보수는 보존한다. 종료 시각과 출전 가능성을 급여 표 하나로 뒤집지 않는다.

## 3. Hall 0달러를 쓰지 않는 비용안

Hall 5/9 계약의 공개 장부는 급여 $79,216와 cap hit $0을 따로 기재한다. 기존 `L_HALL` 구단 공지는 hardship 사용을 확인하지만 금액과 급여 제외 근거를 공개하지 않는다. 2021–22 이후 규정을 이전 시즌에 소급하지 않았으며, 이번에도 **실제 적용 조항과 대체세계 적용은 미확정**이다.

후속 팀 한도 검사에는 이 행을 일반 최저급여 $79,216로 전액 넣는 비용안을 준비했다. 이는 해당 계약 형식 아래의 예산이며, 알 수 없는 모든 추가 부담의 법적 상한이나 작가가 채택한 금액은 아니다. 팀 한도가 이 비용안에서도 성립하면, cap hit 0 여부에 의존하지 않는 금액 검증이 가능하다. 그래도 Hall의 추가 자리 허가는 별도로 필요하다.

| 이번 목록만의 소계 | 보고 급여 합계 | 보고 cap hit 합계 | Hall 전액 반영·일반 보전 적용 비용안 |
|---|---:|---:|---:|
| ORL | $647,781 | $568,565 | $647,781 |
| BOS | $430,729 | $430,729 | $430,729 |
| DEN | $429,049 | $299,694 | $299,694 |

**이 표는 세 팀의 전체 급여 원장이 아니다.** 이전 계약의 방출 잔액·상계, Cannady/Franks 등 앞선 단기 계약, 예외 사용 이력과 apron 한도는 포함하지 않는다. 특히 Wagner의 새 ORL 계약을 BOS의 기존 보장급 삭제 근거로 사용하지 않는다. 같은 소계를 기존 전체 급여에 무조건 더해 이중 계산하지 않는다.

## 4. 종료 패킷에 넘기는 결과

F4의 5명·9계약 공개 금액과 일할 산술은 회수했다. 다음 F4 작업은 **ORL/BOS/DEN 팀별 누적 장부와 한도**이며, 이 9개 금액을 다시 수집하지 않는다. Hall의 기존 5경기 추가 1자리 조건과 A2 승인 사건은 유지한다. 정확 대체세계 charge와 팀 한도 통과는 아직 false/null이다. F1 Chicago R, F2/F3/F5 거래·픽 의무, A1/A3 및 추첨은 이 계산으로 닫히지 않는다.

신규 5개·기존 등록 6개 검증, JSON 재현·diff 검사 PASS. 날짜·계약 길이·서비스 연수 오입력, 조기 해제 시 보수 누락, 반올림 순서, 보고값 0의 승인 승격을 점검했다. 자체검토 `NOT_INDEPENDENT`; 네 K 조건 묶음 전체 종료 0, 진행 중 포함 남은 큰 작업 6개.


## Orlando 누적 한도 후속

[ORLANDO_2020_21_PAYROLL_BOUND.md](ORLANDO_2020_21_PAYROLL_BOUND.md)에서 이 문서의 ORL 6계약을 앞선 Cannady/Franks 3계약 및 13명 기본급에 연결했다. 그 문서의 apron 보정은 여기의 일반 최소급여 비용을 덮어쓰지 않는다. Hall 0달러 적용·정확 전체 장부·등록 허가는 미확정이며 BOS/DEN 누적 계산도 별도다.
