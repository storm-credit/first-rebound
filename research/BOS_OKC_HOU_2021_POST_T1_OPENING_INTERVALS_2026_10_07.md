# T1 후 BOS·OKC·HOU 첫 Chicago 경기 전 운영구간

**HOU 1라운드 신인 서명 루틴 2건만 선택.** 나머지 계약·명단·건강·결과는 실행하지 않았다. T1의 7/28·7/29 old-year 숫자를 8/3 이후에 그대로 이월하지 않는다.

| 첫 CHI 경기 | 원 보고행 | 이번 실행 | 미실행 원 보고행 |
|---|---:|---:|---:|
| BOS 2021-11-01 | 20 | 0 | 20 |
| HOU 2021-11-24 | 27 | 2 | 25 |
| OKC 2022-01-24 | 35 | 0 | 35 |

## 실제 줄어든 입력

T1에서 HOU가 보유한 #2 Jalen Green과 #16 Alperen Sengun 권리를 잇고, NBA 원 보고의 8/4·8/6 서명 GroupSort를 별도 가상 루틴 계약으로 선택했다. 각자는 2021–22 해당 순번 공식 scale의 80–120% 안에서 120% 정책을 선택한다. 공식 scale 정확 달러·사적 계약서·영수증은 인증하지 않는다. 미서명 1라운드 hold를 해당 서명 급여로 교체한다.

법적 근거는 2017 CBA Article VIII §1(PDF 292–295)의 2시즌 계약·독립적인 3/4년차 팀 옵션·연도별 Salary+Unlikely Bonuses 120% 상한·기본급/기술 부족 및 부상 보호 하한이다. 두 옵션은 아직 행사하지 않았다. 신규 보너스·대여는 0으로 선택했고, Sengun은 NBA 계약 전 해외 계약 장애가 적법하게 해소되는 조건으로만 실행했다(실제 해제 문서 인증 0). Article II §15(PDF 84–85)는 권리 보유팀의 1라운드 신인 계약을 모라토리엄 중에도 허용한다. 8/4·8/6은 보고 날짜이며 정확 서명 시각은 인증하지 않는다.

HOU의 T1 직후 명명 carry 15STD+2TW를 전원 유지한다고 가정해도 두 신인 추가 시 17STD+2TW=19명으로 오프시즌 20명 이내다. 이것이 정규시즌 15STD+2TW 또는 실제 8/6 live roster 인증은 아니다. May16 계약 만료·타팀 이전은 후속 GroupSort/권리·비용과 함께 처리한다.

## 비용과 후속

6범주 중 새 신인 RSC 급여 정책만 연결했고 나머지 live/dead/FA/tender/exception은 `six_cost_categories`의 typed input이다. BOS 20·HOU 25·OKC 35 원 보고행은 미실행이며, 실제 명단·계약여부를 보고 feed에서 자동 추론하지 않는다. Kemba waive, Horford/Moses 후속과 거래 상대, HOU 15+2 정리는 다음 원자 적용대상이다.

1. Published 2021–22 #2/#16 official rookie scale cents or a clearly bounded scale interval for numeric new-year salary; the lawful RSC percentage policy is selected, actual contract paper is not a gate.
2. BOS/OKC and HOU post-8/6 GroupSort counterparty/contract-class events, old-contract expiry/waive-dead-money, six new-year cost categories and final 15+2 roster by each first CHI date.
3. Date-specific available 5-player role and opponent health/result choices after legal interval; historical first-CHI box score is not automatically copied.

실제 의료·거래/계약 접수·사적 급여 인증 0, 원고 0, Freeze v0.30 PARTIAL, 설계/원고 CLOSED.
