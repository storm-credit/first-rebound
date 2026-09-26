# O-15G15K — Aminu 선수 옵션: 보도일·통지일·대체 Orlando 선택 분리

- 시작점: `main` `0fc397f` / PR #194. [G15J 계약 입력값](O15G15J_ORLANDO_2021_22_CONTRACT_INPUT_LEDGER.md)의 **5/18 행사일 단정**을 교정하고, [G15I 비용 분기](O15G15I_AMINU_WAIVER_CAP_COST.md)의 첫 사건인 선수 옵션을 평가한다. 기존 [G15F 여름 비용](O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)과 [G15G Chicago–Spurs 인과](O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)의 거래·명단 사실을 다시 확정하지 않는다.
- 상태: `ORLANDO_OWNERSHIP_CONDITIONAL / EXERCISE_WORKING_PRIOR / NOTICE_DATE_UNKNOWN / AUTHOR_HOLD`. 추천은 작가확정·계약 통지·급여 실행이 아니다. 여기서 **3/25 분기**는 원역사 Chicago–Orlando Vučević·Aminu 패키지가 대체세계에서 실행되지 않는 경계를 뜻한다. [T2](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)가 명시적으로 승인한 선수는 Vučević의 **2020–21 잔여 시즌 경로**뿐이다. 시즌말에 계약이 종료된다는 뜻이 아니며 2021–22 구단 소유는 후속 사건으로 판정한다. Aminu의 5월 Orlando 보유는 원패키지 미실행 뒤 **별도 이동이 없다는 조건**을 요구한다.

## 1. 서로 다른 날짜가 증명하는 것

| 자료와 시점 | 직접 확인할 수 있는 내용 | 증명하지 못하는 내용 |
|---|---|---|
| [Orlando의 2020-12-02 무릎 시술 발표](https://www.nba.com/magic/orlando-magic-al-farouq-aminu-undergoes-procedure-right-knee-20201202), [NBA 선수 기록](https://www.nba.com/stats/player/202329/career) | 2020–21 원역사 Orlando 구간 17경기·14선발·경기당 21.6분. 무릎 수술·재활은 2021-03-25 T2 분기 **이전**에 이미 존재했다. | 3/25 이후 대체 Orlando의 경기·건강·시장 제안. 원역사 Chicago 6경기를 Orlando 기록으로 이월할 수 없다. |
| [NBC Sports 2021-05-18 보도](https://www.nbcsports.com/nba/news/report-al-farouq-aminu-exercising-10183800-player-option-with-bulls) | ESPN 취재를 인용해 Chicago 소속 Aminu가 $10,183,800 옵션을 행사할 **계획**이라고 보도했다. 기사 게시일은 5/18이다. | 선수·구단·리그에 옵션 통지가 접수된 정확한 날. 대체 Orlando에서 동일 결정을 내렸다는 증거. |
| [SalarySwish 계약 이력](https://www.salaryswish.com/players/alfarouq-aminu), [Spotrac 거래 이력](https://www.spotrac.com/redirect/player/6890) | 두 비공식 이력은 원역사 **행사 결과**와 약 $10.18m 연봉에 일치한다. 날짜는 각각 **5/18**, **5/21**로 다르다. | 충돌하는 날짜 중 어느 쪽이 공식 통지일인지. 공개 2019 계약서의 통지 마감 조항도 확보하지 못했다. |
| [NBA 2021 Chicago 드래프트 팀 프로필](https://www.nba.com/draft/2021/team-profiles/chicago-bulls) | 여름 드래프트 시점 원역사 Chicago에서 Aminu를 계약 중 선수로 분류한다. | 옵션이 5/18 또는 5/21에 접수됐다는 정확한 사건일과 대체 Orlando의 소속·행사. |

따라서 이 원장에는 `report_date=2021-05-18`, `reported_intent=exercise`, `original_result=exercised`, `original_notice_date=null`, `alternate_orlando_decision=null`을 둔다. 계약 추적 사이트 날짜를 NBA 공식 통지로 승격하지 않는다. G15J의 5/18 문구는 이 구분에 맞춰 정정했다.

옵션은 팀의 자동 명단 정리가 아니라 **선수의 선택·통지 사건**이다. 대체세계에서 언제 어떤 방식으로 통지했는지, 통지하지 않았을 때 계약 조항상 어떤 결과가 되는지 모두 미확보이므로 `EXERCISE_WORKING_PRIOR`를 통지 완료로 해석하지 않는다.

## 2. 대체세계 선택 비교

| 후보 | 선수의 가능한 동기·근거 | Orlando·타 구단 비용 | 판정 |
|---|---|---|---|
| **A. 옵션 행사** | 원역사에서도 무릎 이력 뒤 약 $10.18m 보수를 선택했다. 대체 Orlando에서도 **2020-12-02 시술**은 분기 이전의 사실이므로 **작업상 우선 후보**다. 3/25 뒤 재활 결과·역할·시장 제안은 달라질 수 있다. | Orlando에 기존 계약과 표준 자리 1개가 이어진다. [G15H](O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)의 Herbert 내부 PG안 O15A는 표준 16명으로 **1명 초과**, Gravett 별도 PG안 O15C는 17명으로 **2명 초과**인 조건부 시험이다. 10/16 전에 이름 있는 방출·거래·다른 영입 취소가 필요하고, 보장급여 있는 선수를 방출하면 명단 자리는 줄어도 해당 급여의 cap 비용은 남는다. Chicago는 Aminu를 얻지 않았으므로 8월 Chicago–Spurs 원거래의 Aminu 송출 항목이 빠진다. | `EXERCISE_WORKING_PRIOR / NOT_LOCKED` |
| **B. 옵션 미행사 후 FA** | 더 긴 보장 계약·역할 또는 다른 개인 사정이 있다면 가능하지만, 현재 대체세계의 실제 제안·의료·선수 진술은 없다. 큰 옵션액 포기를 단순 명단 정리 수단으로 쓰지 않는다. | 계약 선수 자리는 사라질 수 있으나 FA 권리·cap hold·다음 계약과 선수 행선지는 별개. 원역사 Chicago 옵션 행사와 달라지는 직접 나비효과를 설명해야 한다. | `ALTERNATIVE / MOTIVE_AND_MARKET_HOLD` |

**추천 이유의 한계:** A가 경제적으로 그럴듯하다는 것은 위 원역사 행동과 분기 이전 의료를 조합한 **추론**이다. ‘다른 팀 제안이 없었다’거나 정확 기대 수입이 $10.18m보다 낮았다고 검증한 것은 아니다. A는 아래 **7/29→10/16 비용 시험에서만** 조건부 입력으로 두고, 작가확정 전 계약 사건·명단 처리·최종 cap 판정에 쓰지 않는다.

**자리 산술의 입력:** [G15E](O15G15E_ORLANDO_STANDARD_SLOT_BRIDGE.md)의 원역사/대체세계 공통 가능 표준 11명에 Vučević·Aminu·Nnaji·Mobley·Herbert 표준 후보 5명을 더하면 O15A **16명**이다. Gravett 표준 후보를 별도로 더한 O15C는 **17명**이다. 투웨이 선수는 두 계산에서 제외한다. 이는 서명 완료나 1/23 활동 명단이 아니라 **과밀 반례 입력**이며 한 명 방출만으로 O15C의 두 자리 초과가 해결되지는 않는다. 방출 보호급여가 팀 샐러리에 남는 근거와 cap stretch 분기는 [G15I](O15G15I_AMINU_WAIVER_CAP_COST.md)의 NBA CBA 101 `I.L`·`I.U`에 있다.

## 3. 행사 가정 뒤의 날짜별 인수점

| 시점 | 이미 있는 원장과 별도 필요한 증명 |
|---|---|
| 2021-03-25~2021-05 | [T2 승인](../canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json)의 Vučević 잔류는 2020–21 잔여 시즌만이다. Aminu는 [2020–21 등록 유지안](../simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.md)에 있지만 Chicago 원거래 뒤 **별도 이동이 없는 경우에만** 5월 Orlando 소속이다. 대체 Orlando의 선수 결정·통지일은 null. |
| 2021-07-29 NBA 드래프트 | [G15F](O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)의 **Orlando 33번 Herbert** 지명 비교를 사용하면 같은 33번 권리를 Clippers에 넘긴 실제 Preston 거래와 2026 Detroit 경유 2R·현금 유입을 함께 취소해야 한다. 이는 **옵션 결정이 일으킨 거래가 아니라 병렬 픽 자산 조건**이다. 지명과 계약 서명도 별개. |
| 2021-08-03~08-11 | [NBA 공식 2021–22 캡 발표](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)의 기준선만 확정. 실제 8/6 Lopez 영입과 8/11 Chicago DeRozan 사인앤트레이드는 각각 대체영입 여부와 Aminu/Young 송출 자산이 필요하다. [G15G](O15G15G_AMINU_DEROZAN_CAUSAL_LEDGER.md)의 거래를 자동 이식하지 않는다. |
| 2021-08-23~09-09 | 원역사 Moritz 재계약과 Moore 영입은 [G15F](O15G15F_ORLANDO_OFFSEASON_BRANCH_COSTS.md)의 실존 선수 비용. 각각의 대체 서명/비서명·FA 권리·상대 팀·급여를 확인해야 한다. |
| 2021-10-16 | [G15H](O15G15H_ORLANDO_DATED_REGISTRATION_WITNESS.md)의 표준 15·투웨이 2·양수 분 집합은 **조건부**다. Aminu 옵션을 행사시키면 초과 자리가 다시 생기므로 waiver 완료 시각 또는 이름 있는 거래·비영입과 보장급여/상대 비용을 함께 검증한다. |

다음 인수는 A를 **시험 입력**으로 둔 `2021-07-29 → 08-11 → 10-16` 선수별 계약 소유·명단·급여 사건표다. 우선 Orlando 기존 계약자와 2021 여름 신규 서명자를 분리하고, 빈 금액은 null로 둔다. Chicago 2020–21 정확 실행, Orlando 2021–22 시즌 선택, G14 ORL4 `ROLE_HOLD`·DET4 `PRIOR_HOLD`, G16/G17은 여전히 열려 있다.

## 4. v2 도구 범위

- **Codex:** 5/18 기사 본문의 `plans to exercise`와 비공식 계약 이력의 5/18·5/21 차이, NBA 선수 기록의 분기 전 Orlando 출전만 대조했다. 공식 통지 문서와 대체세계 의료 기록은 확보하지 못했다.
- **NotebookLM CLI:** NBC Sports 기사 URL을 새 출처 `026c51c3-a1db-41f0-96cc-037e43c28a9d`로 수집했다. 그 출처만 지정한 질의 `ac63df27-052e-4ba8-8c92-34cc23da497c`는 기사 게시일과 계획/완료 차이·무릎 맥락을 추출했고 공식 통지일이나 대체 Orlando 선택을 증명하지 못한다고 답했다. Codex와 **같은 기사**를 읽은 것으로 독립 원자료를 하나 더 얻은 것은 아니다.
- **Anti-Gravity CLI:** 같은 기사 URL 직접 읽기를 시도했으나 60초 `print timeout`, 본문 출력 0건. 새 독립 Evidence Pack으로 세지 않는다.
- **Claude 제한 반증:** [검토 기록](../reviews/R01_O15G15K_CLAUDE_OPTION_REVIEW.md)의 유효한 표현 지적을 반영했고 잘못된 계약 구단·Herbert 지명 구단 전제는 기각했다. `CLAUDE_LIMITED_RUN`이며 G16 전체 독립 검수가 아니다.
- **결과물 단독 맹점:** 앞 분석 없이 결과 요약만 준 새 Claude CLI 세션에서 [편집 의심 4건](../reviews/R02_O15G15K_SOURCE_BLIND_REVIEW.md)을 회수했다. 승인 범위/계약 종료 혼동과 산술 구성 누락 표현을 보완했다. `SOURCE_BLIND_EDITORIAL_RUN`은 공식 NBA 사실의 독립 검증이 아니다.

`PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false` 유지.
