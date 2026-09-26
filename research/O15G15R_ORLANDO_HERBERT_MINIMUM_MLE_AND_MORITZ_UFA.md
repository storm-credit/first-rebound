# O-15G15R — Orlando 33번 Herbert 계약 경로와 Moritz 2021 FA 분류

- 시작점: `main` `598dc96` / PR #201. [G15P 2라운드 권리](O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md), [G15O 세 FA 부분합](O15G15O_ORLANDO_2021_FA_SIGNINGS_AND_HOLDS.md)을 잇는 **조건부 비용 검사**다.
- 상태: `HERBERT_MINIMUM_SCALE_VERIFIED / EXCEPTION_BRANCH_CONDITIONAL / MORITZ_PUBLIC_UFA_VERIFIED_QO_EVENT_HOLD`. Orlando가 Herbert를 33번으로 선택·서명했다는 작가확정은 없다.

## 1. 2021–22 0년 경력 최저급의 재현

[2017 NBA–NBPA CBA Article II §6(a), Exhibit C](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)는 2017–18 신인 첫해 **$815,615**, 2년 계약의 두 번째 해 **$1,378,242**를 싣고, 뒤 연도의 최저급 표는 샐러리캡 변동률로 조정한다고 정한다. [NBA 공식 2017–18 cap $99.093m](https://www.nba.com/news/nba-salary-cap-set-2017-18-season-99093-million)과 [2021–22 cap $112.414m](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)을 사용하면:

| 2021년에 시작하는 0년 경력 계약 | 계산 | 작업상 금액 |
|---|---:|---:|
| 첫해 최저급 | `round(815,615 × 112,414 / 99,093)` | **$925,258** |
| 2년 최저급 계약의 다음 해 | `round(1,378,242 × 112,414 / 99,093)` | **$1,563,518** |
| 2년 합 | `925,258 + 1,563,518` | **$2,488,776** |

[RealGM의 2021–22 Minimum Annual Salary Scale](https://basketball.realgm.com/nba/info)는 세 계산 결과를 같은 값으로 표시한다. RealGM은 **2차 표**이며, 규칙·기준 cap은 위 CBA와 NBA 공지에서 직접 대조했다. 선수 서비스 연수와 시작 시즌이 달라지면 이 수치를 다시 적용하지 않는다.

[CBA Article VII §6(i)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)의 Minimum Player Salary Exception은 첫해 해당 최저급이고 보너스가 없는 1~2시즌 계약에 사용할 수 있다. [G15P](O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md)의 1시즌 Required Tender는 **제안 자체가 서명·급여 확정은 아니다**. Herbert가 수락하거나 별도 최저급 계약에 실제 서명하는 분기에서만 계약 charge와 표준 자리 여부를 계산한다. 보장액·수락일·계약 종류는 `HOLD`다.

## 2. 같은 33번 후보의 상호 배타적 서명 분기

| 분기 | 2021–22 Herbert charge 후보 | G15O의 조건부 11계약 $92,875,761에 단순 추가할 때만 |
|---|---:|---:|
| 미서명 권리 보유 | Herbert **계약 charge 0**, 표준 자리 0. 12명 미만 incomplete roster charge와 다른 의무는 별도. | 11계약 부분합 **유지**, 전체 Team Salary 아님. |
| 1시즌 최저급 tender 수락 또는 별도 1년 최저급 서명 | **$925,258** (시즌 전·전기간 계약 시험) | 조건부 12계약 **$93,801,019** |
| 2시즌 최저급 계약 | 첫해 **$925,258**, 둘째 해 **$1,563,518** 시험; 2년 합 $2,488,776 | 첫해 조건부 12계약 **$93,801,019** |
| 원역사 Pelicans의 첫해 $1.7m을 Orlando가 **새로 협상**하는 비교 | 첫해 **$1,700,000**, 최저급 초과. 예외/룸·계약기간 별도. | 조건부 12계약 **$94,575,761**. 원역사 NOP 계약 자동 이전 아님. |

마지막 $1.7m은 [Herbert 원역사 New Orleans 계약표](https://www.salaryswish.com/players/herbert-jones)의 **비공식 비교값**이다. 최저급보다 **$774,742** 높다. 최저급 예외로 $1.7m을 쓰거나 2라운드 rookie scale로 처리하지 않는다. G15O의 11계약과 이번 Herbert를 같은 시점에 전부 보유·서명한다는 가정이 깨지면 두 조건부 12계약 합도 폐기한다. 1라운드 미서명 hold, Moritz 서명 전 hold, Bacon/Aminu 보호급여, 기타 선수·예외·incomplete roster charge를 포함한 **전체 Orlando Team Salary나 cap room 판정이 아니다**.

[G7의 33번 비교](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)는 Orlando가 빅 역할 중복을 피하고 윙 수비/연결을 찾는다는 당시 관점의 **지명 이유 후보**다. 이것이 실제 33번 선택이나 Herbert의 선발·로테이션 분을 정하지 않는다. 서명 뒤에는 Orlando 감독의 역할·기존 윙의 사용 분과 New Orleans 대체 윙의 수비/공격 기능을 양 팀에서 함께 재배분해야 한다. 이 입력 없이 원역사 Pelicans의 2,335분·승패를 그대로 두지 않는다.

## 3. Lopez와 Herbert에게 MLE를 함께 쓰는 시험

[NBA 2021–22 공식 cap 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)의 첫해 MLE 한도는 **non-taxpayer $9.536m / taxpayer $5.890m / room $4.910m**이다. [CBA Article VII §6(e)~(g)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)은 각 유형의 자격·계약기간·**한 예외에서 여러 계약의 첫해 합산**을 규정한다. G15O의 원역사 Lopez $5m MLE 분류와 Herbert의 원역사 NOP $1.7m MLE 분류를 **대체 Orlando에서 함께 선택**하는 경우만 시험하면 첫해 합은 `$5,000,000 + $1,700,000 = $6,700,000`이다.

| 같은 MLE에서 $6.7m 시험 | 한도와 차이 | 판정 범위 |
|---|---:|---|
| Non-taxpayer MLE | $9.536m − $6.7m = **$2.836m 잔여** | 명목 한도 안. 실제 자격·다른 사용액·apron·계약기간 미검증. |
| Taxpayer MLE | $5.890m − $6.7m = **−$0.810m** | 두 계약을 **그 한 예외에서 함께** 처리하는 안은 명목 초과. |
| Room MLE | $4.910m − $6.7m = **−$1.790m** | 합산 초과이고 Lopez $5m 단독도 $4.910m를 넘는다. |

이는 두 선수를 반드시 MLE로 서명시키라는 추천이 아니다. Herbert 최저급 경로에서는 **Minimum Salary Exception**을 별도 검토할 수 있고, Lopez의 원역사 계약을 대체세계에 채택할지도 미정이다. $1.7m의 다른 가능한 자격, 팀 샐러리의 시간순 계산, non-taxpayer MLE apron 조건을 닫기 전에는 **MLE 적법성 최종 판정 `HOLD`**다. New Orleans의 원역사 Herbert 계약 3년을 Orlando에 그대로 복사하지 않는다.

## 4. Moritz 공개 UFA 분류와 미확보 사건

[NBA 2021 Orlando 드래프트 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 Moritz Wagner를 **unrestricted free agent**로 표시한다. [NBA 2021-08-02 QO 정리](https://www.nba.com/news/2021-free-agency-options-and-qualifying-offers)는 2021 특수 일정에서 RFA 매칭권을 위한 QO와 issued/not-issued 사례를 설명하지만 **Moritz는 어느 목록에도 없다**. 따라서 NBA 공개 분류는 `UFA`로 기록하되, 목록의 부재를 특정 제출·철회·권리 포기 날짜의 직접 증명으로 삼지 않는다. [SalarySwish의 이전 계약 행](https://www.salaryswish.com/players/moritz-wagner)의 RFA/QO $1,989,256 표기는 **자격·이론값 표시**와 실제 2021 제출 사건을 혼동하기 쉬워 별도 보존한다. 같은 표의 8/23 새 계약은 `Minimum Salary Exception`으로 분류돼 있다. 대체 Orlando의 4/27 선행 계약 유지와 여름 QO 결정은 별도 후보이며 원역사 UFA를 자동 재현하지 않는다.

**사실:** CBA 조항·NBA cap/MLE 발표·공개 NBA UFA 표기·비공식 최저급/계약표 수치. **추론:** 공식 수치로 재계산한 최저급 및 조건부 부분합, MLE 한도 비교. **후보:** Herbert 최소급 또는 $1.7m 재협상, Moritz 권리/재서명 경로. **작가확정:** 신규 0건.

## 5. 도구 계보·다음 인수

- **Antigravity CLI:** 로그인 복구 후 NBA QO 기사와 Orlando 드래프트 프로필에 `read_url_content`·`view_file` 단계가 실제 `DONE`이었다. QO 기사 저장 본문에는 목록이 있었으나 Moritz는 없었다. Orlando 프로필의 저장 HTML은 선수 목록 본문을 포함하지 않아 해당 `UFA` 표기는 Codex의 NBA 웹 판독에서 확인했다. 이어 Antigravity가 불필요한 `run_command`를 시도했고 headless 권한에 거절돼 최종 agent 응답은 비었다. **도구 단계별 성공/실패를 분리**하고 완성된 Evidence Pack으로 부풀리지 않는다.
- **NotebookLM CLI:** 공식 NBA QO 기사 소스 `d987a789-1e31-4eb4-9eb6-a2c41410cf72` 추가 성공. RealGM URL 추가는 실패했고, 새 소스·기존 공식 드래프트 소스의 짧은 질의까지 모두 `The notebook returned no answer`였다. 이번 분석 결과는 `NOT_RUN/NO_ANSWER`로 기록한다.
- **Codex:** CBA 전체본, NBA 두 해 cap 발표와 2021 QO/UFA 표기, RealGM 표를 분리해 계산했다. [제한 Claude 반증·결과물 단독 검수](../reviews/R01_O15G15R_CLAUDE_LIMITED_AND_SOURCE_BLIND.md)의 채택/기각은 별도다.

다음에는 **Bacon/Aminu 계약 보호급여와 날짜별 Orlando Team Salary**, Moritz QO 실제 제출·철회 자료, 33번 Herbert와 New Orleans 대체 윙의 실제 명단·분 변화를 순서대로 검토한다. G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, Chicago 2020–21 정확 결과·G16/G17 미완료. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 게이트 `CLOSED`, 원고 불가 유지.
