# R01 — O-15G15I Claude CBA 반증과 원문 재판정

- Anti-Gravity CLI `claude-sonnet-4-6`에 [G15I 비용 원장](../research/O15G15I_AMINU_WAIVER_CAP_COST.md)만 읽기 전용으로 주고 waiver·cap stretch·Moritz FA를 반증하게 했다(대화 `0386020b-76b4-4efa-9020-76215476f786`). 세 지적을 돌려받았다. 아래 판정은 모델 답변을 사실로 승격하지 않고 당시 NBA 공식 문서와 대조한 결과다.

| Claude 지적 | 원문 대조 | 처리 |
|---|---|---|
| “10월 waiver에는 일반 48시간이 적용되지 않고 포스트시즌 별도 기간이다” | [2017 CBA 전체본에 수록된 NBA By-Laws 5.04](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)는 리그 통지 뒤 48시간을 규정한다. Claude가 든 `Article VII Section 3`은 waiver 절이 아니다. `Post-Season Waivers`라는 구분을 이 원문에서 확인하지 못했다. | **핵심 공격 REJECT.** 다만 요청 시각과 리그 **통지 시각**을 구별하도록 G15I 문구를 정밀화했다. 정확 명단 이탈 시점은 계속 HOLD. |
| “Moritz는 2021 제한적 FA이고 qualifying offer cap hold가 확정이다” | [NBA 2021 Orlando 팀 프로필](https://www.nba.com/draft/2021/team-profiles/orlando-magic)은 Moritz를 **unrestricted** FA로 표기한다. [구단 재계약 발표](https://www.nba.com/magic/orlando-magic-re-sign-moritz-wagner-20210823)는 2021-04-27에 그를 FA로 영입한 후 8/23 재계약했다고 적는다. CBA 101은 자체 FA 금액의 일반 규칙을 두지만 이 자료만으로 정확 hold 금액을 계산하지 못한다. | `RFA/QO` 주장은 **REJECT**. G15I에 UFA 출처를 추가하고 cap hold·권리 포기 사건의 검증을 유지했다. |
| “9월 1일은 방출 급여의 cap 처리 경계가 아니다” | [NBA CBA 101 `I.U Stretch`](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)의 9월 1일은 **현금 지급 일정** 설명에 나온다. G15I도 현금과 선택적 cap stretch를 분리해 적었으며 9월 1일을 cap charge 산식의 경계로 주장하지 않았다. | **REJECT.** 현금/캡 구분 유지. |

**결론:** 반증 모델은 읽기 전용으로 실제 실행됐지만 세 주장을 그대로 채택할 수 없다. waiver 통지 시각과 Moritz UFA 분류를 문서에 보강했다. 이를 G16 전체 독립 검수 PASS로 세지 않으며 Aminu 정확 보호급여·Orlando 팀 샐러리·실제 이탈은 HOLD다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
