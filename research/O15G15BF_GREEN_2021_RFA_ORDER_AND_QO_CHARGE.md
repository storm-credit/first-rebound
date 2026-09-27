# O-15G15BF — Green 제한적 FA와 SQ1의 Caruso 선후 장부

- 기준: `main` `113118f` (PR #256), [G8 조건부 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [G1A 15명 제안](../simulation/CHICAGO_2021_23_CONTINUATION.md). 판정: `2021_GREEN_RFA_VERIFIED / LATE_SIGNING_TEAM_SALARY_HOLD / NO_NEW_CONTRACT_LOCK`.
- D1에서 승인된 Theis·Green **3월 선수 이동 방향**과 2021 여름 Green **재계약 수락·서명일**은 별개다. D1 F1의 정확 실행이 열려 있으므로 대체 Chicago의 Green FA 권리도 해당 선행 사건에 조건부다.

## 실제 역사와 규칙의 경계

| 사건·자료 | 확인 범위 | 대체 세계에서 확정하지 않을 것 |
|---|---|---|
| [NBA의 2021-08-02 QO 명단](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers) | Chicago의 Javonte Green을 QO 발급을 받은 제한적 FA에 포함한다. QO 수락·다년 재계약·타 팀 offer sheet는 다른 결과라고 설명한다. | Chicago가 대체 세계에서도 같은 QO를 언제 냈는지, Caruso 계약 때까지 철회하지 않았는지. |
| [NBA 2021 FA 일정](https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency) | 8/2 18:00 ET 협상 시작, 8/6 12:01 ET 일반 FA 서명 가능. | 8/2 협상을 완료 계약으로 취급하지 않는다. |
| [Chicago Caruso 8/10 발표](https://www.nba.com/bulls/news/bulls-sign-alex-caruso)와 [Green 8/19 공동 발표](https://www.nba.com/bulls/news/bulls-sign-free-agents-bradley-green-and-dotson) | 원역사 **발표 순서**는 Caruso→Green. 두 발표는 급여·예외·정확 법적 효력일을 공개하지 않는다. | 발표일만으로 원역사의 서명 원장이나 대체 Chicago의 계약 순서를 잠그지 않는다. |
| [2017–23 CBA Article VII §4(a)(2)(ii), §4(d)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) | 제한적 Veteran FA의 미서명 Team Salary는 `max(Free Agent Amount, outstanding QO salary, First Refusal Exercise Notice salary)`다. §4(d)의 FA 보류액은 재계약·타 팀 계약·권리 포기 때까지 원 소속 팀 장부에 남는다. | QO 발급을 곧 QO **수락**으로, 2년 minimum 제안을 실제 계약으로 바꾸지 않는다. |

## SQ1의 두 시간 경로

현재 [G8 입력](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE_INPUTS.json)은 Duarte의 조건부 120% rookie-scale 서명과 Green의 **2년 minimum 재계약을 Caruso보다 앞에** 둔다. 따라서 G8의 `first_contract=Caruso`는 **그 진입 상태 이후 첫 FA 경로 계약**을 뜻한다. Green에게 Caruso보다 이른 대체 서명을 요청하는 선택은 법적 필수가 아니라 **모델 전제·선수 동의 사건**이다.

| 시간 경로 | Caruso 직전 Green의 일반계약 자리 | 그 시점 Green Team Salary 항목 | 이후 비용 |
|---|---|---|---|
| `SQ1-GREEN-EARLY` — 현재 G8 계산 | 서명된 1자리 | 제안 급여 `$1,669,178` **2차 비교값** | 이미 검산한 240조건만 이 경로에 적용. Green의 조기 수락·신고일 `HOLD`. |
| `SQ1-GREEN-LATE-QO` — 조건부 수치 반례 | FA 권리만 있으며 일반계약 1자리로 등록하지 않음 | QO가 여전히 유효하다면 `max(F,Q,N)`, `F=Free Agent Amount`, `Q=outstanding QO`, `N=First Refusal Exercise Notice`. FA는 12명 미달 차지 검사에서 CBA 규칙대로 셀 수 있지만 일반 명단에 자동 입단하지 않는다. | 아래 세 **가정상 실효 보류액**으로 Caruso 시점 cap/apron와 NTMLE 경로를 재계산. 뒤에 같은 2년 계약이 실제 체결된다면 최종 급여 비교는 현재 G8으로 돌아오지만 중간 순서는 별개다. |
| `SQ1-GREEN-QO-ACCEPT` | QO 수락 시 계약자 | 1시즌 QO 급여 | G8의 2년 minimum 및 2022–23 Green 잔류 비용을 재사용할 수 없다. |

숫자 민감도만 보면, [Green 2차 계약표](https://www.salaryswish.com/players/javonte-green)는 2020–21 급여 `$1,517,981`, 원역사 2021–22 계약 첫해 `$1,669,178`, 8/11 서명일 표기를 제시한다. 이 2차 표기일은 구단의 Caruso 8/10 발표 뒤이지만, 두 자료의 날짜 종류가 달라 법적 선후의 확증은 아니다. [Hoops Rumors의 6/28 사전 전망](https://www.hoopsrumors.com/2021/06/2021-nba-offseason-preview-chicago-bulls.html)은 QO와 보류액을 각각 `$1,897,476`로 **예측**했다. 앞 급여의 125%는 반올림하여 `$1,897,476`이며 [CBA Article XI §1(c)(iv)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)의 기본 비교식과 맞는다. 이 QO가 실제 유효한 경로라면 `N`이 없어도 미서명 항목은 **최소 `$1,897,476`**, 현재 G8의 서명 급여보다 **최소 `$228,298` 높다**. 이는 **조건부 Caruso 직전 차이**이며 전체 팀 장부·최종 apron 차액이 아니다.

그러나 [SalarySwish의 Green QO 계산기](https://www.salaryswish.com/qualifying-offer-calculator/javonte-green/47)는 `Years of Service=3`과 해당 minimum `$1,729,217`을 입력해 QO `$1,929,217`을 반환하고, 선수 페이지의 QO도 그 수치다. [NBA 선수 이력](https://www.nba.com/player/1629750/javonte-green/bio)은 2021 전 NBA 시즌을 2019–20·2020–21 **두 시즌**으로 나열한다. [2017 CBA Exhibit C](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)의 **2년 경력** 첫해 최저급여 `$1,471,382`를 [G15BB의 공식 cap 배수 검산](O15G15BB_2021_MINIMUM_SALARY_SCALE_CROSSCHECK.md) 방식으로 환산하면 2021년 약 `$1.669m`이며, [2차 계약표](https://www.salaryswish.com/players/javonte-green)의 첫해 최저급여 `$1,669,178`과 달러 단위 이내다. 여기에 `$200,000`을 더해도 앞의 125% 급여 기준 `$1,897,476`보다 작다. 따라서 **2021년 2년 NBA 경력 전제의 CBA 계산은 `$1,897,476`을 지지**하고, `$1,929,217`은 계산기 3년 입력의 스트레스값으로만 남긴다. 실제 QO 계약 원문 및 정확 반올림 원장은 없어 리그 접수액을 확정하지 않는다. [ESPN의 별도 FA 보류액 표기](https://www.espn.com/nba/insider/story/_/id/31733302/offseason-moves-chicago-bulls-contract-decisions-zach-lavine-lauri-markkanen)는 `$2,056,061`로 QO 계산치보다 높다. 정확 `F`, 실제 `N`, QO 철회 여부, 선수 수락/신고 시각은 미확인이다.

## 후행 서명 수치 검문 — G8의 180개 추가 민감도

[G8 계산 결과](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json)의 `Green_late_SQ1_sensitivities`는 `SQ1×주인공 급여30×Young 보너스2×가정상 실효 Green 보류액3=180`개 경로다. `$1,897,476`은 2년 경력 QO 계산을 따르며 `F/N`이 이를 넘지 않는 **가정**, `$1,929,217`은 계산기의 잘못된 3년 경력 입력을 일부러 유지한 스트레스, `$2,056,061`은 ESPN의 2차 FA 보류액 후보를 실효값으로 놓은 스트레스다. 실제 `max(F,Q,N)`이 더 높으면 입력을 올려 다시 계산해야 한다.

| 가정한 Caruso 전 Green 실효 보류액 | Green 조기 서명 대비 Caruso 전 cap/apron 여유 차이 | 60개 급여·보너스 조건의 `R=0` 수치 검사 | 최악 조건 최종 apron 순증 한도 |
|---|---:|---:|---:|
| `$1,897,476` | `−$228,298` | 60/60 조건부 성립 | `$36,139,917` |
| `$1,929,217` | `−$260,039` | 60/60 조건부 성립 | `$36,139,917` |
| `$2,056,061` | `−$386,883` | 60/60 조건부 성립 | `$36,139,917` |

후행 경로에서는 진입 일반계약이 9→8자리이고 Green FA 항목이 한 개 늘어 `12명 미달` 공석 수는 그대로다. Caruso NTMLE 뒤 Markkanen Bird·불필요 FA 정리·Green **동일한** 2년 최소계약 순서로 계산했으므로 최종 알려진 총급여도 조기 경로와 같다. 이 입력 범위에서는 마지막 단계가 apron 순증 한도를 묶는다. `R=0`은 미포함 비용이 실제로 0이라는 증거가 아니고, QO 발급이 대체 Chicago에서 계속 유효한지와 Green의 서명 동의도 증명하지 않는다. 따라서 180/180은 **조건부 산술**, 정확 실행 PASS는 0건이다.

**사실:** NBA의 Green QO 발급 명단, Caruso/Green 구단 발표, CBA의 `max(F,Q,N)` 규칙. **추론:** 원역사의 발표 순서와 G8의 가상 입력 순서가 다르므로 조기 Green 서명에는 별도 선수·리그 사건이 필요하다. **후보:** `EARLY/LATE-QO/QO-ACCEPT`의 비교 경로; 위 달러는 2차 자료를 이용한 조건부 민감도. **작가확정:** 이번 추가 0건. Green·Caruso 실제 대체 계약, #10/#39, D1 정확 시즌은 `HOLD`다.

## Research/Verification Layer v2 실행 범위

- **Codex:** NBA QO 명단·구단 발표·2017 CBA Article VII/XI 원문과 G8 입력/출력을 직접 대조했다. 기존 240조건은 Green 조기 서명 한 경로에만 성립한다.
- **NotebookLM CLI:** 비정본 작업실 `303ffd55-e019-476a-9ae3-8dc0e32fe11f`의 NBA QO 한 출처와 2017 CBA 전체 PDF 한 출처만 지정한 대화 `52c56e84-e6b4-4266-acba-7430f723bd8f`는 RFA 및 `max(F,Q,N)`를 연결했고 **정확 Green 금액 부재**를 명시했다. SalarySwish 두 페이지·Hoops Rumors의 **별도 2차 세 출처** 제한 질의는 `$1,897,476/$1,929,217` QO와 보류액 충돌을 추출했다. 같은 원문의 재분석이지 독립 자료 증가가 아니다. 계산기 3년 기준을 검증된 2021 선수 연수로 승격하지 않았다.
- **Antigravity CLI:** 절대경로 `agy.exe`에 NBA QO 명단과 Chicago Green 발표를 `read_url_content→view_file`로 읽도록 요청했다. 45초 제한 뒤 `status=SUCCESS`이나 빈 응답·본문 증거 0건이어서 `AGY_SOURCE_READ_FAILED`다.
- **Claude 독립 반증 / source-blind:** 핵심 주장만 전달해 도구 없는 짧은 반증을 요청했지만 약 1분 동안 응답 본문이 없어 중단했다. 유효한 반증 결과와 source-blind는 `NOT_RUN`; G16/G17 PASS를 대체하지 않는다.

D1 F1~F5 PASS 0/5·A1~A3 최종 채택 0/3·네 K 종료 0/4. 매크로 7개 중 1완료·1진행·5대기, 진행 중 포함 6개 남음. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED` 유지.
