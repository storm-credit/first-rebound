# Chicago 2021 여름 — 지명 후보와 실제 이름을 넣은 15자리 예산

- 단계: `O-15G3 / NAMED_CONDITIONAL_ROSTER_AND_BUDGET`.
- 선행: [G1A](CHICAGO_2021_23_CONTINUATION.md), [잠정 추첨](NBA_2021_PROVISIONAL_DRAFT.md).
- 입력/산출: [입력](CHICAGO_2021_NAMED_ROSTER_INPUTS.json), [계산](CHICAGO_2021_NAMED_ROSTER_OPTIONS.json), [출처](../research/CHICAGO_2021_NAMED_ROSTER_SOURCES.json).
- 선수 지명·계약 합의·최종 시즌 채택은 미실행이다. `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 추천의 범위

가용할 경우 **10순위 Moses Moody, 39순위 Kessler Edwards, 백업 센터 Tony Bradley**를 추천한다. 마지막 윙/가드 자리는 Stanley Johnson·Denzel Valentine의 최소계약 제안으로 구체화한다. 다섯 이름은 G1A의 다섯 빈자리를 교체하며 일반계약 15자리를 초과하지 않는다. 투웨이 선수는 이 15명에 넣지 않았다.

앞선 팀의 실제 지명 보드는 아직 없다. 따라서 이 문서는 Moody·Edwards를 Chicago에 배정하지 않는다. 실제 2021 지명 순번은 자료의 기준점이며 새 추첨 뒤 가용성을 보장하지 않는다. 특히 실제 Ayo 38순위를 새 세계 Chicago 39순위로 자동 이월하지 않는다. 실제 New Orleans/Memphis의 10·17순위 거래도 바뀐 순번에 그대로 복사하지 않는다.

## 네 후보씩 비교

아래 순서는 G1A의 가드 자원과 윙 필요에 맞춘 설계자의 추천이다. 미래 NBA 활약을 2021 구단의 지식으로 사용하지 않는다. 당시 공개 소개의 짧은 사실 근거는 각 링크에 있고, 배치·비용 판단은 이 프로젝트의 추론이다.

| 자리 | 후보 우선순위 | 이 설계에서의 용도와 비용 |
|---|---|---|
| 10순위 1안 | [Moses Moody](https://www.nba.com/draft/2021/prospects/moses-moody) | 무볼 슛·긴 윙 후보. LaMelo/LaVine/P의 볼 점유와 공존시키는 안 |
| 10순위 2안 | [Chris Duarte](https://www.nba.com/draft/2021/prospects/chris-duarte) | 외곽 즉시성 후보. 팀의 장기 성장 시간표를 다시 비교 |
| 10순위 3안 | [Ziaire Williams](https://www.nba.com/draft/2021/prospects/ziaire-williams) | 장신 슈팅 성장안. 즉시 14분 역할을 보장하지 않음 |
| 10순위 4안 | [Alperen Sengun](https://www.nba.com/draft/2021/prospects/alperen-sengun) | 포스트·패스 센터안. Carter/Markkanen/Young/백업C의 분과 윙 보강을 재설계 |
| 39순위 1안 | [Kessler Edwards](https://www.nba.com/draft/2021/prospects/kessler-edwards) | 받아 쏘기·수비 성장 후보. 이미 많은 가드보다 윙 육성에 자리 사용 |
| 39순위 2안 | [Ayo Dosunmu](https://www.nba.com/draft/2021/prospects/ayo-dosunmu) | Illinois 가드 후보. 기존 Coby/Caruso/Satoransky와 기회 배분 재검토 |
| 39순위 3안 | [Herbert Jones](https://www.nba.com/draft/2021/prospects/herbert-jones) | 수비·연결 후보. 슛 개선을 이미 달성한 것으로 처리하지 않음 |
| 39순위 4안 | [JT Thor](https://www.nba.com/draft/2021/prospects/jt-thor) | 크기·기동성 성장 후보. 첫해 안정된 출전 보장 없음 |

각 4명에 대해 선행 지명 여부 16조합씩, 총32개의 가용성 조건을 검사한다. 앞서 지명된 선수는 추천에서 빠지고 모두 지명됐으면 `null`이다. 이는 드래프트 모의실행 32회가 아니라 중복 배정을 막는 조건 검사다.

## 백업 센터 네 계약 경로

공개 계약 이력은 2차 자료다. 금액을 새 세계 제안의 비교 기준으로 쓰며 실제 계약 수락·동일 보장·옵션 행사를 의미하지 않는다.

| 후보 | 실제 2021–22 연간 기본급 참고 | 구조 참고 | 전체 15자리 최고 총액 | apron에서 남는 조건부 예산 |
|---|---:|---|---:|---:|
| [Bradley](https://www.salaryswish.com/players/tony-bradley), 추천 | $1,789,256 | 2년 최소계약·다음 해 선수 옵션 | $106,862,083 | $36,139,917 |
| [Hartenstein](https://www.salaryswish.com/players/isaiah-hartenstein) | $1,729,217 | 1년 최소계약·캠프 초대 | $106,802,044 | $36,199,956 |
| [Dedmon](https://www.salaryswish.com/players/dewayne-dedmon) | $2,389,641 | 1년 최소계약 | $107,462,468 | $35,539,532 |
| [Dieng](https://www.salaryswish.com/players/gorgui-dieng) | $4,000,000 | 실제 Atlanta MLE 계약 | $109,072,827 | $33,929,173 |

각 총액은 미확정 주인공 순번/80·120% 급여 30조건 × Young 보너스 0/100만 달러 2조건으로 계산했다. 네 센터 총240예산 조건은 경기 성적 계산이 아니다. 팀의 미확보 잔여 charge `R`은 포함 여부를 확정하지 않았으므로 표의 차액이 정확한 사용 가능 금액은 아니다.

Bradley안의 범위는 **$103,338,790~$106,862,083**, G1A와 비교한 총액 변화는 **−$856,688**이다. Stanley와 일부 단년 최소계약은 보전 전 연간 기본급을 사용해 보수적으로 비교했다. 리그 보전이 적용된 cap 금액·구단의 현금 부담·세금/apron 장부를 같은 숫자로 단정하지 않는다.

Dieng의 400만 달러는 Caruso의 $8.6m 사용 뒤 NTMLE 잔액 **$936,000**과 단독 BAE **$3,732,000** 중 어느 쪽에도 들어가지 않는다. 두 예외는 더할 수 없다. [2017 CBA VII.6(d), (l)](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf), [당시 예외 금액](https://basketball.realgm.com/nba/info/salary_cap).

이는 Dieng 영입 자체가 불가능하다는 증명이 아니다. 해당 안의 최고 총액은 cap 아래 $3,341,173이며, 그의 계약 전후 권리 포기·다른 계약·실제 잔여 장부를 별도로 구성하면 cap 공간 경로를 검토할 수 있다. 그 순서는 아직 검증하지 않았다. 남은 apron 공간만으로 예외가 생긴다고 처리하지 않는다.

## Caruso 앞에 둘 실제 FA 권리 금액

G1의 예외 분류에는 임의 벤치 예산 대신 실제 정상 cap 산입액이 필요했다. [Valentine 공개 이력](https://www.salaryswish.com/players/denzel-valentine)의 2021 FA 금액 **$8,821,320**을 유지하는 조건을 추가한다. 기존 2020–21 Chicago QO/권리가 이어지는 경로를 전제로 한다.

1. G1에 이미 있는 Markkanen·Theis의 FA 금액 등에 Valentine 금액을 유지한다.
2. Caruso의 $8.6m 계약을 NTMLE로 처리하는 조건을 검사한다.
3. Markkanen의 Bird 재계약, Theis 이탈과 권리 정리, Valentine의 최소계약으로 각 FA 금액을 실제 순서에 맞게 대체한다.
4. Bradley·Stanley 및 지명권을 보유한 39순위 선수의 최소계약을 해당 예외로 검토한다.

이때 Caruso 직전 기존 정상 cap 계산에 Valentine을 더한 범위는 **$110,820,413~$113,343,706**이다. G1의 추가 실제 금액 필요치 최대 $878,908을 모두 충족해 30조건의 추가 필요액은0이 된다. 이 중 cap 미만 조건도 있다는 사실을 숨기지 않는다. NTMLE/room 분류는 cap에 예외 금액을 넣는 기존 CBA 검사에 따른다. 이것은 금액상 후보 경로이며 실제 리그 장부·서명 순서가 인증된 것은 아니다. FA 금액을 현금 지급이나 일반계약 선수 한 자리로 중복 계산하지 않는다.

## 39순위 최소계약과 FA 규칙을 구분

새 39순위 선수에게 2년 최소계약 **$925,258 / $1,563,518**을 제안하는 안이다. 둘째 해 금액은 2022–23 수준 참고다. [실제 Ayo 계약 이력](https://www.salaryswish.com/players/ayo-dosunmu)은 비교 근거이며, Ayo를 새 39순위로 지명했다는 뜻이 아니다. 이 안의 Edwards 일반계약은 그의 실제 Brooklyn 투웨이 계약과도 구분한다.

[2017 CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) I.1(cc), (ggg)는 Free Agent와 Rookie Free Agent를 정의한다. Chicago가 독점 교섭권을 유지한 새 지명 선수는 여기서의 Rookie Free Agent가 아니다. 따라서 VII.12(f)(2), VII.6(m)(3)(B)의 0·1년차 **FA** 세금/apron 하한을 그에게 자동 적용하지 않는다.

권리가 끝난 0년차 FA로 대신 계약하는 반례라면 같은 기본급에도 2021 세금/apron 산입 하한 **$1,669,178**, 차이 **$743,920**을 검토해야 한다. 반례는 추천 경로에 합산하지 않았다. 같은 원래 지명 계약의 둘째 해가 됐다는 이유만으로 새 FA 계약으로 바꾸지 않는다.

최소급여 예외 VII.6(i)는 최대2시즌·각 시즌 해당 최소급여·보너스 없음이라는 구조다. IV.1(g)의 3년 이상 경력자 단년/10일/잔여시즌 보전과 2년 Bradley·Valentine 계약을 구분한다.

## 나머지 두 자리와 다음 시즌 비용

- [Stanley Johnson](https://www.salaryswish.com/players/stanley-johnson): $2,089,448 연간 기본급을 제안 예산에 넣었다. 실제 Chicago 캠프 계약은 2021-10-16 방출됐으므로 새 세계의 시즌 잔류는 창작 제안이다. 실제 무보장을 무비용 잔류로 바꾸지 않는다.
- [Valentine](https://www.salaryswish.com/players/denzel-valentine): 실제 Cleveland의 2년 최소계약을 참고해 첫해 $1,939,350을 넣었다. 부분 보장액·후대 방출 잔액을 시즌 전체 급여로 쓰지 않는다. 새 Chicago 합의는 미확정이다.

2022–23에 Bradley 선수 옵션 $2,036,318, Valentine 둘째 해 $2,193,920, 새 39순위 둘째 해 $1,563,518을 모두 유지하면 G1의 해당 세 자리 예산보다 합계 **$206,244 감소**한다. 옵션 행사·비보장 선수 유지가 모두 조건이다. Stanley의 단년 계약 종료 뒤 자리는 G1의 200만 달러 예비 예산으로 남는다.

## 분 배분과 남은 연결

기본 추천 이름을 G1의 건강한 날 240분 표에 치환했다. 이 검사는 5포지션×48분만 확인한다. Moody의 SF14분·Bradley의 C12분이 실제로 성립하는 능력/전술/가용성 증명이 아니다. Sengun 대안에 같은 SF14분을 복사하지 않는다. Satoransky·Green·39순위·Stanley·Valentine은 이 정상 10인 표 밖이므로 실제 기회·경쟁·결장 대응이 남는다.

다음 기존 작업은 바뀐 상위 지명 보드와 소유권 연결, 실제 계약 합의·예외 순서, 2022 옵션/RFA와 2021–23 가용성·시즌 인과다. 네 K 사실 묶음과 G2의 장기·대표팀·문체·독립 승인 HOLD는 유지한다. 새 승인 게이트는 만들지 않는다.
