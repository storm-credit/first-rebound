# O-15F14-O — Hall 복귀 5경기 최종 박스의 4인 미출전 대조

- 기준 `main` `c7ab4ec`; 선행 [5경기 경기 전 `Out` 원장](O15F14N_HALL_MAY9_16_FOUR_PLAYER_STATUS.md)과 [등록 자리 원장](../simulation/ORLANDO_2020_21_REGISTRATION_LEDGER.md).
- 판정 `ORIGINAL_FINAL_BOX_FOUR_MISSED_ALL_FIVE / ALTERNATE_HARDSHIP_APPROVAL_HOLD`.
- 질문: 경기 전 보고의 20개 `Out` 행이 **원역사 최종 경기 기록의 실제 미출전**과 일치하는가? 그 일치가 대체 Orlando의 등록 예외를 승인하는가?

| 날짜·경기 | NBA 공식 최종 박스 | Carter-Williams | Fultz | Isaac | Ross | Hall 원역사 출전 |
|---|---|---|---|---|---|---:|
| 5/9 MIN@ORL | [FINAL BOX](https://statsdmz.nba.com/pdfs/20210509/20210509_MINORL.pdf) | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive` | `DND`, 허리 경련 | 16:41 |
| 5/11 ORL@MIL | [FINAL BOX](https://statsdmz.nba.com/pdfs/20210511/20210511_ORLMIL.pdf) | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive` | `NWT`, 허리 경련 | 17:03 |
| 5/13 ORL@ATL | [FINAL BOX](https://statsdmz.nba.com/pdfs/20210513/20210513_ORLATL.pdf) | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive` | `NWT`, 허리 경련 | 20:40 |
| 5/14 ORL@PHI | [FINAL BOX](https://statsdmz.nba.com/pdfs/20210514/20210514_ORLPHI.pdf) | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive` | `NWT - Not With Team` | 07:24 |
| 5/16 ORL@PHI | [FINAL BOX](https://statsdmz.nba.com/pdfs/20210516/20210516_ORLPHI.pdf) | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive` | 부상 `Inactive`, 허리 경련 | 25:05 |

**원역사 사실:** 네 선수는 다섯 최종 박스에서 실제 출전 0건, 미출전 20행이다. Hall은 매 경기 양수 분을 뛰었다. 경기 전 [5/14 부상 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-14_05PM.pdf)는 Ross를 `Out / Back Spasms`라고 했지만, 그날 최종 박스 표기는 `NWT - Not With Team`뿐이다. **5/14 최종 박스 단독으로 Ross의 결장 사유가 부상이라고 말하지 않는다.** 앞선 5/3·5/5·5/7의 네 선수 3연속 미출전은 [실행 조항 원장](../simulation/CHICAGO_2020_21_EXECUTION_TERMS.md)에 별도 보존한다.

Ross의 최종 분류는 `DND → NWT → NWT → NWT → Inactive`로 변한다. 따라서 `20 미출전`은 **실제 경기 미참여의 계수**이며 최종 박스 20행 모두가 동일 부상 유형을 인증했다는 뜻이 아니다.

2019 [NBA By-Laws §6.08](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2019/09/NBA-Constitution-By-Laws-September-2019-1.pdf)는 네 선수의 선행 3연속 부상/질병 결장과 **대체 선수 서명 시점에 계속 출전할 수 없으리라는 리그 판단**을 나눈다. 이번 최종 박스는 사후 미출전을 입증하지만 서명 당시 리그의 판단·승인 문서, 예외 유효 기간, 대체 Orlando의 건강 달력·명단·승인을 입증하지 않는다. [5/9 Hall 구단 발표](https://www.nba.com/magic/orlando-magic-sign-donta-hall-remainder-season-20210509)는 원역사의 hardship 사용 사실이며 대체 세계의 허가서가 아니다.

**추론:** 원역사 최종 결장 연속성은 K1에서 동일 건강 달력을 유지하는 A1/A2 후보를 시험할 근거를 강화한다. **후보:** 대체 Orlando의 4인 건강 달력, 신청·리그 허가, 추가 1자리 5경기 사용. **작가확정:** 0건. 기존 조건부 일반계약 16명·투웨이 2명과 5경기/추가 1자리 산술, Hall 전액 비용안, K1/L2 및 CP2 잠정 추첨은 변경하지 않는다. F4/K_REGISTRATION과 A1/A2는 `HOLD`다.

## 도구별 실제 범위

| 도구 | 결과 |
|---|---|
| Antigravity CLI | 5/9 NBA 최종 박스 읽기 요청. headless `RunCommand` 권한 자동 거절, 빈 응답·원문 회수 0건. |
| NotebookLM CLI | 5/9와 5/14 NBA 최종 박스 PDF 두 개를 업로드해 출처 한정 질의. 네 선수의 미출전·Hall의 양수 분·5/14 Ross 최종 박스 사유의 한계를 올바로 구분했다. 같은 NBA 원본의 재독이다. |
| Codex | NBA 최종 박스 PDF 다섯 개를 내려받아 페이지 이미지를 렌더링하고 선수 행·inactive 각주를 육안 대조했다. PDF 단순 텍스트 추출에서 이름과 분이 어긋난 사례를 발견해 육안 기준으로 바로잡았다. |
| Claude | 결과물 단독으로 날짜·출전/부상 사유·원역사/대체 세계·승인 비약을 반증했다. [R01](../reviews/R01_O15F14O_FINAL_BOX_BLIND.md)에 수용한 경계와 원본 미접근 범위를 기록했다. |

`PROJECT_FREEZE v0.30 PARTIAL`, 설계·원고 `CLOSED`, `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`.
