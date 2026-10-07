# 2020–21 전체 날짜별 등록 실행 연결 감사

**전체 일정은 연결했으며 명단 실행 공백은 HOLD다.** 원NBA 등록 인증·새 재정 선택·최종시즌 확정이 아니다.

- 기존1174경기/2348팀/30팀 분·승패·건강 입력을 참조한다. 벡터나 결과 재계산0.
- 개막 원PDF4쪽+고정NBA 이동 feed의 선수 사건281개, 명단상태374개와 기존 승인 원본문 해제 보완3건을 재현했다.
- 기존 양수분 선수 소속이 포함되는 팀경기2348, 빠지는 팀경기0.
- 소속 포함은 금융·수락·정확 리그접수 증명이 아니다. 명단 초과/변경 경로가 남으면 실행 완료로 세지 않는다. 원feed 날짜만으로 임시 초과나 hardship를 실제위법으로 판정하지 않는다.
- 승인 드래프트 착지와F1–F5 변경만 적용했다. Bonga/Homesley/Hutchison/Riller를 임의삭제하거나 계약하지 않는다.

| 남은 유한 관측 | 관측수 | 최초 | 마지막 |
|---|---:|---|---|
| STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION:CHA: | 29 | 2021-03-26 | 2021-05-16 |
| STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION:CLE: | 4 | 2021-01-11 | 2021-01-20 |
| STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION:HOU: | 6 | 2021-05-07 | 2021-05-16 |
| STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION:SAC: | 1 | 2021-03-25 | 2021-03-25 |
| STANDARD_COUNT_ABOVE15_NO_POSITIVE_EXCEPTION:WAS: | 58 | 2020-12-23 | 2021-05-18 |
| GSW_HUTCHISON_OPERATION_UNSELECTED | — | — | — |
| WAS_BONGA_RIGHTS_TO_STANDARD_UNSELECTED | — | — | — |
| WAS_HOMESLEY_SIGNING_UNSELECTED | — | — | — |
| CHA_RILLER_UDFA_CONTRACT_CARRY_UNSELECTED | — | — | — |

## 자료·모델·미인증 구분

개막명단의 inactive 비별표 선수는 standard이며 별표 선수만 two-way다. 실제 보장 급여는 이 파일에서 선택하지 않는다.
원feed의00:00은 시각증거가 아니다. 같은 날짜 사건을 해당 작업 경기 전 적용하는 후보를 명시하여, 양수분과 충돌한 날짜를 감춘 채 실제 소속으로 인증하지 않는다.
ORL/CLE/DEN의 이미 검문된 등록 증인을 재구성하고 원feed에 빠진 ORL 조기해제3건을 보존했다. 사건일 당일 해제를 취득보다 앞에 두는 작업 순서다. 그 밖의10일계약은 2017 CBA II9(a), PDF69/인쇄47의10일 또는3경기 중 긴 기간으로 잠정 끝을 계산했다. 2020수정 적용성·실제 시작시각은 미인증이며 그 한계를 exact 등록 완료로 승격하지 않는다.
양수분은 기존 위임 건강·코치 모델이고 예비0분의 의료 상태는null이다. 방출·만료는 선수 자리만 제거하며 급여잔액0이라는 뜻이 아니다.
가상 사건을 보존할 수 있다는 인과 모형과 실제 계약·당일 접수의 사실 인증을 구별한다. 모든 비공개 해제부재나 실제 의료기록을 새필수조건으로 요구하지 않는다.

## 확인된 명명 예외와 작업 적용

Memphis 구단 2022–23 가이드 PDF136/인쇄134는 Tim Frazier의2021-01-04 hardship 계약과1/14만료를 직접 명시한다. 당시 구단1/4원발표의보존본문도읽었다. 이명명된2021예외를작업family로보존해해당5경기일의일반16명을단순위법/미공표부재게이트로취급하지않는다. 원실제의료조건·리그접수·예비0진단인증은false다.

## 다음 실제 실행

named_gaps의 각 선수/날짜에 이미 존재하는 구단 원문·계약기간·승인델타를 연결한다. 공백은 새 임의계약으로 채우지 않고 원자료의 누락/날짜 차이와 미선택 대체 경로를 구분한다.
전체membership와자리/법적family 실행이 검문된 뒤 S2 closing_witness를 별도 판정한다. 이번파일A/K·원장·시즌승격0, v0.30 PARTIAL·설계/원고 CLOSED·원고0.

[기계 입력](NBA_2020_21_DATED_ROSTER_EXECUTION_BRIDGE.json)
