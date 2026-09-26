# O-15G15S — Orlando 2021 여름 날짜별 계약 비용 시험

- 기준: `main` `58b82fe` / PR #202. [G15L 사건표](O15G15L_ORLANDO_SUMMER_CONTRACT_EVENT_LEDGER.md), [G15N 공통 8명](O15G15N_ORLANDO_COMMON_2021_22_CONTRACT_CHARGES.md), [G15O 세 FA](O15G15O_ORLANDO_2021_FA_SIGNINGS_AND_HOLDS.md), [G15M Bacon·Mobley](O15G15M_BACON_GUARANTEE_AND_ROOKIE_CAP_HOLD.md), [G15R Herbert](O15G15R_ORLANDO_HERBERT_MINIMUM_MLE_AND_MORITZ_UFA.md)의 **이미 검토한 입력**을 날짜순으로 연결한다.
- 상태: `ENUMERATED_CHARGE_WITNESS / TEAM_SALARY_AND_APRON_HOLD`. 아래 값은 **이름을 적은 계약과 Mobley 미서명 1라운드 hold의 조건부 부분합**이다. 실제 Orlando 급여, 세금 지위, MLE 자격 또는 대체세계 사건 확정값이 아니다.

## 1. 시간 경계와 공동 가정

[NBA의 2021–22 캡 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)에 따르면 새 시즌 cap **$112,414,000**과 tax line **$136,606,000**은 **2021-08-03 00:01 ET**에 발효하고 FA 모라토리엄은 **8/6 정오 ET**에 끝났다. 따라서 G15L의 **7/29 드래프트 12계약**은 다음 시즌 약정의 선수 집합 미리보기로만 읽는다. 이를 7/29 당일의 *발효된 2021–22 Team Salary*라고 부르지 않는다. 3번 선택 직후의 1R hold 규칙은 [2017 CBA Article VII §4(e)(1)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)에 있으나, 아래 장부는 8/3부터 해당 시즌 수치로 비교한다.

**한 경로만 시험한다:** 공통 8명 전원, Vučević의 2021–22 잔류, Aminu 옵션 행사·잔류, Denver 거래 A에 따른 Nnaji #24·Harris 유입과 Nnaji의 120% 신인 계약 유지, Bacon의 원계약, Orlando의 3번 Mobley 선택·미서명, 33번 Herbert 선택·미서명을 모두 가정한다. Lopez·Moritz·Moore는 원역사 날짜와 조건을 같은 금액으로 **선택했을 때만** 뒤에 더한다. Bacon은 원계약 보호조건 아래 보장 전에 **8/8 waiver를 요청하고 이후 적법한 이탈이 완료**돼 잔여 보호액 $0인 **B0 시험**이다. 이 중 어느 것도 작가확정이 아니다. G15N의 공통 8명 **$84,477,366**, G15J의 Vučević **$24,000,000**·Aminu **$10,183,800**, G15N의 #24 Nnaji **$2,303,040** 후보, G15M의 Bacon **$1,824,003**·미서명 Mobley3 hold **$8,075,160**을 사용한다. 8/3 첫 열은 `84,477,366+24,000,000+10,183,800+2,303,040+1,824,003=122,788,209`이다.

## 2. 계약 자리와 열거된 비용의 날짜별 이동

| 대체 사건을 그날 채택한 시험 | 표준계약 수 | 이름 있는 계약 charge 부분합 | + Mobley3 미서명 hold | 계산상 이동 |
|---|---:|---:|---:|---|
| **8/3** 새 캡 발효 뒤 시작 시험 | 12 | **$122,788,209** | **$130,863,369** | 12계약 + Mobley 권리. Herbert는 미서명 2R 권리라 이 열에 charge 없음. |
| **8/6** Lopez $5m 서명 채택 | 13 | **$127,788,209** | **$135,863,369** | +$5,000,000; MLE의 실제 사용 자격은 따로 검사. |
| **8/8 요청 후 이탈 완료 시점** Bacon B0 채택 | 12 | **$125,964,206** | **$134,039,366** | 보유 중 계약 charge −$1,824,003. **8/8 요청 즉시의 수치가 아니다.** 정확 완료 시각과 대체 계약 보호액 $0 조건 확인 필요. |
| **8/23** Moritz $1,729,217 재계약 채택 | 13 | **$127,693,423** | **$135,768,583** | +$1,729,217. 그 이전 Orlando FA hold는 **별도**이며 이 표에 0이라고 증명된 것이 아님. |
| **9/9** Moore $1,669,178 charge 계약 채택 | 14 | **$129,362,601** | **$137,437,761** | +$1,669,178. 기본급 $2,641,691을 charge로 중복 사용하지 않음. |
| **10/16 이전** Herbert 1년 최저급 $925,258 서명까지 가정 | 15, Mobley 미서명 | **$130,287,859** | **$138,363,019** | 서명일 자체는 `HOLD`; 10/16 이전 서명 시험일 뿐. |

위 마지막 행에서 Mobley도 10/16 전에 **$8,075,160에 실제 서명**하면 hold를 **같은 금액의 계약 charge로 교체**한다. 이름 있는 비용 합은 **$138,363,019 그대로**, 표준계약 수만 **16명**이 된다. 금액 일치는 #3·120% 서명이라는 별도 가정에 의존한다. 미서명 권리의 hold와 서명 계약을 동시에 더하지 않는다. 다른 금액에 서명하면 실제 첫해 charge로 다시 계산한다.

[2017 CBA에 수록된 NBA By-Laws 5.04](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 일반 waiver 청구 기간은 리그 통지 뒤 **48시간**이다. 공개된 8/8 사건일만으로 정확 통지·청구 종료 시각을 알 수 없으므로, 8/8 행의 `−1`을 그날 00:00 또는 기사 게시 시각에 소급하지 않는다. 늦어도 8/23 이전에 B0 이탈이 완료됐다는 별도 조건에서만 뒤 행의 13·14명을 잇는다.

## 3. 같은 10/16 선수 집합의 상호 배타적 자리·비용 사건

| 추가 사건 | 표준 자리 시험 | 위 이름 있는 charge + Mobley 계약의 계산 | 남는 증명 |
|---|---:|---:|---|
| Bacon B0, Aminu 계속 보유 | **16** | **$138,363,019** | 표준 최대 15를 1명 초과. |
| Bacon B0, Aminu를 개막 전 waiver 완료; $10,183,800 전액 보호·차감 없음 | **15** | **$138,363,019** | 자리는 풀려도 보장급여 의무는 남는다는 **전액 보호 조건의 산술**. 실제 보호액·set-off·stretch·통과 시각 `HOLD`. |
| Bacon B0, Aminu를 표준 선수 유입 없이 다른 팀에 거래 완료; Orlando에 해당 charge가 남지 않음 | **15** | **$128,179,219** | 수취 팀·대가·매칭·실행일·Chicago–Spurs DeRozan 연쇄 `HOLD`. 절감액 $10,183,800은 실제 거래 성립 전에는 없음. |
| Bacon B1, Aminu 전액 보호 waiver | **15** | **$140,187,022** | Bacon을 보장 경계 뒤 waiver해 $1,824,003 전액이 잔존하고 별도 차감이 없다는 조건. 정확 보장 시각 `HOLD`. |
| Bacon B2 계속 보유, Aminu 거래로 이탈 | **16** | **$130,003,222** | Aminu 1명 이탈만으로 표준 15를 회복하지 못함. Bacon의 역할·Knicks 후속도 다시 설계해야 함. |

이 비교는 [G15I의 Aminu 자리·비용 구분](O15G15I_AMINU_WAIVER_CAP_COST.md)과 [G15M의 Bacon B0/B1/B2](O15G15M_BACON_GUARANTEE_AND_ROOKIE_CAP_HOLD.md)를 **하나의 날짜별 이름 있는 숫자 집합**에 적용한 것이다. 9/9 행의 부분합은 NBA의 tax line보다 $831,761, 10/16 미서명 Mobley hold 포함 행은 $1,757,019 크다. 그러나 빠진 FA hold·방출급여·보너스·기타 계약·실제 서명 시각과 tax 산식이 있으므로 **실제 세금 발생이나 non-taxpayer MLE의 apron 준수를 판정하지 않는다**. 특히 Lopez를 8/6에 non-taxpayer MLE로 서명하는 안은 **그날과 이후의 Team Salary가 해당 apron을 넘지 않는지** 검사해야 한다([NBA CBA 101의 예외 자격 설명](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)). 9월 숫자만으로 8월 당시 자격을 역산하지 않는다.

**사실:** NBA의 cap·tax 발효일/모라토리엄, CBA의 미서명 1R hold·MLE 조건, 기존 문서에 출처별 기록한 원역사 계약·날짜. **추론:** 위 명시 조건에서만 성립하는 계약 수와 산술, waiver/거래 비용 차이. **후보:** B0/B1/B2·Aminu 처리·3 FA·두 신인 서명. **작가확정:** 신규 0건.

## 4. 검증 경계와 다음 인수

- **Codex:** 위 여섯 날짜의 다섯 입력·세 FA·Herbert/Mobley 합을 별도 산술로 재현했다. G15L 12→14→16 자리 원장과 선수 이름, G15O/R의 charge·hold 이중계상 방지를 대조한다.
- **Antigravity CLI:** 2021 NBA cap 공식 URL 재시험 첫 호출은 검사 가능한 출력을 남기지 않았다. 두 번째 `--output-format json` 호출은 `status=SUCCESS`, `num_turns=1`과 **8/3 00:01 ET·tax $136.606m**이라는 최종 응답을 반환했다(대화 `af453848-aec3-4b1c-a5ab-0e36a768f961`). 단, 해당 호출의 `read_url_content`·`view_file` 실행 기록이나 저장 본문은 출력에서 확인하지 못해 **새 본문 검증 Evidence Pack은 0건**이다. [G15I에서 완료한 동일 NBA 기사 본문 판독](O15G15I_AMINU_WAIVER_CAP_COST.md)은 이력으로 유지하고 독립 자료를 하나 더 얻었다고 세지 않는다.
- **NotebookLM CLI:** 기존 NBA cap·Bacon 계약 두 소스만 지정한 재질의가 `The notebook returned no answer`로 끝났다. **이번 출처 연결 분석은 0건**이며 도구 실행 자체를 성공 분석으로 쓰지 않는다.
- **Claude 독립 반증·결과물 단독 검수:** [검토 기록](../reviews/R01_O15G15S_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)에 실제 실행과 채택/기각만 남긴다. G16 전체 감사와 구별한다.

다음에는 Moritz의 서명 전 FA hold/권리 포기·QO 실제 사건, Bacon/Aminu의 정확 보호조건과 waiver 통과 시각, 두 신인 서명일, Lopez MLE 사용 시 매일의 **빠진 charge**를 확인해야 한다. 그 전에는 위 $138,363,019를 완전 Team Salary나 확정 세금 상태로 승격하지 않는다. Chicago 2020–21 정확 시즌, G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16/G17은 열린 상태다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 원고 금지를 유지한다.
