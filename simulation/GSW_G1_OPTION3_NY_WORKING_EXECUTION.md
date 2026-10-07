# GSW G1: 3년차 옵션·MIN→NY·보호 급여를 잇는 운영 구현 가족

**Root selected routine working family / independent Codex review accepted.** 2026-10-07 부모가 직접 독립 검문 뒤 현재 conditional GSW28 baseline 안의 이 운영 가족을 선택했다. 기존 Golden State 28순위 working 착지의 `NOT_LOCKED / EXACT_LANDING_HOLD`, 실제 금액·통지·수락 null은 보존한다. 원장·중앙 파일 변경0.

## 다음 실행 단위

2018-start #28 rookie 계약 → 2019년 기한 내 3년차 옵션 행사 → 2020-02-06 G1 MIN 양도 → 2020-11-24 H/Spellman/기존 MIN2026 2R와 Ed Davis 교환 → 2020-12-09 NY 작업 waiver, 4년차 옵션 **명시적 미행사**. 실제 통지·승낙·정확 지급액·waiver 완료시각은 null이다. 2020 조정된 옵션 기한을 보통 October31로 오기하지 않는다. 개막 전 waiver 완료를 운영 조건으로 둔다. CBA I1(cc)(iii)/I1(hhhh)/VII4(a)(2): waived Veteran과 계약을 마친 Veteran Free Agent가 달라 이 waiver에 만료 VFA hold/renounce를 잘못 덧붙이지 않는다. 현재 protected dead salary는 유지한다. H와 Portland의 Jacob Evans는 다른 선수이며 실제 Evans의 미래를 자동 복사하지 않는다.

N3(옵션 미행사·2020 만료)는 추천에서 제외: MIN의 Davis 거래 outgoing 급여를 없애므로 비용 감소만으로 matching이 보존되지 않는다. Davis 양수 출전23경기를 보존하는 위 경로를 선택 가능한 최소 운영안으로 제시한다.

## 공개 입력·두 팀 matching

- 원 Davis 당해 base/cap 5,005,350; 원 Spellman 1,988,280. 새 H 당해 합법 가족은 1,936,000–2,017,320이며 그중 실제 급여는 선택하지 않았다.
- MIN: 과세 여부에 상관없이 125%+100,000 한도로 최소 5,005,350, 여유 0–101,650. NY: 한도 6,356,687.5, incoming 최대 4,005,600, 여유 2,351,087.5.
- 모든 80–120% 계약을 통과시킨 것이 아니다. 동일 #28/2018-start의 원 year3 상한이 비공허 구성 증인이다. 원 2019–20 Evans cap/base 10달러 차이와 Davis 보장열 50,053,500은 H 금액/보장 사실로 채택하지 않는다.

## CBA와 비용

직접 읽은 2017 CBA PDF292/294/295: two seasons/options, scale 80–120%, 보호 급여, bonus 한도. PDF233/234: 동시 합산·125%+100,000·2개월 제한. PDF202: waiver 뒤 paid/payable 급여도 Team Salary에 포함. PDF240/241/254: apron 조정 및 S&T 이후 연속 상한.

원 lawful financial realization의 공통 비용 Γ(t)를 같은 모델 안에서 보존하고 H≤E로 구성하면 Γ+H≤Γ+E이다. 이는 실제 H의 원계약·모든 미래 성과급·모든 private 장부를 인증하거나 모든 임의 Γ를 합법으로 정의하는 증명이 아니다. 원 public cost interval과 미확인 X를 삭제하거나 X=0으로 만들지 않는다. NY 현재 protected dead charge도 H 전액을 유지하고 stretch/setoff/claiming-team을 만들지 않는다. years1/2는 rookie80% 외 II6 최저급여도 교집합으로 적용하고 상한은 min(Ebase,Ecap,120%scale)로 둔다. 독립 source/의미 검문과 root 직접 Fraction·현재성 검문 뒤 이 한정 운영 가족이 채택됐다.

[MIN 공식 거래](https://www.nba.com/timberwolves/news/minnesota-timberwolves-acquire-ed-davis-new-york)는 web indexed 본문 확인. 직접 다운로드403 raw는 증거로 제외했다. 새 [MIN 2020–21 공식 guide](https://cdn.wolveslynx.com/timberwolves/communications/guides/2020-21_Wolves-MediaGuide.pdf) PDF228 원문에서 MIN2026 2R를 포함한 교환을 직접 확인했고, Rubio의 별도2024 2R와 구분한다. NBA frozen feed의 Trade2020010/Waive1033884와 원 Evans full2020–21 dead row도 대조했다. SS는 자체 편집 공개 입력이며 league memo가 아니다.

## 출전·등록 영향

현재 정규2160 팀게임 중 Hutchison 양수0; MIN Davis 양수23게임 유지. GSW 두 L2 전체 객체 동일·각14,400초·8명 보존. GSW May standard15/TW2 보존. 이는 actual 전체 등록·의료 인증이 아니다. 이전 두 후보와 중앙 파일을 수정하지 않았다.

## 독립 검문

Codex chi: 원raw6·MINguide228·NBA표29/30·CBA12쪽 및 code/MD/수학을 직접 대조, year4 charge 복구와 MIN2026→2024 변조 거부. Root: Fraction 양끝·최저보다1달러 낮은 값·min(base,cap) 및 NY charge/지명권/옵션 변조 거부. 실질 남은 결함0. [Claude 실행 기록](../reviews/GSW_G1_OPTION3_NY_CLAUDE_BLIND_2026_10_07.md)은 선택 전 입력의55.0548초 timeout·분석0을 보존하며 현재 선택/최저급여 교집합 등의 후속 수리와 구분한다. 전체G16 승격0.

## 전체 진행

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md). 이 leaf의 완료와 전체 작업 완료를 구분한다.

| 번호 | 현재 범위 |
|---|---|
|1|2020 드래프트 연쇄 완료|
|2|Chicago2020–21 법적12/12; A/K 전체 종료 검문·named 운영 경로 진행|
|3|2021–23 승인 방향·후속 정확 실행 진행|
|4|장기 커리어 선행 시즌 결산 연결 대기|
|5|전체 구조 골격; 회차 기능표 진행|
|6|집필 규격·Context Pack 기능13/780, 미배치767|
|7|통합·독립·최종 작가 승인 대기|

**미완료 큰 묶음6. v0.30 PARTIAL / 설계·원고 CLOSED / 원고0 / 실제Pack0.**
