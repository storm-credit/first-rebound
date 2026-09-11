# O-15F14-I — 공식 사유 대조·조건부 결장 영향

- 기준: 2026-09-11 / PR #152 main
- 상태: `PRIMARY_REASON_ANCHORS_AND_BOUNDED_STRESS_COMPLETE / FINAL_SEASON_HOLD`
- 공식 사실 권위: `research/NBA_2020_21_CAUSAL_AVAILABILITY_SOURCES.json`
- 계산 권위: `CHICAGO_2020_21_CAUSAL_AVAILABILITY.json`, `CHICAGO_2020_21_REPORTED_ABSENCE_STRESS.json`, `CHICAGO_2020_21_JOINT_ABSENCE_STRESS.json`
- R1/T1~T4 방향 승인 보존. 원고CLOSED / manuscript_allowed false.

## 이번에 닫은 범위

NBA 공식 부상 보고서9건에서39개 상태·사유 항목을 확인했다. 보고서 날짜, 대상 경기 날짜, 페이지를 별도로 기록했다. H의170우선 항목을14개 조사 묶음으로 연결했고, 그중159항목이 속한13묶음에서 관련 사유 근거를 찾았다. **159개 날짜의 원인과 결장을 모두 입증했다는 뜻은 아니다.** Carter의1~2월11항목은 상세1차 사유 미확보로 남는다.

같은 날짜의 확정 OUT을 적용하는 조건부 시험은 단독 공백4경기8조건, Washington 동시 공백1경기12조건으로 총5경기20조건이다. 새로운 부상 발생이나 결장 일정을 정본으로 선택하지 않았다. 기존 계산을 먼저 재현한 뒤 결장 선수만 변경했다.

## 공식 사유와 대체 세계의 처리

| 조사 묶음 | H 항목 수 | 찾은 사유 | 대체 세계 처리 |
|---|---:|---|---|
| LaMelo 손목 | 23 | 오른쪽 손목 골절 | Charlotte의 사건·회복 달력을 Chicago에 자동 이식하지 않음 |
| Porter 겨울 | 15 | 허리 경련 | Chicago 실제 분 유지 조건과 연결. 발병 경위·매일의 사유까지 확정하지 않음 |
| Porter 후반 | 17 | 왼발 통증 | Orlando 관측을 Chicago 건강 승인으로 사용하지 않음 |
| Carter 겨울 | 11 | 상세1차 사유 미확보 | 기록 공백에서 진단을 만들지 않음 |
| Carter4/22 | 1 | 오른쪽 발목 통증 | 실제 Orlando 사건의 발생 맥락 회수 필요 |
| Carter5월 | 3 | 왼쪽 눈 표면 찰과상 | 같은 사유의 보고 지점 확인. 모든 날의 결장을 보간하지 않음 |
| Terry2~3월 | 14 | G리그 파견 | Dallas의 파견을 Charlotte에 자동 복사하지 않음 |
| Terry후반 | 27 | 개인 사유 | 사생활·정신건강 진단을 추측하지 않음. 새 팀 가용성은 별도 |
| Hampton3월 | 7 | 보건·안전 프로토콜 | 실제 Denver의 노출·절차를 Dallas에 자동 이식하지 않음 |
| Hayes고관절 | 41 | 오른쪽 고관절 손상·복귀 후 관리 | Detroit 사건이 NOP에서도 같은 날 생겼다고 가정하지 않음 |
| Vučević5/1 | 1 | 오른쪽 내전근 긴장, 당시QUESTIONABLE | 관측DNP와 보고 상태를 함께 보존. QUESTIONABLE을OUT으로 바꾸지 않음 |
| Hood4월 | 2 | 오른쪽 고관절 굴곡근 손상 | Toronto 사건과 Portland 역할을 구분 |
| Hood5/16 | 1 | 왼손 둘째 손허리뼈 골절 | 실제 Toronto의 발생 맥락이 필요 |
| Brown후반 | 7 | 왼쪽 발목 염좌 | 실제 Chicago 사건을 Washington에 자동 복사하지 않음 |

Terry의 파견, Hampton의 프로토콜, Hayes·Porter의 당시 사유는 [3/3 공식 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-03-03_05PM.pdf)에 있다. LaMelo의 골절 사유는 [3/22 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-03-22_05PM.pdf), Hood·Hayes의 관리 및 Terry 개인 사유는 [4/6 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-04-06_05PM.pdf)를 따른다.

Carter 발목은 [4/22 20:30 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-04-22_08PM.pdf), Brown의 발목과Terry 개인 사유는 [4/23 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-04-23_05PM.pdf), Vučević·Trent 등의 상태는 [5/1 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-01_05PM.pdf)에 있다. Carter의 눈과Porter의 발 사유는 [5/7](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-07_05PM.pdf)·[5/9 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-09_05PM.pdf), Hood의 손 골절과5/16 대상 상태는 [5/15 보고서](https://ak-static.cms.nba.com/referee/injury/Injury-Report_2021-05-15_05PM.pdf)를 따른다.

보고서의 사유는 상세 영상·진단서·발병 원인 전체가 아니다. 보고 시각이 경기 시작 이후인 자료도 있으므로 모두 경기 전 예측 입력이라고 부르지 않는다. 5/1 LaMelo는QUESTIONABLE로 기재됐지만 실제 양수분 출전 기록이 있다. 상태와 최종 출전을 혼동하지 않는다.

## H의 우선 목록에서 빠진 항목

긴 공백과명시DNP를 기준으로 한H 목록 밖에서 공식OUT3개를 추가 확인했다.

- Hayes:4/6 NOP 가용성 목표 날짜와 겹치는 실제 Detroit의 고관절 관리.
- Brown와Trent:5/1 Dallas–Washington과 겹치는 각각 발목·하퇴부 사유.

170항목/147경기는 검토 우선순위였으며 전체 가용성 보장이 아니었다. 특히 Brown와Trent는 **같은Washington경기의 동시 공백**이다. 두 단독 시험의 영향치를 더하지 않고 새 공동 분 배정과5인 조합을 검증했다.

## 단독 공백4경기

F의LOW_MINUTES·피로0.5를 유지한 조건부 시험이다. 기존 선수의 실제 가용성, 분 상한, 다른 신규 선수 목표, 상대 팀 분은 보존했다. 원래F 분 배정을 동일 솔버로 재현한 뒤 대상만 제거했다.

| 경기·대상 | 대체 분 처리 | 시험 결과 |
|---|---|---|
| 4/6 ATL–NOP, Hayes16분 공백 | Bledsoe17→33분, 실제 기준 분으로 복귀 | 두 지표 ATL승 유지 |
| 4/6 LAC–POR, Hood12분 공백 | Jones Jr. 약10.57분·Anthony 약1.43분 추가 | 두 지표 LAC승 유지 |
| 5/1 CHA–DET, Terry6분 공백 | Cody Martin2.1분·Caleb Martin3.9분 추가 | 두 지표 CHA승 유지 |
| 5/16 POR–DEN, Hood12분 공백 | Jones Jr.9.05분·Little2.95분 추가 | 두 지표 POR승 유지 |

이4경기8조건의 방향 유지가 다른 결장일·동시 공백·가상 선수의 무부상 시즌을 보장하지 않는다. 계수에 따라 결장 뒤 추정 점수차가 개선되는 경우도 있으며 이를 실제 부상이 팀에 유리하다는 인과 결론으로 해석하지 않는다.

## Washington 동시 공백 — 순위가 바뀌는 반례

5/1 Brown와Trent를 함께 제거했다. 선행D의배정 알고리즘으로 통제군을 정확히 재현하고, 같은 방식의 두 출전시간 정책·두 지표·피로0/0.5/1을 비교했다. DAL배정은 해당정책 그대로 유지한다. WAS는Neto·Smith·Mathews·Bertāns가 합계32분(LOW) 또는40분(HIGH)을 받는다. 실제 비가용 선수를 투입하지 않았고5인조합을 검증했다.

| 정책·지표 | 피로0.5의 DAL 기준 예상 점수차 | 판정 |
|---|---:|---|
| LOW / RAPTOR | +0.1398 | DAL승 유지, 매우 근소 |
| LOW / BPM | +0.8329 | DAL승 유지 |
| HIGH / RAPTOR | −0.3796 | **WAS승으로 반전** |
| HIGH / BPM | +0.7212 | DAL승 유지 |

HIGH/RAPTOR에서는 피로0·0.5·1의3조건 모두WAS승으로 바뀌며 나머지9조건은DAL승을 유지한다. 이는 지표 불일치가 있는 조건부 반례다. 둘의 부상으로Washington이 실제로 강해진다는 주장이 아니다.

R1의지표별 계수·28분, 피로0.5와 두Porter조건을 고정해 해당경기만 전체1,080경기에 재연결했다. LOW/RAPTOR F138은CHI9위, LOW/BPM F038은10위를 유지한다. **HIGH/RAPTOR F137은DAL−1승·WAS+1승에 따라CHI9→10위**로 변한다. HIGH/BPM은10위를 유지한다. 양팀 승수 이전 합계0·리그 총승수1,080을 확인했다. 다른 건강 사건은 여전히 기존조건이므로 새 최종시즌이 아니다.

## 다음 종료 기준

I에서 공식 사유 대조, 단독·동시 공백의 조건부 계산, 순위반례 연결을 완료했다. 원인 발생 경위와 대체세계의실제부상/등록달력은 아직 선택하지 않았다. 정확계약charge·픽조항도이번에새로확보하지않았다.

다음 O-15F14-J는 가용성 정책 후보를 압축하고, Chicago 자체공백·Terry의파견/개인사유·새팀부상사건·EX04/06 후속등록을 시즌 결산에 연결한다. 확인된사유를동일날짜의자동결장으로복사하지않고, 선택할가정과그영향을구체화한다. 기존경기입력전체를재수집하거나이미채택한R1/T1~T4를다시묻지않는다.

검증7개 및 저장증명/JSON 재현 PASS. 자체검토NOT_INDEPENDENT. 전체1완료·1진행·5대기/남은6개·원고CLOSED 유지.
