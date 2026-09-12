# O-15G5 — 2021 드래프트 자산 투영

상태: **CP2 조건부 추천 / NOT_CANON / NOT_INDEPENDENT**. M의 추첨을 다시 실행하지 않는다. 60행의 원소유 팀을 새 순번에 연결한 후 네 거래 정책을 비교한다. 전체 드래프트 최종 지배권 감사나 지명 완료가 아니다. `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, 설계·원고 CLOSED 유지.

## 네 거래 정책

| 안 | Boston–OKC Kemba/Horford | NOP–MEM 빅맨/픽 | 후속 |
|---|---|---|---|
| **AP1 추천** | 조건부 진행 | 진행하지 않음 | G4 DB1~4의 1~14 지배팀과 호환 |
| AP2 | 조건부 진행 | 조건부 진행 | 9/17과 40/49의 수취팀 변경; G4 재판정 필요 |
| AP3 | 진행하지 않음 | 진행하지 않음 | Boston이16 유지; 15 이후 후보 비교 변경 |
| AP4 | 진행하지 않음 | 조건부 진행 | Boston16 유지, Memphis9; G4 재판정 필요 |

서로 배타적인 두 거래의 발생 조합이다. 네 안은 확률/리그 승인 사건이 아니다. AP1을 후속 작업 입력으로 추천하되 `selected_scenario=null`이다.

Boston은 Walker의 비용을 조정하면서 Horford/Brown의 전방 기능을 받는 공개 역사상 거래를 기준으로 삼는다. Boston16은 변경 세계에서도16이고 앞선2020 Pritchard·Nesmith 경로가 유지돼 있어 조건부 승계가 가능하다. 그러나 실제 Stevens 취임/코치 변경·의료 판단·거래일 charge/예외·각 팀 수락까지 검증한 것은 아니다. Horford와 Brown이 없는 Boston 경로는 AP3/AP4로 남긴다.

NOP는 Killian Hayes13·Zion/Ingram이 있는 조건에서9번의 외곽 보강 기회를 먼저 유지하는 안이다. 7/26 시점에17번에서 누가 남을지를 미래 사실로 아는 설명은 쓰지 않는다. Memphis의 이동 의사나 Ziaire17 가용성을 선지식으로 삼지 않는다. 거래를 하지 않는 비용은 Adams/Bledsoe 잔류 부담, Valanciunas 부재, 별도 유동성 조정이다. Graham/Lonzo/Hart 계약과 Bledsoe 후속 Clippers 거래를 자동 복사하지 않는다. AP2/AP4는 실제 거래 패키지를 새 번호에 연결한 비교안이며 가격이 같아야 한다는 사실이 아니다.

## 시간과 자산 정체성

[NBA 원소유 표](https://api-hub.nba.com/news/2021-draft-order)는6/23 게시 표시지만7/29 현금 거래까지 반영돼 있다. [별도 공식 공지](https://www.nba.com/news/sixers-acquire-no-53-pick-in-2021-draft-from-pelicans)로 Dallas 유래 픽이 NOP에서 PHI로 이동한 날짜를 분리했다. 기본표에서 BOS16→OKC 및 DAL2R→PHI를 되돌린 뒤 선택한 거래만 적용한다. ‘NBA의6월 원장 그대로’라고 부르지 않는다.

| 자산 | 실제 참고 번호 | 변경 세계 번호/처리 |
|---|---|---|
| NOP 자체1R |10|9; AP1 NOP 유지 |
| MEM 자체1R |17|17 |
| MEM 소유 POR2R |51|49; AP2/AP4 NOP 수취 |
| NOP 자체2R |38; 실제 Chicago swap |40; Chicago39가 앞이므로 swap 없음 |
| Chicago 자체2R |40; 실제 NOP 수취 |39 Chicago 유지 |
| Dallas 유래2R |53; 7/29 PHI 현금 취득 |52; 현금 거래 미실행 기본은 NOP |
| Lakers 유래2R |52|53 DET; Dallas 현금 거래와 무관 |
| Charlotte 유래2R |42|38 DET; CHA 자체 원래 권리로 오인 금지 |
| Minnesota1R/2R |7/36|GSW7/OKC36, M의 기존 조건 승계 |

AP2/AP4는 **9·17·40·49** 네 자산을 이동시킨다. 실제40/51을 기계적으로 복사하지 않는다. 2022 LAL top10 보호1R의 MEM 이전을 조건부로 붙이지만 미전달 종료/변환 조항은 `null`; 다음 해 실제 순번을 대입하지 않는다. AP1은 해당 새 이전이 없고 NOP의 선행 권리를 유지한다.

기존 M의 Chicago 무거래1R·MIN 보호 결과를 보존한다. 나머지 과거 거래는 공개 원소유 표와 기존2020 승인 연쇄의 조건부 승계이며 모든2018–21 자산 이동을 독립적으로 다시 증명한 것은 아니다. 후속 초안은 이 구분을 상속한다.

## Boston 미래2R는 두 갈래를 합치지 않는다

기존 Bane 거래로 Boston이 MEM2025 자체2R를 확보한 연결은 `NBA_2021_ASSET_CHAIN.md`가 권위다. Fournier에게 **BOS/MEM 중 뒤 순번**이 이미 묶인다. Kemba 교환을 진행할 때 OKC가 받는 것은 **같은 두 자산 중 앞 순번**이다. Kemba 교환이 없으면 앞 순번을 Boston이 유지한다. 같은 출처를 두 번 지불하지 않는다. [SalarySwish 이력](https://www.salaryswish.com/trades/players/kemba-walker)과 [RealGM](https://basketball.realgm.com/player/Al-Horford/Summary/35)을 대조했다. 공식6/18과 SalarySwish6/19 표시 차이는 남긴다.

2023 Boston 수취 조건은 [Hoops Rumors 전재](https://kref.com/2021-nba-offseason-in-review-oklahoma-city-thunder/)에서 구체화했다. 숫자가 클수록 뒤 순번일 때 **max(OKC, WAS, min(DAL, MIA))**다. 네 자산의 단순 최댓값이 아니다. 예시 OKC31/WAS32/DAL59/MIA60이면 DAL59가 Boston 대상으로 남고 MIA60은 이 수취식에 포함되지 않는다. 이것은 픽의 최종 숫자를 가정한 산술 예시이며 실제2023 결산이 아니다. OKC 공식 검색은 세 자산 중 least favorable라는 요약만 확보했다. 전체 구성은2차 출처 해석으로 표시하며 비공개 거래 문서 검증 완료로 확대하지 않는다.

24개 상대순서와2025 앞뒤 두 순서×거래 유무4조건을 검사한다. 동률 추첨이 끝난 서로 다른2R 최종 번호만 입력하며 새로운 추첨을 만들지 않는다. 2023 다른 자산의 전체 수취팀까지 계산하는 함수가 아니다.

## AP1의 드래프트 당일 추가 거래 전 지배팀

| 순번 | 원소유 | 조건부 지배팀 |
|---:|---|---|
| 1 | CHA | CHA |
| 2 | HOU | HOU |
| 3 | ORL | ORL |
| 4 | OKC | OKC |
| 5 | DET | DET |
| 6 | CLE | CLE |
| 7 | MIN | GSW |
| 8 | TOR | TOR |
| 9 | NOP | NOP |
| 10 | CHI | CHI |
| 11 | SAC | SAC |
| 12 | WAS | WAS |
| 13 | SAS | SAS |
| 14 | GSW | GSW |
| 15 | IND | IND |
| 16 | BOS | OKC |
| 17 | MEM | MEM |
| 18 | MIA | OKC |
| 19 | ATL | ATL |
| 20 | NYK | NYK |
| 21 | POR | HOU |
| 22 | LAL | LAL |
| 23 | DAL | NYK |
| 24 | MIL | HOU |
| 25 | LAC | LAC |
| 26 | DEN | DEN |
| 27 | BKN | BKN |
| 28 | PHI | PHI |
| 29 | PHX | PHX |
| 30 | UTA | UTA |
| 31 | HOU | MIL |
| 32 | DET | NYK |
| 33 | ORL | ORL |
| 34 | CLE | NOP |
| 35 | OKC | OKC |
| 36 | MIN | OKC |
| 37 | TOR | DET |
| 38 | CHA | DET |
| 39 | CHI | CHI |
| 40 | NOP | NOP |
| 41 | SAC | SAC |
| 42 | WAS | NOP |
| 43 | IND | BKN |
| 44 | SAS | SAS |
| 45 | BOS | BOS |
| 46 | MEM | TOR |
| 47 | MIA | ATL |
| 48 | GSW | TOR |
| 49 | POR | MEM |
| 50 | NYK | PHI |
| 51 | ATL | BKN |
| 52 | DAL | NOP |
| 53 | LAL | DET |
| 54 | MIL | IND |
| 55 | DEN | OKC |
| 56 | LAC | CHA |
| 57 | PHI | NYK |
| 58 | BKN | CHA |
| 59 | PHX | BKN |
| 60 | UTA | IND |

OKC16→HOU의 Sengun 목적 거래, NYK20/23의 이동, MIL31/IND54·60, LAL22/WAS의 Westbrook 연쇄, DET37/CHA58, ORL33 현금/미래픽 거래 등은 이 표에 아직 실행하지 않았다. 이 표를 실제 드래프트 종료 소유권으로 사용하면 안 된다. Chicago39 Edwards도 앞선 선수 비교가 끝나기 전에는 가용성 미확정이다. 다음은 AP1과 G4 각 보드에 기반한15번 이후 선수·목적 거래 재판정이다.

## 검증

신규6개 검사 PASS. 네 안240행의 정체성, 잘못된 송신자/이중 양도 거부, 서로 뒤집힌 CHI/NOP swap, Dallas52 현금 사건, 중첩2023/분리2025 수취, G4 재판정 표시를 확인했다. 이 산술은 거래의 동기·규정 적법성·의학적 가용성을 증명하지 않는다. JSON 재현과 G2 원본 해시 검사는 별도 검토 기록을 따른다.
