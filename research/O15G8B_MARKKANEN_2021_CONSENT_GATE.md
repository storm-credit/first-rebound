# O-15G8B — Markkanen 2021 잔류의 선수 동의 관문

- 기준: `main` `27d0f38`; [G1 여름 4안](../simulation/CHICAGO_2021_23_CONTINUATION.md), [G8 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [CP2 D2](../design/CP2_INTEGRATED_REVIEW_PACKET.md).
- 판정: `G1A_CONSENT_HOLD / G1B_COMPARATOR_OPEN`. 기존 G1A 추천·금액 시험은 조건부 입력으로 보존한다. 신규 계약·선수 의사·작가확정은 없다.

## 원역사 사실과 출처 범위

| 시점 | 검증된 원역사 사실 | 대체 세계에 옮길 수 없는 것 |
|---|---|---|
| 2021-08-06 | [Yle의 Markkanen 직접 인터뷰](https://yle.fi/a/3-12049590)는 Chicago 이외에서 새 출발을 원하며 다른 구단의 제안이 있다고 전한다. 제한적 FA인 Chicago의 매칭·사인앤트레이드 권리도 설명한다. | 실제 Chicago에서의 이적 희망을 Vučević가 없고 Carter·주인공·LaMelo가 있는 세계의 동일한 의사로 자동 복사할 수 없다. 반대로 그 세계에서 잔류 의사가 생겼다고 자동 가정할 수도 없다. |
| 2021-08-28 | [Cleveland 구단의 공식 거래 발표](https://www.nba.com/news/cavs-acquire-lauri-markkanen-from-bulls-in-3-team-trade)는 Markkanen의 CLE 사인앤트레이드, CLE→POR Nance Jr., CLE→CHI Denver 경유 보호 2023 2R, POR→CHI Derrick Jones Jr.·lottery 보호 2022 1R을 명시한다. | 세 팀의 대체 세계 협상·동의, 동일 픽의 가용성·보호·전달, 같은 계약 금액은 보장하지 않는다. |

Yle는 **선수 발언을 직접 받은 1차 보도**이고 Cleveland 발표는 **완료 거래의 구단 1차 공지**다. 이 둘은 서로 다른 사건을 다룬다. [G1의 급여 입력](../simulation/CHICAGO_2021_23_CONTINUATION_INPUTS.json)는 G1A Markkanen 2021–22 $15,690,909·2022–23 $16,475,454의 **두 시즌 급여 비교 예산**이다. 원역사 Cleveland 계약 이력을 참조한 숫자를 Chicago 잔류 계약의 금액·기간·수락 증거로 쓰지 않는다. 대체 제안이 달라지면 G1A 팀 샐러리·SQ1 순서·2022 비용을 다시 계산한다.

## 기존 추천에 생긴 정확한 부담

G1A는 Vučević가 없고 Markkanen에게 정상 가용일 PF 28분을 배정한다. 이는 원역사의 불만 동기를 바꿀 수 있는 **설계상 차이**이지만 28분 산술만으로 선수의 장기 역할·공격권·보장 기간·계약 수락이 입증되지는 않는다. 주인공 32분, Carter C 28분, Young PF/C 20분도 같은 날 역할 비용이다. 기존 G1A 15자리·예외 순서·cap 240조건은 **구단 쪽 실행 가능성의 조건부 시험**이며 선수 쪽 동의를 포함하지 않는다.

G1A 최종 채택 전에 다음 세 항목을 같은 협상 사건으로 연결한다.

1. **역할:** 대체 2020–21 확정 결과와 2021–22 전술에서 Markkanen의 PF·공격 기회가 어떤 이유로 원역사의 이탈 희망을 바꿀 수 있는지. 다른 실존 선수의 분을 이유 없이 삭제하지 않는다.
2. **제안과 선택:** 두 시즌 비교 예산과 별도로 대체 세계의 구체적 계약 기간·보장·연차·경쟁 제안, 선수/대리인이 그 조건을 선택할 만한 이유를 제시한다. 원역사 제안·의사를 그대로 복사하지 않는다. RFA 매칭 권리는 자발적 다년 계약 동의가 아니다. 계약 금액의 산술 통과만으로 `accepted=true`를 만들지 않는다.
3. **후손:** 잔류 시 Caruso SQ1·Bradley·Green·#10 Duarte/#39 Wieskamp·Young의 자리/분/비용을 다시 대조한다. 잔류 불성립 시 [G1B](../simulation/CHICAGO_2021_23_CONTINUATION.md)는 검토할 대안이지 자동 원역사 복구가 아니다. Cleveland·Portland의 선수/자산 동기, 2022 POR 1R·2023 DEN 2R 가용성과 후속 픽/계약/분을 새로 시험한다.

**현재 결정:** G1A의 `추천`은 `선수 동의 미검증 조건부 추천`으로 해석한다. 위 세 조건 중 하나라도 공백이면 `D2 실제 계약=HOLD`; G1B 자산을 G1A 명단에 동시에 더하지 않는다. 대체 세계의 동의를 원역사 문서에서 발견할 수는 없다. 닫는 방법은 역할·계약·경쟁안·후손 비용을 갖춘 **작품 사건 후보**를 검토하고, 기존 최종 작가 선택 단계에서 그 사건을 채택하는 것이다. 채택 전에는 선수 의사 `null`이다. 이는 별도 승인 요청을 지금 만드는 것이 아니라 기존 D2 계약·나비효과 검사의 누락된 선수 관문을 드러낸 것이다. D1 정확 실행 및 CP2 잠정 픽이 최종화되지 않은 상태도 그대로다.

## 도구 판독의 실제 범위

- Codex: Yle 8/6 기사 본문과 Cleveland 8/28 공식 발표를 직접 대조하고 기존 G1/G8·CP2 역할/계약 입력을 확인했다.
- NotebookLM CLI: First Rebound 비정본 작업실에 Cleveland 공식 URL을 새 소스 `173202e1-1dd2-4c57-8b24-2102a0470bf0`로 추가하고 **그 소스 하나만** 질의했다. 거래 세 팀·선수·픽을 인용했으며 대체 Chicago의 재계약은 증명하지 못한다고 답했다. Yle URL 소스 추가는 실패해 선수 의사에 대한 NotebookLM 직접 판독은 0건이다.
- Antigravity CLI: 두 URL 읽기 전용 headless 요청이 45초 제한 뒤 `SUCCESS` 상태이나 `response=""`였다. 저장 본문이나 실제 URL 도구 단계가 확인되지 않아 **이번 직접 Evidence Pack 0건**이다.

같은 Cleveland 원문을 Codex·NotebookLM이 읽은 결과는 독립된 두 사실 출처가 아니다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`를 유지한다.

Claude의 문서 단독 반증과 고정 제약을 준 결과물 단독 검수의 수용·기각은 [R01 검토](../reviews/R01_O15G8B_MARKKANEN_CONSENT_AND_BLIND.md)에 기록했다. 둘 다 선수 동의의 역사적 인증은 아니다.
