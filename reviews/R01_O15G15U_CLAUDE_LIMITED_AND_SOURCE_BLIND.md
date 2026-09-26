# O-15G15U — Claude 제한 CBA 반증·결과물 단독 맹점

- 대상: [Moritz 8/6 FA hold·통지 합의 분기](../research/O15G15U_MORITZ_FA_HOLD_INTERIM_CAP_AND_ROLE_GATE.md). Claude CLI `haiku`, 도구 비활성. 첫 반증은 조항 원문이 없어 판단 유보, 이후 CBA 조항 발췌를 입력한 제한 반증과 결론을 주지 않은 편집 검수를 각각 1회 수행했다. 독립 원문 수집/G16 검수는 아니다.

| 출력 | 대조·판정 |
|---|---|
| 첫 호출은 CBA 원문과 2021 개인별 자료에 접근할 수 없어 반례를 제시하지 않음 | `NO_SUBSTANTIVE_AUDIT`로 기록. 모델의 유보를 통과 판정으로 바꾸지 않음. |
| 조항 발췌 뒤 H/R/D의 **8/6 산술** 및 FA amount·통지된 예상 급여 분리를 논리상 일관적이라고 평가 | 산술 자체는 Codex가 별도 재현. Claude에게 제공한 **같은 CBA 발췌**에 대한 제한 검토이며 독립 사실 확인은 아님. 실제 NBA 통지일·경제 조건을 모른다는 지적은 `HOLD`로 수용. |
| source-blind가 공개 합의 보도와 NBA 등록 시점을 구별해야 한다고 지적 | 문제의식 수용. 다만 **정식 서명 계약 등록만** Team Salary에 영향을 준다는 표현은 [2017 CBA Article VII §4(a)(1)(iv), Article II §13(a)(i)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf)의 **리그에 통지된 구두·서면 합의 예상 급여**를 놓쳐 기각. |
| 조항 발췌 호출은 `미통지` 경로를 산술상 가능하다고 봄 | 실제 8/4 보도가 경제 조건까지 성립한 구두 합의를 정확히 전했다면 Article II §13(a)(i)의 즉시 통지 의무가 있다. **미통지를 적법한 cap 절약 선택지로 쓰지 않는다**는 문장을 결과물에 추가. |

이번 검수는 QO/renounce/통지의 원역사 제출 서류를 찾지 못했다. H/R/D는 서로 다른 증거 조건을 가진 시험이며 author lock 0건, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
