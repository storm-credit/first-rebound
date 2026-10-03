# Fournier 2021 assignment bonus — 조건부 상한과 F2 증명 공백

2026-10-04 / 기준 main `108858f570abc69c1f36176b9787161fe80283a4`.
판정: `CONDITIONAL_BOUND_NOT_COMPLETE_LEGAL_DOMAIN`. [수치·권위 원장](FOURNIER_2021_ASSIGNMENT_BONUS_BOUND.json).

## 확인된 조항과 조건부 입력

[2017 NBA CBA](https://ak-static.cms.nba.com/wp-content/uploads/sites/4/2017/10/2017-NBA-Collective-Bargaining-Agreement.pdf)의 Article XXIV §2(a)(ii), 인쇄376/PDF398을 로컬 원문에서 읽었다. 트레이드 보너스의 상한은 거래 시점 계약상 잔여 **Base Compensation의15%**이며 미행사 옵션 연도는 제외한다. Article II의 signing bonus와 다른 조항이다. PDF633쪽·SHA256은 JSON에 기록한다. 이번 웹 도구에서는 PDF 접근 오류였으므로 웹 본문 회수로 기록하지 않는다.

[NBA의 2016 Orlando 프리뷰](https://www.nba.com/news/2016-17-season-preview-orlando-magic)는 Fournier의 당시 계약을 5년·85m으로 보도했다. 이는 2021 거래 시점의 계약 변경·연장 부재나 서명된 계약 전체를 인증하지 않는다. [기존 Boston 급여 원장](../simulation/BOSTON_DENVER_2020_21_PAYROLL.json)의17m 기본급·450k 인센티브는 공개 보도 입력이다. 실제 트레이드 보너스와 포기 동의는 미확인이다.

**조건:** 이 조항이2020–21 해당 계약에 적용되고, 추가 계약 연도가 없고 거래 시점 계약 전체의 잔여 기본급 합계가17m을 넘지 않으며, 공개된 성과 보너스450k가 이 계산의 성과 보너스 전체를 포괄할 때만 아래 상한이 성립한다. 이 조건들의 완전 검증은 아직 없다. 미행사 옵션 제외는 기본급 상한을 키우지 않는다. 거래 시점 잔여 기본급을 정확히 안다는 뜻도 아니다.

### 계약기간 보강 — 회수 권위 구분

2026-10-04 추가검색에서 [Orlando의 거래일 회고](https://www.nba.com/magic/orlando-magic-trade-deadline-recap-nikola-vucevic-aaron-gordon-evan-fournier-wendell-carter-gary-harris-otto-porter-rj-hampton-draft-pick-story-20210325)의 검색 색인은 Fournier가2021여름 UFA가 될 예정이었다고 전한다. 작성자는 Dan Savage·구단 Digital News Director, 게시시간2021-03-26 00:15 EDT로 표시된다. 2016계약의 연수만으로 추정하던 기간 조건에 보조 근거가 생겼다.

부모와 수집 에이전트 모두 검색 제공자의 공식URL 색인 추출을 본 것이며 직접 본문 검문은 아니다. 부모 web open은HTML셸1행·HTTP요청은403이었다. `SEARCH_PROVIDER_INDEX_EXTRACT_OF_OFFICIAL_URL`로 기록하고, 추가 계약 연도 부재의 전체 인증·기본급17m·성과450k전체·2020규칙 적용을PASS로 바꾸지 않는다.

## 새 계산

| 항목 | 조건부 값 | 해석 |
|---|---:|---|
| 트레이드 보너스 최대 |2,550,000|17,000,000×15%; 연간 전체 기본급을 쓰는 보수적 상한 |
| 수취 비용 스트레스 |20,000,000|기본급17m+보고된 성과 보너스450k+트레이드 보너스 최대2.55m |
| 보도 명목 Hayward TPE와 차이 |8,500,000|28.5m−20m; 당일 가용 잔액이나 예외 사용 PASS가 아님 |
| 기존4/16 Boston 스트레스 예산+최대 보너스 |136,096,805|133,546,805+2,550,000; 성과450k는 기존 예산에 이미 포함되어 재가산하지 않음 |
| 기존 apron 입력과 잔여 차이 |2,831,195|138,928,000−136,096,805; 미포함 R_BOS를 감당할 조건부 여유 |

트레이드 보너스0부터2.55m까지의 연속 구간은 이 선형 스트레스 계산에서 상단이 최악이다. 실제 보너스0을 선택하거나 선수 포기를 강제할 필요는 없다. 다만 상단 계산을 통과해도 **미포함 비용 R_BOS의 상한**·거래일 TPE 잔액·적용 규칙·실제 계약 범위가 검증되지 않아 전체 법적 구간이 닫히지는 않는다. 위20m은 합산 스트레스 값이며 정확한 CBA TPE charge 인증이 아니다.

## 동일성 증명에서 수정해야 할 연결

[기존 Fournier 동일성 경로](O15F14R_BOSTON_FOURNIER_PRIMARY_EQUIVALENCE.md)의 Boston 기존 계약·권리·예외 상태를 원역사와 같게 보존하는 방법은 여전히 검토 가능하다. 하지만 Orlando의 선행 결과가 달라질 때 Fournier 성과 보너스의 분류, 최초 유효 거래 여부, 보너스 포기·지급 경제 상태까지 자동으로 같다고 가정할 수 없다. 이름과 연간 보도 금액이 같다는 이유로 이 입력을 제거하지 않는다.

현재 기록 가능한 것은 공식 원거래가 보여 주는 법적 가능성과 위 조건부 상한이다. 적용 가능한 입력 전체를 감싸는 닫힌 구간 또는 완전한 분기 증인이 필요하다. S2가 비공개 장부 원본을 항상 요구하는 것은 아니다. 이번 문서는 그 증인 전체를 제공하지 않는다.

- 실제 trade bonus·waiver·잔여 기본급·R_BOS·당일 TPE capacity는 null.
- `BOS_COMPLETE_COST`, `BOS_TPE_AND_PICKS`의 complete/source_verified=false 및 법적12HOLD를 유지한다.
- F0/5·A0/3·K0/4, 새 작가 선택0, 시즌 실행 HOLD.
- freeze v0.30 PARTIAL·설계/원고 CLOSED·원고0.

## 수집의 실제 결과

2020–21 Dallas 공식 미디어가이드 URL은403이었다. Internet Archive의 구단 제작 가이드381쪽을 회수하고 작성자·파일 지문·당해 일정 페이지를 확인했지만, CBA101 급여·예외 규칙 표는 찾지 못했다. 구단 문서의 보존 미러라는 출처 성격과 원본 해시 대조 미확인을 유지한다. 이 파일을2020 수정 CBA의 증거로 사용하지 않는다. 경로/해시는 JSON에 기록한다.

Antigravity의 새 지정 조항 수집은55.121초 timeout·회수false. NotebookLM의 같은 CBA 출처 질의는6.588초에 인증 만료 오류를 반환했다. 자동refresh13.209초 성공 후 같은CBA질의는55.041초timeout으로 분석false다. 별도 A01자료는등록10.852초/분석35.436초에 회수했지만 CBA 독립 검증이 아니다. 원문 직접 검문과 독립 Codex 반증을 이 두 도구의 성공으로 세지 않는다. [이번 검수·처분 기록](../reviews/A01_AND_FOURNIER_REVIEW_2026_10_04.md)에 연결한다.
