# O-15G15C — Orlando 2022-01-23 가드 계약 원역사 점검

- 출발점: `main` `d730e48` (PR #185), [G15B의 두 240분 조건부 증명](../simulation/CHICAGO_2021_22_G15B_REVIEW.md). **계약·등록·활동·역할 HOLD만 좁힌다.** G14 원본이나 시즌 경로는 바꾸지 않는다.
- 1차 자료: [Orlando Magic 2022–23 미디어 가이드](https://cdn.nba.com/teams/uploads/sites/1610612753/2022/11/orlando-magic-media-guide-2022-23.pdf)의 인쇄 230–231쪽(파일 117쪽) 거래 연표, [NBA 2022-01-23 17:30 ET 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2022-01-23_05PM.pdf) 2쪽, [CHI@ORL 공식 박스스코어](https://www.nba.com/magic/game/0022100701). 구단 연표는 2022–23에 발행된 **사후 기록**이다. 원역사 확인에는 쓰되 2021–22 당시 작중 인물의 사전 지식으로 넣지 않는다.

| 날짜 | 원역사 / 공식 거래 연표의 사건 | 가상 세계 적용 한계 |
|---|---|---|
| 2021-09-08 | ORL이 Hassani Gravett를 자유계약으로 영입 | 이후 유지의 증거 아님 |
| 2021-10-16 | Gravett와 Admiral Schofield 방출 | 2021–22 시즌 개막 등록을 자동 가정할 수 없음 |
| 2021-12-17 | 두 선수 모두 하드십 예외 10일 계약 | 2022-01-23 유효 계약의 증거 아님 |
| 2021-12-27 | 두 선수 모두 하드십 예외 **두 번째** 10일 계약 | 1월 23일에 이어진다고 추정하지 않음 |
| 2022-01-06 | Schofield 투웨이 계약, Mychal Mulder 방출 | Gravett의 계약 연장이나 투웨이 전환 기록은 해당 연표에 없음. 다른 문서의 존재 가능성까지 부정하지 않음 |

**원역사 당일:** 부상 보고서는 Michael Carter-Williams, Markelle Fultz, R.J. Hampton, Gary Harris, Jonathan Isaac, E'Twaun Moore, Terrence Ross를 `Out`으로 기재한다. 부상 보고서는 전체 등록·활동 명단이 아니다. 공식 CHI@ORL 박스스코어에 Gravett 출전 기록은 없으나, 그것만으로 계약 상태 전부를 역산하지 않는다. 실존 보고서의 R.J. Hampton 등은 가상 ORL 로스터에 자동 복원하지 않는다.

**O15C Gravett 신규 계약 후보 / HOLD:** 두 10일 계약의 원역사 기록만으로 가상 1월 23일 12분 출전을 열 수 없다. 그 날짜에 유효한 **별도 계약 경로**, 2021–22 당시 그 경로의 적법성(하드십 자격·계약 횟수 포함), 자리/급여/투웨이 슬롯, 당일 활동 가능, 12분을 빼앗기는 기존 선수와 공격·수비 비용을 명시해야 한다. 2021–22 하드십 특례에 일반적인 10일 계약 제한을 기계적으로 적용하지 않는다. [NBA의 같은 시즌 Portland 사례](https://www.nba.com/news/blazers-sign-kris-dunn-and-drew-eubanks-for-remainder-of-2021-22-season)는 한 선수가 네 차례 10일 계약을 맺었다고 기록하므로, 3차 계약의 적법 여부는 **해당 시점·예외 요건 감사 전 HOLD**다.

**O15A Herbert 내부 전개 후보 / HOLD:** 추가 가드 계약 가정은 없지만 G7 DB1에 따른 Herbert의 실제 대체 세계 등록·당일 활동 및 PG12 역할, 36분 다중 역할의 수비·공간 비용이 여전히 미증명이다. 따라서 이번 거래 연표는 O15C의 부담을 구체화하지만 O15A를 확정하지 않는다.

## 도구 출력의 채택 범위

- Anti-Gravity CLI `agy`는 사용자 로그인 후 실제 실행됐다. 지정 NBA 기사 두 건의 본문은 접근 실패했다. CLI가 **URL만 보고 기사일·계약 내용을 추정**한 부분은 사실 근거로 채택하지 않았다. NBA PDF/Gonzaga 페이지는 가져왔어도 내용 분석 전 파일로 저장되어 이 세션의 읽기 전용 실행에서 값이 `null`이었다. 후속 파일 읽기 요청은 시간 초과로 결과가 없다. **Anti-Gravity 검증된 Evidence Pack은 여전히 0건.**
- NotebookLM CLI의 [비정본 작업실](https://notebooklm.google.com/notebook/303ffd55-e019-476a-9ae3-8dc0e32fe11f)에 공식 미디어 가이드의 해당 한 쪽을 추가했다(자료 ID `e14dffef-f958-490f-9801-6a86a90971f1`). 도구는 거래 날짜를 올바로 인용했지만, **부상 보고서 미기재 = 전체 공식 명단 부재**, **거래 연표에 없음 = 다른 계약 없음**으로 확대 추론했다. 그 두 결론은 기각한다. 가상 경기의 `Available` 표기와 실제 박스스코어도 사전 증거로 요구하지 않는다.
- Codex는 공식 PDF 원문을 내려받아 거래 연표의 인쇄 230–231쪽을 직접 대조했다. 이 독해는 Anti-Gravity가 수집한 결과나 독립 검수 횟수로 계산하지 않는다.

다음에는 가상 ORL의 2021 여름~1월 23일 등록 원장과 하드십/투웨이/정규 계약 조건을 날짜별로 연결하고, O15A의 전개·수비/공간 비용과 O15C의 자리·급여 비용을 비교한다. G14의 ORL4 `ROLE_HOLD`, DET4 `PRIOR_HOLD`, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`, 모든 author/season/exact/manuscript false를 유지한다.
