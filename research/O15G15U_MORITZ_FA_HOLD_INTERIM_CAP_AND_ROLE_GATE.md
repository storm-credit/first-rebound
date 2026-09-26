# O-15G15U — Moritz FA hold의 8월 중간 비용과 빅맨 분 게이트

- 시작점: `main` `74af4b7` / PR #204. [G15T의 Moritz M1/M0-H/M0-R](O15G15T_MORITZ_2021_AGREEMENT_SIGNING_AND_HOLD_BRANCH.md) 중 **8/6 Lopez 계약 전후**에 비어 있던 금액을 채운다. G15S의 다른 선수·계약은 바꾸지 않는다.
- 상태: `CBA_FA_HOLD_AND_DISCLOSED_AGREEMENT_RULE_VERIFIED / EXACT_2021_QO_RENOUNCE_DISCLOSURE_EVENT_HOLD / ALTERNATE_TEAM_SALARY_HOLD`. 출전 분과 대체 계약 선택은 확정하지 않는다.

## 1. QO와 UFA cap hold를 별개로 다룬다

[2021년에 적용된 2017 NBA–NBPA CBA Article VII §4(a)(2)(i), §4(d)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 이전 팀의 **UFA**도 재계약·타 팀 서명·권리 포기 전에는 그 팀의 Team Salary에 Free Agent Amount가 들어간다고 정한다. **UFA라는 분류만으로 hold가 0이 되지 않는다.** §4(d)(4)는 직전 급여가 적용 최저급 이하였던 FA의 금액에 리그 환급을 제외한 해당 시즌 최저급 부분을 적용한다. [Moritz의 2021-04-27 원역사 Orlando 잔여시즌 계약표](https://www.salaryswish.com/players/moritz-wagner)는 기본급·cap hit **$221,995**, 2021–22 FA hold **$1,669,178**을 표시한다. 이는 [G15O](O15G15O_ORLANDO_2021_FA_SIGNINGS_AND_HOLDS.md)에서 분리한 **비공식 숫자**이며 CBA 원칙과 방향이 맞지만, 공개 리그의 Moritz 개인 cap sheet가 없어 정확 금액은 조건부다.

같은 CBA §4(g)(1)는 팀이 **서면으로 권리를 포기**할 수 있고, 그 뒤에도 **Minimum Player Salary Exception**으로 그 선수를 재계약할 수 있다고 규정한다. 따라서 `8/6 이전 적법 renounce → 8/23 최저급 재계약`은 **제도상 검토 가능한 순서**다. 원역사 Orlando가 그 순서를 실제 택했다는 기록은 확보하지 못했다. §4(g)(2)는 **아직 유효한 QO가 있으면 권리 포기할 수 없다**고 정한다. 또 §4(a)(2)(ii)는 RFA일 경우 해당 Free Agent Amount와 유효한 QO 급여 등 중 더 큰 금액을 Team Salary에 반영한다. [NBA 드래프트 전 Orlando 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)의 Moritz `UFA` 표기와 [G15R](O15G15R_ORLANDO_HERBERT_MINIMUM_MLE_AND_MORITZ_UFA.md)의 QO 미확보를 유지한다. SalarySwish의 **$1,989,256 QO 표기**는 잠재 자격/수치일 뿐 **실제 발행·잔존의 증거가 아니다**.

**합의 통지의 별도 경계:** [2017 CBA Article II §13(a)(i)·(ii), Article VII §4(a)(1)(iv)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 고용 조건에 관한 구두·서면 합의를 NBA에 즉시 통지하고, 통지된 합의의 예상 급여도 Team Salary에 반영하도록 한다. 구두 합의는 정식 계약서 실행 전 **선수·팀에 구속력이 있는 계약이라는 뜻이 아니다**. [8/4 NBA의 기자 인용 합의 보도](https://www.nba.com/news/nba-offseason-2021-aug-4-roundup)는 리그에 실제로 통지된 합의인지, 당시 경제 조건이 8/23 계약과 같은지 증명하지 않는다. 따라서 아래 H/R 두 열은 **8/6에 별도 통지된 예상 급여가 없다는 조건**에서만 비교한다. 통지된 합의가 있었다면 권리 포기로 앞 FA hold만 제거해 8/6 비용을 낮출 수 있다고 단정하지 않는다.

## 2. 같은 8/6 Lopez 계약의 두 금액 경로

공동 조건: G15S의 **공통 8명+Vučević/Aminu/Nnaji+Bacon**, Mobley3의 **미서명 1R hold $8,075,160**, Lopez 원역사식 8/6 계약 $5m, Herbert는 미서명, 그 외 선수·계약·FA 권리 사건은 **표 밖**이다. Bacon B0는 **8/8 요청 뒤 실제 이탈 완료 시점**에만 차감한다. `H`는 Orlando가 Moritz의 4/27 선행 계약 및 FA 권리를 보유해 비공식 표시 hold **$1,669,178**이 살아 있다는 조건, `R`은 그 전에 적법하게 권리를 포기해 이 hold가 제거됐다는 조건이다. **H/R 비교에는 리그에 통지된 별도 Moritz 예상 급여가 없다는 조건도 필요하다.** 양 경로 모두 Moritz의 **표준계약 자리는 서명 전 0**이다.

| 점검점 | G15S 열거 계약 + Mobley hold, Moritz 제외 | **H:** Moritz FA hold 유지 | **R:** 앞 hold 적법 제거 |
|---|---:|---:|---:|
| **8/3** 새 cap 발효 뒤 | $130,863,369 | **$132,532,547** | **$130,863,369** |
| **8/6** Lopez $5m 계약 채택 직후 | $135,863,369 | **$137,532,547** | **$135,863,369** |
| **8/8 요청 뒤** Bacon B0 이탈 완료 시 | $134,039,366 | **$135,708,544** | **$134,039,366** |
| **8/23** Moritz 원역사식 $1,729,217에 새로 서명한 경우 | 계약 비용으로 대체 | **$135,768,583** | **$135,768,583** |

`8/6 H−R=$1,669,178`이다. 8/23 새 계약을 **같은 날 채택**하면 H에서는 `1,669,178` hold를 **빼고** `1,729,217` 계약 charge를 더하므로 그 순간 열거 부분합의 순증은 **$60,039**다. R에서는 앞 hold가 없으므로 새 계약 charge **$1,729,217** 전부가 그날 추가된다. 종점 금액은 같지만 **8/6 MLE 사용 시점의 Team Salary 입력은 다르다.** [NBA의 2021–22 cap/tax·MLE 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)와 [NBA CBA 101의 non-taxpayer MLE 제한](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)을 적용하려면 실제 권리 처리일, 다른 FA hold, 예외 자체의 Team Salary 반영과 향후 변동까지 채워야 한다. 위 금액은 **완전 Team Salary도 apron 여유액도 아니다.**

| 추가 **D** 시험: 8/6 전에 NBA에 통지된 Moritz 합의가 있었고 첫해 예상 급여가 8/23 원역사 계약과 같은 **$1,729,217** | 열거 부분합 | 해석 |
|---|---:|---|
| 8/6 Lopez 계약 직후 | **$137,592,586** | `135,863,369+1,729,217`. 앞 FA amount가 $1,669,178이라면 **같은 선수의 두 금액을 더하지 않고** 더 큰 예상 급여를 반영하는 조건부 시험. |
| Bacon B0 이탈 완료 뒤, 8/23 전 | **$135,768,583** | `134,039,366+1,729,217`. Moritz의 표준계약 자리 0일 수 있어도 급여 예상액은 별도다. |

**D는 8/4 보도의 사실 판정이 아니다.** 보도는 리그 통지·합의 조건·계약 효력의 증거가 아니고, Article II §13(a)(ii)는 정식 계약 전 구속력도 부정한다. D가 실제 성립했다면 8/6 H/R의 단순 headroom 비교 대신 D와 다른 Team Salary 항목을 다시 검사해야 한다.

반대로 8/4 보도가 **경제 조건까지 합의한 사건**을 정확히 전한 것이라면 Article II §13(a)(i)의 즉시 리그 통지 의무도 검토해야 한다. 공개 보도만 보고 `NBA 미통지`를 편의상 채택하거나, 미통지를 정당한 cap room 확보 수단으로 설계하지 않는다. H/R은 보도 성격과 통지 사건이 확인될 때까지 진단용으로만 남긴다.

`R`은 권리 포기에 따른 incumbent 재계약 권한 손실이 있으나 최저급 예외 서명은 열려 있다는 **법적 후보**다. [G15T의 8/4 합의 보도](O15G15T_MORITZ_2021_AGREEMENT_SIGNING_AND_HOLD_BRANCH.md)가 실제 계약서 또는 실제 renounce 통지를 증명하지 않으므로 H/R 어느 쪽도 원역사 복원값으로 선택하지 않는다. QO가 살아 있었다는 별도 증거가 나오면 R의 조기 renounce는 **§4(g)(2) 위반**일 수 있고, RFA 금액은 $1,669,178보다 클 수 있어 다시 계산한다.

## 3. 명단 한 자리와 출전 분은 별도의 선택

Moritz가 8/23에 서명하는 **M1**은 [G15T](O15G15T_MORITZ_2021_AGREEMENT_SIGNING_AND_HOLD_BRANCH.md)의 10/16 **16표준/15한도**를 남긴다. 8/23에 서명하지 않고 개막까지 다른 표준 선수를 추가하지 않는 **M0**는 **15표준** 시험이지만, H처럼 FA hold가 남을 수 있다. 이는 출전 분을 0으로 만들거나 기존 선수에게 자동 배분하는 해결책이 아니다.

연장 없는 한 경기의 **센터 48분·파워포워드 48분**은 별도 고정 예산이다. 현재 조건부 후보에는 Vučević, Bamba, Lopez, Nnaji, Mobley가 이미 있고 M1이면 Moritz도 추가된다. Moritz가 빠질 때 되돌려야 할 분은 **대체세계에서 실제로 그에게 배정하려던 `m_C+m_P`**이며, 원역사 Orlando의 [2020–21 마지막 11경기 26.0분](https://www.nba.com/magic/orlando-magic-re-sign-moritz-wagner-20210823)을 그대로 `m=26`으로 놓지 않는다. Vučević 잔류와 Nnaji/Mobley 존재가 당시 출전 경쟁을 바꾼다. 이 선수들의 **동시 가용성·의료·코치 로테이션·각 팀에서 실제 잃는 분**을 채울 때까지 `m_C`, `m_P` 및 후속 선수의 분은 `null`이다. Moritz가 타 구단과 계약하는 M0-R이라면 새 팀의 자리·급여·분과 원역사 Orlando 역할 소실도 별도 장부가 필요하다.

**사실:** CBA의 UFA/RFA FA amount·권리 포기/최저급 예외 규칙, NBA 원역사 분류·캡, 비공식 계약표의 표시값. **추론:** H/R 중간 부분합과 8/23 교체 산술, M1/M0의 조건부 자리 변화·분 예산. **후보:** Moritz 권리 유지/포기·재계약/타 팀 계약. **작가확정:** 신규 0건.

## 4. 도구별 실행 범위와 다음 증거

- **Antigravity CLI:** Orlando의 공식 8/23 URL을 재요청했다. `status=SUCCESS`, `num_turns=1`이지만 **최종 답변은 빈 문자열**이었다(대화 `de78c6ba-4641-44fc-9989-e55a8203e07e`). 저장 `content.md`의 `Source:` URL은 맞지만 HTML에 재계약 기사 본문·선수 이름이 없어 **이번 새 본문 증거 0건**이다. 구단 기사 사실은 Codex의 NBA 원문 판독과 G15T 기존 출처에서 사용했다.
- **NotebookLM CLI:** `nlm doctor`는 로그인 정보와 설치 상태를 확인했고, 기존 NBA CBA 요약 소스 `4e516c8c-d38b-4a27-8c70-1e05f8c5dced`만 지정한 질의 `0573ed95-5398-4c61-bb8f-c6835229e396`는 **FA amount 포함·renounce 제거·재계약 뒤 실제 급여 교체**를 출처와 함께 답했다. 같은 2차 CBA 요약의 재분석이며 `다른 팀 서명` 문구·QO 제한·통지된 합의 세부 조항까지 검증한 답변은 아니다. 그 세 규칙은 Codex가 2017 CBA 전체본에서 직접 대조했다.
- **Codex:** NBA 원문과 2017 CBA Article II §13 및 Article VII §4를 읽고 H/R/D 서로 배타적 조건과 부분합을 재계산했다. 같은 선수의 FA amount와 예상 급여를 중복 합산하지 않는다.
- **Claude CLI:** 좁은 CBA 반증을 요청했다. 첫 호출은 CBA 원문 미제공을 이유로 구체 반증을 유보했고, 정확 조항 발췌를 붙인 재요청은 [제한 검토 기록](../reviews/R01_O15G15U_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)에 따로 판정한다. 독립 원문 수집과 G16 감사가 아니다.

원역사 Moritz의 **QO 실제 발행/철회 여부와 시각**, Orlando의 **renounce 통지 여부와 날짜**, 8/4 합의의 **NBA 통지·경제 조건**, 8/6의 다른 FA hold·예외 Team Salary 금액, 대체 2020–21 출전 근거와 2021–22 각 빅맨의 팀별 분 배분을 채워야 한다. 공식 CBA로 법적 분기를 정리했지만 개인별 원계약·통지 문서가 없으므로 QO 사건과 H/R/D 사실 여부는 `HOLD`다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, Chicago 2020–21 정확 시즌·G14 ORL4/DET4·G16/G17 열린 상태를 유지한다.
