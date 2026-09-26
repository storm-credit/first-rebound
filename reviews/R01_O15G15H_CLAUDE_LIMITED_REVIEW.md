# R01 — O-15G15H Claude 제한 반증 검토

- 대상: [G15H 날짜별 자리 증명](../research/O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)과 G15B/G15E/G15G의 불변 전제. Anti-Gravity CLI의 `claude-sonnet-4-6` 모델을 **읽기 전용**으로 호출했다. 이 검토는 G16 전체 독립 검수나 source-blind 편집 검수가 아니다.
- 넓은 반증 요청은 `--print-timeout 100s`에 도달해 **부분 출력**만 남겼다. 이를 완료된 독립 검수로 세지 않는다. 후속 좁은 요청은 G15H 단일 문서의 인원·날짜 산술을 검토하고 종료했으며 `확실한 산술 오류 NONE`을 반환했다. 원자료를 새로 독립 수집한 검수는 아니다.

## 수용한 지적

1. 원역사 부상 `Out` 이월이 표의 `15/15` 계약 자리와 혼동될 수 있었다. G15H의 열을 **계약 자리 가정**으로 명시하고 M0(이월 없음)·M6(겹치는 6명 이월) 의료 분기를 따로 적었다. 두 의료 분기 모두 15 표준/2 투웨이 **계약 수**는 그대로다.
2. 양수 분 집합의 이름 포함이 실제 서명·등록으로 읽힐 여지가 있었다. G15H는 `서명·보유를 가정한 문자열 집합`이라고 명시하고 Gravett의 새 계약 실패 시 O15C 분 증명이 실행 불가임을 적었다.

## 기각하거나 보류한 지적

| 지적 | 판정 | 이유 |
|---|---|---|
| 원역사 Aminu가 3/25 Chicago로 갔으므로 대체세계 10/16 Orlando 후보에 있을 수 없음 | `REJECT` | [T2 방향 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)은 원역사 Chicago의 Vučević·Aminu 거래를 실행하지 않고 Vučević의 2020–21 Orlando 잔류를 선택한다. 원역사와 대체세계의 거래 상태를 섞은 공격이다. Aminu의 이후 경로는 여전히 HOLD다. |
| 1/23 `15/15` 계약 수가 원역사 `Out` 이월에 의존함 | `REJECT_WITH_CLARIFICATION` | 계약 수와 의료는 서로 다른 변수다. M0/M6 표기로 구분했다. |
| Mobley·Herbert가 아직 실제 Orlando 지명/계약이 아니므로 조건부 집합에 넣을 수 없음 | `REJECT_AS_ARITHMETIC / HOLD_AS_EXECUTION` | 가정 집합에는 넣어 수량을 계산할 수 있지만 실제 지명·서명·활동 여부는 미검증이다. 원본 JSON `registration_cleared=false` 유지. |
| 부상 보고서 표제가 `05:30 PM`인지 재확인 필요 | `RESOLVED` | [공식 PDF](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_05PM.pdf) 첫 쪽 표제는 `01/23/22 05:30 PM`이다. NotebookLM의 `05:00 PM` 병기만 오류였다. |
| 10/16 표준 14명 예시의 최소 명단 적법성 | `HOLD` | NBA의 [2017 CBA 요약](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)은 일반적으로 14/15명을 허용하나 리그 평균에 따른 15명 최소치 발동 조건이 있다. 2021–22 적용 여부·정확 시점은 미검증. G15H의 15→15 순서 예시는 이 문제를 회피하는 수량 대조일 뿐 실제 거래가 아니다. |

**종료:** 이름 집합·날짜·상한의 확실한 산술 오류는 찾지 못했다. 계약·픽·급여·의료·PG 수행·G16/G17은 열려 있다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`를 유지한다.
