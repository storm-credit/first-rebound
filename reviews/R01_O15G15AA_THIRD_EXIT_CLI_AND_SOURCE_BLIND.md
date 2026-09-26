# R01 — G15AA 세 번째 이탈의 출처·제한 맹점 검수

- 시작 권위: `main` `9092b8d`; 대상: [G15AA](../research/O15G15AA_DETROIT_HAYES_THIRD_EXIT_AND_MEDICAL_BOUNDARY.md). 도구 검토는 G16 독립 검수가 아니다.
- **Codex 원자료:** [NBA DET@DEN 2022-01-23 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)에서 Hayes `24:42`·5 FGA·8점·3 TOV, Bey `30:42`·11 FGA·11점, Cade `36:14`·15 FGA·18점을 대조했다. [NBA 19:30 ET 공식 부상 보고](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_07PM.pdf)는 원역사 Detroit Hayes `Available / Right Hip Contusion`, Chicago Patrick `Out / Left Wrist Ligament Tear` 및 **다음날 1/24 NOP 경기용** 원역사 Kira `Out / Right Knee ACL/MCL`을 적는다. 서로 다른 경기 날짜를 현재 DET 1/23 상태로 바꾸지 않는다.
- **NotebookLM CLI:** 기존 공식 부상 보고 출처 `c8189748-40fd-473a-afcc-f7cc35b396dd`만 지정한 새 대화 `aecf5791-d80a-460e-b511-396941f329cf`가 Hayes `Available/Right Hip Contusion`과 JaMychal `Available/Health and Safety Protocols`를 인용했다. 그 문서에는 실제 출전 분이나 대체 팀 의료기록이 없다고 답했고 원문과 일치한다. 같은 PDF 재질의는 독립 새 출처가 아니다.
- **Antigravity CLI:** 공식 NBA 박스 직접 판독 시 headless `RunCommand` 권한이 자동 거부돼 최종 응답 본문이 비었다. 상태가 `SUCCESS`여도 **NBA 증거 0건**이다. CLI 연결 자체와 자료 판독을 구분한다.
- **Claude CLI 제한 source-blind:** 도구 없이 이동·분·의료 조건을 준 논리 검토에서 “원역사 기록을 새 팀으로 이식하지 않는다”는 원칙은 유효했다. 하지만 **원역사 Bey가 Denver, 원역사 Hayes가 New Orleans**였다는 주장, 2020 대체 드래프트 때문에 2021 Cade가 Detroit에 없다고 단정한 주장, Kira+Suggs를 서로 다른 양립 불가 분기라고 한 주장은 모두 **기각**한다. 원역사 [NBA 박스](https://www.nba.com/game/det-vs-den-0022100707/box-score)는 세 선수를 Detroit에 기록하며 DB1 Suggs5는 2020 Kira16 다음 해의 **조건부 연속안**이다. 모델의 반증을 사실로 승격하지 않는다.

**결과물 단독 검사:** G15Y의 Bey+Cade `66:56` 자체는 올바른 부분합이지만 Hayes `24:42`를 빠뜨려 이탈 집합을 과소 기술했다. G15AA는 2020 확정 두 명과 DB1까지 가정한 세 명을 별도 행으로 분리했다. 동시에 팀 이동만으로 서명·의료·분·승패가 결정되지 않는다는 `HOLD`를 남겼다. 원고/설계 게이트 `CLOSED`, `PROJECT_FREEZE v0.30 PARTIAL`, G16/G17 미완료.
