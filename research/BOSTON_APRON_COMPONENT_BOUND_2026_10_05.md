# Boston apron 구성요소 상한 검문 — 2026-10-05

상태: **S2_SOURCE_SUPPORTED_COMPLETE_PRESERVED_BOSTON_COST_BOUND**. 독립 원자료·정본·법률·네 비용 상태 검문을 완료해 `BOS_COMPLETE_COST`의 유한 보존 비용모델 범위를 종료했다. 분석기간은 **2021-03-25~2021-05-16**이다. 6월18일 Walker/Horford 거래와 정확한2025/2027픽 권리선택, TPE흡수순서는 별도 범위다. 실제 계약료·서명·접수·정본 선택·게이트는 변경하지 않았다.

## 실제 회수한 사실

동시대 [BasketballInsiders Boston 본문](https://web.archive.org/web/20210420161634id_/http://www.basketballinsiders.com/boston-celtics-team-salary/)은 본문 갱신3/29, 보존4/20이다. 본문이 연결한 [team_id=1 위젯](https://web.archive.org/web/20210423114126id_/http://hw-files.com/tools/salaries/salaries_widget_new.php?team_id=1)은 별도로4/23 보존본을 회수했다. 두 HTTP200 원문과 decoded문자열 지문은 JSON에 기록했다. 공개 cap분석 원자료이며 NBA 비공개 장부 인증으로 바꾸지 않는다.

위젯에는 Yabusele1,039,080과 DemetriusJackson92,857의2020–21 잔여행이 있다. contemporaneous original2019/2017 cap보도에서도 각각3년/7년 stretch를 직접 확인했다. BI본문은 Amile의1시즌 최저급여 Exhibit9+10 캠프계약과12/19방출을 명시한다. 전체 공개 거래표를 직접 회수해 같은기간 Amile,3/25수취,4/16Parker/Wagner 사건을 대조했다.

**기존 원장의 Fournier unlikely=0은 단일상한의 근거로 쓸 수 없다.** BI원위젯 tooltip에 unlikely1,150,000이 명시되어 있다. 현재SalarySwish 역사행은0으로 보고하므로 두포인트의 최대1,150,000을 모두 포함한다. 실제 달성·지급·올바른보너스재분류를 선택할 필요가 없는 상한이다.

Brown/Smart와 나머지14현재계약 및 Wagner/Parker의 SalarySwish **CONTRACT HISTORY 2020–21 실제행**을 이번에 전수 HTTP200 회수했다. Brown22,991,071/likely446,429/unlikely2,232,143, Smart12,946,428/likely500,000/unlikely0은 기존원장 해시와도 일치한다. 현재2024이후 계약금액을 사용하지 않았다. 신규지문이 바뀐 다른 선수는 이번 원문 지문을 기록했다.

## 법률 추론과 전체 분기 상한

[NBA공식2017CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 **633쪽 판본**, PDF쪽수는1기준이다.

| 항목 | 원문 위치 | 이 연구의 처리 |
|---|---|---|
| 모든 성과보너스 | VII6(m)(3)(A), PDF240/인쇄218 | Brown/Smart/Fournier likely와unlikely 전부 포함 |
| 수취 tradebonus | XXIV2(a)(i)-(ii), PDF398/376; VII3(b)(1)-(2), PDF193/171 | 미획득base하한0, 현재연도배분 전액상한; Fournier2,550,000+Kornet337,500 |
| Wagner 원rookie계약 | VIII1(c)(i), PDF294/272; VII3(b)(1)(ii), PDF193/171 | Salary에 들어가는 tradebonus도 전체Salary+Unlikely120% 안에 포함; 추가324,288 중복금지 |
| 0/1YOS FAfloor | I1(cc)/(fff)/(ggg), PDF27/31; VII12(f)(2), PDF286/264 | Carsen/Jackson의 원exclusive-draft서명은 RookieFA가 아님; 연차만 보고 가산하지 않음 |
| TW | VII4(j), PDF216/194 | Fall/Waters의 TeamSalary제외; 현금지급0주장 아님 |
| Exhibit10 | VII4(k), PDF217/195 | 보너스 TeamSalary제외 |
| Amile 캠프 | II3(p)-(q) PDF42–44/20–22; UPC3(b) PDF514–515/A2–3; Ex9 PDF555/A43 | 연간1,678,854 스트레스가 Ex9부상6,000 및 veteran캠프advance최대8,000을 넘음; 실제미지급0 인증 불필요 |
| 기타apron항목 | VII6(m)(3)(B)-(G), PDF240–241/218–219 | 일반FAhold·exceptionhold·빈자리hold 제외; outstandingRequiredTender/RFAoffer 및 구체grievance가 있다면 포함해야 함 |

Wagner는2018#25 원rookie계약의 첫option해다. [NBA공식2018–19 guide](https://cdn.nba.com/manage/2021/03/2018-19-CBA.pdf)의 **PDF29/ExhibitA**, 단위$000, #25 thirdyear1,801.6의120%=2,161,920을 사용한다. 2017CBA 첨부의 가정성5%성장 예시표를 실제2018scale로 쓰지 않았다. 이 상한은 실제120%계약을 새로 선택하거나 tradebonus0을 인증하는 것이 아니다. 적법한 원rookie계약의80–120 전체구간을 덮는다.

Fournier/Kornet은 역사계약기간 표에서2020–21 마지막해로 읽었다. 현재연도base 전액의15%를 더하여 경과일/실제bonus유무/최종보호별배분을 확정하지 않고 모든 해당금액 분기를 덮는다. 옵션 미행사해와 2023규칙을 역대입하지 않는다.

## 검산

| 구성 | USD |
|---|---:|
| 기존 부분합 | 133,546,805 |
| 추가 priorstretch2건 | 1,131,937 |
| Fournier unlikely 정정상한 | 1,150,000 |
| 정정 공개구성+캠프 | 135,828,742 |
| Fournier/Kornet tradebonus 전체상한 추가 | 2,887,500 |
| **공개유한구성 상한** | **138,716,242** |
| Apron | 138,928,000 |
| **여유** | **211,758** |

Wagner를 별도15%로 중복 추가하면139,040,530으로112,530 초과한다. 먼저 rookie전체Salary상한에 포함되는 항목임을 검문해야 한다. 캠프 Exhibit10을 따로 더하지 않은 것은 지급0추정이 아니라 VII4(k)의 제외규칙 때문이다.

## 작성한 비용 경로·법률 지도

총괄은 JSON의8개 정본·활성 사건 경로/지문을 실제 읽고 연결 주장을 작성했다. 기존 causality의 로스터·계약 기본값, 활성2018주분기의23~27유지, 2020Nesmith14/Pritchard26의승인, 2021Boston의동일Theis/Green송출·Wagner/Kornet수취와 T3를 대응시켰다. Brown/Trent의WAS변경·F4/F5/C2의타구단변경은 Boston 새 계약으로 넣지 않는다. **보존된 Boston 공개 비용모델의 법적 가능성 증인**이며 미선택2018주인공순번이나 정확 계약료를 선택하는 행위는 아니다. 후일 승인된 변화가 이 계약군을 대체하면 증인은 무효화·재계산한다.

VII6m3(A)-(G), TW/Ex10, 공개된stretch/캠프/후속계약의 포괄 지도를 JSON에 작성했다. QO·미서명1R 부재의 직접 보고와 전수 공개 목록은 유한 비용범위의 근거다. 구체 식별된 미산입 grievance는 발견되지 않았으며 후일 식별되면 재검문한다. 모든 미공표 사건의 전역부재나 비공개 원장 제출을 새 필수조건으로 요구하지 않는다.

거래일의 **비용상 안전한 순서 존재 증인**도 작성했다. 총괄은 Theis/Green/Teague의2020역사행을 새로 직접 회수했다. Teague는 BI본문2,320,044 대신 SalarySwishBoston표의 더 큰 선수기본급2,564,753 전액을 사용하며, 팀 보전액1,620,564나 이후 Milwaukee계약과 구분한다. 모든 상태에 Parker의후속비용과 Amile연간스트레스를 미리 예약한다.

| 비용 상태 | 상단 USD |
|---|---:|
| 두3/25거래 직전: 모든incoming상단 제거·모든outgoing전액 가산 | 121,899,556 |
| 원자적Theis/Green송출·Kornet/Wagner수취 후 | 120,130,995 |
| Fournier수취·Teague송출 후 | 138,716,242 |
| 4/16Parker계약·Wagner방출 뒤~5/16 | 138,716,242 |

네 상태 모두 apron138,928,000 이하이다. 모든incoming을 먼저받고 outgoing을 나중에 보내는 임의순서까지 인증하는 것이 아니다. 자산 적법성·실제 TPE배분·리그 접수는 별도이며 **BOS_TPE_AND_PICKS 전체/픽2분기/TPE순서**가 자동통과하지 않는다. 독립 `/root/independent_finish_scope`가8개 정본 연결·새outgoing행·네 비용 상태를 실제 재대조해 이 한정 S2비용행 종료를 수용했다. 총괄은 두 연결을 true로 판정하고 전체상단138,716,242를 비용행에 연결했다. 원고게이트 CLOSED 유지.

원문파일 경로·SHA·직접회수방식·사실/조건부법률추론·남은claim은 동명 JSON을 따른다. AG/NLM은 이 하위작업에서 호출하지 않았다.

## 보존 계약의 정본 연결 제안

JSON `canon_relevance_proposal`은8개 실제파일 지문·행·긍정 주장을 기록한다. 2018구board31은 Lakers의 이미 지명한Wagner25를 명시하며, Chicago22 재개 주분기54–56은23–27유지다. 2019AD 대체급여99는Wagner를 유지하고Bonga만Trent로 치환한다. 2020lockedboard4/17/41은Nesmith14/Pritchard26이다. 2021cascade37–39/57에서 Boston은Theis/Green방출·Wagner/Kornet수취를 유지한다. 기존Bos비용표14/62/65는승인된수취와Parker후속을 그대로사용한다. 인과모델54/57/58의원역사계약보존은이 입력에조건부로연결한다.

SalarySwish의Wagner2018계약섹션은 **ROOKIE SCALE CONTRACT / Rookie Exception / July1,2018 LAL**을 직접명시하고2020–21 option실행Sep25,2019·2021–22 option미실행Dec29,2020을표시한다. 현재veteran계약을rookie로간주하지않았다.

따라서 보존된이공개유한비용범위의 S2비용행 종료를 기록한다. 이번회수범위에서211,758을넘기는새실제계약·법적청구field는식별하지않았다. 두 연결claim을 작성·독립 검문해 true로 판정했다. 실제서명접수증이나모든미공표채무부재를추가필수로요구하지 않는다. 최신 통합은 **법적3완료/9HOLD·F0/5 A0/3 K0/4**, 미완료큰묶음6이다.
