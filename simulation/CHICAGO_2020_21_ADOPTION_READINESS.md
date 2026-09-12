# O-15F14-L — 시즌 채택 전 마지막 의존 항목

- 기준: PR #160, main `38b7a95b33303a7cf42b4cd3a8c9e20dad3e2d37`, 2026-09-12.
- 판정: `PACKET_ASSEMBLED / FACT_BLOCKERS_OPEN / NOT_READY_FOR_FINAL_ADOPTION`.
- 기존 K1·L2 추천과 H 방향 승인을 연결하는 검토 색인이다. 사실·수치의 권위 문서는 아래 링크를 유지한다.
- `author_locked=false`, `season_selected=false`, `manuscript_allowed=false`. v0.30 PARTIAL·설계/원고 CLOSED.

## 1. 현재 추천을 한 번에 읽기

K1은 J1 Terry 후반 공백, Orlando Hall/Wagner 유지, LOW 분 정책, Porter ZERO, 라이벌 R1/28분, 피로 0.5, BPM 전체 경로다. Chicago 31승 41패·동부 10위, Minnesota 24승 48패·서부 13위로 연결된다. RAPTOR는 다른 전체 경로로 보존한다. 경기마다 유리한 지표를 고르지 않는다.

L2는 Chicago가 Washington 원정에서 이긴 뒤 Indiana 원정에서 탈락하는 사건 추천이다. 정규시즌 계산이 플레이인 승패까지 예측한 것은 아니다. 동부 BOS의 IND전 승리, 서부 POR–GSW/POR승·MEM–SAS/MEM승·MEM–GSW/MEM승도 같은 사건 패킷에 포함된다. Chicago만 선택하고 다른 참가팀을 실역사로 자동 채우지 않는다.

| 선택 ID | 새로 채택할 구체적 내용 | 보존할 제한 |
|---|---|---|
| A1 가용성 | K1의 1,079행 조건부 달력과 J1 Terry 27경기 공백 | 실제 진단·발병일·시즌 건강 인증이 아니다. Carter/Porter의 기존 겨울 공백을 다시 차감하지 않는다. |
| A2 등록 사건 | 기존 Carter-Williams·Fultz·Isaac·Ross 결장 조건을 유지하고 Hall hardship 신청·승인 경로를 작품 사건으로 채택 | 4명의 새 부상·의사 발언을 만들지 않는다. 확인된 규정/등록 비용과 결합해야 한다. |
| A3 방법·시즌 사건 | K1/BPM의 전체 정규시즌과 L2 동서부 플레이인 패킷 | 점수·개인 박스·추첨 결과는 포함하지 않는다. R1/T1~T4 방향 재승인이 아니다. |

세 선택은 아직 채택되지 않았다. 현재의 ‘이어서’는 조사·패킷 정리 실행으로 기록하며, 미해소 사실이나 시즌 승패의 자동 승인으로 확대하지 않는다. 아래 사실 조건이 남아 있으므로 이번 작업에서 최종 승인을 요청하지 않는다.

## 2. 남은 사실 항목은 다섯 묶음으로 관리한다

아래 다섯 행은 새로운 조사 범위가 아니라 기존 네 K 조건에 흩어진 잔여 필드를 묶은 것이다. 모든 필드의 원계약 원문만을 유일한 해소 수단으로 삼지는 않되, 공개 근거 수준과 조건부 추론을 명시해야 한다. 근거가 없는 값은 작가 선택으로 채우지 않는다.

| ID / 연결 조건 | 확보된 범위와 권위 | 마지막 필요한 결과 | 조건이 달라지면 다시 볼 범위 |
|---|---|---|---|
| F1 / K_TRANSACTIONS | [Chicago 급여 범위](CHICAGO_2020_21_TAX_BOUND.md): 알려진 급여 상단 $127,017,028, R 한도 $5,609,972 | 해당 거래 직후의 방출/미서명/예외 등 적용 항목을 식별한 R 원장 또는 근거 있는 상한. incoming/outgoing 정확 charge도 연결 | R이 한도를 넘거나 matching 여유 $175,985.75를 소진할 때 Chicago 거래 구조를 재검토. 이를 확인하기 위한 주인공 순번 선확정은 불필요 |
| F2 / K_TRANSACTIONS | [Boston 자산 연결](NBA_2021_ASSET_CHAIN.md): TPE 사용 보도, 후대 잔액, Bane발 MEM2025 출처 | 거래 시점 다른 TPE 사용 및 수취 charge, BOS/MEM2025·BOS2027 의무의 보호/우선권 확인 | Fournier 수취 불가나 대가 자산 중복이면 거래를 재검토. 후대 $11.05m 잔액만으로 당일 적법성을 확정하지 않는다 |
| F3 / K_TRANSACTIONS | [거래 조건](CHICAGO_2020_21_EXECUTION_TERMS.md), [자산 연결](NBA_2021_ASSET_CHAIN.md): Gordon 공개 인센티브 포함 산술·선행/후행 보호 보도 | 미확인 추가 charge 및 적용 팀 제한, 선행 의무와 Gordon 후행 의무의 연결·최종 종료, 해당 자산 가용성 | 금전 부담 변화는 matching 검사부터, 픽 변화는 2020 Nnaji24 취득 의무와 미래 처분 가능 연도부터 재검토. 픽이 먼 미래라는 이유로 거래 확정의 HOLD를 삭제하지 않는다 |
| F4 / K_REGISTRATION | [등록 장부](ORLANDO_2020_21_REGISTRATION_LEDGER.md), [실행 조건](CHICAGO_2020_21_EXECUTION_TERMS.md): 날짜·자리·Hall 신청 4명 근거 | Hall/Wagner/Parker/Rivers/Brazdeikis 등 후속 계약의 적용 charge·사용 예외와 팀 한도. Hall cap-hit 0의 당시 적용 근거 | 등록이 달라지는 선수·날짜의 분 배정부터 수정. 1,080경기 전량 재수집은 하지 않는다. F5와 중복 수집하지 않는다 |
| F5 / K_REGISTRATION·K_TRANSACTIONS | [종료 패킷](CHICAGO_2020_21_EXECUTION_CLOSEOUT.md): McGee 구단 공지와 후속 날짜 근거 | McGee 거래의 미기재 보호/종료 및 기존 픽 처분·등록 비용, 나머지 거래 당사자의 열린 실행 필드 회수 | 해당 거래와 상대 분 입력부터 확인. 공식 공지의 무기재를 무보호 계약으로 바꾸지 않는다 |

각 행은 한 개의 간단한 조회로 끝난다는 의미가 아니다. 기존 출처 JSON의 null 필드와 대조해 실제로 해소한 필드만 갱신한다. 네 K 묶음의 전체 종료 수는 여전히 0이다.

## 3. 무엇을 지금 계산하지 않는가

건강·등록·거래의 사실 조건을 통과하고 A1~A3의 채택 기록이 생기기 전에는 2021 동률 추첨과 상위 4픽 추첨을 실행하지 않는다. 먼저 결과를 본 뒤 시즌안이나 seed를 바꾸는 역선택을 막기 위해서다. 기존 [드래프트 인과 규약](DRAFT_CAUSALITY_PROTOCOL.md)의 고정 seed 규칙을 그대로 사용하며 새 seed 후보를 만들지 않는다.

L2 조건부 추첨 전 Chicago 9~10 동률군·Minnesota 6위는 최종 지명 순번이 아니다. Chicago 자기 1R 보유 경로와 Minnesota 보호픽 소유권은 실제 추첨 뒤 해당 의무에 따라 결산한다. F3의 2025~27 종료 문제를 2021 순번 산술과 혼동하지 않되, 거래 발생을 확정하는 데 필요한 조건으로는 계속 보존한다.

I의 Washington HIGH/RAPTOR 반례, F의 비상 역할 비용 반례, K의 4경기 잔여 빅맨 중복은 기존 권위에 남긴다. 이번 색인은 이를 해소하거나 합산한 새 계산이 아니다.

## 4. 이번 추가 조회의 결과와 중단 지점

2026-09-12에 Gordon 종료 문구와 Chicago dead money를 추가 검색했다. 검색 결과는 일부 서비스의 홈으로 연결됐고 다음 상세 페이지는 본문을 확보하지 못했다. 공개 페이지 직접 요청은 HTTP 403이었다.

- https://www.prosportstransactions.com/basketball/DraftTrades/Future/Nuggets.htm
- https://basketball.realgm.com/nba/draft/future_drafts/detailed
- https://www.spotrac.com/nba/chicago-bulls/cap/_/year/2020

검색 요약에 보인 Vonleh 금액을 R의 실제값으로 채택하지 않았고, 현재 시점 픽 목록을 2021 원계약으로 사용하지 않았다. 이번 신규 확정 사실은 0건이다. 접근 실패를 거래 부재·보장액 0의 증거로 쓰지 않는다.

## 5. 다음 실행 순서와 종료 기준

다음 조사 시작점은 F1이다. 기존 15명 급여를 다시 합산하지 말고 누락 charge의 구성 항목과 적용 여부만 회수한다. F2~F5는 서로의 근거를 재사용한다. 새 출처가 없으면 ‘재조회 완료’를 ‘조건 해소’로 세지 않고 해당 필드와 실패한 경로를 남긴다.

사실 조건 통과 → A1~A3 구체안 채택 기록 → 고정 규약의 동률/lottery 실행 → 보호픽/소유권 결산 → 2020–21 종료 → 2021–23 거래·계약 순서다. 이미 승인한 Chicago 원클럽·Minnesota 라이벌·2020 드래프트·Theis/Green A·R1/T1~T4는 다시 묻지 않는다.

이번 수용 기준은 분산된 선택과 사실 의존의 단일 색인, 원권위 연결, 변경 시 재검토 범위, 무단 시즌/추첨 채택 방지다. 시즌 완료 수용 기준은 아직 미충족이다. 전체 7묶음 중 1완료·1진행·5대기, 진행 중 포함 남은 큰 작업 6개.


### F1 구성 후속

`CHICAGO_2020_21_RESIDUAL_COMPONENTS.md` 및 동명JSON에서 타팀계약3건과 빈자리 규칙을 연결했다. 앞서 미분류였던 해당 FA항목만 좁혔으며 실제R·정확거래·시즌은 여전히HOLD다. 기존한도에서 제외액을 다시 빼지 않는다. 다음은 방출잔액 및 이전FA/1R권리 목록이다.


### F4 후반 계약 금액 후속

[NBA_2020_21_REGISTRATION_COSTS.md](NBA_2020_21_REGISTRATION_COSTS.md)와 동명 JSON에서 5명·9계약의 보고 급여와 일할 계산을 회수했다. 이전의 해당 금액 미확보 표현은 이 범위에서 이력이다. Hall의 0달러 제외 근거는 HOLD이며, 전액 비용안으로도 팀 한도를 검사할 수 있게 했다. 다음은 이 금액을 재조회하는 일이 아니라 ORL/BOS/DEN의 누적 장부·한도와 남은 앞선 단기 계약을 연결하는 작업이다. 기존 등록 구간·추가 1자리 5경기·K1/L2·작가/시즌 HOLD는 유지한다.
