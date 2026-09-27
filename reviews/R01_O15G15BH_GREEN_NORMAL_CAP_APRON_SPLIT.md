# R01 O-15G15BH — Green 미서명 장부의 일반 cap/apron 분리 검토

- 기준 `main` `8554ed2` (PR #260). 변경 대상: [G8 계산기](../tools/build_chicago_2021_23_contract_sequence.py), [G8 결과](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [G15BF](../research/O15G15BF_GREEN_2021_RFA_ORDER_AND_QO_CHARGE.md), [G15BG](../research/O15G15BG_GREEN_MINIMUM_CONTRACT_FA_AMOUNT.md).
- 결론: `CBA_RULE_CORRECTION_PASS / CONDITIONAL_NUMERIC_PASS / REAL_FILING_HOLD / G16_NOT_PASS`.

## 발견과 수정

[2017–23 CBA Article VII §4(a)(2)(ii)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 미서명 RFA의 일반 Team Salary를 `max(F,Q,N)`으로 정의한다. 그러나 같은 CBA §6(m)(3)(D)는 NTMLE 등에서 쓰는 apron 조정 Team Salary에서 `F`를 **제외**하고 유효 QO 또는 First Refusal Exercise Notice 중 큰 금액을 넣는다. 보너스 없는 조건부 수치에서는 Green의 일반 cap 항목과 apron 항목을 각각 `max(F,Q,N)`과 `max(Q,N)`으로 모델링해야 한다. 기존 G8은 ESPN의 높은 `F=$2,056,061` 스트레스를 두 항목 모두에 넣어 Caruso 직전 apron 여유도 `$386,883` 줄였는데, `Q=$1,897,476,N=0` 전제라면 apron 감소는 `$228,298`이다. 일반 cap 감소 `$386,883`은 그대로다.

| 조건부 입력 | Green 일반 cap | Green apron | 조기 Green 서명 대비 Caruso 직전 일반 cap 여유 | 같은 시점 apron 여유 |
|---|---:|---:|---:|---:|
| 2년 경력 QO 후보, `F<Q,N=0` | `$1,897,476` | `$1,897,476` | `−$228,298` | `−$228,298` |
| 3년 경력 QO 계산기 오입력 스트레스 | `$1,929,217` | `$1,929,217` | `−$260,039` | `−$260,039` |
| ESPN 높은 `F` 스트레스, 2년 경력 `Q`, `N=0` | `$2,056,061` | `$1,897,476` | `−$386,883` | `−$228,298` |

세 스트레스의 후행 최종 제안 급여와 최종 apron 순증 한도 `$36,139,917`은 그대로다. 이는 동일한 2년 minimum 계약으로 **나중에 실제 서명한다는 모델 전제** 때문이며, 그 선수 동의나 법적 사건은 증명하지 않는다. QO/통지의 실제 금액·유효 시각, 미포함 순증 `R`, 원역사와 대체 세계 계약 원본은 `HOLD`다. QO/통지에 Unlikely Bonuses가 있으면 §6(m)(3)(D)에 따라 apron 항목을 다시 계산한다.

## Research/Verification Layer v2 판독

- **Codex:** CBA §4(a)(2)(ii)와 §6(m)(3)(D) 원문을 직접 대조했다. 생성기 입력을 일반 cap/apron 쌍으로 분리하고 결과 JSON을 재생성했다. UTF-8 환경에서 계약 순서 검사 8개와 생성 JSON 재현 검사, 문서 링크 검사를 통과했다. 이는 조건부 모델 내부 검증이다.
- **NotebookLM CLI:** CBA 전체 PDF **한 출처** `fb655448-b9dc-49ba-95ec-ff26ca9ed3f6`만 질의한 대화 `546b4bb9-7dcd-471f-b575-3cb374ada363`는 위 두 조항과 `$2,056,061/$1,897,476` 분리를 인용했다. Codex와 **같은 CBA 원문**을 다시 읽은 것이므로 새 독립 원자료가 아니다.
- **Antigravity CLI:** 설치된 `agy.exe`에 CBA PDF를 `read_url_content→view_file`로 읽도록 요청했으나 50초 제한 뒤 `status=SUCCESS,response=""`, 실제 본문 증거 0건이다. `AGY_SOURCE_READ_FAILED`.
- **Claude 도구 없는 반증:** 산술 차액 `$158,585`는 맞았으나 원문을 읽지 못해 §6(m)(3)(D)의 제외 문구를 확인하지 못했다. `Q`를 120% 급여일 수 있다고 추측한 주장은 [G15BF의 CBA QO 검산](../research/O15G15BF_GREEN_2021_RFA_ORDER_AND_QO_CHARGE.md)보다 약하고 근거가 없어서 기각한다. 조기/후행 **중간 장부 차이**를 두 경로의 **최종 급여 차이** 반례로 읽은 것도 다른 시점의 비교이므로 기각한다. 실제 접수 서류 필요성만 `HOLD`로 수용한다.
- **Source-blind:** 결과표만 준 별도 요청에 Claude가 표가 없다고 응답해 결과를 처리하지 못했다. `NOT_RUN`; 독립 맹점 PASS로 세지 않는다.

**사실:** CBA의 두 Team Salary 정의. **추론:** 보너스 없는 가정에서 ESPN의 높은 `F` 스트레스는 일반 cap에만 추가된다. **후보:** Green 후행 서명 3개 수치 쌍. **작가확정:** 신규 0건. D1 F1~F5 0/5·A1~A3 0/3·네 K 종료 0/4, G16/G17 `HOLD`, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.
