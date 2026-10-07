# Chicago 2025 만료 minimum 5 — 같은 선수 1년 갱신 후보

권고는 MIN25_A다. 기존 다섯 선수의 소유·서비스 가족을 보존하며 새 2025년 1년 minimum UPC를 비교한다. 가격·서명·수락은 아직 선택하지 않았다. Duarte는 별도이며 Chicago 15명 전체를 인증하지 않는다.

## 원 계약과 서비스

| 선수 | FY24 선택 bucket | FY25 조건부 bucket | 새 급여 |
|---|---:|---|
| Thaddeus Young | 10 | 10 | `M25(10,Year1)` |
| Javonte Green | 5 | 6 | `M25(6,Year1)` |
| Joe Wieskamp | 3 | 4 | `M25(4,Year1)` |
| Denzel Valentine | 8 | 9 | `M25(9,Year1)` |
| Tomas Satoransky | 8 | 9 | `M25(9,Year1)` |

원 선택은 2024-07-07부터 한 Season의 minimum이다. 2025-06-30은 salary-cap fiscal 말단이고 서비스 종료일을 따로 인증하지 않는다. 원 UPC가 요구하는 서비스를 마쳐야 Veteran Free Agent가 된다. I1(iiii)의 Active/Inactive List 정규기간 하루 이상 및 제외조건 없는 FY24 서비스이면 한 크레딧을 연말에 얻는다. 82경기 실제 출전·건강·급여 영수증은 요구하지 않는다. Young은10+ 상단 bucket이며 나머지5→6/3→4/8→9/8→9다.

## 법정 minimum과 계산 화면

2023 CBA I1(jj), II6(a)/(f), ExhibitC에 따른 `M25(YOS,Year1)`가 본체다. 2025 signing-year scale을 적용하고 Exhibit1A의 minimum 준수 및 deemed amendment를 보존한다. 공식 조정표와 정확 반올림 원문은 아직 회수하지 않아 표값을 실제 센트로 인증하지 않는다.

ExC×154647000/123655000은 매년 표 반올림을 생략한 정확 유리수 참고치다. 세 번의 각 조정 오차가 절댓값1달러 이하라는 **별도 조건**이면 누적오차<3.24달러이고 `ceil(참고치)+4`가 보수적 상단이다. 이 ROUND 조건을 공식 법칙이라고 주장하지 않는다. 조건 밖에서는 숫자 화면을 폐기하고 법정 M25 함수를 쓴다.

| YOS | ExC Year1 | 반올림 생략 유리수 | ROUND 조건부 상단 |
|---:|---:|---|---:|
| 2 | 1,836,090 | `56789162046/24731` | 2,296,279 |
| 4 | 1,968,175 | `60874471845/24731` | 2,461,469 |
| 6 | 2,298,385 | `71087669019/24731` | 2,874,440 |
| 9 | 2,641,682 | `408528196254/123655` | 3,303,779 |
| 10 | 2,905,851 | `449381139597/123655` | 3,634,157 |

다섯 선수 fullcash 조건부 상단은 15,577,624달러다. 조건부 환급 가족의 normal/apron Salary 상단은 5×M25(2)의 11,481,395달러이며 같은 개념이 아니다.

## 1년과 2년 비교

- **MIN25_A 권고:** 1년·보너스0·옵션0·표준 조건 아래 skill/injury 전액 보호. IV6(h)의3+YOS 1년 minimum이면 팀은 선수에게 전액 M25를 지급한 후 Season말에 league-wide fund 환급을 받는다. VII3(f)의 Salary는 비환급 부분인 M25(2)다. 기존 Γ를 그 차액으로 지우지 않는다.
- **MIN25_B 비교:** 최대2년 minimum exception도 가능하지만 후년은 같은2025 signing scale의 Year2·서비스 bucket 조건이다. 1년 환급을 2년 계약에 자동 적용하지 않으며 2026 새 보호·서비스 의무가 생긴다. 아직 어느 안도 선택하지 않았다.

## 권리·날짜·비용

- 다섯은 이 서비스 가족에서4년 이상·비TW·비RSC 만료이므로 ordinary UFA다. Bird 연쇄가 유지돼도 최소계약 체결 권한과 hold는 구분한다. 만료 minimum의 hold는 VII4(d)(4) 비환급 현행 minimum이다. 150/190% 일반 Bird multiplier를 억지 적용하지 않는다.
- July1의 만료만으로 hold가 지워지지 않는다. 유효한 재서명·다른 NBA팀 서명·별도 적법 renounce가 생길 때까지 유지한다. 새 same-player Salary가 붙으면 같은 hold를 한 번만 교체한다. 원 Γ·발생 지급·정확연도 귀속은 그대로다.
- [NBA 공식2025 발표](https://pr.nba.com/nba-salary-cap-2025-26-season/)와 보존 HTTP200 본문에서 cap154,647,000·July6 noon ET moratorium말단을 읽었다. 후보 July7 12:02 ET는 이후다. minimum은 CBA가 moratorium 중 허용하는 예외를 별도로 강제할 필요 없이 이 날짜를 택한다.
- 공식 표시 floor139,182,000과 법정90%×cap139,182,300을 구분한다. 이5만으로 floor·tax·cash·전체 apron이 충족됐다고 주장하지 않는다.
- LIVE/원Γ/FA·QO·FRN/unsigned·RT/unused exceptions/roster·floor·tax·cash 6범주를 JSON에 연결했다. minimum exception만으로 새 hardcap을 발동시키지 않지만 다른 기존 trigger를 부재로 인증하지 않는다.
- **등록 subtotal:** 다른선택유효 n_other≤9일 때 n_other+5≤14. 이는 Duarte와 새신인 UPC를 제외한 명명 부분합이다. FAhold는 STD가 아니며 incomplete capcount는 VII4(f)의 별도 기준이다. 정규시즌14–15 기준은 이후 전체등록 join에서 적용한다.

## 원자료와 검증

- `research/CHICAGO_2025_NAMED_ROLLOVER_INPUT_PACKET_2026_10_08.json` — LF `f728fc6b7891422c0ce204bf61aa60a8fa7c21331bd4ade904017b78a057b006`
- `simulation/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION.json` — LF `ef48f0a1931037ec58ec59e53fde30baedddf8d96f13e2bc86120da2a7572cf5`
- `research/CHICAGO_2024_25_A10_NAMED_ROLE_WINDOW_COST_FAMILY_2026_10_08.json` — LF `af4f3b340841251a50646fb05aeefcc415e95c4fc07b3c2e02e3f9af8bb14bb1`
- `research/CHICAGO_2025_MARKKANEN_ROUTINE_RENEWAL_COST_FAMILY_2026_10_08.json` — LF `5c4cf3f32e4fcec302c347e10a61e008f750e1a76826446a8df7b3e527615d7a`
- `reviews/CHICAGO_2024_A10_SELECTED_RENEWAL_EXECUTION_DEN_INDEPENDENT_REVIEW_2026_10_08.json` — LF `9d3485811fe67139896f322b52ae699c7bf418d53029e6035a4438a5fcf517c3`

- CBA raw SHA `bf178ca0f2d64f9dfe6fde095d3ae43d576b12e19ce7a679618d632584f7ab32`; PDF29/33/34/37/57–58/125/210–211/234–235/241–242/244–245/264/343/453/632의 필요한 조항만 읽었다. 기존31쪽 전체 검문·조상 생성기 재실행은 하지 않았다.
- NBA cap raw SHA `8b20484615b529dbcb0b6e6ba3f08997db4b2cdd259d8ffb4d9ed44f75320988`; 공식 URL과 cache article본문을 교차했다.
- 다섯 pointer/선수/YOS와 Fraction 화면·법정 서비스/환급/hold 함수를 실제 대조했다. 정적 문서 constructor시험0·독립검문 pending이다.

## 남은 유한 입력

권고의 root 채택·조건부 가상 합의와 원서비스 완료 범위를 연결하면 이5의 함수 실행으로 이어갈 수 있다. 실제 시장수락·private cents·전체82경기·30팀·임상 원장은 새 게이트가 아니다. 다른 선수·옵션·Duarte·신인·R25/N25/A25는 별도 기존 포트이며 이 패킷으로 삭제하지 않는다. 원고 CLOSED를 보존한다.
