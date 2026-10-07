# 2023 드래프트 원점 순서 · 가상 추첨 후보

검문된1230 경기·16 PO/14 로터리를 사용한다. 정규 동률 대진순위와 드래프트 순열을 구분하며 CHA/WAS 미해결 점수차는 draft drawing을 막지 않는다.

첫 실행 전 공개한 seed: `first-rebound|2023-draft-origin|candidate-v1|2026-10-08`. 원하는 결과로 다시 뽑지 않았다. 이번 결과는 **후보**이며 root 검문·채택 전 정본화0이다.

[원2023 NBA 발표](https://pr.nba.com/ties-broken-for-order-of-selection-in-nba-draft-2023-presented-by-state-farm/)의 top4/기록순/동률추첨과 원2019규약PDF85–87§7.02를 직접 대조했다. 공식본문은 web관측이고 직접HTTP403 bytes는 실패로만 보존했다. NBA 실제2023 당첨팀·원순번·후대보유자·제재를 복사하지 않았다.

CHA/WAS14승은 inverse-record4·5의125+105개를 공동배분해 각115개다. 다른 네 PO 동률군과 함께 공정순열을 기록했다. 2R은 로터리 당첨 이후 **실제 가상1R 선택순서**의 역순이다. 선행coin순서만 뒤집으면 로터리upset 때 규약과 어긋난다.

전체 top4 ordered 경로24,024개·동률순열32개 공동법칙을 정확한 factorization으로 보존한다. 모든top4경로 확률합1을 Fraction으로 계산했다. 이 한seed가 확률 추정이나 물리난수기 인증은 아니다.

| 잠재순번 | 원점 | 공개보유자 |
|---|---|---|
| 1 | MEM | 미평가 |
| 2 | ORL | 미평가 |
| 3 | CHA | 미평가 |
| 4 | CLE | 미평가 |
| 5 | DET | 미평가 |
| 6 | OKC | 미평가 |
| 7 | WAS | 미평가 |
| 8 | HOU | 미평가 |
| 9 | SAC | 미평가 |
| 10 | MIN | 미평가 |
| 11 | SAS | 미평가 |
| 12 | POR | 미평가 |
| 13 | NYK | 미평가 |
| 14 | TOR | 미평가 |
| 15 | NOP | 미평가 |
| 16 | CHI | 미평가 |
| 17 | MIA | 미평가 |
| 18 | ATL | 미평가 |
| 19 | GSW | 미평가 |
| 20 | DAL | 미평가 |
| 21 | IND | 미평가 |
| 22 | BOS | 미평가 |
| 23 | PHX | 미평가 |
| 24 | LAL | 미평가 |
| 25 | DEN | 미평가 |
| 26 | LAC | 미평가 |
| 27 | PHI | 미평가 |
| 28 | BKN | 미평가 |
| 29 | UTA | 미평가 |
| 30 | MIL | 미평가 |
| 31 | DET | 미평가 |
| 32 | OKC | 미평가 |
| 33 | CLE | 미평가 |
| 34 | WAS | 미평가 |
| 35 | CHA | 미평가 |
| 36 | ORL | 미평가 |
| 37 | HOU | 미평가 |
| 38 | MEM | 미평가 |
| 39 | SAC | 미평가 |
| 40 | MIN | 미평가 |
| 41 | SAS | 미평가 |
| 42 | POR | 미평가 |
| 43 | NYK | 미평가 |
| 44 | NOP | 미평가 |
| 45 | TOR | 미평가 |
| 46 | CHI | 미평가 |
| 47 | MIA | 미평가 |
| 48 | GSW | 미평가 |
| 49 | ATL | 미평가 |
| 50 | IND | 미평가 |
| 51 | DAL | 미평가 |
| 52 | BOS | 미평가 |
| 53 | PHX | 미평가 |
| 54 | DEN | 미평가 |
| 55 | LAL | 미평가 |
| 56 | LAC | 미평가 |
| 57 | PHI | 미평가 |
| 58 | BKN | 미평가 |
| 59 | MIL | 미평가 |
| 60 | UTA | 미평가 |

Chicago 자체1R은 검문된16번으로 불변이다. CHI원점2R의 후보순번은46이며 명명된 보유자는WAS다. 전체60 보유권·제재 집행은 이 원점순서의 인증범위가 아니다. 선수·UPC·Tender·가격·우승/MVP/core 선택0.

## 남은 유한 입력

- Root review/adoption of candidate draw; does not condition known CHI16 on unrelated lottery adoption.
- Public holder/conditional prior-right/sanction functions for each actually consumed non-CHI claim; no assumed actual 58-pick forfeitures.
- CHI16 draftee/price and WAS-owned CHI second are separate downstream consumers.

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)

| 묶음 | 상태 |
|---|---|
| 1 | 완료 |
| 2 | 완료 |
| 3 | 진행 |
| 4 | 진행 |
| 5 | 대기 |
| 6 | 대기 |
| 7 | CLOSED |

미완료큰묶음5 /6번까지4 · v0.30 PARTIAL · CLOSED · Pack0 · 원고0.
