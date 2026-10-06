# Denver–Lakers 6경기 날짜별 감독 작업 계획

2026-10-07 / 기준 main `76cd80b` / **DATED_AUTHOR_MODELED_COACH_PLAN_APPLIED_6_GAMES**.

[기존 위임](../canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json) 안에서 [승인된 시리즈 가용 모델·승자](DEN_LAL_2021_DELEGATED_SERIES.json)와 날짜 후보를 실제 감독 **작업 계획**으로 적용했다. [실행 JSON](DEN_LAL_2021_DATED_COACH_PLAN.json), [생성·검문기](../tools/build_den_lal_dated_coach_plan.py), [원자료·명단 연결](../research/DEN_LAL_2021_COACH_PLAN_SOURCE_BRIDGE.json).

## 적용한 여섯 경기

| 경기 | 채택한 모델 날짜 | 홈 | 기존 선택 승자 | 모델 경기 시간 | 각 팀 예정 분 |
|---|---|---|---|---|---|
| 1 | 2021-05-22 | DEN | DEN | 48분 | 240분 |
| 2 | 2021-05-24 | DEN | LAL | 48분 | 240분 |
| 3 | 2021-05-27 | LAL | LAL | 48분 | 240분 |
| 4 | 2021-05-29 | LAL | DEN | 48분 | 240분 |
| 5 | 2021-06-01 | DEN | LAL | 48분 | 240분 |
| 6 | 2021-06-03 | LAL | LAL | 48분 | 240분 |

원역사 DEN–POR 날짜 골격을 대체세계 작업 날짜로 채택했다. 앞선 날짜 후보 파일은 생성 당시 기록으로 보존한다. 새 계획의 권위는 이 파일과 JSON이다. 전체 15시리즈/88경기의 날짜 확정이나 실제 구장 예약·이동 시간 인증은 아니다. 원역사 G5의 2OT를 복사하지 않고 이 작업 계획의 여섯 경기는 정규시간 종료로 명시했다.

각 경기에는 기존 8개 6분 블록을 작업 감독 계획으로 적용했다. 동일 계획의 반복은 실제 여섯 경기에서 교체·부하가 같았다는 관측 주장이 아니다. 승자는 기존 선택을 유지하며 분배로 승리를 예측했다는 주장도 하지 않는다. 각 팀 시리즈 예정 총분1,440, James/Davis/Jokic/Porter 각각216분이다. 정확 득점·포제션·개인 박스는 null이며 다음 전술 설계에서 변경되는 계획은 재검산한다.

## 명단·건강·미출전 구분

- DEN은 앞선 두 Clark 날짜 분기의 같은 5/16 일반15·TW2 명단을 보존했다. Bey22/Hartenstein 잔류, Nnaji24 ORL 이동, McGee 미취득을 검사한다. Howard는 **TW**로 유지한다.
- LAL은 NBA 작성 12/22 원명단 PDF2의 일반14·TW2에 공개 사건5개를 연결했다. Cook 방출, Jones 두10일 만료, Drummond/McLemore 잔여시즌 계약으로 일반15·TW2가 된다.
- 고정한 NBA 공개 feed9,927행에서 두 팀5/17~6/3 18일의 관련 사건은0이다. 이는 유한 공개 사건 연결이다. 비공개 거래의 전역 부재나 실제 활동명단 제출을 인증하지 않는다.
- [Shams의 3/11 직접 원보도](https://twitter.com/ShamsCharania/status/1370149027786932228)를 공식 oEmbed에서 회수해 당시 TW의 플레이오프 가용 변경을 연결했다. 원 개정 합의서 전체나 2022/2026 규칙의 인증은 아니다. Howard의 계약 전환·추가 일반 자리·급여를 만들지 않는다. 원5/22 공식 gamebook 요청은 ReadTimeout으로 본문 미회수다.
- DEN의 Murray/Barton/Dozier 결장은 기존 시리즈 작가 모델이다. James/Davis 등의 가용 모델도 기존 선택이며 의료 사실로 승격하지 않는다. 원 Phoenix의 Davis 부상과 Cleveland의 Hartenstein 부상은 가져오지 않는다.
- Millsap/Cančar/Bol/Harrison, LAL Harrell/Dudley/McKinnie/McLemore/Cacok/Antetokounmpo 등 비rotation 선수는 계획0분·건강null이다. 미출전은 부상 결장이나 활동명단 제외와 다르다.

## 실제 검문과 계수

6날짜·48공통 시계 블록·204전체 명단 칸을 적용했다. 각 블록 고유5명, 48분 연결, 팀240분과 선수 합계, 시리즈1,440분, 기존 선수 방향·승자를 검사한다. `--check --self-test`는 결장 선수 투입, McGee 재삽입, 잘못된 별칭/명단, 중복 날짜, 시계 공백, 예비0분의 의료 승격, 시즌 승격을 거부한다.

이는 국소 감독 **설계 실행** 진도다. 실제 활동명단·의료 인증·법적 등록·전체 A1/A2/A3·K·시즌/G16/원고 완료는 각각 false/HOLD다. 전체88개 중 다른82경기의 감독·건강 적용은 이 문서가 완료하지 않았다. freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.
