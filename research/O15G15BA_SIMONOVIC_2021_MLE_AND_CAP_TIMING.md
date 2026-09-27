# O-15G15BA — Simonović의 2021 계약 기간과 Caruso 후 MLE·cap 순서

- 기준: `main` `40d744a`, [G15AZ 2021 합류 자리](O15G15AZ_SIMONOVIC_2021_ACTIVATION_SLOT_GATE.md), [G8 SQ1 계약 순서/JSON](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md). 판정: `FIRST_YEAR_MLE_FITS / THREE_YEAR_LEGALITY_AND_COMPLETE_CAP_HOLD`.
- 2020 Chicago #44 Simonović **지명권**은 이미 작가확정. 2021 NBA 합류·계약 기간·급여·선수 동의는 아니다. 아래 가격은 원역사 비교값을 한 변수로 넣은 **조건부 실험**이다.

## 원역사 자료의 서로 다른 증명력

| 자료 | 확인되는 범위 | 사용할 수 없는 결론 |
|---|---|---|
| [Bulls 2021-08-18 계약 발표](https://www.nba.com/bulls/news/bulls-sign-rookies-dosunmu-and-simonovic) | #44 Simonović와 원역사 계약 발표. 구단은 세부 조건 비공개. | 8/18을 법적 효력일·대체 Chicago 계약일로 만들거나 달러/예외를 구단 인증으로 표시하지 않음. |
| [Bulls 2022-07-06 회고](https://www.nba.com/bulls/news/marko-simonovic-looks-to-impress-during-summer-league-with-added-muscle-experience) | 원역사 계약이 **3년, 2023–24까지**라고 구단 기사에서 설명. | 대체 세계에서 같은 3년 계약을 수락했다는 증거가 아님. |
| [SalarySwish 계약표](https://www.salaryswish.com/players/marko-simonovic) | **2차 기록:** 2021–22 `$925,258`, 2022–23 `$1,563,518` 각각 보장, 2023–24 `$1,836,096` 비보장, 3년 총 `$4,324,872`, MLE 사용·8/13 서명일 표시. | 구단이 금액/보장·MLE 사용을 공표한 적 없음. 2차 사이트의 8/13과 구단 발표 8/18은 서로 다른 사건 시계이며 실제 접수·효력 시각 인증도 아님. |
| [NBA 2021–22 cap·예외 공식 발표](https://pr.nba.com/nba-salary-cap-for-2021-22-season-set-at-112-414-million/), [당시 CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf), [NBPA의 2017–23 CBA 원문](https://www.nbpa.com/cba) | 2021 비납세 MLE 첫해 총액 `$9,536,000`. 해당 예외는 **복수 선수 첫해 급여 합산**과 최대 4시즌, minimum exception은 최대 2시즌. NTMLE 사용의 그해 apron 제한. CBA Article VII §5(c)(1)의 일반 연간 인상 한도와 Article II §6의 최저급여·deemed amendment 조항은 별도로 대조해야 함. | 특정 팀의 미공개 실제 cap sheet, Marko의 3년 예외 방식, 가상 계약 승인까지 직접 인증하지 않음. |

## G8 SQ1에 원역사 **급여만** 넣는 한 변수 시험

G8은 Caruso에게 첫해 `$8,600,000`을 비납세 MLE로 쓰는 **제안**이고 Markkanen Bird 재계약·FA 권리 정리 뒤 #39 Wieskamp 2년 일반 최소계약을 두어 최종 일반 15명이다. [G15AZ](O15G15AZ_SIMONOVIC_2021_ACTIVATION_SLOT_GATE.md)의 `S1`은 #39를 투웨이로 바꾸고 Simonović에게 일반 15번째 자리를 주는 별도 후보, `S2`는 #39를 미서명으로 두는 후보이다. Dotson/Cook의 두 투웨이 자리는 [G15AY](O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md)에 따라 다시 배정해야 한다. 아래의 `M1=$925,258`, `M2=$1,563,518`, `M3=$1,836,096`은 SalarySwish **원역사 2차 비교값**이며 가상 합의 금액은 `null`이다.

| 시도할 계약 수단 | G8에 끼워 넣을 시점 | 기간·자리 검사 | 남는 검문 |
|---|---|---|---|
| `N3` — 비납세 MLE 잔액, 3년 | Caruso NTMLE 사용 **뒤**, G8의 `RENOUNCE_UNUSED_FA_AND_APPLICABLE_EXCEPTIONS` **전** | `$9,536,000 − $8,600,000 = $936,000`; 여기에 `M1=$925,258`을 쓰면 두 선수 첫해 합계 `$9,525,258`, 명목 잔액 **`$10,742`**. CBA 101상 NTMLE는 최대 4시즌이라 3년 자체는 기간 한도 안이다. | 다른 NTMLE 사용자·Caruso 실제 제안액/보너스·Marko의 예외 적격성·당시 Team Salary/rights·계약의 해마다 최소급/상승 규칙·선수 동의 `HOLD`. 1년차 합산만으로 3년 계약 전체 적법성 PASS는 아님. |
| `C3` — renounce 뒤 cap 공간, 3년 | G8의 FA/예외 정리 **뒤**, 다른 최소계약 전 | G8의 `R=0` 상단 예시는 #39 서명 전 **일반 11명+미충원 1개**, normal-cap room `$11,369,971`. `M1`이 그 미충원 차지 `$925,258`과 같으면 자리 12·표시된 중간 합계는 `$101,044,029`로 동일. | 실제 `R_normal`·권리/예외 포기·cap 공간 보유·3년 계약 조건이 `HOLD`. 이미 Caruso에 사용한 MLE의 그해 apron 제한은 사라지지 않는다. 남은 MLE를 사후 재생하지 않는다. |
| `MIN2` — minimum exception, 최대 2년 | 정리 뒤 최소계약 단계 | 첫해 `M1`과 둘째 해 `M2`를 **비교값**으로 쓰는 2년 제안은 기간상 가능 후보. 세 번째 해는 없다. | 선수의 2년 수락/보장·차년도 급여·등록 및 2023 재협상 `HOLD`. 구단 원역사 3년 계약을 2년으로 다시 이름 붙이지 않는다. |

`N3`은 남은 MLE가 **사라지기 전 사용**하는 길이고 `C3`는 MLE 잔액 없이 **새 cap 공간으로** 3년을 검토하는 길이다. 두 수단을 같은 계약의 중복 예외로 합산하지 않는다. `C3`의 `$11,369,971`은 G8의 다른 순증 `R_normal=0` 예시에서만 나온 **계약 직전 room**이며 실제 Chicago cap 여유가 아니다. `MIN2`는 3년을 주지 않는 다른 선수 거래다. 어느 경우든 `S1/S2`의 15번째 일반 자리는 Simonović에게 배정하고 #39 일반계약 급여 행을 지운 뒤 권리/투웨이 상태를 처리해야 한다.

**3년 급여 법규 별도 검문:** `M2−M1=$638,260`은 첫해 `$925,258`의 5%(`$46,262.90`)를 크게 넘는다. [2017–23 CBA Article VII §5(c)(1)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 일반 계약의 연간 급여 인상을 첫해 급여의 5% 이내로 제한한다. 반면 Article II §6(a),(d),(f)는 계약 시작 연도의 최저급여표 적용, 향후 최저급여 미달 시 자동 수정, 최저급여 연동 계약 문구를 둔다. [G15BB 원문 표 역산](O15G15BB_2021_MINIMUM_SALARY_SCALE_CROSSCHECK.md)에서 2차 계약표의 **세 해 금액 모두 2021 계약 시작 연도 최저급여표 경로와 정확히 일치**함을 확인했다. 따라서 `$638,260`을 임의 협상한 일반 5% 인상으로 해석하는 반론은 성립하지 않는다. 다만 원역사 계약서·실제 사용 예외가 공개되지 않았고 대체 Chicago의 `N3/C3` 시점·전체 Team Salary도 미완성이므로 **개별 3년 계약의 최종 적법성 `HOLD`**다. 첫해 MLE 산술과 최저급여표 재구성은 각각 검증된 제한적 결론이다.

G8 SQ1 상단 예시에서 Caruso 뒤 일반 10, Markkanen Bird 뒤 일반 11이다. `N3`을 Markkanen 뒤·renounce 전에 12번째 일반로 끼워 넣고 `M1=$925,258`이라 가정하면 renounce 뒤 미충원 차지는 **0**이고 normal-cap 표시 합계는 `S1/S2`와 G8의 원래 #39 일반 경로 모두 `$101,044,029`이다. 원래 G8은 같은 위치에 **11명+미충원 `$925,258`**을 두고 다음 #39 일반계약이 이를 대체한다. 이 동액은 실제 급여/선수 동의나 `R=0`을 확정하지 않으며, 누락된 다른 계약까지 합친 최종 Team Salary PASS가 아니다.

같은 **첫해 급여** `M1=$925,258`만 #39의 G8 첫해 `$925,258`과 교환하면 알려진 최종 apron 합계 예시 `$106,862,083`은 바뀌지 않는다. 같은 **둘째 해 급여** `M2=$1,563,518`을 기존 #39 둘째 해 `$1,563,518`과 바꾸면 G8 RT1~RT4 192조건의 알려진 급여 부분합도 **각각 차이 0**이다. 이는 2022–23 #39 투웨이 재계약·다른 명단 사용자·Simonović 3년차 권리/급여·실제 `R_2022`가 같다는 말이 아니다. `N3/C3`의 2023–24 `$1,836,096`은 2차 자료상 비보장·방출 조건을 따로 검토해야 하는 **새 후속 자리**이며 2021–22/2022–23의 숫자 동액으로 장기 비용을 지우지 않는다. G1A 정상일 10인 분표에는 #39/Simonović 모두 없으므로 실제 NBA 분·G League 배정과 센터/윙 개발 대가도 `HOLD`다.

## 판정·도구 계보

- **사실:** 2020 #44 지명권 확정; 원역사 Bulls 계약 발표 및 구단 후속 기사 3년 설명; NBA의 2021 MLE 금액과 당시 CBA 101의 계약기간·합산 규칙.
- **추론:** G8의 Caruso `$8.6m`과 `M1` 비교값을 NTMLE에 넣으면 잔액 `$10,742`. `M1/M2`가 기존 #39 급여와 동액이면 **그 두 해** 알려진 급여 부분합 차이는 0이지만 계약 기간·자리는 다르다.
- **후보:** `S1/S2` 안의 `N3`, `C3`, `MIN2`. G8 `SQ1`의 Wieskamp 일반계약은 기존 주 비교안으로 남는다.
- **작가확정:** 신규 0건. 2021 계약 종류·기간·대체 선수를 고르지 않았다.

Codex는 NBA cap/CBA 원문과 G8 SQ1 JSON, Bulls 발표의 검색 가능한 텍스트, SalarySwish 2차 표를 분리했다. NotebookLM CLI는 SalarySwish URL을 소스 `df7bdaac-cfce-4a5c-8009-883d5df5f51f`로 추가해 **그 한 출처만** 실제 인용했다. 기존 Bulls URL은 목록에 보여도 질의에는 본문이 없어 구단 계약 발표를 NotebookLM으로 검증하지 못했다. 같은 SalarySwish 재독은 독립 원자료 증가가 아니다. Antigravity CLI의 Bulls 2022 URL 읽기 전용 요청은 `429 Individual quota reached`로 끝나 본문 0건이다. Claude CLI의 [제한 반증](../reviews/R01_O15G15BA_SIMONOVIC_MLE_REBUTTAL.md)은 5% 인상 한도와 최저급여 자동 수정의 접점을 미해결로 지목했고, 후속 G15BB가 **최저급여표 금액 경로**를 직접 역산했다. `THREE_YEAR_LEGALITY_HOLD`는 개별 계약 형식/예외/Team Salary에만 남는다. 새 source-blind `NOT_RUN`. D1 F1~F5 PASS 0/5·A1~A3 0/3·K 0/4, G1A 동의·D2 실제 계약/시즌·G16/G17 `HOLD`. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 원고 없음.
