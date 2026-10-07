# 주인공2022 E1–E4 계약 구현 후보

상태: INDEPENDENTLY_REVIEWED_EXISTING_E1_E4_CONSENSUAL_FORMS_NO_AUTHOR_SELECTION. 추천≠작가확정, 실제 수락·정확지명·전체비용 인증0.

|기존안|형태|2022 시작 연봉·급여 일정 USD|합계|
|---|---|---|---:|
|E1|2021 rookie 연장, 새4년|18m /19.44m /20.88m /22.32m|80.64m|
|E2|2022 Chicago 직접 Bird RFA4년, 기존 권고|22m /23.76m /25.52m /27.28m|98.56m|
|E3|2022 Chicago 직접 Bird5년·기존25% 최대 기준|30.91375m /33.38685m /35.85995m /38.33305m /40.80615m|179.29975m|
|E4|유효 보통QO1년 수락→서비스완료조건2023UFA|16–30순위×선발/비선발30가지 함수 유지|미선택|

## 조건부 법적 구현

E1은2021-10-15 12:00ET 후보, 유효 창은8/6 12:01–10/18 18:00ET이다. 옵션과 Bird자격을 보존하며 현재2021–22 원급여를 새18m로 바꾸지 않는다. 새4년과 현재1년을 합해5시즌, 각 증가는 첫해8%이다. 실제 계약은 미서명이다.
E2/E3는2022-07-07 12:00ET 같은Chicago 직접계약 후보다. [NBA2022공식 발표](https://pr.nba.com/nba-salary-cap-2022-23-season/)에서 cap123.655m,6/30 18시FA협상,7/6 noon모라토리움 종료를 확인하고 CBA의 Bird12:01pm 시작과 연결했다. E3 직접5년 계약을 Designated Rookie5년 연장이나30%성과 최대급으로 표시하지 않는다.
E1–E3는 전액 기본급 skill/injury 보호와 표준 지급, 옵션/ETO·새 서명/성과/홍보/트레이드 보너스·대여/새 buyout0을 제안한다. 이는 새 상호합의 후보의 조건이다. 원계약의 미지 bonus를0으로 인증하지 않는다. E1은 원기간을 보존하며 unearned원bonus가 있으면 XXIV2a5의 상호합의 Ex4로 연장기간만 제외하는 후보다. 기존 발생·잔여채무를 삭제하지 않는다.
18/22/30.91375m 첫해는25%max 이하이고 새4/5년의8% 일정과 기간을 검문했다. minimum은 II6/ExC와 법정 conformity를 보존하며 표의 보수적 첫5년 cell stress보다 제안액이 높다. 정확 NBA rounding이나 후년 새CBA의 실행액은 인증하지 않는다.

## QO·거래 후손

E4는 시즌이 끝나 XI4a창이 열렸다는 조건에서6/29 유효QO 제시와7/7 수락을 별도 모델링한다. 새 미래통계 없이16–30×2분기와 원성분 함수만 재사용한다. QO발행이 수락은 아니며 두번째 옵션/서비스완료·미철회가 필요하다. 기본급보호·표준지급/허용 원조건을 유지하고 MaxQO/offer sheet/FirstRefusal을 새로 선택하지 않는다. 2023UFA는 실제 서비스완료를 전제로 하며 다른 구단·2023연봉은 null이다.
E1은7/1 2022 전까지 acquiring기준 평균과 outgoing현재Salary를 분리한다. VII8f의7a six-month 일반규제를7b rookie연장에 자동 적용하지 않는다. 기존의 Γ가0이라는 주장이나 전체matchingPASS는 없다.
E2/E3/E4는 FA서명 뒤3개월/12/15 규제, above-cap Bird+120%초과 조건이면1/15 규제를 보존한다. 위/아래cap 상태를 선택하지 않는다. E4는1년 Bird계약의 거래동의와 거래시 Bird연속성 변경도 별도다. 모든 실제 거래·동의는 미선택이다.

## 재현·권위

[원CBA](https://cdn.nba.com/manage/2021/03/2017-NBA-Collective-Bargaining-Agreement.pdf) 및 검문된 Carter/QO leaf를 직접 재구성한다. raw/쪽/원정본 SHA는JSON에 있다. 새2022PR 직접요청은 AccessDenied본문이었고 원HTTP상태는 보존되지 않았다. 재시도0이며 기존HTTP200 원캐시와 실제webopen본문을 재검문했다. 실패본문은 근거로 사용하지 않는다.
`python -B tools/build_protagonist_2022_contract_candidate_family.py --check --self-test`.

## 현행7행 진행표

미완료 큰 묶음5; v0.30 PARTIAL, 설계/원고 CLOSED, Pack0·원고0. 현행 로드맵·누적 등록기 참조.
|번호|상태|
|---|---|
|1 2020드래프트연쇄|완료|
|2 Chicago2020–21|완료|
|3 2021–23거래·계약|M1/A 유지; E1–E4 후보, 중요선택/전체실행 미완료|
|4 장기커리어|후속시즌 설계 미완료|
|5 결말·전체구조|골격 유지, 전체기능표 미완료|
|6 집필규격·Context Pack|현행 등록기 참조, 전체G13/Pack 미완료|
|7 통합·독립·작가승인|최종게이트 미완료|
