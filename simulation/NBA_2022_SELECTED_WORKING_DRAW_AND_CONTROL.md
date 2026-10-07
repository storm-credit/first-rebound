# 2022 가상 추첨과 정확한 작업 순번

SELECTED_FICTIONAL_DRAW_AND_SIXTY_EXACT_WORKING_RANKS_INDEPENDENT_REVIEW_PENDING

공개 seed `first-rebound|2022-draft|routine-v1|2026-10-08`는 첫 실행 전에 루트에 전달했다. 동일 seed·counter를 재생하여 같은 결과를 검산한다. 원하는 결과를 얻기 위한 재추첨은 하지 않았다. 실제 NBA의 물리 추첨·원역사 선수 지명과는 별개이다.

## 원 규칙과 구현

[2022 NBA 공식 확률·일정](https://pr.nba.com/2022-nba-draft-tiebreakers/)과 원 2019규약 PDF85–87을 직접 대조했다. [당대 Wizards 방식 설명](https://www.nba.com/wizards/nba-draft-lottery-2022-everything-you-need-know-about-wizards-odds), [Pacers 설명](https://www.nba.com/pacers/news/how-the-nba-draft-lottery-works)은 색인 본문 관측이며 정상 open은 iframe, 직접HTTP는403이다. 실패 bytes는 본문 증거가 아니다.

현재 lottery14팀은 성적 동률이 없으므로 확률 평균 배분을 실행할 필요가 없다. 각 순위의 공식 가중치를 원선수·실제팀 대신 선택된 역성적순14원점에 적용한다. 1001개 사중조합의 동등 추첨, 미배정/이미 당첨된 원점의 무효 반복, 4당첨 뒤 미당첨 역성적순을 구현한다. 조합의 세부 소유배열은 명시 가상 lexicographic 배정이며 실제 NBA 배열을 읽었다고 주장하지 않는다.

비lottery52승2팀과64승4팀은 별도 무작위 순열이다. 2라운드는 독립 추첨하지 않고 원 기록순·동률 first순서 역방향으로 연결한다. 난수 primitive와 모든 승인/기각 단계·선택 순열을 JSON에 기록했다.

## 선택 결과

| 순번 | 원점 | 공개가족 수령자 |
|---|---|
| 1 | OKC | OKC |
| 2 | CLE | CLE |
| 3 | ORL | ORL |
| 4 | WAS | WAS |
| 5 | DET | DET |
| 6 | CHA | CHA |
| 7 | HOU | HOU |
| 8 | MIN | MIN |
| 9 | SAC | SAC |
| 10 | NOP | NOP |
| 11 | MEM | MEM |
| 12 | SAS | SAS |
| 13 | NYK | NYK |
| 14 | TOR | TOR |
| 15 | POR | POR |
| 16 | MIA | HOU |
| 17 | GSW | GSW |
| 18 | CHI | CHI |
| 19 | ATL | ATL |
| 20 | IND | IND |
| 21 | DAL | DAL |
| 22 | DEN | DEN |
| 23 | BKN | MIA |
| 24 | LAL | NOP |
| 25 | LAC | OKC |
| 26 | PHX | OKC |
| 27 | BOS | BOS |
| 28 | PHI | PHI |
| 29 | UTA | MEM |
| 30 | MIL | MIL |
| 31 | OKC | OKC |
| 32 | DET | WAS |
| 33 | ORL | ORL |
| 34 | CHA | CHA |
| 35 | CLE | NOP |
| 36 | WAS | CLE |
| 37 | HOU | CLE |
| 38 | MIN | MIN |
| 39 | SAC | SAC |
| 40 | NOP | NOP |
| 41 | MEM | MEM |
| 42 | SAS | CLE |
| 43 | POR | POR |
| 44 | NYK | NYK |
| 45 | TOR | GSW |
| 46 | MIA | IND |
| 47 | CHI | SAC |
| 48 | GSW | GSW |
| 49 | ATL | ATL |
| 50 | IND | ORL |
| 51 | DAL | DAL |
| 52 | DEN | MIN |
| 53 | BKN | BKN |
| 54 | BOS | BOS |
| 55 | PHX | PHX |
| 56 | LAC | LAC |
| 57 | LAL | CHI |
| 58 | PHI | MIA |
| 59 | UTA | NOP |
| 60 | MIL | MIL |

CHI가 보유하는 작업 순번: [18, 57]. 당첨top4의 순서 사건 확률은 `3087/6655325`이며 두tie의 공동순열 확률은1/48이다. 이는 새확률 추정·실제 난수기 인증이 아니다.

직접 caller 검문은 returned draw의 primitive digest/선택단계/남은순서, exactrank의 원bucket·역순,60수령자의 검문된 명명함수를 각각 대조한다. 조상 전체 constructor·원승패모델·192/2880배정을 재실행하지 않는다. 원CHI82·전리그1230 결과와 비용·명단·건강은 불변이다.

작가잠금·선수/Tender/UPC·미래전달·실접수·전체macro3는 미승격이다. 독립 검문 뒤 루트가 이 작업선택을 채택할 수 있다.

[현행 로드맵](../design/WORLD_BIBLE_COMPLETION_ROADMAP.md)

| 묶음 | 현황 |
|---|---|
| 1 | 완료 |
| 2 | 완료 |
| 3 | 전역1230/순위/play-in·공개60함수 완료, 가상draw 후속 검문 |
| 4 | 진행 |
| 5 | 진행 |
| 6 | 진행·Pack0 |
| 7 | 미완료 |

미완료5 /6번까지4. v0.30 PARTIAL·CLOSED·원고0.
