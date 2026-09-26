# O-15G15AP — Saben Lee FA Amount와 Olynyk 직전 인원 정정

- 기준: `main` `601b6dd`의 [G15AL](O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.md)·[G15AN](O15G15AN_DETROIT_WAIVER_AND_EXCEPTION_BRANCHES.md)·[G15AO](O15G15AO_DETROIT_DISCLOSED_AGREEMENT_CAP_TIMING.md). 판정: `CONDITIONAL_LEDGER_CORRECTED / ACTUAL_RIGHTS_AND_SEQUENCE_HOLD`.
- `PROJECT_FREEZE v0.30 PARTIAL`; 설계·원고 게이트 `CLOSED`. Chicago 2020–21 정확 시즌이 진행 중이며, Detroit 2021–22는 미래 조건 분기다. 신규 작가확정 0건.

## 근거와 조건

[NBA의 2021-08-02 자유계약/QO 목록](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers)은 Saben Lee를 Detroit의 **제한적 자유계약 투웨이 선수**로 열거한다. [2017 NBA–NBPA CBA Article VII §4(d)(7), §4(a)(2)(ii), §4(f)(2)](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)에 따르면, 투웨이를 마친 FA의 Free Agent Amount는 그 시즌 경력 0년 **표준 계약** 최저급이고, RFA의 Team Salary는 FA Amount와 투웨이 QO를 제외한 다른 적용 금액 중 높은 값이다. Team Salary에 포함된 해당 FA는 오프시즌 12명 인원에도 포함된다. 따라서 **Lee 권리를 Olynyk 계약 직전까지 유지했고 아직 Lee 계약을 체결하지 않았다면**, G15AL에는 Lee FA Amount와 인원 한 명이 들어간다. Lee의 실제 권리 포기·리그 통지·계약 접수 시각은 회수되지 않았다.

G15AL의 `$925,258`은 [2021–22 최저 연봉 2차 표](https://www.hoopsrumors.com/2021/08/nba-minimum-salaries-for-2021-22.html)에서 취한 **후보**다. 이 금액의 공식 2021 스케일 독립 확인은 남았다. Lee의 투웨이 QO가 있더라도 이를 표준 계약 FA Amount보다 높은 별도 QO 차지로 자동 더하지 않는다. 3년 Lee 계약의 실제 서명 예외·권리 보유 방식도 확인되지 않았다. CBA Article VII §6(b)(2)의 Non-Bird 최대 첫해 금액은 가능한 **규칙상 경로 후보**일 뿐 실제 적용 증거가 아니다.

## 기존 원장에 미치는 효과

Lee FA Amount `$925,258`은 G15AL이 원래 넣었던 미충원 1자리 `$925,258`과 **같은 금액**이다. 원역사 후보는 `10명+미충원2`에서 `11명+미충원1`, P0-B는 `11명+미충원1`에서 `12명+미충원0`으로 바뀌되 Olynyk 직전 조건부 소계 `$95,844,426` / `$100,052,228`은 유지된다. Lee 권리를 그 시점 전에 실제 포기했다면 기존 인원 계산이 별도 조건 분기로 돌아올 수 있으며, 그 경우 Lee의 후속 3년 계약 수단을 새로 입증해야 한다.

| P0-B의 단독 조건 분기 | 정정된 Olynyk 직전 여지 | 이전 표에서 바뀐 점 |
|---|---:|---|
| Olynyk 먼저 | `+$166,650` | 서명 후 제거할 미충원 차지 없음. 이전의 `+$1,091,908`은 무효. |
| Lyles 계약 또는 예상 급여 통지 먼저 | `-$2,333,350` | 계약 체결 때 미충원 차지 감소 없음. 이전 계약 분기의 `-$1,408,092`는 무효. |
| Lee `$1,489,065` 계약 먼저 | `-$397,157` | FA Amount를 계약 급여로 교체하며 기존 값 유지. |
| Livers `$1,057,260` 계약 먼저 | `-$890,610` | 미충원 차지 감소 없음. 이전의 `+$34,648`은 무효. |
| McGruder 구계약 `$5m` 유지 | `-$4,833,350` | P0-B 인원 13명, 소계 `$105,052,228`. 이전 `-$3,908,092`는 무효. |

원역사 후보에서 McGruder를 다시 넣으면 12명이 되어 마지막 미충원 차지 한 자리가 사라진다. 이 분기는 조건부 소계 `$99,919,168`, Olynyk 직전 여지 `+$299,710`이다. 실제 Detroit의 완전 Team Salary, 다른 FA/예외 차지, McGruder 웨이버 효력, NBA 합의 통지·접수 순서를 이 표가 증명하지 않는다.

Lee 첫해 `$1,489,065` 역시 [G15AJ의 2차 계약표](O15G15AJ_DETROIT_AUG6_NAMED_SALARY_LEDGER.md)에서 상속한 **후보**다. Lee 서명 분기의 증가액은 기존 FA Amount와 후보 계약 급여의 차이 `$1,489,065−$925,258=$563,807`이며, 이미 12명인 P0-B에서는 미충원 차지를 더 제거하지 않는다. 위 McGruder 분기는 G15AL의 **구계약 차지 제거·인원 제외** 기준을 G15AN의 **비보장 `$5m` 차지 유지·인원 포함** 가정으로 바꾼 시험이다.

## 도구 검증과 다음 게이트

| 단계 | 이번 실행과 증거 한계 |
|---|---|
| Antigravity CLI | 절대 경로의 `agy.exe` v1.2.11로 `read_url_content→view_file` 읽기 전용 호출에 성공했다. 저장된 NBA 기사 본문에 제한적 투웨이 FA 목록과 `Saben Lee (DET)`가 실제 포함됐음을 확인했다. 같은 NBA 기사 재독이며 독립 원자료 추가는 아니다. |
| NotebookLM CLI | 별도 작업실의 업로드된 **2017 CBA PDF 한 출처**에 한정 질의해 §4(d)(7) FA Amount, 투웨이 QO 제외, §4(f)(2) 인원 처리를 재독했다. 실제 Detroit 장부를 알려주는 출처가 아니다. |
| Codex | 공식 NBA 명단과 CBA 원문을 직접 대조하고 [G15AL 검사기](../tools/check_o15g15al_detroit_roster_charge.py)·[G15AN 검사기](../tools/check_o15g15an_detroit_waiver_branches.py)로 조건부 산술을 재계산했다. |
| Claude | [문서 단독 반증 기록](../reviews/R01_O15G15AP_LEE_HOLD_BLIND.md)에 별도 기록한다. 원문 독립 확인으로 세지 않는다. |

**사실**: NBA 명단상 Lee 제한적 투웨이 FA, CBA의 FA Amount·인원 규칙. **추론**: Lee 권리 존속과 금액 후보가 맞으면 위 인원·산술. **후보**: 실제 8/6 권리/합의/서명 시각, 계약 예외, 다른 차지와 P0-B 동일 거래 경로. **작가확정**: 0건.

다음에는 실제 8/6 리그 Team Salary·권리 포기 및 계약 접수 순서와 Lee의 3년 계약 수단을 회수한다. 그 뒤 Olynyk→Lyles/Lee/Livers/Frank→8/10 Joseph를 한 연속 원장으로 검증한다. Chicago 정확 시즌, G14, G16/G17은 `HOLD`; 7개 매크로 게이트 1완료·1진행·5대기, 남은 큰 작업 6개다.
