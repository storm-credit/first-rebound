# O-15F14-N — Hall 추가 자리의 5/9~5/16 공개 결장 상태

- 기준: `main` `ec45ac5`; [L 등록 인원 원장](../simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.md)의 5/9 이후 **일반계약 16명·추가 1자리 필요 5경기**, [실행 조항 원장](../simulation/CHICAGO_2020_21_EXECUTION_TERMS.md)의 5/3·5/5·5/7 네 선수 연속 결장과 2019 NBA By-Laws §6.08. 판정: `FOUR_NAMED_OUT_STATUS_ALL_FIVE_DATES / ALTERNATE_APPROVAL_HOLD`.
- 조사 질문: 원역사 Orlando가 Hall을 5/9 재계약한 뒤 5경기 동안 Carter-Williams·Fultz·Isaac·Ross의 **공개 보고 상태**가 계속 `Out`이었는가? 이 사실이 대체 Orlando의 예외 승인을 뜻하는가?

| 경기일·대진 | NBA 공식 보고 시각 | Carter-Williams | Fultz | Isaac | Ross |
|---|---|---|---|---|---|
| [5/9 MIN@ORL](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-09_05PM.pdf) | 5/9 17:30 ET | Out | Out | Out | Out |
| [5/11 ORL@MIL](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-11_05PM.pdf) | 5/11 17:30 ET | Out | Out | Out | Out |
| [5/13 ORL@ATL](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-13_05PM.pdf) | 5/13 17:30 ET | Out | Out | Out | Out |
| [5/14 ORL@PHI](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-14_05PM.pdf) | 5/14 17:30 ET | Out | Out | Out | Out |
| [5/16 ORL@PHI](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-16_05PM.pdf) | 5/16 17:30 ET | Out | Out | Out | Out |

**20개 상태 행은 경기 전 보고값**이다. 다섯 경기의 최종 박스나 실제 리그 예외 승인 문서 5건을 새로 검수한 수치가 아니다. 네 명의 사유는 해당 보고서에서 Carter-Williams 왼발목 염좌, Fultz 왼무릎 ACL, Isaac 왼무릎 회복, Ross 허리 경련으로 기재된다. [5/9 구단의 Hall 잔여시즌 계약 발표](https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509)는 17:22 ET, 5/9 보고서는 **그보다 8분 뒤**다. 따라서 5/9 보고서를 계약 전 리그 결정 서류라고 부르지 않는다. 선행 [5/3·5/5·5/7 결장 증거](../simulation/CHICAGO_2020_21_EXECUTION_TERMS.md)는 별개로 유지한다.

이 공개 연속성은 K1의 Hall 추가 1자리 **신청·유지 후보**에 구체 근거를 더한다. 대체 Orlando가 원역사의 Carter-Williams·Fultz·Isaac·Ross 부상 조건을 모두 유지하는지는 A1/A2 선택이고, §6.08의 리그 판단·허가 시각·기간을 공개 `Out` 행으로 대신할 수 없다. 자리 허가는 [Hall의 `$79,216` 전액 비용안](../simulation/NBA_2020_21_REGISTRATION_COSTS.md) 및 ORL 실제 전체 Team Salary 판정과도 분리한다. 실패 시 자리 조정/분 재배정이 필요하지만 이번에 어느 사건도 채택하거나 K1 승패를 재계산하지 않았다.

## 검증 레이어

| 도구 | 실제 관측 |
|---|---|
| Antigravity CLI | 5/14 NBA PDF를 `read_url_content→view_file`로 요청했지만 headless `RunCommand` 권한이 자동 거절됐고 최종 응답은 빈 문자열. 원문 회수 0건. |
| NotebookLM CLI | NBA 공식 5/9·5/16 PDF URL 두 건은 작업실에 추가 성공. 두 출처 한정 질의에서 각 날짜 네 선수 모두 `Out`을 출처 인용과 함께 반환했고, 보고서가 리그 승인·대체 건강을 입증하지 않는다고 구분했다. 나머지 세 날짜는 NotebookLM 새 소스로 넣지 않았다. |
| Codex | NBA 공식 PDF 다섯 건의 17:30 ET 표를 직접 대조하고 `4명 × 5경기 = 20` 보고 상태를 계수했다. 같은 NBA 원문을 NotebookLM과 중복 독립 출처로 세지 않는다. |
| Claude | 완성 원장의 날짜·원역사/대체 세계·신청/승인 경계만 문서 단독으로 반증했다. [R01 검토 기록](../reviews/R01_O15F14N_HALL_STATUS_BLIND.md)에 지적과 처리·원문 접근 한계를 남겼다. |

**사실:** NBA 공식 PDF의 해당 시각 `Out` 20행, 원역사 Hall 계약 공지의 발표 시각·hardship 사용. **추론:** 네 명의 공개 결장 연속성이 추가 자리 유지 신청의 근거에 도움을 준다는 판단. **후보:** 대체 Orlando의 동일 건강 달력·hardship 신청/승인. **작가확정:** 0건. F4/K_REGISTRATION과 A1/A2는 미완료, `PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`.
