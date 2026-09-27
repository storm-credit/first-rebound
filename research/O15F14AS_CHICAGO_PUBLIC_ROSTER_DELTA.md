# O-15F14-AS — Chicago 2021-03-25 원역사·선택 경로의 공개 15인 급여 차액

- 판정: `NAMED_ROSTER_DELTA_BOUNDED / F1_EXACT_TEAM_SALARY_HOLD`.
- 범위: F1의 **이름 있는 15인** 기본급 비교. 명단 밖 `R`, 거래일 정확 Team Salary, 리그 거래 허가를 인증하지 않는다.
- 기존 작가확정 Theis/Green 이동 방향, Chicago 원클럽과 2020 #4 LaMelo는 유지한다. 주인공의 2018 정확 순번·급여는 선택하지 않는다.

## 출처와 같은 항목 비교

[Chicago의 3/25 Vučević/Aminu 거래 발표](https://www.nba.com/bulls/news/bulls-acquire-all-star-nikola-vucevic-and-al-farouq-aminu-trade-magic)는 원역사 Chicago가 Porter/Carter를 보내고 Vučević/Aminu를 받았음을, [같은 날 3팀 거래 발표](https://www.nba.com/bulls/news/bulls-complete-three-team-trade-wizards-celtics)는 Brown/Theis/Green 수취를 확인한다. 두 구단 발표는 **선수 이동의 1차 근거**이며 급여 원장은 아니다.

[Salary Sport의 2020시즌 Chicago 보관 표](https://salarysport.com/basketball/nba/chicago-bulls/2020/)는 거래 뒤 원역사 일반 선수 15명에 **$127,968,089**를 배분한다. 15개 숫자를 더해 표시 총액과 대조했다. 같은 페이지의 `Additional contracts` Vonleh **$97,261**은 그 15인 합계와 **별도**다. 사이트의 다른 영역에는 현재 선수/기한도 섞이므로 이 표를 2021-03-25 **리그 공식 cap sheet**나 완전한 Team Salary로 취급하지 않는다. Vonleh의 거래일 비용 여부는 [날짜별 방출잔액 검문](O15F14AR_CHICAGO_DEAD_MONEY_DATED_SCREEN.md)의 `HOLD`를 따른다.

기존 [선택 경로 급여 원장](../simulation/CHICAGO_2020_21_TAX_BOUND.md)은 같은 15자리의 주인공 제외 기본급 **$122,812,428**, 주인공 3년차 급여 시험 **$1,325,520~$3,204,600**을 기록한다. 아래 비교에서 Young의 unlikely bonus는 **양쪽에 동일하게 0 또는 $1,000,000**을 적용해 상쇄한다. 원역사 Patrick Williams #4와 선택 경로 LaMelo #4의 급여 슬롯은 같은 **$7,068,360**이다.

| 15인 차액을 만드는 이름 | 원역사 공개 기본급 | 선택 경로의 기존 입력 |
|---|---:|---:|
| Vučević ↔ Porter | $26,000,000 | $28,489,239 |
| Aminu ↔ Carter | $9,720,900 | $5,448,840 |
| Brown ↔ 주인공 | $3,372,840 | $1,325,520~$3,204,600 |
| **위 세 자리 합계** | **$39,093,740** | **$35,263,599~$37,142,679** |

나머지 **11자리는 같은 이름·기본급**이고, 별도의 Patrick Williams↔LaMelo #4 한 자리는 이름만 다르며 이 비교의 급여 입력은 같다. 따라서 이 공개 입력들의 선택 경로 15인 기본급은 **$124,137,948~$126,017,028**(Young bonus 제외)이고 원역사 보관 표보다 **$3,830,141~$1,951,061 낮다**. 양쪽에 Young bonus $1m을 넣어도 차액은 같다. 선택 경로의 가장 높은 기존 알려진 합계 **$127,017,028**은 bonus를 포함하며, 이를 bonus 미포함 원역사 $127,968,089와 바로 빼서 차액을 주장하지 않는다.

## 실행에 미치는 범위

**사실:** 구단 발표의 원역사 선수 이동, Salary Sport의 15인 보관 숫자와 별도 Vonleh 행, 기존 선택 경로 산술 입력. **추론:** 같은 급여 정의와 공유 선수 계약 경로가 유지되면 선택 경로의 이름 있는 15인 비용이 최소 $1,951,061 낮다. **후보:** 동일한 명단 밖 부담까지 증명하여 F1 비납세 경계에 연결하는 경로. **작가확정:** 기존 선수 이동 방향만; 새 급여·시즌 선택 0건.

명단 밖 `R`은 두 세계에서 같다고 검증되지 않았다. Porter/Carter 잔류, Vučević/Aminu/Brown 미수취, 다른 거래·예외/권리의 차이가 있을 수 있다. 원역사 보관 15인 합계와 거래일 Team Salary 또는 최종 사치세 판정도 동일한 필드가 아니다. 이 차액은 **F1의 알려진 선수 부분을 좁히는 비교**이며 `R=null`, F1 `HOLD`, F1~F5 전체 `0/5`, A1~A3 `0/3`, K 종료 `0/4`를 바꾸지 않는다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, 원고 금지.

Codex가 구단 발표·보관 표·기존 JSON을 직접 대조하고 세 자리 합계와 15인 차액을 재계산했다. Anti-Gravity·NotebookLM·Claude·별도 source-blind는 이 차액에 대해 `NOT_RUN`이며 원자료 독립 검증으로 세지 않는다.
