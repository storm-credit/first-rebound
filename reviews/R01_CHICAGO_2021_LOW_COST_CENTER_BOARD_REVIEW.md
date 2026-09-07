# R01 Chicago 2021 Low-Cost Center Board Review

- 검토 범위: O-15F5 Theis·Green 대체 거래, 다른 저비용 빅, 타깃 실패
- 판정: `PASS_FOR_AUTHOR_SELECTION / A_PRIMARY_LEAN / EXACT_EVENT_HOLD`
- 독립 검수 대체 여부: `NO — R16 전체 설계 독립 검수는 별도`

## 결론

Hutchison 없는 대체 구조는 6인이 아니라 **3팀 5인 거래**다. 선수 수 표기는 틀렸지만 급여 합계와 이동 방향은 맞았다. 수정된 A는 Chicago가 Gafford·Kornet을 보내고 Theis·Green을 받으며, Washington이 Wagner를 Gafford로, Boston이 Theis·Green을 Wagner·Kornet으로 바꾸는 구조다.

급여는 세 팀 모두 통과하고 roster count도 보존된다. Washington과 Boston의 당시 동기는 강하다. Chicago도 저사용률 베테랑 빅과 수비 윙을 얻는 동기가 있지만, Vučević가 없는 세계에서는 값싼 Gafford를 만료계약 Theis로 바꾸는 비용이 실제보다 커진다. 따라서 A는 `PRIMARY_LEAN`이지 자동 정본이 아니다.

## 맹점 검토

| 맹점 | 교정 |
|---|---|
| 5명을 6인 거래라고 반복 표기 | 고유 선수 set를 검증기에 넣고 5명으로 정정 |
| 급여 PASS면 사건도 PASS | 세 팀 동기와 Chicago의 Gafford 가치 비용을 별도 판정 |
| 실제 현금을 대체 거래에도 복사 | 현금은 필수 조건이 아니며 정확 이동 HOLD |
| Vučević가 없어도 Gafford는 같은 잉여 자산 | Carter·Gafford만 남는 세계의 센터 가치 상승을 반대 비용으로 등록 |
| Theis 실제 Chicago 기록 복사 | 마감일 뒤 29경기 분·생산성 원장 전 기록 HOLD |
| McGee의 실제 가격을 Chicago에 그대로 적용 | 1R 없는 시장 존재만 anchor로 사용, 정확 패키지 HOLD |
| buyout을 공짜 영입으로 취급 | 선수의 행선지 선택 때문에 비통제 시장으로 분류 |
| Brown·Trent를 거래 밖에 남기고 Washington 분을 무시 | Washington 후속 player-game blocker 유지 |

## 반대 가능성

1. Chicago가 Gafford의 저비용 통제와 성장 표본을 높게 보면 A 협상을 거부하고 C로 갈 수 있다.
2. Boston이 세금 절감 외 추가 자산을 요구하면 현재 A의 정확 가격은 달라질 수 있다.
3. Washington이 Gafford를 강하게 원하더라도 Brown·Trent 동시 잔류는 별도의 윙 분·계약 비용을 만든다.
4. B의 다른 센터가 더 싸게 나오면 A의 적합성보다 자산 보존이 우선될 수 있다.

## 총괄 판정

- A Theis·Green 3팀 5인 거래: `CAP_PASS / ROSTER_COUNT_PASS / MOTIVE_PASS_WITH_CHICAGO_VALUE_TENSION / PRIMARY_LEAN`
- B 다른 저비용 빅: `MARKET_EXISTS / EXACT_PACKAGE_HOLD / SECONDARY_MARKET`
- C 타깃 실패·무거래: `FAILURE_CONTINGENCY`
- 정확 거래 발생: `AUTHOR_GATE`
- 마감일 뒤 29경기·2021 lottery·여름 계약: `HOLD`
- 원고 게이트: `CLOSED`
