# O-15G15AW — Chicago 잠정 39번 Wieskamp 계약 종류·자리 검문

- 기준: `main` `4ba8345`, [G7 드래프트 비교](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)와 [G8 SQ1 계약 순서](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md). 판정: `STANDARD_15_VS_TWO_WAY_14_BRANCH / D2_CONTRACT_HOLD`.
- Chicago 2020–21 D1 정확 시즌은 미완료다. CP2의 `DB1/C39A` Chicago #10 Duarte·#39 Wieskamp와 SQ1 Caruso/Bradley는 **조건부 주 경로**이며 지명·서명·선수 동의의 작가확정이 아니다.

## 같은 선수, 다른 계약

| 층위 | 날짜·출처 | 이 프로젝트에 허용되는 판정 |
|---|---|---|
| 원역사 지명·계약 | [Spurs의 2021-09-07 공식 발표](https://www.nba.com/spurs/news/spurs-sign-joe-wieskamp-two-way-contract): San Antonio는 Wieskamp를 **41번**에 지명하고 **투웨이 계약**을 맺었다. | Chicago #39의 계약 종류·서명일·선수 수락을 인증하지 않는다. 다만 2021년 선수/시장에서 투웨이 경로가 실제로 사용됐다는 기준선이다. |
| CP2 조건부 권리 | [G7](../simulation/NBA_2021_FULL_DRAFT_COMPARISON.md)은 Chicago #39 Wieskamp를 주 비교안에 둔다. [G3의 이전 Moody/Edwards 보드](../simulation/CHICAGO_2021_NAMED_ROSTER_OPTIONS.md)는 당시 입력 이력이다. | #39를 실제 지명했다는 결론이 아니며 Spurs #41 권리·계약을 동시에 보존하지 않는다. |
| 현재 주 계약 | [G8](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.md)은 #39에게 2년 **일반 최소계약** `$925,258 / $1,563,518`을 제안한다. | 원역사 Spurs 투웨이와 **다른** 대체 계약 제안. 일반 명단 1자리와 2022–23 예산이 포함된다. |

[NBA의 2021–22 로스터 규칙](https://pr.nba.com/nba-board-of-governors-play-in-roster-rules-2021-22-season/)은 계약 최대치를 일반 15명·투웨이 2명으로 분리한다. [당시 NBA CBA 101의 로스터/투웨이 설명](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)은 정규시즌 일반 명단이 통상 14~15명이고 투웨이 계약 급여는 **Team Salary에 넣지 않는다**고 설명한다. 투웨이는 일반계약의 저렴한 이름표가 아니다. NBA 경기 가용성·전환·투웨이 슬롯을 따로 추적해야 한다. #39 지명권 보유와 계약 체결 사이에는 [2라운드 Required Tender 경계](O15G15P_HERBERT_33_SECOND_ROUND_TENDER.md)도 적용된다. 제안만으로 계약 수락을 만들지 않는다.

## 기존 SQ1 상단 예산의 두 분기

[G8의 SQ1 최상단 산술 예시](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json)는 주인공 급여 상단·Young 보너스 `$1m`·미확인 순증 `R=0`을 **시험 입력**으로 두고, Duarte·Green→Caruso NTMLE→Markkanen Bird→권리 정리→Wieskamp·Bradley·Stanley·Valentine 일반 최소계약 순서를 기록한다. `R=0`을 실제 팀 원장으로 채택하지 않는다.

| 조건부 경로 | 최종 일반계약 | 투웨이 Wieskamp | 같은 가정의 알려진 apron 예산 | `$143,002,000`까지 단순 차이 |
|---|---:|---:|---:|---:|
| G8 SQ1 일반 2년 계약 | 15 | 0 | `$106,862,083` | `$36,139,917` |
| #39 투웨이로 계약 종류만 변경 | 14 | 1 | `$105,936,825` | `$37,065,175` |

두 번째 행은 첫째 행에서 **일반계약 첫해 `$925,258`만 제거한 민감도**다. 투웨이 급여가 팀 샐러리에서 제외된다는 규칙을 적용했지만 실제 현금 지급을 0이라 하지 않는다. 정상 cap·다른 FA 보류액/예외·실제 `R`·계약 보호·2021–22 두 투웨이 슬롯의 다른 사용자까지 인증한 팀 예산이 아니다. 14명은 일반 최소명단의 하한에 닿으므로 **다른 일반계약 한 명이 불성립하면** 대체 계약·자리 처리가 필요하다. 기존 Dotson 등의 투웨이 상태도 원역사 [Chicago 8/19 공지](https://www.nba.com/bulls/news/bulls-sign-free-agents-bradley-green-and-dotson)에서 대체 세계로 자동 복사하지 않는다.

G8 SQ1의 Caruso는 [원역사 Chicago 8/10 공지](https://www.nba.com/bulls/news/bulls-sign-alex-caruso), Bradley·Green은 **8/19 공지**와 비교할 수 있지만, 대체 팀이 같은 날 같은 조건으로 서명했다는 뜻이 아니다. [NBA의 2021 FA 일정](https://www.nba.com/news/nba-announces-start-date-for-2021-free-agency)은 협상 8/2, FA 서명 8/6 이후를 구분한다. #10 Duarte의 원역사 Indiana **13번·8/4 서명**은 [Pacers 공식 2022 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612754/2022/10/2022-23-Pacers-Media-Guide-compressed.pdf)의 사건표다. 대체 #10 권리와 계약일을 Indiana에서 복사하지 않는다. 조건부 2021 Chicago 사건 순서는 **드래프트 권리 확보→가능한 계약 종류/선수 수락→SQ1 Caruso/Mark/최소계약**으로 유지하되, 각 대체 날짜는 `HOLD`다.

2022–23에는 G8의 Wieskamp 일반계약 **둘째 해 `$1,563,518`**과 Coby RFA/새 신인·Bradley 옵션을 함께 예산화했다. 투웨이 분기를 택하면 그 일반계약 둘째 해 행을 그대로 두거나 동일한 투웨이 보수로 치환할 수 없다. Wieskamp가 현재 [G1A 정상일 10인 분표](../simulation/CHICAGO_2021_23_CONTINUATION.md) 밖이라는 이유로 투웨이 전환을 확정하지 않는다.

## 2022–23 RT1~RT4 연결: 계약 행 하나의 민감도

[당시 CBA 101](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)의 투웨이 설명은 계약 기간을 1년 또는 2년으로 제한하고, 투웨이 급여를 Team Salary에서 제외하며, 계약 기간 중 일반계약 전환은 해당 선수의 최소급여·같은 기간을 따른다고 한다. 따라서 **2021년에 2년 투웨이를 실제로 체결했거나, 1년 뒤 적법하게 다시 체결해 2022–23에도 투웨이인 경우**에만 아래 `TW22` 비교가 해당한다. 1년 계약이 만료되었다는 사실만으로 2022–23 재계약·제한적 FA·권리 보유를 만들지 않는다. 2017 CBA의 투웨이 RFA에는 마지막 시즌 NBA 활성/비활성 명단 15일 이상 및 qualifying offer 조건이 있다. 원역사 Spurs 계약 기간이나 대체 Chicago의 해당 일수는 아직 확인하지 않았다.

기존 [G8 JSON](../simulation/CHICAGO_2021_23_CONTRACT_SEQUENCE.json)의 RT1~RT4 **192조건 전부**는 일반계약 15명, Wieskamp 둘째 해 `$1,563,518`을 포함한다. 다른 14명·P/Carter/Young·2022 신인 예산을 고정하고 이 한 행만 빼면 `TW22`의 일반계약은 14명이며, 알려진 팀 예산은 각 조건에서 정확히 `$1,563,518` 감소한다. 투웨이 급여는 팀 예산에서 제외하지만 지급 현금이 없다는 뜻은 아니다. 새 일반계약·미확인 순증 `R_2022`·방출잔액은 아직 더하지 않은 **한 변수 민감도**다.

| G8 유지 정책 | 같은 입력의 일반계약 예산 | `TW22` 일반 14명 예산 | `TW22` 세금선까지 | 새 hard-cap 유발 시 apron까지 |
|---|---:|---:|---:|---:|
| RT1 Bradley·Valentine 유지 | `$146,922,422` | `$145,358,904` | `$4,908,096` | `$11,624,096` |
| RT2 Bradley 이탈 | `$146,886,104` | `$145,322,586` | `$4,944,414` | `$11,660,414` |
| RT3 Valentine 이탈 | `$146,728,502` | `$145,164,984` | `$5,102,016` | `$11,818,016` |
| RT4 둘 다 이탈 | `$146,692,184` | `$145,128,666` | `$5,138,334` | `$11,854,334` |

표는 G8의 동일 예시 `P 첫해 $22m / Carter $14.15m / Young 또는 대체 $8.65m / 2022 신인 예비 $10.13m`를 고정했다. [NBA의 2022–23 세금선 `$150.267m`](https://pr.nba.com/nba-salary-cap-2022-23-season/)과 G8의 **새 hard-cap이 실제 유발되는 경우에만 쓰는** apron `$156.983m`을 비교했다. 2021 NTMLE 사용을 2022 hard-cap 사건으로 복사하지 않는다. RT3/RT4의 Valentine 방출잔액은 G8에서 `null`이며, 여유 표에 0으로 확정하지 않았다. 동일 192조건에서 자리 15→14, 팀 예산 `−$1,563,518`, 세금선/조건부 apron 차이 `+$1,563,518`을 재집계했다. 이것은 투웨이 계약의 적법성·선수 수락·실제 팀 샐러리 PASS가 아니다.

일반 15번째 자리에 **다른 선수**를 계약하면 위 팀 예산에 그 선수의 실제 Team Salary 차지 `S`를 다시 더하고 빈자리·예외·최소명단을 재검사한다. Wieskamp 자신을 일반계약으로 전환하면 `S`는 그의 적용 최소급여와 유효 기간에서 결정되므로 이 표의 절약액을 유지할 수 없다. 2022–23 [구단 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612754/2022/10/2022-23-Pacers-Media-Guide-compressed.pdf)는 투웨이 선수의 정규시즌 활성 명단을 최대 50경기로 설명하며 늦게 서명하면 비례 축소한다. [NBA의 2023 파이널 명단 설명](https://www.nba.com/news/how-the-2023-nba-finals-rosters-were-built-denver-nuggets)은 투웨이 선수가 포스트시즌에 출전할 수 없다고 명시한다. 따라서 `TW22` Wieskamp는 자격·가용성을 충족하는 **정규시즌 최대 50경기 안에서는 백업으로 쓸 수 있으나**, 무제한 정규시즌 백업이나 플레이오프 출전 선수로 계획할 수 없다. 대체 Chicago의 실제 투웨이 2자리 사용자·계약 기간·활성 경기 수·전환 날짜와 추가 일반계약 선수는 `HOLD`다.

**사실:** 원역사 Spurs #41·9/7 투웨이, Bulls 원역사 발표일, 당시 일반/투웨이 명단·팀 샐러리 규칙. **추론:** 같은 G8 가정에서 일반→투웨이 변경 시 일반 명단 15→14, 알려진 첫해 예산 `−$925,258`. **후보:** Chicago #39 Wieskamp, 일반 2년/투웨이 두 경로. **작가확정:** 0건. G1A 선수 동의·D1 F1~F5/A1~A3·D2 실제 계약/픽/시즌은 `HOLD`, K1/L2/CP2는 잠정이다.

## 검증 계보와 이어갈 조건

Codex가 G7/G8/G3의 지명권·계약 종류와 NBA/Spurs/Bulls/Pacers 공식 원문을 분리하고 첫해 두 뺄셈을 검산했다. 최초 Antigravity CLI의 Spurs URL 읽기 요청은 25초 print 제한 뒤 `SUCCESS` 메타데이터와 **빈 응답**이라 본문 증거 0건이다. 최초 NotebookLM CLI의 같은 URL 추가는 `Could not add url source`로 실패했다.

2022–23 후속에서는 Codex가 G8 JSON의 **192조건 전부**에서 둘째 해 `$1,563,518` 제거·15→14자리·세금선/조건부 apron 차이를 재집계하고 당시 CBA 101·NBA 공식 2022–23 자료를 직접 대조했다. NotebookLM CLI는 NBA의 2023 Denver 파이널 명단 기사를 URL 소스 `dfc143e8-240f-4f5c-b92a-fe63ac499ae7`로 추가하고 **그 한 출처만** 질의해 투웨이 포스트시즌 불가만 확인했다. 50경기 규칙·Chicago Wieskamp·팀 샐러리는 그 출처에 없다고 명시했으므로 NotebookLM으로 해당 항목을 인증하지 않는다. Antigravity CLI는 같은 URL의 `read_url_content DONE` 이벤트까지 보였으나 후속 `view_file` 본문 회수 전 **429 개인 사용 한도**로 종료했다. 따라서 이번 새 원문 Evidence Pack은 0건이다. 동일 NBA 기사를 Codex·NotebookLM이 읽은 것은 독립 원자료 두 건이 아니다. Claude CLI의 문서 단독 반증은 [R01 검토](../reviews/R01_O15G15AX_TWO_WAY_2022_REBUTTAL.md)에 근거별 수용·기각을 기록했다. Source-blind는 `NOT_RUN`; G16 PASS가 아니다.

다음에는 #39의 선수/대리인 계약 선택, 2021·2022 각각의 두 투웨이 슬롯 사용자와 14번째 일반계약 유지, 2022 계약 기간/활성 경기·전환 또는 대체 일반계약 `S`, G8 SQ1의 정확 날짜별 권리와 미확인 `R`을 같은 분기에 놓는다. `TW22` 숫자는 조건부 비용 비교만 닫았으며 D1/D2 정확 실행이나 작가확정은 닫지 않았다. `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `manuscript_allowed=false` 유지.
