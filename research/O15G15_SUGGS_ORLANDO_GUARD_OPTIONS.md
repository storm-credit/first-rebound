# O-15G15 — Suggs 개막 이전 기준선과 Orlando 12분 선택지

- 기준: `main` 71e29ea / O-15G14. 이 문서는 G14의 `PRIOR_HOLD`와 `ROLE_HOLD`를 풀기 위한 조사 패킷이다. 시즌·거래·득점·승패의 권위가 아니다.
- 판정: `COLLEGE_SOURCE_VERIFIED / NBA_TRANSLATION_HOLD / ORLANDO_ROLE_HOLD / NOT_INDEPENDENT`.
- 시점 방화벽: Suggs 입력은 2021-10-20 개막 전 공개된 2020–21 Gonzaga 통계만 사용한다. 2021–22 NBA 기록과 2022-01-23 실제 박스는 개막 예측값에 넣지 않는다.

## 사실과 후보를 분리한 Suggs 입력

| 구분 | 값 | 판정 |
|---|---:|---|
| Gonzaga 2020–21 | 30경기·30선발·870분, 308 FGA·104 3PA·114 FTA·88 TOV·136 AST | `VERIFIED_SOURCE` |
| 대학 per36 | FGA 12.745, 3PA 4.303, FTA 4.717, TOV 3.641, AST 5.628 | 위 총합의 산술 변환 |
| 24분 단순 노출량 | FGA 8.497, 3PA 2.869, FTA 3.145, TOV 2.428, AST 3.752 | `ARITHMETIC_ONLY`; NBA 환산 예측 아님 |
| NBA 효율·역할·상대 수비·포제션 조정 | `null` | `RESEARCH_HOLD` |

출처: [Gonzaga 공식 2020–21 누적 통계](https://gozags.com/sports/mens-basketball/stats/2020-21). 30경기/870분과 시도·실책·도움 총합을 같은 표에서 확인했다. `24/870 × 대학 총합`은 시간만 환산하므로 대학과 NBA의 경기 속도, 수비, 사용률, 동료 역할 차이를 보정하지 않는다. 따라서 G14의 Detroit 공격기회 4정책을 숫자로 승격시키지 않는다.

| 상호 배타적인 다음 입력 방법 | 장점 | 결정적 한계 | 현재 처리 |
|---|---|---|---|
| S15A 대학 24분 원비율 | 완전 재현 가능한 무보정 노출 점검 | 대학 비율을 NBA 능력으로 착각 | 스트레스 대조만 허용 |
| S15B 개막 이전 동시대 신인 비교군으로 위치·속도·역할별 보정 | 시점 방화벽 유지 가능 | 비교군·계수·역할 매칭 미구축 | `NEXT_RESEARCH` 추천 |
| S15C 드래프트 당시 스카우팅 범위만 쓰고 수치 비움 | 과도한 숫자 확신 방지 | G14 숫자 정책은 계속 HOLD | B의 계수 확보에 실패할 때의 게시 방식 |
| S15D 실제 NBA 루키 시즌 비율 역주입 | 수치가 빨리 채워짐 | 개막 시점 미래 유출·대체세계 팀 변화 무시 | `REJECTED_FOR_OPENING_PRIOR` |

S15B는 **후속 연구 순서 추천**이지 보정값·Suggs 생산성의 작가 확정이 아니다. 비교군은 2021-10-20 이전 시즌 데이터만 쓰고, 역할 및 대학→NBA 차이의 분산을 공개해야 한다.

## 2022-01-23 Orlando의 12분 공백

G14의 ORL 조건은 Mobley3·Herbert33, Suggs DET·Hampton DAL·Carter CHI, Vučević 잔류다. [NBA 공식 해당 경기 페이지](https://www.nba.com/game/chi-vs-orl-0022100701)와 [17:30 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_05PM.pdf)는 **원역사**의 출전/결장 근거다. 대체세계 명단·동일 의료 상태·등록을 보장하지 않는다. Cole 36분 상한과 매분 지정 주 가드 규칙을 유지할 때 12분이 부족하다는 G14 산술은 유효하다.

| 상호 배타적인 역할 정책 | 12분의 수신자 | 먼저 확인할 조건 | 농구·인과 비용 | 판정 |
|---|---|---|---|---|
| O15A 내부 포워드 전개 | Herbert Jones를 12분 지정 전개자로 재훈련·기용 | G7 DB1 ORL33 지명/등록, 해당일 가용, 기존 포워드 분의 대체 수신자 | 신인 윙의 볼 운반·압박 대응, 원래 수비/무볼 역할 손실 | `CONDITIONAL_CANDIDATE` |
| O15B 내부 포워드 전개 | Chuma Okeke를 12분 지정 전개자로 기용 | 등록·가용, 기존 윙/포워드 분 재배분 | 온볼 부담과 원래 수비 역할의 기회비용 | `CONDITIONAL_CANDIDATE` |
| O15C 별도 가드 | 해당 날짜 이전 합법 등록된 실명 가드에게 12분 | 15자리/투웨이·계약·취득·의료·당일 활동 명단 | 다른 로스터 자리·급여·기존 선수 분 이동 | `TRANSACTION_HOLD` |
| O15D 규칙 완화 | Cole의 36분 설계 상한을 48분까지 늘림 | 의료·체력·경기 사용 근거와 G14 개인 상한 변경 | 한 명에게 전체 가드 48분을 부과 | 현행 G14 조건에서는 `REJECTED`; 별도 재설계만 가능 |

O15A/B는 실제 선수의 당일 볼 운반 능력을 증명한 판정이 아니다. [G7 DB1 보드](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)에서 Franz Wagner는 GSW7, Herbert Jones는 ORL33이므로 원역사 Magic의 [시즌 프리뷰](https://www.nba.com/news/2021-22-season-preview-orl)에 보이는 Franz를 ORL 명단에 복사하지 않는다. Herbert/Okeke의 12분 주 가드 수행을 뒷받침할 개막 이전 자료는 아직 확인되지 않았다. O15C의 가드를 이름 없이 만들어 등록 완료로 간주하지 않는다. A/B/C 중 하나를 고르기 전에 **전체 포지션 240분, 동시 5명, 해당일 가용성, 공통 공격기회와 기존 선수 분의 기회비용**을 다시 증명한다.

## 다음 계산 순서와 게이트

1. S15B 개막 이전 비교군·동시대 스카우팅 근거를 확보하고 보정 불확실성을 명시한다. 실패하면 S15C로 Suggs 숫자 HOLD 유지.
2. O15A/B의 실제 등록·가용성 및 기존 포워드 분과 12분 수신자를 감사한다. C는 실명 거래·계약 증거가 있을 때만 계산한다.
3. G14의 2021-10-20 DET, 2022-01-23 ORL 두 양팀 조건을 새 입력으로 **새 버전**에서 재계산한다. 과거 G14 산출물을 덮어쓰지 않는다.
4. 실제 점수·승수·시즌 선택·2022 계약/픽, D1의 2020–21 정확 실행, SAC S14B~D는 계속 HOLD.

`PROJECT_FREEZE v0.30 PARTIAL`; 설계/원고 `CLOSED`; `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.
