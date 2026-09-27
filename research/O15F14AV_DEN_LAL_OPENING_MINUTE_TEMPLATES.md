# O-15F14-AV — Denver–Lakers 조건부 대진의 원역사 개막 분 비교

- 판정: `TWO_HISTORICAL_240_MINUTE_COMPARATORS_RECONCILED / SERIES_EXECUTION_HOLD`.
- [기계 검문 JSON](../simulation/CHICAGO_2020_21_DEN_LAL_OPENING_MINUTE_TEMPLATES.json) · [검문 도구](../tools/check_chicago_2020_21_den_lal_opening_templates.py).
- 적용 대진은 [K1/F038+L2의 조건부 Denver 3번–Lakers 6번](../simulation/CHICAGO_2020_21_K1_L2_BRACKET_BRIDGE.md)이다. K1과 L2 모두 최종 작가 선택 전이므로 이 표의 시리즈도 정본이 아니다.

## 1. 원역사 두 팀의 별도 경기책

| 팀·출처 | 240분에 들어간 실명 | 빠진 실명/주의 |
|---|---|---|
| Denver 홈: [2021-05-22 Portland @ Denver 공식 최종 경기책](https://statsdmz.nba.com/pdfs/20210522/20210522_PORDEN_book.pdf) | Porter Jr. `37:26`, Gordon `28:19`, Jokić `35:22`, Rivers `33:05`, Campazzo `31:32`, Morris `21:59`, Green `17:37`, Howard `19:58`, Millsap `14:42` | 원역사 McGee·Nnaji **감독 선택 DNP**. Murray ACL 수술, Barton·Dozier 부상 inactive. 선택된 거래 생략/선수 이동에서는 McGee·Nnaji가 Denver 명단에 없고 Hartenstein·Bey가 남는다. |
| Lakers 원정: [2021-05-23 Lakers @ Phoenix 공식 최종 경기책](https://statsdmz.nba.com/pdfs/20210523/20210523_LALPHX_book.pdf) | James `36:04`, Davis `38:48`, Drummond `19:05`, Caldwell-Pope `34:56`, Schröder `34:08`, Kuzma `19:24`, Harrell `14:38`, Caruso `24:07`, Horton-Tucker `7:05`, Matthews `11:45` | **Gasol은 감독 선택 DNP**였다. 기존 [AU 비교표](O15F14AU_DENVER_LAKERS_PLAYOFF_COMPARATOR.md)의 `Gasol 7:05`는 선수 행을 잘못 읽은 것으로 정정했다. |

**원자료/산술:** 두 PDF의 첫 장을 직접 시각 판독했다. SHA-256은 각각 `23362aa3f7b3332e543ea28d25e9aff54d5ddb89d97a29801e71f4e829bc10d1`, `f6dea38257ed7d83ea210d1f1e87a7734c38c08dc01eed8c574deed0f81d60ca`이며 이전 [AU 검수](../reviews/R01_O15F14AU_DEN_LAL_BASELINE_REBUTTAL.md)의 회수본과 일치한다. JSON의 실명 분 합계는 **팀마다 240:00**이다. PDF 텍스트 추출은 선수 이름과 오른쪽 분 열을 별도 순서로 반환할 수 있어 인접 텍스트만 이어 읽으면 Gasol/Horton-Tucker를 뒤바꾼다. 이 건은 렌더링한 첫 장의 같은 행을 판독했다.

## 2. 대체 세계로 옮길 수 있는 범위

**관측 비교:** 두 원역사 경기는 모두 연장 없이 끝났고 공식 최종 경기책의 각 팀 합계는 **개별 240:00**이다. Denver의 원역사 출전자 9명에는 확정된 이탈 선수 McGee·Nnaji가 없으므로, 이름 수준의 충돌은 없다. 이것은 대체 세계의 9인 분을 그대로 복사하거나 잔류 Hartenstein·Bey를 0분으로 선택할 근거가 아니다. Lakers의 Phoenix 상대 5/23 분도 Denver 상대 코치 선택으로 승격하지 않는다. 특히 Jokić를 상대할 때 Gasol DNP가 유지된다는 근거는 없다.

**새로 드러난 검문:** 원래 AU의 `Gasol 7:05`를 그대로 쓰면 Lakers의 센터 로테이션·240분 원장에 실명 오류가 난다. 수정된 관측은 Drummond `19:05`와 Harrell `14:38` 출전, Gasol DNP다. 나머지 센터 역할 시간을 Davis 또는 다른 선수에게 자동 할당할 수 없다. 양 팀이 서로 다른 상대와 다른 날짜에 뛴 경기책이므로 **서로 맞물리는 5대5 시간축, 매치업별 포제션/득점, Game 1 날짜, 4~7경기 승패를 검증하지 않는다**.

**다음 입력:** 첫 경기 후보의 건강·등록 달력을 날짜별로 정하고, Denver의 Hartenstein/Bey 사용 여부와 Lakers의 Gasol/Drummond/Harrell·Davis 센터 기용을 명시한 뒤 같은 경기 시계의 5인조·팀 분·포제션을 검산한다. 연장 가능성을 배제하기 전에는 대체 경기 팀 분을 240:00으로 고정하지 않는다. 이후 Phoenix–Portland 승자와 다음 라운드 파급을 연결한다. 역사적 두 박스를 한 가상 경기의 실제 통계로 합치지 않는다.

F5·A1/A3·K_METHOD_EVENTS `HOLD`, F1~F5 `0/5`·A1~A3 `0/3`·네 K `0/4`; 7행 1완료·1진행·5대기/미완료 6개. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 원고 금지.

[Claude 제한 논리 반증과 처분](../reviews/R01_O15F14AV_DEN_LAL_OPENING_MINUTE_REBUTTAL.md)은 원역사 분을 대체 경기 후보로 오인할 위험을 수용했고, PDF를 보지 않은 상태에서 제기한 원역사 연장 가능성은 공식 4쿼터 최종 경기책으로 기각했다.
