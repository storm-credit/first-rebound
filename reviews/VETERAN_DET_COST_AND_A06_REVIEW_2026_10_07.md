# 베테랑·Detroit 비용 및 A06 통합 검문

기준 main: PR457 merge `e8070d14e7cfa43eab17c7e1cf62c5cbc71bba85`. 사실/공개 근거 기반 추론/미선택 후보/작가 확정을 분리한다. 승인 S2·M1·A 방향을 보존한다.

## 비용과 권리

- [Young·Satoransky](../research/CHICAGO_2022_YOUNG_SATORANSKY_ROSTER_FAMILY_2026_10_07.md): 미선택 12계약 조합/36상태/192셀/기존165조합과5940결합을 독립 재계산했다. minimum 비용을2m으로 바꿔도 통과하던 실제 반례를 계약형태→비용/slot/hold/Bird guard로 수리하고 같은 반례 거부를 확인했다. 2m 대체 예약은 선수 계약이 아니다. 두 선수를 모두 일반계약하면15STD라 신인 일반계약 자리는 없다. Bird/minimum만으로 새 hardcap이 생기지 않으며 apron screen 음수는 실제 위법 인증이 아니다. 전체 FY22/rookie/TW/연간 예외와 실제 수락은 미완료다.
- [Detroit 초기 잔여비용](../research/DETROIT_2021_INITIAL_RESIDUAL_COST_FAMILY_2026_10_07.md): 공개 명명 여섯범주의 X=5,361,732, Olynyk 새 급여 후보 q=3,000,000~7,000,040의 조건부 비용 가족을 독립 수용했다. 과거 보고 차액과 캠프 전액 예약을 포함한 공개 template이며 비공개 모든 부채 부재 인증이 아니다. 25raw/11source/CBA 본문과 source 의미 변조 반례를 별도 대조했다. Olynyk 감액·Nets 거래 방향은 미선택, DET/BKN 공동 자산/현금/전체 비용은 미완료다.

## 구조·인계

- [A05 운영](../design/A05_EARLY_NBA_OPERATING_BATCH_2026_10_07.md): 기존 E4 역할 기회 안에 맡은 수비선 복귀·한 박스아웃·동료 확보 뒤 단순 outlet을 가시화했다. 새 경기/개인 리바운드/득점/승패 원인/주전 PG 확정이 아니다. 기존 네 기능 의미와 슬롯을 보존하며 소막3/3 및 Act 한정 역할 관측을 수용했다. 전체 NBA 역사/전체 G13 완료와 구분한다.
- [A06 묶음](../design/A06_2020_21_FINITE_FUNCTION_BATCH_2026_10_07.md): 기존 CF01~08을 다섯 최종 기능32~36/계획slot249~253으로 묶어 별도 독립 검문했다. 현행 S2 시즌 선택, 승인 Theis·Green, WAS 승→IND 패, 다음 첫 패스 지연 학습 과제를 연결했다. WAS 승을 개인 공헌 단독 인과로 만들지 않았고 IND 승 반전/M1 계약 반전 constructor 반례를 거부한다. 소막3/3의 한정 출구와 Act 한정 시즌 출구를 수용하되 전체 A06 역사 완료는 아니다.
- [A03/A04 감사](../design/A03_A04_BOUNDED_EXIT_AUDIT_2026_10_07.md): 소막6개 중5 bounded PASS/1 HOLD. A03 다음 동료의 좁은 역할 재배정 관측, A04 기관 계약·개발 책임 인수 관측이 남는다. 두 CP2 의미 반전 false PASS를 consumed-meaning SHA로 수리하고 같은 반례 거부를 별도 확인했다. 기존 부분순서로 대학 연습→Mar25 및 A04 사후 제시를 구분해 새 정확 날짜/공격 장면을 소급하지 않는다.
- [현재 등록](../control/G13_FINAL_FUNCTION_REGISTER.md): 36기능/45원천/18소막 경로·없는24. A06 다섯 row는 같은 batch JSON의 서로 다른 `/functions/i`를 `record_pointer`로 해석한다. 36개 모두 파일+pointer로 실제 dereference하여 ID/exit를 대조했다. 780계획 중744미배정은744새 사건/Pack 의무가 아니다.

## 도구와 독립 검문

[Claude 실제 결과](A03_A04_HANDOFF_SOURCE_BLIND_CLAUDE_2026_10_07.json)는53.71초에 회수했다. 이전 검문 결론을 숨긴 A03/A04 행동·비용·출구 입력을 사용했다. 지적 두 건은 A04 개인 공격 근거의 모호한 E1~E3 라벨을 A04-EF-001~003으로 명시하고, 기존 대학 부분순서를 감사에 기록해 처리했다. 원 호출 전 지문과 판정 시점 지문은 당시 snapshot이며 이후 수정의 현재 지문으로 위장하지 않는다. 이 국소 답변은 전체 G16 인증이 아니다. 이번 범위의 새 AGY/NLM 실행은 NOT_RUN; PR457의 AGY UNVERIFIED·NLM 등록 성공/분석 timeout·Claude timeout은 이력 그대로 보존한다.

통합 검문: staged37파일 JSON 파싱·상대링크513·정적 감사22원천 지문·whitespace PASS. 등록36 및 모든 JSON pointer 대조 PASS. 해당 범위 검문을 마친 뒤 PR→main으로 반영한다.

## 전체 7행 진행표

| 번호 | 작업 | 상태 |
|---|---|---|
|1|2020 드래프트 연쇄|완료|
|2|Chicago 2020–21|S2 완료: 법적12/12·F5/5·A3/3·K4/4|
|3|2021–23 거래·계약|승인 M1/A 비용 완료; FY22 베테랑/DET 초기 비용 후보 검문. 전체 실행·중요 방향·시즌 미완료|
|4|장기 커리어|17시즌 골격; 정확 후속 시즌·중요 결과 미완료|
|5|결말·전체 구조|14막42소막·36국소 기능/18소막 경로. 전체 기능표·역사잠금 미완료|
|6|집필 규격·Context Pack|독서110/110·문체 완료; 설계샘플2·실제Pack0. 전체G13/G14 미완료|
|7|통합·독립·작가 승인|G15/G16/G17 미완료|

미완료 큰 묶음5개, 요청6번까지4개. 다음은 A03/A04 두 관측 인계·A07/A08 묶음, FY22 남은 비용/등록범주, DET/BKN 공동거래 검문이다. PROJECT_FREEZE v0.30 PARTIAL·설계/원고 CLOSED·원고0 유지.
