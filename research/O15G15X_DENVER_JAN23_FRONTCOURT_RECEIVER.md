# O-15G15X — 2022-01-23 Denver 앞코트 수신자 시험

- 기준: G15W의 `DET@DEN` 인과 부채. 원역사 NBA 공식 부상 보고·박스·구단 계약 연표를 대조한다.
- 판정: `NAMED_RECEIVER_CANDIDATE / EXACT_LINEUP_AND_CONTRACT_HOLD`. G15W의 Denver 수신자 미지정을 **조건부 후보 수준에서만** 좁혔다.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.

## 1. 결장 사유의 시간순서 교정

[NBA 2022-01-23 19:30 ET 공식 부상 보고서 4쪽](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)은 20:00 ET `DET@DEN`에 대해 JaMychal Green을 **Available**, Jeff Green·Vlatko Čančar·Michael Porter Jr.를 **Out**으로 적는다. JaMychal의 사유 칸은 방역 규정이며, `Available`을 실제 출전으로 읽을 수 없다. [NBA 최종 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)는 JaMychal을 `DNP - Coach's Decision`으로 표시한다. Jeff의 박스상 DNP 표기와 공식 사전 `Out` 표기가 다르면, 적어도 경기 전 의료 상태를 말할 때는 시각이 명시된 보고서를 사용한다.

[NBA 경기 요약](https://www.nba.com/game/det-vs-den-0022100707)은 JaMychal이 방역으로 결장했다고 서술하고, [구단 전날 프리뷰](https://www.nba.com/nuggets/news/preview-nuggets-pistons/)는 JaMychal·Jeff를 `Questionable`로 적었다. 사전 프리뷰 → 경기 30분 전 보고 → 최종 박스 순서로 보면, 원역사 JaMychal은 **최종 보고 Available / 실제 감독 결정 0분**이다. 요약의 방역 문구를 그날 확정 `Out`으로 이월하지 않는다. 이 교정은 대체세계에서 그가 의학적으로 반드시 뛰었다는 뜻도 아니다.

[Denver 구단 경기 노트](https://cdn.nba.com/teams/uploads/sites/1610612743/2022/02/nuggets-NYK.pdf)는 원역사 JaMychal의 **2021-08-18 재계약**을 기록한다. [NBA의 Cousins 계약 공지](https://www.nba.com/news/nuggets-sign-demarcus-cousins-10-day-deal)는 원역사 2022-01-21 10일 계약을 기록한다. 두 사건을 Nnaji가 2021년에 Orlando로 가는 세계에서 자동 승인하지 않는다. 이 문서의 후보는 두 계약을 유지하는 분기다.

## 2. 한 경기 분의 필요량과 수학적 증명

원역사 최종 박스의 Gordon `31:15`, Jokić `36:06`, Cousins `11:49` 합은 `79:10`이다. C+PF 정규시간은 `96:00`이므로, 세 명의 원역사 분을 모두 앞코트에 쓴다는 **가장 유리한 가정** 아래도 `16:50`이 빈다. 실제 Nnaji는 `16:45`를 뛰었다. 원역사 포지션·동시 출전 판독은 아니며 5초 잔차를 숨기지 않는다. JaMychal이 기존의 실제 `0분`을 그대로 유지하면 누군가의 분 또는 포지션을 더 바꾸어야 한다.

다음은 **분/포지션 가능성 후보 X1**이다. Gordon A 정확 거래·JaMychal/Cousins의 대체세계 계약 및 당일 출전 허가가 모두 성립할 때만 검토한다. 수치는 경기 기록 예측이 아니다.

| 앞코트 자리 | 조건부 배정 | 합 |
|---|---|---:|
| PF | Gordon `31:15` + JaMychal `16:45` | `48:00` |
| C | Jokić `36:06` + Cousins `11:54` | `48:00` |

후보 X1은 Cousins의 원역사 분을 **5초 늘리고**, 예컨대 Reed의 `12:13`을 `12:08`로 줄여 팀 전체 240분을 유지한다. 다른 여섯 외곽 선수의 합은 그때 `144:00`이다. 이 5초는 박스의 숨은 반올림으로 간주하지 않고 명시적 분 이동으로 둔다. 외곽 3자리와 실제 동시 5인, 교체 시각, 포지션 적합성은 아직 증명하지 않았다. JaMychal의 `16:45`도 원역사에서 실제 뛰지 않은 새 코치 선택이므로, **원역사 Nnaji의 12점·5/5 FG나 2021–22 생산성을 이식하지 않는다.**

X1의 대안은 Gordon/Jokić/Cousins의 분 증가 또는 Barton/Reed 등 외곽 선수의 PF 이동이다. 대안을 쓰면 해당 선수의 원래 포지션 분과 체력·공격 기회를 같이 빼야 한다. `Available` 한 단어만으로 X1을 최종 로테이션으로 확정하지 않는다.

## 3. 남은 사실·추론·후보·작가확정

| 구분 | 이번 결론 |
|---|---|
| 사실 | 19:30 ET 보고의 상태, 원역사 박스의 DNP/출전 분, 구단의 원역사 JaMychal 재계약 및 Cousins 10일 계약 |
| 추론 | 세 빅맨 원역사 분만으로 C+PF 96분을 채울 수 없고, Nnaji를 Orlando로 보내면 Denver의 수신자 사건이 필요하다 |
| 후보 | 원역사 계약 유지 + JaMychal PF `16:45` + Cousins 추가 `0:05` + Reed 감축 `0:05`의 X1 |
| 작가확정 | 신규 0건. Gordon A 정확 실행, Denver 계약/급여·등록, 당시 건강의 대체세계 이월, 코치 선택, Detroit 대체 명단·공격 예산, 결과 모두 `HOLD` |

다음은 X1의 선수별 계약·자리와 5인 교대 가능성을 검증하고, Detroit의 Suggs/Patrick/Stewart 연쇄와 맞대조하는 것이다. G14 `DET PRIOR_HOLD`, G15B `ORL ROLE_HOLD`와 2020–21 Chicago 정확 시즌의 미완료 상태는 유지한다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 남은 6개다.

**도구 대조:** Codex가 위 NBA 공식 PDF와 박스·계약 공지를 직접 읽었다. NotebookLM CLI는 같은 PDF를 출처 `c8189748-40fd-473a-afcc-f7cc35b396dd`로 수집하고, 해당 출처만의 질의에서 JaMychal `Available`, Jeff/Čančar/Porter Jr. `Out`, Detroit Olynyk `Out`을 재확인했다. `Available`의 일반적 의미에 관한 NotebookLM 설명은 원문에 없는 해석이므로 사실 행으로 올리지 않는다. Antigravity CLI는 구단 프리뷰 직접 판독에서 `ACCESS_FAILED`를 반환해 본문 증거가 0건이다. CLI 통신 성공과 원문 검증 성공을 구분한다.

[Claude 제한·source-blind 검토](../reviews/R01_O15G15X_CLAUDE_SOURCE_BLIND.md)는 분 산술을 확인하고 5인 교대 미증명을 지적했다. 원역사 감독 DNP를 대체세계 출전의 절대 금지로 읽은 주장은 기각했다. G16 독립 검수는 여전히 미완료다.

### 후속 — O-15G15Y의 Denver Bey22 대조

[세 경기 선수 이동 원장](O15G15Y_2022_01_23_THREE_GAME_PLAYER_FLOW.md)은 2020 작가 확정 Denver Bey22와 조건부 2021–22 잔류를 1/23 `DET@DEN`에 연결한다. 따라서 이 문서 X1의 JaMychal `16:45`는 유일한 수신자가 아니다. Bey를 PF 수신자로 놓는 X2도 분 합계 후보이지만, 두 안 모두 Bey의 다른 윙 분·계약·코치 결정과 Detroit 상대 변화가 `HOLD`다. 원역사 Detroit Bey `30:42`를 Denver로 옮겨 쓰지 않는다.
