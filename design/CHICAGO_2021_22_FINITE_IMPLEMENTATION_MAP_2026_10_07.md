# Chicago2021–22 유한 구현 입력 지도

새 날짜·건강·분·승패·우승·AP1/SG16 선택은 **0**. 이미 완료된 S2를 다시 열지 않는다. 이 문서는 현재 입력을 실제로 조인해 다음 구현 단위를 찾은 지도이며 시즌 실행 인증이 아니다.

## 이미 사용할 수 있는 입력

- historical 리그1,230경기·30팀 각82. Chicago82개 game_id/date/home/away가 리그표와 정확히 일치한다. 홈41·원정41, 상대29팀. 관측 일정·점수는 pinned NBA V3 mirror이며 새 공식 숫자박스 검문0이다.
- 15명×82=1,230선수·날짜 관측, 우선사유32행,2020–21개막 prior와16개P/Duarte 생산성 비교, DET/ORL/SAC3개 조건부 양팀 비교를 재수집할 필요가 없다. 같은날 기록 부재·DNP·부상 문구는 자동으로 작품 건강을 정하지 않는다.
- reviewed SQ1의15STD+2TW·10서명상태와 six-category 공개 비용 가족 PASS(상한128,914,775·apron여유14,087,225)는 신규2021–22 working roster의 개막 입력으로 사용할 수 있다. 구판 signing leaf의 wholecost HOLD는 보존이력이며 named fullcost producer의 범위만 최신판정으로 소비한다. 실제등록·실동의 인증이 아니다.

## 구판28/22를 새32/18로 읽지 않는다

정상 M1은 Markkanen32·Caruso18·주인공32다. 구판R21A는 Markkanen28·Caruso22다. SF에서 Caruso−4/주인공+4, PF에서 주인공−4/Markkanen+4를 보존해야 한다. 기존G12–15B의 세경기 분·생산성 비교는 구판을 기반으로 하므로 자동 승격할 수 없다.

M1 저장11개 순서없는5인 블록에 **Coby PG10→Satoransky10, SG8→Valentine8**을 적용한 후보는 모든 블록5명 중복0·창조자존재·48분/240팀분을 충족한다. Markkanen32·Caruso18·주인공32는 보존된다. 이 실제 산술 stencil은 JSON에 있다. 어느 날짜에 Coby가 빠진다거나 수신자가 건강하다는 선택은 하지 않았다. 첫13경기 자동 반복·실제 교대순서·선발 인증도 아니다.

M1 원증인의5핀 중4개는 현재와 같고 live FREEZE만 옛 지문이다. 역할 의미와 승인 direction은 그대로다. 구판 전체검사기의 current PASS를 주장하지 않으며, 다음 새 carrier는 현행 고정 의미를 직접검문하고 원이력을 보존한다.

## 변경 구단과 정확 범위

Chicago 후보명단의 역사적 선수 관측 소속과 다른 **9개 이름**, 잠재 **10개 상대 구단/30Chicago경기**의 정체성 footprint를 직접 산출했다. 이는 단순 급여절감이 아니라 원래 상대팀에 있던 LaMelo/Carter/Markkanen/Duarte/Young/Satoransky/Wieskamp/Stanley/Valentine의 슬롯·분·반환대가를 다시 연결할 출발점이다. 관측팀 집합이 해당시즌 매일 같은 소속이었다는 뜻이 아니므로 실제 날짜별 transaction을 대조해야 한다.

2020지명·T1–T4의 이미 승인된 귀속은 보존한다.2021 DB1의 다른58명·AP1/SG16 중요방향은 후보이며, #16미서명권리 순간을 HOU선수등록이나 무기한 비용0으로 바꾸지 않는다. BOS/OKC/HOU와Chicago의7경기는 선택 route를 매개변수로 둘 수 있다. S2의 과거 exact 결산을 바꾸지 않는다.

DET는 Suggs후보/다른2020착지를, ORL은Herbert12PG 역할 혹은 새Gravett계약을, SAC는Sabonis/4팀거래별 구단·선수·픽·등록·비용을 구분한다. O15A/O15C 분증인은 있지만 역할·취득·당일가용 조건은 남는다. 새지명/FA/2022마감원거래를 사실처럼 복사하지 않는다.

## 다음 실제 최소 구현

`tools/build_chicago_2021_22_m1_dated_working_minutes.py` + `simulation/CHICAGO_2021_22_M1_DATED_WORKING_MINUTES.json/.md`가 아직 없다. 다음 단위는 이미 있는82키에 M1정상/Coby-out 조건부 stencil을 연결한 날짜별 roster/availability/clock carrier다. 양수 이름의 날짜별 등록, 조건부 결장, zero사유미선택,12–15active nomination/TW50활동카운터,48/240과5인 증인을 검문해야 한다. 이는 새 private 의료·영수증 gate가 아니라 유한 working 모델의 입력과 구현 공백이다.

그다음82상대·총164팀행의 변경명단·가용성·분을 조인하고 선택된 한 방법으로 생산성/impact를 연결한다. G14의 과거FGA/FTA/TOV고정 예산 배분은 예측기·BPM·대체점수가 아니다. 리그순위까지 종료하려면 나중에 전체1,230결과 join이 필요할 수 있지만,82정상함수 정의를 위해 원행1,230개를 새로 수집하라는 요건은 아니다.

Carter CX1–4나 주인공2022연장 선택은 미래 사건이다. 어느 연장분기도2021–22원 rookie 급여 자체를 변경하지 않으므로, 미래 중요계약 선택이 기존현재시즌 역할함수 작성의 영구장애가 되지는 않는다. ordinaryQO 함수/선발기준도 미래통계 입력을 매개변수로 미리 정의할 수 있다.

## 재현과 남은 범위

JSON의 source31 LF지문,82원소의 정확 date/team join,1,230개 선수키,32/18role합계,11블록 Coby-out 변환,9이름/10팀/30경기 footprint를 직접 검사했다. 새 generator는 만들지 않았고 기존producer·정본·중앙을 수정하지 않았다. 같은자료 수집·기존전체검사 반복0. 함수뿐인 지도를 전체시즌 완료로 계수하지 않는다.

[JSON](CHICAGO_2021_22_FINITE_IMPLEMENTATION_MAP_2026_10_07.json) · [현행 전체 로드맵](WORLD_BIBLE_COMPLETION_ROADMAP.md) · [누적 기능 등록기](../control/G13_FINAL_FUNCTION_REGISTER.md)

|번호|묶음|상태|
|---|---|---|
|1|2020드래프트 연쇄|완료|
|2|Chicago2020–21|S2완료|
|3|2021–23거래·계약|공개비용/계약함수 진행,2021–22 날짜모델 미구현|
|4|장기 커리어|후속시즌 입력 대기|
|5|결말·전체 구조|골격 유지·전체기능표 미완료|
|6|집필규격·Context Pack|현행 누적등록기 참조·실제Pack0|
|7|통합·독립·작가 승인|최종CLOSED|

미완료 큰 묶음 **5**. `v0.30 PARTIAL` / 설계·원고 `CLOSED` / 원고0.
