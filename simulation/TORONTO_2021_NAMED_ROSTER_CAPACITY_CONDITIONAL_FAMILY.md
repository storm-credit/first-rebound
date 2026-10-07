# Toronto 명명 조건부 정규 capacity 함수

REVIEW_PENDING_FINITE_FOUR_CAPACITIES_NOT_DATED_EXECUTION

T0/T1의 중요한 Lowry 경로·계약가격은 미선택이며 두 경로의 Siakam 가용/비가용을 각각 조건부 입력으로 받는다. 양수 선수의 이 경기 작업 가용을 구성하되 실제 임상/전체 시즌 건강으로 읽지 않는다.

| 경로 | 가용 조건 | 양수 인원 | 명목 active/inactive | 팀분 |
|---|---|---:|---|---:|
| T0 | SIAKAM_AVAILABLE | 11 | 12/3 STD + TW 미호명 | 240 |
| T0 | SIAKAM_UNAVAILABLE | 10 | 12/3 STD + TW 미호명 | 240 |
| T1 | SIAKAM_AVAILABLE | 11 | 12/3 STD + TW 미호명 | 240 |
| T1 | SIAKAM_UNAVAILABLE | 10 | 12/3 STD + TW 미호명 | 240 |

## 선택한 국소 코칭 방법

12개의 240초 창을 순서대로 배열한다. PG/SG/SF/PF/C는 이 모델의 역할 배정이며 NBA 공식 포지션 인증이 아니다. 창마다 다섯 명·creator 한 명을 포함하고 각 역할48분/선수≤48분을 보존한다. T0는 Lowry/Fred/Giddey, T1은 Fred/Dragic/Giddey가 주 생성자다. Powell은 유지된 가드 득점 역할이며, Siakam 비가용일 때 Boucher/Yuta의 PF 몫으로 재배정한다. 새로운 기술 성공/효율/득점/승패는 없다.

12명 작업 active는 양수 인원 전부+명단순 0분 filler로 구성하며 3명 standard inactive와 완전 분할한다. TW 두 명은 NBA active/inactive 어느 쪽에도 올리지 않고 이 함수의 regular active 사용0을 기록한다. 0분·inactive의 의료 상태는 null. TW를 새로 투입하려면 독립 명목 호명·50경기 누적·XXIX inactive조정을 다시 적용해야 한다.

## 역사와 가상 선택 경계

[Siakam 공식 발표](https://www.nba.com/news/raptors-pascal-siakam-undergoes-shoulder-surgery)는 접촉 기원의 수술/회복 전망만 지지한다. 가용 두 값은 수정 세계의 조건부 입력이며 원접촉·수술·개막 결장을 자동 복사하지 않는다. [Giddey 공식 프로필](https://www.nba.com/draft/2021/prospects/josh-giddey)의 역할은 분배자 배정 근거이고 #8 TOR·성공을 지지하지 않는다. Powell의 가드 분류는 NBA에 실린 AP 보도 검색 관측이며 실제 원거래는 적용하지 않는다. 다른 세부 역할/분은 명명된 일상 가상 코칭 설계다. TORGSW gamebook 직접20초 시도1회 timeout/본문0/재시도0를 실패로 기록한다.

## 입력과 미완료

동결 이름은행의 T0/T1 정확15STD2TW·DB1·Bonga0YOS·법적 수단 목록을 source-bound caller에서 대조한다. 살아 있는 은행의 양도/서명/방출 조건과 전체비용HOLD는 그대로다. 가용 모형이 법적 계약을 대신하지 않는다. target0022100046/10-25는 원일정 참조키이며 해당 날짜의 거래/임상/실제 출장 또는 결과를 선택하지 않는다. 2020–21분 이월0·OT 자동이월0.

함수 API `TOR_NAMED_ROSTER_CAPACITY_CONDITIONAL_FAMILY(path, availability_parameter, root)`는 하나의 source-bound 국소 row를 반환한다. 27missing→26missing은 독립수용/공통dispatcher 통합 뒤의 예상 감소이며 이번 파일이 중앙 dispatcher를 변경하지 않는다. 전체 전시즌 적용도 미완료다.

## 진행표

| 묶음 | 상태 |
|---|---|
| 1 | 완료 |
| 2 | S2 완료 |
| 3 | TOR 조건부 함수1 신규·경제/중요 경로 미선택 |
| 4 | 선행 결과 의존 |
| 5 | 전체 미완료 |
| 6 | Pack0·미완료 |
| 7 | 최종 미완료 |

미완료5 / 6번까지4. PARTIAL/CLOSED·원고0.
