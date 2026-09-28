# R01 O-15G8G — M1 거래 연쇄 독립 반증의 수용·기각

- 대상: [M1 후손 원장](../research/O15G8G_M1_2021_23_DEPENDENCY_CHAIN.md), [작가 선택](../canon/CHICAGO_2021_MARKKANEN_M1_DECISION.json).
- 범위: Anti-Gravity CLI `claude-sonnet-4-6`의 좁은 거래 인과 반증, 대화 `aa3facf0-7c44-4abb-87fd-f41092e480c6`. 직접 `claude -p` 문서 전체 요청은 응답 없이 종료해 **완료 검수로 세지 않는다**. CLI 모델 반증은 50초 만료 시 부분 응답을 반환했으므로 읽힌 항목만 판단한다. 새 독립 원자료는 0건.

| 반증 지적 | 판정 | 공식 원자료와 수정 범위 |
|---|---|---|
| M1이면 원형 Mitchell **대가**는 불가하지만 Mitchell→Cleveland 자체는 다른 제안으로 가능 | `ACCEPT` | [Utah 구단 발표](https://www.nba.com/jazz/news/utah-jazz-acquire-agbaji-markkanen-sexton-and-future-draft-assets)의 Markkanen 포함 대가만 부정한다. [본문](../research/O15G8G_M1_2021_23_DEPENDENCY_CHAIN.md)은 대체 제안/다른 행선지/Utah 잔류를 후보로 두고 거래 전체 불가능이라고 하지 않는다. 대체 matching salary와 Utah 수락은 HOLD. |
| Sexton이 2022에도 rookie-scale 계약이라 원거래의 salary matching을 쉽게 옮길 수 있다는 서술 | `REJECT_FACT` | [Cleveland 공식 2022–23 거래 기록](https://cdn.nba.com/teams/uploads/sites/1610612739/2023/04/2023-playoff-guide.pdf)은 Sexton이 **sign-and-trade**로 Utah에 갔다고 명시한다. Markkanen 대체 급여만 더해 원형 거래가 자동 통과한다는 계산을 하지 않는다. |
| Branham #20이 Young→Toronto 거래의 1R이 아닌 Charlotte 별도 픽이라는 지적 | `REJECT_FACT` | [NBA의 Spurs 경로 회고](https://www.nba.com/news/how-spurs-laid-the-groundwork-for-2023-nba-draft-to-change-everything)는 Young→Toronto 대가의 2022 1R이 Branham으로 이어졌다고 명시한다. [2022 거래 원장](https://www.nba.com/news/raptors-spurs-trade-dragic-young-eubanks)은 Spurs 1R 수취, [Spurs 지명 공지](https://www.nba.com/spurs/news/spurs-sign-2022-first-round-draft-pick-malaki-branham)는 #20을 확인한다. 다른 거래로 같은 픽을 얻을 가능성은 후보로 열어 둔다. |
| Young이 대체 Chicago에 어떻게 왔는지 불명이라는 지적 | `REJECT_FACT` | [Chicago의 2021 DeRozan 공지](https://www.nba.com/bulls/news/bulls-acquire-demar-derozan)는 Young이 2019년 FA로 Chicago와 계약했다고 적는다. M1만으로 Young의 2022 잔류가 확정된 것은 아니므로 원장은 **G1A 비교 경로에서 Young이 남는 경우**로 한정한다. |
| Chicago 2R 박탈이 Lonzo 부상/DPE 분쟁 때문이라는 지적 | `REJECT_FACT` | [NBA 공식 2021-12-01 제재 공지](https://pr.nba.com/bulls-heat-penalties-free-agency/)는 Lonzo 관련 **FA 협상 시각 위반**을 원인으로 명시한다. 대체 2023 2R의 무조건 반환/깨끗한 소유도 주장하지 않고 자산·다른 제재를 HOLD로 둔다. |

**수렴:** 역사 사실과 모델 반박을 같은 권위로 세지 않았다. 원장의 M1 선택·원형 대가 불복사·Young/제재의 조건부 처리에는 변경이 필요하지 않다. 교차 구단 salary matching·대체 2022 거래/2023 픽 원장은 계속 HOLD다. 별도 [결과물 단독 검수](R02_O15G8G_M1_SOURCE_BLIND.md)는 이후 실행했고 Cleveland 선행 시즌 파급을 추가했다. 어느 검수도 G16/G17이나 3번 종료가 아니다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED` 유지.
