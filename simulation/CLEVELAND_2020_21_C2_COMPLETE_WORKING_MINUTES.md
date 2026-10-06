# Cleveland C2 — 5경기 완전 분 벡터와 작업 교체 구간

2026-10-07 / 기준 main `94a672bd`. [기계 입력](CLEVELAND_2020_21_C2_COMPLETE_WORKING_MINUTES.json), [생성·검문기](../tools/build_cleveland_c2_complete_working_minutes.py).

[Varejão 복귀 계약 생략](../canon/CLEVELAND_2021_VAREJAO_C2_DECISION.json)과 [McGee 거래 생략](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)은 이미 승인됐다. 이 파일은 [기존 건강·시즌 설계 위임](../canon/DELEGATED_HEALTH_SEASON_STYLE_DECISION_2026_10_02.json) 아래 유지된 McGee의 양의 출전분과 감독 구간을 작업 모델로 선택한다. 실제 등록·의료·경기 결과의 인증은 아니다. 전체 명단을 제공하는 파일도 아니다.

## 완전 치환 입력

| event_id | Varejão 제거(초) | 원역사 Hartenstein 제거(초) | McGee 작업 출전(초) | 5인조 구간 수 |
|---|---:|---:|---:|---:|
| 2021-05-05_CLE_POR | 397 | 770 | 1167 | 12 |
| 2021-05-07_DAL_CLE | 277 | 755 | 1032 | 11 |
| 2021-05-09_CLE_DAL | 983 | 0 | 983 | 11 |
| 2021-05-12_CLE_BOS | 192 | 0 | 192 | 10 |
| 2021-05-14_WAS_CLE | 307 | 0 | 307 | 11 |
| 합계 | 2156 | 1525 | 3681 | 55 |

`rows`의 `(event_id, team)`으로 연결하며 단위는 **초**다. `alternate_seconds`는 팀 전체 양의 출전 선수 벡터다. 기존 `NBA_2020_21_FINAL859_MINUTES.json`의 `OBSERVED_HELD` Cleveland 벡터에서 Varejão와 Hartenstein을 모두 지우고 둘의 초 합계를 McGee에게 **한 번** 준다. `delta_seconds`는 같은 경기의 원역사 `actual_seconds`에 대한 최종 차이이며 이전 F5 차이를 다시 더하지 않는다.

5월 5일·7일은 기존 F5 Cleveland 치환까지 포함한 완성 벡터다. 전체 모델 적용 때 이 C2 행이 이전 F5 행을 대체해야 한다. 770초와 755초를 또 더하면 중복이다. 나머지 세 경기는 기존 F5 양의 Hartenstein 분 화면에 없던 새 치환이다. 5월 4일·10일·16일 등 Varejão가 양의 분을 기록하지 않은 날짜의 전체 명단·계약 생략은 별도 등록 입력의 영역이다.

## 시간·선수·모델 검문

원자료의 다섯 경기 clock은 각각 2880초이며 각 벡터 합계는14400선수초다. 선언된 Cleveland 역할군 아래 LP를 풀어 실명5명씩의 공통 시간 증인을 저장했다. 기존 F5 Cleveland14행의 저장 증인도 원분 벡터를 Hartenstein→McGee로 바꾼 전체 벡터와 대조했다. 기존 평점·승패·시즌 화면을 다시 실행하거나 변경하지 않았다.

`lineup_witness`는 분 충족 증인이다. `ordered_working_stints`는 선발5명 구간을 먼저 두고 나머지를 안정된 이름 순으로 배치한 **새 감독 작업 선택**이며, 실제 교체 순서의 복원이 아니다. 시작0→종료2880초, 선발 구간180초 이상, 선수별 분과5인조 동시성 합계를 검문한다. 실제 효율·포제션·득점·상대팀 구간은 미인증이다.

McGee와 나머지 양의 분 선수의 availability는 작가 위임 아래 선택한 모델이다. 실제 의학적 허가나 이전 Hartenstein/Varejão의 건강을 승계한 사실이 아니다. 0분 예비 선수의 건강·전체 registered roster는 이 파일에서 생성하지 않는다. 기존 화면의 역할 정의는 전술 가정이며 Cedi Osman의 handler 사용 등을 실제 감독 판단으로 인증하지 않는다.

사실은 기존 원자료의 분·승인된 생략 방향, 추론은 두 제거 선수의 부담 합계, 작가 위임 선택은 McGee 출전과 작업 구간이다. 실제 등록·의료·전체 법적 실행·시즌 최종확정·원고 허용은 모두 false다. `PROJECT_FREEZE v0.30 PARTIAL`·설계/원고 CLOSED를 유지한다.

## 재현과 경계

`python -B -X utf8 tools/build_cleveland_c2_complete_working_minutes.py --check --self-test`

원입력은 UTF-8 BOM을 제거해 읽으며 저장소 SHA는 CRLF/CR→LF 정규화 후 계산한다. 최초 스크린·관측 입력의 원자료 지문은 변경하지 않았다. McGee 중복가산, Varejão/Hartenstein 재삽입, clock 변조, 의료·시즌·권한 승격, 행 삭제를 음성 검사로 거부한다. 이전 스크린의 `selected=false`는 당시 국소 감도 결과의 상태이며 이 새 작업 모델의 출전 선택과 구분한다. 루트의 독립 검문·전체1080경기 조인은 대기다.
