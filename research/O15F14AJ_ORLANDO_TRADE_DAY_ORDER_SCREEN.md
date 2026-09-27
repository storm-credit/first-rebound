# O-15F14-AJ — Orlando 2021-03-25 거래 순서별 급여 검문

- 판정: `CONDITIONAL_ORDER_SENSITIVITY_FOUND / F2_HOLD`.
- 재현: `python tools/build_orlando_2021_trade_day_order_screen.py` → `simulation/ORLANDO_2021_MARCH25_TRADE_ORDER_SCREEN.json`.
- 입력: [Orlando 후반 계약 원장](ORLANDO_2020_21_PAYROLL_SOURCES.json), [거래 선수 급여 항목](NBA_2020_21_L_EXECUTION_TERMS_SOURCES.json), [4월 이후 대조 장부](../simulation/ORLANDO_2020_21_PAYROLL_BOUND.json). 공개 2차 급여와 승인된 대체 24순위 Nnaji의 조건부 기본급을 사용한다.

## 사실과 조건

[Orlando 구단의 Gordon 거래 발표](https://www.nba.com/magic/orlando-magic-acquire-rj-hampton-garry-harris-draft-pick-denver-nuggets-aaron-gordon-gary-clark-trade-20210325)는 원역사에 Gordon·Clark와 Harris·Hampton·1R이 이동했다고 기록한다. 대체 설계는 Hampton 대신 Nnaji를 받는다. [Orlando 구단의 Fournier 거래 발표](https://www.nba.com/magic/orlando-magic-acquire-two-future-second-round-draft-picks-boston-celtics-evan-fournier-trade-20210325)는 Fournier를 보내고 Teague·두 2R을 받았으며 Teague가 합류하지 않는다고 기록한다. [NBA의 3/27 기사](https://www.nba.com/news/magic-waive-veteran-guard-jeff-teague)는 Teague 방출을 확인한다. 발표의 게시 시각은 **리그가 두 거래를 승인·장부 처리한 순서의 증거가 아니다**.

[NBA/NBPA 2020-21 발표](https://pr.nba.com/nba-nbpa-2020-21-season/)의 사치세 기준은 `$132,627,000`이다. `$138,928,000` apron은 기존 [역사 한도표](https://www.salaryswish.com/salary-cap)의 2차 수치이며, 실제 hard-cap 발생 여부와 별개다. [2017 CBA VII §6(m)(3)(A)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 해당 **apron용 Team Salary**에 일반 Salary에서 빠진 성과 보너스도 넣는다. 따라서 일반 팀 급여 비교에는 공개 기본급+likely 보너스만, 별도의 apron 시험에는 unlikely 보너스까지 넣는다. 세금선과 비교하는 중간 일반 급여는 연말 사치세 납부액이 아니다. CBA VII §6(j)의 거래 판정에도 단순히 apron용 보너스 전액을 옮겨 쓰지 않는다.

정확한 거래일 Team Salary·인센티브 판정·Teague 차지와 과거 계약 조정은 리그 원장이 아니다. Birch `$3m`은 거래일의 보유 계약을 전액 예산화한 값이며, 뒤에 보고된 방출 후 charge `$2,586,036`보다 `$413,964` 크다. Teague는 취득 뒤 **방출 후 이월 장부에서 재사용한 잠정 `$1,620,564`**를 넣는다. 일반/조정 열에서 같은 금액을 쓰는 것은 확인된 추가 보너스가 없다는 입력의 한계이지 보너스 부재 인증이 아니다. 3/25 정확 incoming charge는 미확인이다. 3/27 방출이 계약 비용을 0으로 만든다고 가정하지 않는다. 기존 [Mozgov cap relief 보도](https://slamonline.com/nba/magic-granted-salary-cap-relief-for-timofey-mozgov/)를 같은 경로로 이월해 중복 가산하지 않지만, 대체 세계의 리그 제외 인증은 없다.

## 같은 최종 명단에 이르는 두 순서

| 상태 | 일반 급여 기재액 | 일반 급여의 세금선 거리 | unlikely 포함 apron 시험액 | apron 거리 | 캠프 4명 연간 기본급 전액 `$4,140,627` 추가 시 apron 거리 |
|---|---:|---:|---:|---:|---:|
| 두 거래 전 | `$130,112,621` | `+$2,514,379` | `$132,112,621` | `+$6,815,379` | `+$2,674,752` |
| Gordon/Clark 거래 먼저, Fournier 잔류 | `$131,330,451` | `+$1,296,549` | `$134,863,784` | `+$4,064,216` | `−$76,411` |
| Fournier/Teague 거래 먼저, Gordon·Clark 잔류 | `$114,283,185` | `+$18,343,815` | `$116,283,185` | `+$22,644,815` | `+$18,504,188` |
| 두 거래 뒤 | `$115,501,015` | `+$17,125,985` | `$119,034,348` | `+$19,893,652` | `+$15,753,025` |

공통 기초액은 Harris·Nnaji를 제외한 11명 기본급·해당 열의 공개 보너스와 Birch `$3m`이다. 거래 전에는 Gordon `$18,136,364`+공개 **unlikely** `$1m`, Clark `$2m`, Fournier `$17m`+공개 likely `$450,000`을 더한다. Gordon 거래 시 Harris `$19,160,714`+공개 unlikely `$2,533,333` 및 대체 Nnaji `$2,193,480`으로 교체한다. Fournier 거래 시 Teague의 잠정 charge `$1,620,564`로 교체한다. 마지막 apron 시험액 `$119,034,348`은 **같은 입력에서 파생된** 기존 4월 장부의 13명 기본급+보너스+Birch/Teague 예산과 일치한다. 이는 내부 일관성 검사이지 독립 리그 검증은 아니다. 4월 이후 Cannady·Franks 등 단기계약을 **3/25에 앞당겨 넣지 않았다**.

**추론:** 공개 금액과 위 조건이 유지된다면 두 거래의 중간 부담은 서로 다르다. Gordon 먼저 경로의 **일반 급여 시험**은 세금선 아래 `$1,296,549`이고, **apron용 조정 급여 시험**은 apron 아래 `$4,064,216`이다. 0보장 캠프 계약 4명의 *연간 기본급 전액*을 추가하면 이 마지막 차액만 `$76,411` 음수가 된다. Birch의 전액 예산과 실제 보고 방출 후 charge의 차이만도 `$413,964`이므로 음수 `$76,411`은 매우 민감한 **가상 스트레스**이며 실제 위반 판정이 아니다. 캠프 계약의 실제 잔존 charge도, Orlando의 hard-cap 트리거도 확정하지 못했다.

[비납세 MLE→납세 MLE 조건부 재분류 규칙](O15F14AK_ORLANDO_2020_MLE_RECLASSIFICATION_GATE.md)도 이 음수 시험을 법적 실패로 올리지 못하게 한다. 공개된 Ennis·Clark 첫해 합계 `$5.3m`과 조건부 납세 MLE `$5.718m`의 `$418,000` 차이는 **재분류 자격의 입력**이며 팀 급여 초과분을 상쇄하는 금액이 아니다. 계약 원문·추가 예외 사용·2020 수정 규칙을 확인해야 적용 가능하다.

**후보 실행 규칙:** 거래 승인 순서의 증거 또는 대체 세계의 명시적 처리 순서가 나오기 전에는 `Gordon 먼저`와 `Fournier 먼저`를 둘 다 남긴다. Fournier 먼저 경로의 낮은 중간 부담은 큰 outgoing 급여를 먼저 제거한 산술 결과이며, 실행 가능성에 관한 새 역사 증거가 아니다. 어느 순서도 작가확정이 아니다. 6(j) 거래 matching과 해당 6(m)(3) apron 검사는 다른 정의를 쓴다. 세금선 거리도 중간 일반 급여의 **조건부 화면**일 뿐 사치세 납부 결론이나 거래 분류의 확정은 아니다. 기존 [3/25~27 등록 자리 증인](O15F14S_ORLANDO_MARCH25_REGISTRATION_BRIDGE.md)의 15+2→14+2는 이 급여 순서 조사 때문에 무효가 되지 않는다.

## 남은 정확 필드

Orlando의 거래 전 과거 방출·상계·보너스·권리/예외·캠프 계약 중 실제 포함액, Mozgov 제외 조건의 대체 세계 적용, 두 거래의 승인/처리 순서, Gordon·Fournier·Harris·Teague의 당일 리그 charge, hard-cap 발생, Boston TPE·픽 가용성을 확인해야 F2를 닫을 수 있다. 이 화면은 **순서 민감성을 특정한 조건부 증인**이며 `F2=HOLD`, F 전체 `0/5`, A `0/3`, K `0/4`, 시즌 최종 선택 없음이다. `PROJECT_FREEZE v0.30 PARTIAL`과 설계/원고 게이트 `CLOSED`를 유지한다. [Claude 반증 수렴](../reviews/R01_O15F14AJ_ORLANDO_ORDER_REVIEW.md)은 수용·기각 범위를 기록한다.
