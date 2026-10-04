# Orlando 2020–21 — 날짜별 등록 법적 범위 증인

기준 main `e3ef70bef8b96c7ae79ede6d6cde5a985431118b` / PR #413. 범위는 2021-03-25~05-16의 **계약 분류·기간·등록 정원·공개 사건별 적법한 실행 순서**다. [재현 JSON](ORLANDO_REGISTRATION_LEGAL_DOMAIN_2026_10_05.json)과 [생성기](../tools/build_orlando_registration_legal_domain.py)에 법규 원문 지문·입력 지문·53일·21사건을 저장한다.

## 권위와 법규

- **사실:** [2017 공식 CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 I 정의, II §9·§11, VIII §1–3을 실제 읽었다. PDF 32/69/70/74/292/294/295/296쪽 지문이 JSON에 있다. 신인 첫 계약의 분류와 급여 범위, 10일 기간/시즌 종료, 팀별 최대 두 번, 정원에 따른 동시 계약 한도, 조기 해제 통지와 보수 보존을 구분한다.
- **사실:** [2020–21 G League 공식 일정](https://gleague.nba.com/news/2020-21-nba-g-league-key-dates)의 2021-02-01 발표는 NBA 10일 계약 시작 가능일을 **2021-02-23**으로 제시한다. [NBA 2020-12-18 공지](https://www.nba.com/news/teams-allowed-to-carry-15-players-on-active-roster-for-2020-21-season)는 활동 15명·투웨이 2자리를 확인한다. 웹 본문 관측이며 HTML 원본 지문은 미회수다.
- **작가확정:** [기존 T1/T2/T3 방향](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)과 [Hall 5/9 생략](../canon/CHICAGO_2020_21_F4_F5_FOLLOWUP_DECISION.json)을 재사용한다. 새 거래·급여·건강·계약 선택을 확정하지 않는다.
- **추론/법적 범위:** T1로 적법하게 양도할 수 있는 유효한 대체 2020 #24 첫 rookie-scale 계약이라는 범위 전체에서 Nnaji는 일반계약 한 자리다. `0.8*S24 ≤ 현재 기본급`, `Salary+Unlikely ≤ 1.2*S24` 및 허용되는 계약 구조를 전제로 **정확 120%를 먼저 선택할 필요가 없다**. 미서명 권리만 양도하거나 계약 상실 뒤 새 투웨이에 들어가는 별개 경로는 승인 T1 증인의 범위가 아니다.
- **후보:** 공개 역사에서 이월한 해제/서명 사건과 당일 적법한 순서다. 이 증인은 해당 경로의 등록 법규 적합성을 검증하며, 가상 세계 계약서의 실제 서명·접수 시각이나 T5 전체의 작가확정을 주장하지 않는다.

## 유한 범위 전수검문

[공개 목록](ORLANDO_PUBLIC_EVENT_COVERAGE_2026_10_05.json)의 21사건을 하나씩 실행한다. Chicago–Orlando 거래와 Hall 5/9 계약은 기존 승인에 따라 생략하고, Denver 거래는 Hampton→Nnaji의 기존 승인 변환을 적용한다. 남은 사건은 날짜와 선수 이름을 그대로 대조한다. 해제·만료를 같은 날 신규 서명보다 먼저 두는 순서 증인이며, 원역사 리그 접수 시간의 복원은 아니다.

| 검문 | 재현 결과 |
|---|---|
| 전 기간 | 연속 53일의 일반 14~15·투웨이 0~2, 중복 선수 없음 |
| 공개 사건 | 21/21 근거 ID 연결, 설명되지 않은 명단 변화 0 |
| 거래일 | 일반 2:2·1:1 교환 모두 15→15, 순서 두 가지 적법 |
| 10일 계약 | 유지하는 6건 모두 2/23 이후·시즌 종료 전에 종료, 팀 3경기보다 10일이 길거나 같음 |
| 동시 10일 한도 | 일반14명일 때 2건, 15명일 때 3건이 법규 상한; 이 경로의 실제 최댓값은 2건 |
| 같은 선수 | Franks/Hall 각 2회, Cannady/Brazdeikis 각 1회 |
| 조기 해제 | 등록 자리 종료와 원래 10일 보수 의무 분리; 서면 통지 법규 전제 |
| 갱신 | Franks4/22·Hall4/23·Brazdeikis5/12 이전 계약 만료 후 다음 계약 |
| 음성 대조 | 잘못된 Nnaji 분류·16번째 자리·중복/누락일·정원15 유지하는 무근거 교체 모두 거부 |

최초 독립 반증이 **Aminu를 근거 없는 선수로 하루 교체해도 통과**하는 결함을 찾았다. 명단 차이에서 임의 사건을 추론하는 코드를 제거하고 공개 사건을 직접 재실행해 모든 날짜의 최종 이름 집합과 일치하도록 수리했다.

## 종료 범위

독립 검수와 원장 검문을 완료해 `ORL_DATED_REGISTRATION` 하나의 세 분기 `game_days / intervening_days / all_other_transactions`에 `LEGAL_BOUND_PASS`를 적용했다. 급여 최소치·서명 및 양도 자격·유효한 계약/서면 해제라는 법적 범위 전제는 유지한다. 허용 전제를 벗어난 경로는 이 증인으로 인증하지 않는다.

전체 급여/보너스/잔여 보수/예외 사용/매칭은 `ORL_COMPLETE_COST` 등 기존 별도 필드에 남는다. 53일 경기 건강·활동 명단·분 배정, 실제 T5 실행과 F4 전체 종료도 HOLD다. 따라서 다른 11개 법적 필드·F0/5·A0/3·K0/4·season_selected=false를 보존한다. `PROJECT_FREEZE v0.30 PARTIAL`·설계/원고 CLOSED·원고0.

## 재현

```powershell
C:/Python314/python.exe -B -X utf8 tools/build_orlando_registration_legal_domain.py --cache-dir 'C:/Users/Storm Credit/AppData/Local/Temp' --check --self-test
```

공식 CBA 원본 캐시는 필요하며 지문이 다르면 실행을 거부한다. 캐시는 저장소에 추가하지 않는다. 문서/JSON은 법적 범위 증인으로 보존하고 후속 실제 사건 실행은 별도로 검문한다.
