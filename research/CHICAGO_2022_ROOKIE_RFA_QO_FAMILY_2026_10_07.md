# Chicago2022 rookie RFA/QO 함수·비용 상한

상태: INDEPENDENTLY_REVIEWED_ORDINARY_QO_FUNCTION_AND_CONDITIONAL_COST_INPUT. 작가 선택·실제 금액·실제 접수·전체 비용 인증은 0.

## 새로 완료한 범위

2017CBA VIII1c / XI1c·4와 NBA2018 실제 ExhibitA(PDF29)를 연결했다. Carter7과 주인공16–30의32개 선발/비선발 가지, 원3년차 기본급·likely·unlikely의 연속80–120% 성분영역을128개 꼭짓점으로 검문한다. 미래 통계나 주인공 정확 순위를 선택하지 않는다.
Carter 선발은 자기 순위의 QO, 비선발은 자기 제안과15번 기본급 제안 중 작은 쪽이다. 주인공 선발은9번120% 기본급·보너스0, 비선발은 자기 원성분의 증가식이다. 원성분 각각의 증가를 보존하며 Carter 비선발의 최종 UPC 성분을 임의로 구성하지 않는다.
정확 유리수 법정 입력식과 보수적 달러 상한을 분리한다. 성분3개에서 각 단계의 ceil 합≤전체 ceil+2를 사용해 원래 계약 성분을 지우지 않는다. 공식 NBA 반올림 알고리즘이나 실제 계약 달러를 인증하지 않는다.

| 비용 입력 | USD 상한 |
|---|---:|
| Carter | 9,279,761 |
| 주인공 | 7,921,302 |
| 합계 | 17,201,063 |
| 기존2×25%cap 예약 축소 | 44,626,437 |
| 기존 부분 비용식에 이 입력만 대입 | 95,076,705 |
| 동일 조건의 미입력X 여유 | 61,905,295 |

별도 minimum floor/ceil 조건을 채택한다면 위 부분 비용/여유는 각각50달러 감소/증가한다. 기존 core 파일은 변경하지 않았다. 이 수치는 아직 미입력X가 있는 조건부 apron screen이며 normal salary-cap 또는 전체FY22 PASS가 아니다.

## 시간·권리·분류

양쪽 옵션의 유효 행사와 계약 서비스 완료가 조건이다. 보통 QO는 해당 두번째 옵션 시즌 다음날부터2022-06-29까지 발행하고10-01까지 수락 가능해야 한다. 실제 제시·수락이나 미래 선발 결과는 null/false이다. 미행사 옵션·QO미제시는 별도 UFA 경로이다.
MaximumQO(5년 최대급), FA cap hold(250/300% 등), offer sheet/FirstRefusal 비용은 보통 QO와 별도다. 이 후보는 no2021extension/noMaximumQO/noFirstRefusal 범위에서만 상한 입력을 공급한다. CX4/E4를 작가 확정하지 않는다. 새로운 관련 사건 발생 시 해당 비용을 다시 연다.

## 원천·재현

[NBA2018 actual scale](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf) PDF29 실제 표를 읽고 시각 대조했다.2017ExhibitB3의 예시 표는 사용하지 않았다. [2017CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) PDF208–209/240–241/294–295/309–311/314–320을 직접 읽었다. 원cache SHA와 각 추출쪽 SHA는 JSON에 남겼다. 이번 새 다운로드0.
`python -B tools/build_chicago_2022_rookie_rfa_qo_family.py --check --self-test`. 출처LF 지문·upstream 전체재구성·동일ID 표/정책 변조를 거부한다. 작성자 음성검사는 독립 감리로 계수하지 않는다.

## 현행7행 진행표

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)·[누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md) 기준. 미완료 큰 묶음5, v0.30 PARTIAL / 설계·원고 CLOSED / 실제Pack0 / 원고0.
| 번호 | 상태 |
|---|---|
|1 2020드래프트 연쇄|완료|
|2 Chicago2020–21|완료|
|3 2021–23거래·계약|승인M1/A core 유지; QO 함수 입력 완료, 중요 선택·전체 실행 미완료|
|4 장기 커리어|후속 시즌 입력 대기|
|5 결말·전체 구조|골격 유지, 전체 기능표 미완료|
|6 집필 규격·Context Pack|누적 등록기 참조; 전체G13/실제Pack 미완료|
|7 통합·독립·작가 승인|최종 게이트 미완료|
