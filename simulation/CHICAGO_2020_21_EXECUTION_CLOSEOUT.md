# O-15F14-L — 실행 근거 회수와 시즌 종료 사건안

- 기준: 2026-09-12, PR #155 병합 main `c78fbe8b8055b2ace673ec5a349d37389cacacd6`.
- 상태: **L 부분 완료. 사실 회수·사건 추천 완료 / 정확 실행·작가 채택·추첨 HOLD.**
- 계산 권위: 동명 JSON. 사실 권위: `research/NBA_2020_21_L_EXECUTION_SOURCES.json`.
- K의 `author_locked=false`, `season_selected=false`를 유지한다. v0.30 PARTIAL, 설계/원고 CLOSED.

## 1. K 게시 복구 완료

기존 경로의 로컬 커밋 `f94be5c`와 검증 tree `86c0f66f04495f1008c1bef3de1e088a53586952`를 확인했다. 원격 main은 PR #154였고 K 브랜치/PR은 없었다. 14개 blob을 로컬 hash-object와 대조하고 같은 tree로 원격 커밋 `cfb99742b036edb21c3b10dabc74b8e3d8a99563`을 생성했다.

[PR #155](https://github.com/storm-credit/first-rebound/pull/155)를 그 head SHA 조건으로 병합했다. 원격·로컬 main SHA와 tree를 대조했고 원격 status/check-run은 모두 0건이었다. K 로컬 검증 6개·JSON 재현·공백 검사는 통과했다. 원격 CI PASS 또는 독립 검수 완료라는 뜻은 아니다. `tools/__pycache__/`는 제외했다.

## 2. 이번에 실제로 확보한 근거

검색 화면에서는 본문이 보이지 않았던 구단 공지를 공개 HTML 안의 본문 데이터에서 회수했다. 검색 요약만 읽은 자료와 구분하며, URL·발행시각·원문 및 본문 해시를 출처 JSON에 남겼다. 핵심 사실은 그 JSON의 6개 행을 단일 권위로 사용한다.

| 출처 ID | 이번에 해소한 빈칸 | 여전히 해소되지 않은 것 |
|---|---|---|
| [L_HALL](https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509) | 실제 계약 연쇄·마지막 계약의 예외 유형 | 새 세계 예외 자격·등록 자리·금액 |
| [L_WAGNER](https://www.nba.com/magic/orlando-magic-sign-moe-wagner-free-agent-center-20210427) | 영입과 방출의 연결 | 새 세계 해당 거래의 필요·급여 |
| [L_PARKER](https://www.nba.com/celtics/news/pressrelease/celtics-sign-jabari-parker) | 영입과 방출의 연결·현지 날짜 | 새 세계 계약 비용·의사결정 |
| [L_MCGEE](https://www.nba.com/cavaliers/releases/hartenstein-trade-210326) | 실제 대가와 일부 보호 범위 | 미기재 종료 문구·새 세계 자산 가용성 |
| [L_FOURNIER](https://www.nba.com/magic/orlando-magic-acquire-two-future-second-round-draft-picks-boston-celtics-evan-fournier-trade-20210325) | Orlando 쪽 예외 생성 | Boston 쪽 예외 잔액·정확 charge·픽 연도 |
| [L_WIGGINS](https://www.nba.com/warriors/news/warriors-acquire-wiggins-20200206) | 실제 2021 1R 보호 범위 | 대체 거래의 의무 채택·이연 조건 |

**받는 팀과 보내는 팀의 예외를 혼동하지 않는다.** L_FOURNIER가 Orlando 쪽을 설명한다고 Boston의 수취 조건까지 통과한 것은 아니다. L_MCGEE에 2027 보호가 적혀 있지 않다는 사실을 무보호·무조건 전달 계약의 원문 확보로 확대하지 않는다. 미공개 계약 조건은 0으로 채우지 않는다.

L_PARKER의 발행시각은 UTC 4/17이지만 미국 동부 날짜는 4/16이다. 출전 대조에는 현지 사건일을 적용한다. McGee의 구단 발표일과 거래 마감일을 동일한 시각으로 꾸미지 않으며, 여기서는 발표 이후 후반 달력만 검사한다.

## 3. 등록 날짜 대조와 남은 실무 조건

J의 후속선수 달력 중 Hall·Wagner·Parker·McGee 각 28행과 K의 Orlando Franks 28행, **총 140행**을 검사했다. K의 LOW 분을 사용했다. 등록 전·해제 뒤에 양수 분을 배정한 충돌은 0건이다. 양수 날짜는 Hall 14, Wagner 11, Parker 10, McGee 13, Franks 7이다. 이는 실제 GP나 새 세계 등록 적법성 인증이 아니다.

Hall의 새 세계 예외를 성립시키기 위해 실존 선수에게 새 부상을 만들지 않는다. 필요한 것은 당시 등록 인원·실제로 보존한 결장 조건·적용 규정의 대조다. 예외를 성립시킬 수 없다면 허용되는 자리 조정과 해당 선수의 분 영향만 재계산한다. K의 백업 필요성이나 J2 실패는 예외 자격의 대용물이 아니다.

Rivers는 K의 10일 계약 근거를 보존하지만, 그 하나만으로 잔여 시즌 전체의 등록 기간을 채우지 않는다. 이번 140행의 검증 대상에 Rivers와 Hutchison을 넣어 완료 수를 부풀리지 않았다. 새 경기 전량 수집은 만들지 않는다.

## 4. Chicago matching 여유의 정확한 산술

기존 CSV는 표시를 위해 허용액과 여유를 정수 달러로 반올림했다. 기존 비납세 구간과 기본급을 전제로 한 정확한 계산은 다음과 같다.

`3,767,981 × 1.75 + 100,000 − 6,517,981 = $175,985.75`

표시값 `$175,986` 전체를 추가 incoming charge로 써도 된다는 뜻은 아니다. outgoing charge가 고정이면 그 입력은 한도를 $0.25 넘는다. outgoing charge도 변하면 허용액이 같이 바뀌므로 incoming 추가분만 보는 검사를 전체 판정으로 쓰지 않는다. 기존 CSV의 역사적 표시는 보존하고 이번 정확 산술을 후속 기준으로 연결한다. 실제 bonus·당일 팀 비납세 자격은 여전히 미확보다.

## 5. 작가에게 제시할 네 사건안

공통 정규시즌 검토안은 K1/BPM F038이다. Chicago 31–41·동부10위, Minnesota 24–48·서부13위. RAPTOR F138은 별도 교차검산이며 경기마다 섞지 않는다. 1,079행 조건부 가용성도 K1과 한 패킷으로 검토한다. 주인공·LaMelo의 전 시즌 양수 분 배정과 Terry 후반 공백을 숨기지 않는다.

**L2를 추천한다.** 탈락전 한 번의 승리로 팀의 진전을 보여 주고, 다음 경기에서 드러난 지속성·역할 분담의 과제를 2021년 여름 설계로 넘길 수 있다. 이는 경기 모형의 예측이나 실존 팀에 대한 사실 판단이 아니라 서사 기능에 따른 추천이다. 점수·개인 박스·특정 선수의 패인 책임은 정하지 않는다.

| 사건안 | 동부 7–8위 경기 | Chicago의 결과 | 동부 진출팀 | Chicago 픽 위치의 의미 |
|---|---|---|---|---|
| L1 | BOS 승 | WAS 원정 패, 종료. WAS가 IND에도 승 | BOS·WAS | 추첨 전 성적순서 9~10 |
| **L2 추천** | BOS 승 | **WAS 원정 승 → IND 원정 패** | **BOS·IND** | **추첨 전 성적순서 9~10** |
| L3 | BOS 승 | WAS·IND 원정 연승 | BOS·CHI | 플레이오프팀 성적순서 15 |
| L4 | IND 승 | WAS 원정 승 → BOS 원정 패 | IND·BOS | 추첨 전 성적순서 9~10 |

L1은 시즌 끝의 단기 성취가 약하고, L3는 두 원정 승리의 비용과 이후 Philadelphia 시리즈 설계가 추가로 필요하다. L4는 가능하지만 Boston을 두 번째 문턱으로 삼아야 하는 별도 이유가 아직 없다. L2는 한 차례의 성취와 다음 단계의 과제를 연결하기에 적합하다. 넷은 상호 배타적인 사건 패킷이며 전체 8개 동부 분기를 다시 전수조사한 표가 아니다.

비교를 위한 **공통 서부 추천 사건**은 POR이 GSW에 승, MEM이 SAS에 승, MEM이 GSW에 승이다. 서부 7·8번시드는 POR·MEM이며 LAL은 K1에서 이미 6위다. 실제 2021 플레이인을 그대로 복사한 결과가 아니다. 서부 결과도 `AUTHOR_EVENT_PROPOSAL_NOT_GAME_MODEL`이고 별도 승패 계산·작가 채택은 없다.

## 6. L2의 픽 결산 준비

동서부 사건안을 결합해 16개 플레이오프팀과 14개 추첨팀을 분리했다. L2의 추첨팀 성적순서는 다음과 같다. 이는 우리 조건부 시즌을 직접 계산한 결과다.

| 추첨 전 성적순서 | 팀 | 승수 |
|---|---|---:|
| 1 | HOU | 17 |
| 2~3 | DET·ORL | 20 |
| 4~5 | CLE·OKC | 22 |
| 6 | MIN | 24 |
| 7 | TOR | 28 |
| 8 | CHA | 30 |
| 9~10 | CHI·NOP | 31 |
| 11 | SAC | 32 |
| 12 | WAS | 33 |
| 13 | SAS | 34 |
| 14 | GSW | 40 |

Chicago는 Vučević 거래를 하지 않았으므로 자기 1R을 보유하는 승인 경로를 유지한다. Minnesota의 성적순서 6을 최종 6번 픽이나 GSW 전달로 바꾸지 않는다. 기존 거래 의무가 새 세계에서 확정된 경우에만 보호 조항과 실제 추첨 결과를 결합한다. 위 두 팀의 `final_pick`은 모두 `null`이다.

동률 추첨과 상위 4픽 추첨은 별도다. [2021 공식 형식](https://www.nba.com/news/ties-broken-for-order-of-selection-in-2021-nba-draft)을 보존하며 실제 추첨 결과를 복사하지 않는다. 현재 연도로 갱신된 일반 FAQ는 당시 기록의 대체 근거로 쓰지 않았다. 픽 결산 완료는 아직 아니다.

## 7. 네 조건 묶음의 종료 기준

| 조건 | 이번 처리 | 아직 필요한 마지막 결과 |
|---|---|---|
| K_HEALTH | K1의 구체적 가용성 패킷 추천 유지 | 새 세계 달력 채택. 실존인 진단 창작 금지 |
| K_REGISTRATION | 공식 날짜·교체 연결 회수, 140행 충돌0 | 자리·예외 자격·charge 및 Rivers 후속 기간 |
| K_TRANSACTIONS | 실제 자산 일부·예외 생성 회수, CHI 정확 산술 | CHI 당일 전제, Gordon 선행/후행1R, BOS 예외·픽 의무 |
| K_METHOD_EVENTS | 네 사건안·L2 추천·14팀·성적 동률군 | 단일 경로와 사건 채택 후 동률/lottery·소유권 결산 |

**네 묶음 중 완전히 닫힌 묶음은 0개다.** 세부 사실 회수를 시즌 확정으로 포장하지 않는다. 이미 승인한 R1/T1~T4·Chicago 방향은 다시 묻지 않는다. 미확보 사실을 작가 승인으로 대체할 수도 없으므로 이번 종료 보고에서 시즌 확정 승인을 요청하지 않는다.

다음은 L 잔여 실행 장부다. 이번에 확보한 사실을 다시 찾지 않고, Hall의 등록 인원/예외 조건과 Chicago·Gordon·Fournier의 아직 비어 있는 실행 필드부터 처리한다. 서사 추천과 정확 사실이 갖춰진 뒤 채택 결과를 한 번 기록하고 추첨을 연결한다. 전체 7묶음 중 1완료·1진행·5대기, 남은 큰 작업 6개다.


## L 등록 인원 후속 반영

`ORLANDO_2020_21_REGISTRATION_LEDGER.md` 및 동명JSON을 후속 권위로 연결한다. 앞선 Rivers 후속 본문 미확보와 ORL 자리 수 미산출은 이력이다. 후속에서 구단본문9건 추가·계약 유형 및 기간을 회수하고 ORL 5/9 이후 일반계약16+투웨이2/추가1자리 필요5경기를 특정했다. 정확 허가·charge·거래 의무·작가 채택은 여전히 HOLD다. 날짜만 확인한 선행140행과 새 등록 인원 대조의 범위를 혼합하지 않는다.


## L 실행 조항·급여 후속 반영

`CHICAGO_2020_21_EXECUTION_TERMS.md` 및 동명JSON을 후속 권위로 연결한다. Hall 신청의4명 결장 근거·2019규약6.08, Harris/Gordon 등8명의2차 급여 항목, Denver 선행 보호기간과 Fournier 픽 연도 일부를 회수했다. 선행 미확보 표현은 해당 범위에서 이력이다. 정확charge·리그 승인·당일 팀 세금/예외·픽 연결/종료는 미완료이며 K1/L2 추천을 작가 확정으로 올리지 않는다.
