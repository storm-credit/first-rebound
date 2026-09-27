# O-15F14-AI — Boston Fournier 수취 예외의 거래일 용량 하한

- 기준 `main` `c635aee`, 조회일 2026-09-28. D1 F2의 **Boston Hayward TPE 용량**만 다룬다.
- 판정 `PUBLIC_CAPACITY_BOUND / EXACT_F2_HOLD`. 사실은 원역사 거래·기사와 CBA 규칙, 추론은 대체세계 동일 선행거래 및 아래 상한 시험, 작가확정은 없음.

## 원역사에서 3월 16일~25일에 확인된 경로

[NBA의 2021-03-16 거래예외 설명](https://www.nba.com/news/trade-exceptions-what-they-are-and-why-they-matter)은 Boston의 Hayward 출처 TPE를 **약 $28.5m**으로 보도하고, 별도 Kanter 약 $5m·Poirier 약 $2.5m TPE도 열거한다. 이는 정확 센트 단위 리그 잔액증명서가 아니다. [NBA 공식 2020–21 시즌 거래 추적](https://www.nba.com/news/2020-21-nba-trade-tracker)은 리그 승인·구단 발표 거래를 모은다고 밝힌다. 3/16~3/24에 Boston 거래는 목록에 없고 3/25에는 **Fournier 수취/Teague·2R 두 장 송출**과 **Theis·Green 송출/Kornet·Wagner 수취** 두 거래가 있다. [NBA 거래일 해설](https://www.nba.com/news/2021-nba-trade-deadline-notes-and-numbers)은 실제 Fournier 수취에 Hayward 예외를 썼다고 명시한다.

다만 공식 거래 추적에 빠진 별도 사건, 같은 날 리그 접수 순서, 각 TPE의 정확 원장과 보호픽 계약 원문은 이 세 자료에 없다. 원역사 Boston의 거래 이력과 예외 배분을 대체세계에서도 유지하는 것은 별도 **조건**이다.

## 같은 날 두 거래의 순서를 몰라도 남는 조건부 여유

[기존 Boston 공개 계약 장부](../simulation/BOSTON_DENVER_2020_21_PAYROLL.md)의 비교액은 Kornet **$2,250,000**, Wagner **$2,161,920**, Fournier 기본급·공개 보너스 합 **$17,450,000**이다. 모두 2차 계약자료를 사용한 **시험값**이고 거래일 리그 charge 원본은 아니다. Hayward TPE 명목 $28.5m에서 일부러 더 낮은 **$28,000,000**을 시작값으로 놓는다. Kornet·Wagner 수취액 **둘 다** 동일 Hayward TPE에서 먼저 차감되고, 그 다음 Fournier 전액도 그 예외에서 차감된다는 보수적 시험은 다음과 같다.

| 조건부 시험 | 달러 |
|---|---:|
| 공개 Hayward TPE 약액보다 낮게 잡은 출발값 | $28,000,000 |
| Kornet + Wagner 선차감 | −$4,411,920 |
| Fournier 전액 후차감 | −$17,450,000 |
| **잔여 용량** | **$6,138,080** |

이는 실제 3팀 거래에서 두 선수를 그 TPE에 넣었다는 뜻이 아니다. 다른 TPE·선수 계약 매칭을 쓰면 Hayward 잔액은 이 시험보다 크다. CBA Article VII §6(j)(1)은 원선수 계약 송출 뒤 1년 안에 **한 명 이상**의 대체 선수를 받을 수 있게 하며, 비동시 수취의 합산 상한을 §6(j)(1)(ii)가 정한다. 이 규칙과 공개 비교액을 적용하면, 3/16~3/25에 **공개 추적의 두 거래만** 있고 대체 Boston의 세 계약액·동일 예외가 원역사와 같다는 조건에서 같은 날 두 거래의 순서는 Fournier 수취 **명목 용량**을 막지 않는다. $28m 출발값은 보도 약액에서 임의로 보수화한 시험값이며 법적 하한 증명이 아니다. 미공개 사용액·계약 보너스·리그 charge가 이 여유를 소진하지 않았다는 정확 원장 검증은 남는다. Orlando가 Fournier 송출로 받은 자체 TPE는 Boston의 Hayward TPE 잔액과 별개다.

NBA 설명 기사의 예외가 팀의 cap/tax 부담을 늘리지 않는다는 일반화는 이 계산의 근거로 쓰지 않는다. 선수 수취에 따른 Team Salary와 거래 예외 용량은 [2017 NBA–NBPA CBA](https://cosmic-s3.imgix.net/3c7a0a50-8e11-11e9-875d-3d44e94ae33f-2017-NBA-NBPA-Collective-Bargaining-Agreement.pdf) Article VII §4(a)·§6(j)를 각각 적용한다. **예외로 계약을 받을 수 있음 ≠ 그 선수 급여가 팀급여/사치세에서 사라짐**이다.

## F2에서 실제로 좁혀진 것과 남은 것

`F2_BOS_TPE_NOMINAL_CAPACITY`는 위 공개 거래·계약 입력의 **조건부 여유 $6,138,080**으로 좁혔다. 별도 Kanter/Poirier TPE는 이 시험에 합산하지 않았다. 아래는 그대로 `HOLD`다.

1. 3/25 리그 원장의 정확 TPE 잔액·Fournier 수취 charge·같은 날 예외 배분, Boston 전체 apron/Team Salary 및 변경된 세계의 다른 선행 거래 부재.
2. BOS/MEM 중 뒤 2025 2R과 BOS 자체 2027 2R의 3/25 소유·보호/우선권 및 [승인된 Bane30 경로](../simulation/NBA_2021_ASSET_CHAIN.md)와의 충돌.
3. Orlando의 Vučević 잔류·Gordon 대체 거래와 Teague 3/25 수취→3/27 방출의 날짜별 계약/명단 비용 및 상대 수락.

따라서 `F2` 전체는 `HOLD`; F1~F5 `0/5`, A1~A3 `0/3`, K 네 묶음 `0/4`, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`. K1/L2·CP2 잠정 결과나 이미 승인한 선수 이동 방향은 바꾸지 않는다.

## 도구 범위

Codex가 위 NBA 원문 세 건과 저장소 급여 줄을 대조했다. NotebookLM CLI 작업실 `a3f30584-3a9d-4a8b-8960-b661615d98e9`에 첫 두 NBA URL을 추가하고 저장 본문 및 두 출처 한정 질의를 확인했다. 거래·$28.5m은 반환했지만 **정확 선수 계약액/당일 순서는 자료에 없다**고 답했다. Antigravity CLI는 같은 두 NBA URL을 읽도록 지시한 JSON 응답에서 일치하는 기사 본문 인용을 반환했다. 이번 JSON에는 개별 도구 이벤트가 없어 실제 `read_url_content→view_file` 호출 성공을 별도 입증하지 않는다. 두 CLI는 동일 NBA 자료를 재독했으며 독립 원자료 건수를 늘리지 않는다. Claude와 source-blind는 별도 [검토 기록](../reviews/R01_O15F14AI_BOSTON_TPE_CAPACITY_REVIEW.md)에 둔다.
