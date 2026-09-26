# R01 O-15G15AL — CLI 실행과 Claude 문서 단독 반증

- 입력 기준: `main` `e81d84f`; 대상 [G15AL](../research/O15G15AL_DETROIT_PRE_OLYNYK_ROSTER_CHARGE_SEQUENCE.md). 설계·원고 `CLOSED`; 작가확정 0건.
- Antigravity CLI 1.2.11: NBA 자유계약 설명 URL 직접 요청은 headless `RunCommand` 권한 자동 거절, `status=SUCCESS`이나 `response=""`; **증거 0건**. 인증 실패라고 단정하지 않는다.
- NotebookLM CLI: notebook `303ffd55-e019-476a-9ae3-8dc0e32fe11f`, NBA 2018 CBA 101 소스 `4e516c8c-d38b-4a27-8c70-1e05f8c5dced` 하나로 제한 질의. 해당 요약에 **12명 미달 차지와 2021–22 `$925,258`이 없다고** 명시했다. 답변이 길었으나 관련 결론은 두 부재 확인뿐이다. 공식 2017 CBA와 2021–22 급여 검증으로 계수하지 않는다.
- Codex: [NBA–NBPA 2017 CBA Article VII §4(f)](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 오프시즌 12명 미달·인원 범위를 직접 대조. [NBA 공식 캡](https://www.nba.com/news/salary-cap-set-at-112-4-million-for-2021-22-season)과 [2차 최저급](https://www.hoopsrumors.com/2021/08/nba-minimum-salaries-for-2021-22.html)을 분리했다. [조건부 산술 검사](../tools/check_o15g15al_detroit_roster_charge.py)는 PASS. 실제 NBA 거래 접수 순서와 완전 Team Salary는 `HOLD`.
- Claude CLI `haiku --restricted --tools '' --max-turns 1`: 위 문서 **텍스트만** 받은 source-blind 반증. CBA·급여 링크 원문 접근은 없었다. 독립 원자료 검증으로 계수하지 않는다.

| Claude 지적 | 판정·수정 |
|---|---|
| Olynyk 전 권리 포기·McGruder 웨이버·서명 순서 미입증 | **수용**, 핵심 blocker로 유지. 문서의 `+$166,650`은 조건부 여지일 뿐 실행 가능한 실제 순서가 아니다. |
| `$925,258`과 Olynyk 첫해 급여는 2차 자료; `$203,571` 차이로 부호 반전 | **수용**, 후보 수치·민감도 표를 유지. NBA 공식 계약 원장 확보 전 cap-room PASS 금지. |
| QO 두 명을 §4(f) 인원으로 세는 근거 불명확 | **표현 보강**. §4(f)(2)가 §4(a)(2)로 포함한 FA를 인원에 세며, 두 QO의 실제 존속은 `HOLD`. |
| 방출 잔액 다섯 건의 인원 제외·명칭이 모호 | **표현 보강**. 다섯 항목을 본문에 명명하고 금액은 Team Salary 후보에만 넣는다. |
| Plumlee 원역사 이적과 P0-B 잔류를 혼동할 수 있음 | **표현 보강**. 원역사와 2020 계약 계속 보유의 대체 분기를 명시했다. Plumlee가 새로 8/6에 서명한 계약이라는 뜻이 아니다. |
| Olynyk까지의 단일 계약 여지를 전체 동일 사건 경로로 오인할 위험 | **수용**, G15AJ 사건 후 초과와 구별하고 Lyles/Lee/Frank 및 Joseph까지 포함하는 완전 경로는 `HOLD`. |
| `+$166,650`이 Olynyk 급여보다 작다는 주장 | **산술 오독 기각**. 이 숫자는 `$12,361,772−$12,195,122`의 **서명 직전 남는 여지**다. 서명 후 12명 도달로 미충원 차지 하나가 제거되는 별도 항목까지 계산하면 `$1,091,908`이다. |

이번 검토는 자료 출처 수를 늘리지 않는다. `P0_B_SAME_ROUTE_HOLD`, G16/G17 미완료, `PROJECT_FREEZE v0.30 PARTIAL`과 설계/원고 `CLOSED`를 유지한다.

**후속 정정 G15AP:** 이 검토 당시 Lee FA Amount를 누락했다. 위 마지막 행의 서명 후 `$1,091,908`은 무효이며 [G15AP](../research/O15G15AP_SABEN_LEE_HOLD_AND_SEQUENCE_CORRECTION.md)의 P0-B 12명·미충원0, 서명 후 `$166,650`을 따른다. 과거 반증 입력과 판정은 이력으로 보존한다.
