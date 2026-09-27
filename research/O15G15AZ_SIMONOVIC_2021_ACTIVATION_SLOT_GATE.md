# O-15G15AZ — Simonović 2020 지명권의 2021 일반명단 전환 검문

- 기준: `main` `49ca10e`, [2020 Draft 44번 확정](../simulation/2020_DRAFT_NICK_RICHARDS_RELANDING_BOARD.md), [PROJECT_FREEZE v0.30](../canon/PROJECT_FREEZE.md), [G8 2021 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md), [G15AY 투웨이 자리](O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md). 판정: `2020_DRAFT_RIGHTS_LOCKED / 2021_ACTIVATION_AND_STANDARD_SLOT_HOLD`.
- 작가확정은 **Chicago 2020년 44번 Marko Simonović 지명권**이다. [STORY_BIBLE](../canon/STORY_BIBLE.md)의 2020–21 개막 시 **조기 합류 없음**도 정본이다. 이 둘을 2021–22에도 반드시 해외 보관하거나 반드시 NBA 계약시킨다는 결정으로 확대하지 않는다.

## 실제 사건과 대체 세계의 경계

| 원역사 시점 | 1차 자료가 확인하는 범위 | 조건부 Chicago 처리 |
|---|---|---|
| 2020 Draft→2020–21 | 2020 #44 Bulls 지명은 [2020 NBA 이동표](https://www.nba.com/news/nba-player-movement-2020-offseason)와 정본 일치. [Chicago의 2021-08-18 계약 발표](https://www.nba.com/bulls/news/bulls-sign-rookies-dosunmu-and-simonovic)는 그가 2020–21 Mega Basket에서 뛰었다고 밝힌다. | 이 작품의 2020–21 조기 합류 금지는 유지한다. 지명권 자체를 삭제하지 않는다. |
| 2021-08-04 | [Chicago Summer League 명단 발표](https://www.nba.com/bulls/news/bulls-announce-mgm-resorts-nba-summer-league-2021-roster)는 실제 Simonović를 포함한다. | Summer League 참가만으로 대체 NBA 일반계약 서명을 만들지 않는다. |
| 2021-08-18 | [Bulls의 Dosunmu·Simonović 계약 발표](https://www.nba.com/bulls/news/bulls-sign-rookies-dosunmu-and-simonovic)는 실제 #44 선수의 NBA 계약과 **계약 조항 비공개**를 확인한다. | 대체 #39 Wieskamp와 2020 #44 Simonović의 둘 다 서명 여부·순서·급여·선수/구단 합의는 별도 `HOLD`. 원역사 계약일이나 미공개 급여를 복사하지 않는다. |
| 2021-10-25/28 | [Windy City 공식 공지](https://windycity.gleague.nba.com/news/windy-city-bulls-finalize-training-camp-roster-announce-basketball-operations-staff)와 [NBA 경기 기록](https://statsdmz.nba.com/pdfs/20211028/20211028_NYKCHI_book.pdf)은 Simonović를 Chicago의 **G League 배정 선수**, Dotson/Cook을 투웨이로 따로 표시한다. | 배정은 원역사 **일반 NBA 계약 이후의** 경기 운영 형태다. “G League 소속이니 투웨이 자리”로 읽지 않는다. 10/20 Chicago 첫 경기 상태는 이 두 자료만으로 소급하지 않는다. |

원역사의 2021 #38 Dosunmu는 [G7 조건부 2021 Draft 보드](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)에서 다른 팀에 배치됐으므로 같은 8/18 발표의 Dosunmu 계약을 대체 Chicago에 동시에 복사할 수 없다. 실제 Simonović의 NBA 계약도 위 2020 지명권으로 **가능한 선례**이지 이 세계의 자동 계약은 아니다.

## G8 마지막 일반계약 자리의 충돌

[G8 SQ1의 15명 예산](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json)은 조건부 #10 Duarte·#39 Wieskamp **일반계약**, Bradley·Stanley·Valentine 등을 포함하며 Simonović의 2021 계약 급여/자리는 포함하지 않는다. G3의 이전 Moody/Edwards 명단을 현재 지명 결과로 세지 않는다. 아래는 나머지 G8 입력과 미확인 순증 `R`을 고정한 **자리 구조와 부분합 식**이다. `M`은 대체 Simonović 일반계약의 Team Salary 차지, `X`는 그 대신 빠지는 G8 일반계약 선수의 기존 차지다. 둘 다 실제 값은 `null`이고, 방출잔액·권리 정리·예외/순서 효과는 별도다.

여기서 자리 15명은 **정규시즌 최종 일반계약 명단**의 검문이다. 여름 캠프 중 일시적으로 16명을 계약할 수 있는지와 시즌 개막에 16명 일반계약을 그대로 보유할 수 있는지는 다른 문제다. 이 표는 캠프 계약 상한이나 컷다운 날짜를 인증하지 않는다.

이 표의 `$106,862,083`은 G8 SQ1의 **알려진 급여·산입액 합계 예시**이지 apron 상한 `$143,002,000`이나 그 상한까지 남은 공간이 아니다. 실제 전체 Team Salary는 미확인 `R` 때문에 확정되지 않았다. 아래 식의 `M/X`가 미정이면 새 최종 합계도 미정이다.

| 후보 | Simonović / #39 | 조건부 최종 일반 / 투웨이 | 알려진 G8 apron 예산의 한 변수 식 | 검문 |
|---|---|---:|---:|---|
| `S0` | Simonović 미서명·해외 보관 또는 지명권만 유지 / #39 일반 | 15 / #39 이외 투웨이 미배정 | `$106,862,083` | 2021 해외 계약·선수 의사·지명권/Required Tender 상태·도착 시점 `HOLD`. 미서명을 무료 무기한 권리로 단정하지 않는다. |
| `S1` | Simonović 일반 / #39 투웨이 | 15 / 최소 1 | `$106,862,083 − $925,258 + M` | 일반 마지막 자리를 두 선수 사이에서 교환. #39 투웨이 선수 동의·나머지 Dotson/Cook 자리 선택 필요. `M`이 없으므로 총액 숫자 `HOLD`. |
| `S2` | Simonović 일반 / #39 미서명·별도 보관 | 15 / #39 투웨이 0 | `$106,862,083 − $925,258 + M` | 같은 자리 산술이지만 #39 권리·Required Tender·해외 계약·선수 의사가 S1과 다르다. Wieskamp의 NBA 사용을 보장하지 않는다. |
| `S3` | Simonović 일반 / #39 일반 **모두** | 시즌 최종 선수 교체 전 16 / 불가 | 교체 후에만 `$106,862,083 − X + M` | G8의 다른 실명 일반계약 **한 명이 실제로 빠져야** 시즌 최종 15명. 방출·계약 미성립·트레이드는 서로 다른 거래이며 `X`와 남는 죽은 급여를 같이 검증한다. |

이 표는 Simonović가 **일반계약**인 경우와 2021 미서명/보관을 검사한다. Simonović 자신에게 투웨이를 제안하는 추가 경로는 2020 지명권·선수 자격·계약 동의·투웨이 두 자리와 두 신인 동시 소속을 별도로 확인해야 하므로 `UNMODELED_HOLD`다. 표의 `S0`도 해외 보관을 **확정 추천**한 것이 아니다. [G15AY](O15G15AY_CHICAGO_2021_TWO_WAY_SLOT_SCREEN.md)의 Dotson/Cook 역사 비교와 #39 투웨이 분기는 `S1`과 겹쳐 검사하고, 다른 선수들의 대체 계약을 자동 보존하지 않는다.

`S1/S2`의 식에서 `$106,862,083 − $925,258 = $105,936,825`는 #39 첫해 일반 급여를 뺀 **확인 가능한 부분합**이다. 여기에 미확인 `M`을 더하므로 `S1/S2`의 최종 알려진 산입액도 아직 숫자로 닫히지 않는다. G15AW의 `$105,936,825` 분기는 **Simonović를 추가하지 않아 일반계약 14명**이고, 여기의 `S1`은 **Simonović 일반계약을 추가해 15명**이다. 두 분기는 #39가 투웨이라는 점만 같고 일반명단 수와 비용이 다르다. normal cap의 계약 전후 빈자리/FA 보류액도 다시 계산해야 한다. 같은 해 NTMLE 사용에 따른 hard cap 경계, 2022–23 Simonović 계약 기간/보장·#39 상태는 아직 인증하지 않았다.

## 다음 판정 입력

- **사실:** 대체 세계 Chicago의 2020 #44 Simonović 지명권은 작가확정. 원역사 2021-08-18 Bulls는 그와 계약했다고 발표했고 조건을 공개하지 않았으며 10/25·10/28에는 배정 선수로 표시된다.
- **추론:** G8의 15명에 Simonović 일반계약을 단순 추가하면 16명이다. 서명하려면 #39의 계약 종류/서명 여부 또는 다른 일반계약 실명 한 명의 자리를 다시 정해야 한다.
- **후보:** `S0`~`S3`의 상호 배타적 자리 처리; Simonović 투웨이는 자격·자리 입력 전 미모델링. G8 `STD` 주 경로와 CP2 잠정 Draft 보드는 그대로 비교안이다.
- **작가확정:** 이번 새 선택 0건. 기존 2020 #44 지명권만 유지. Simonović의 2021 합류·Wieskamp 계약·선수 동의·2022 급여와 분·건강·시즌은 `HOLD`.

Codex는 기존 정본 2020 #44와 G8/G7 명단, Chicago 공식 발표·NBA 경기 기록을 직접 대조했다. NotebookLM CLI의 8/18 Chicago URL 추가는 `Could not add url source`로 실패해 새 출처 연결 분석 0건이다. Antigravity CLI는 직전 429 개인 한도 후 새 수집 `NOT_RUN`; 실패를 수집 성공으로 세지 않는다. Claude CLI의 도구 없는 [제한 반증](../reviews/R01_O15G15AZ_SIMONOVIC_SLOT_REBUTTAL.md)은 숫자 1건과 명단 1건을 모순으로 의심했으나 둘 다 원장 대조 후 **표현 명확화**로 처리했다. 새 source-blind는 `NOT_RUN`; 이 문서는 G16 전체 독립 검수나 정확 계약/시즌의 PASS가 아니다. D1 F1~F5 PASS 0/5·A1~A3 0/3·K 종료 0/4, G1A 선수 동의·D2 계약/픽/시즌 `HOLD`, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`.

Simonović를 실제로 계약하는 `S1/S2` 후보의 2년/3년 비용과 Caruso NTMLE 잔액·renounce 뒤 cap 공간의 **서로 다른 서명 순서**는 [G15BA 후속](O15G15BA_SIMONOVIC_2021_MLE_AND_CAP_TIMING.md)에 둔다. 원역사 2차 급여표의 `M1/M2`가 #39 제안 급여와 동액이어도 선수·계약 기간·예외 사용은 같지 않다.
