# O-15G15AG — 2021-10-20 Detroit 개막 공식 경기 기록의 17명 대조

- 시작 권위: `main` `885deb9`, [G15AF 실명 재구성](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)의 **독립 개막 명부 미회수**. 판정: `OPENING_17_NAMES_OFFICIAL_BOX_MATCH / CONTRACT_TYPE_CROSS_SOURCE / ALTERNATE_ROSTER_HOLD`.
- `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`; `author_locked=false`, `season_selected=false`, `exact_execution_cleared=false`, `manuscript_allowed=false`. 신규 작가확정 0건.

## 1. 경기일 이름의 독립 대조

[NBA 공식 2021-10-20 CHI@DET 기록 PDF, 첫 페이지 FINAL BOX](https://statsdmz.nba.com/pdfs/20211020/20211020_CHIDET_book.pdf)는 Detroit의 선발 5명, 출전한 교체 5명, DNP 4명, inactive 3명을 함께 싣는다. [G15AF](O15G15AF_DETROIT_NAMED_ROSTER_TO_OPENING_GATE.md)가 앞선 거래 계보에서 만든 이름 집합과 **독립 경로의 당일 명단**을 비교할 수 있게 됐다.

| 공식 기록의 분류 | Detroit 이름 | 수 |
|---|---|---:|
| 선발 | Saddiq Bey, Jerami Grant, Isaiah Stewart, Frank Jackson, Killian Hayes | 5 |
| 출전한 교체 | Hamidou Diallo, Kelly Olynyk, Cory Joseph, Trey Lyles, Josh Jackson | 5 |
| DNP | Luka Garza, Saben Lee, Rodney McGruder, **Jamorko Pickett** | 4 |
| Inactive | Cade Cunningham(발목), Isaiah Livers(발), **Chris Smith**(무릎) | 3 |
| 총계 | 고유 이름 | **17** |

공식 경기 기록에는 **계약 유형이 쓰여 있지 않다**. 별도 [Detroit 9/29 구단 문답](https://www.nba.com/pistons/chatmailbox/pistons-mailbag-september-29-2021)은 **Pickett와 Smith가 투웨이 계약**이라고 밝힌다. 개막에 더 가까운 [10/5 구단 기사](https://www.nba.com/pistons/preseason-primer-cunninghams-ankle-likely-hold-him-out-pistons-opener-casey-says)는 Smith를, [10/13 구단 기사](https://www.nba.com/pistons/features/minus-3-starters-pistons-go-cold-2nd-half-and-come-short-new-york)는 Pickett를 각각 투웨이로 부른다. 두 이름을 17명에서 빼면 **15명**, 그 이름 집합이 G15AF **원역사** 개막 재구성 15명과 **정확히 일치**한다. [12/1 구단 문답](https://www.nba.com/pistons/news/pistons-mailbag-december-1-2021)도 이후 표준 15명·투웨이 2명 보유를 설명한다. **17−2=15는 경기 기록 자체의 계약 분류가 아니라 별도 구단 자료를 합친 추론**이다. 경기 기록의 DNP/inactive는 선수 명시 범주일 뿐 계약 유형이 아니다. 이 교차 대조는 10/20의 **선수 이름**을 독립 확인한 것이며 선수별 계약서·당일 NBA 등록 시스템 원본, 10/13–10/20 모든 임시 계약 사건을 확보했다는 뜻은 아니다. Cade/Livers의 결장 사유는 PDF의 inactive 행에 표기된다. 두 선수는 **등록 이름에는 있지만 결장**했으므로 개막 박스의 득점·분을 배정하지 않는다. Pickett가 DNP 명단에 있다고 표준계약자로 바꾸지 않는다.

## 2. 대체세계에 넘길 수 없는 것

같은 원역사 경기 기록에서 Chicago의 Patrick Williams는 **28:26**을 뛰었다. [2020 정본](../canon/PROJECT_FREEZE.md)은 Patrick의 Detroit 7번을 확정했고, [G14 Detroit 조건부 10/20 배분](../simulation/CHICAGO_2021_22_PAIRED_REVIEW.md)은 Patrick에게 Detroit SF 28분을 준다. 따라서 원역사 Chicago의 그의 28:26이나 6점을 **대체 Chicago의 실적**으로 옮길 수 없다. G14의 Chicago 분안은 별도 조건부 수학 배분이므로 이 원역사 PDF로 그 분안의 계약·득점을 인증하지 않는다.

P0-B의 `16`은 G15AF의 **다른 모든 계약·거래가 성립할 때만** 나타난다. 이번 공식 경기 기록은 **원역사** 17명과 계약 유형의 외부 교차 대조일 뿐, 대체 Plumlee/Olynyk 동시 보유나 9/4 Nets 거래 수락을 증명하지 않는다. 대체세계에서는 Patrick/Kira와 미선택 Suggs의 서명, 추가 한 자리 실명 이탈, Olynyk 8/6 cap 경로, Charlotte의 센터/권리 손실, 개막 당일 활동·의료를 별도로 채워야 한다. 원역사의 88:94 최종 점수와 선수 출전시간도 자동 이전하지 않는다.

## 3. 검증과 다음 지점

[별도 JSON](O15G15AG_DETROIT_2021_OPENING_GAMEBOOK.json)과 [검사기](../tools/check_o15g15ag_detroit_gamebook.py)는 `5+5+4+3=17`, Pickett·Smith 제외 후 G15AF의 15명과 이름 집합 일치, inactive 3명을 대조한다. 원본 PDF는 저장소에 복제하지 않고 공식 URL을 근거로 둔다. [도구별 검수](../reviews/R01_O15G15AG_GAMEBOOK_CLI_AND_BLIND.md)는 Antigravity의 시간 초과, NotebookLM의 같은 PDF 제한 분석, Codex의 직접 PDF 대조를 독립 원자료 수로 중복 계수하지 않는다.

| 구분 | 판정 |
|---|---|
| 사실 | 공식 원역사 FINAL BOX의 Detroit 17명·DNP/inactive 및 Chicago Patrick28:26; 9/29 구단 자료의 Pickett/Smith 투웨이. |
| 추론 | 공식 경기 기록과 9/29·10/5·10/13 구단 계약 유형 자료를 합쳐 본 10/20 원역사 표준계약 15명 이름이 G15AF의 사건 재구성과 일치. 당일 계약 원장·완전한 계약 조항·팀 급여 증명은 아님. |
| 후보 | P0-B 개막 16명 스트레스는 조건부 유지. 이 PDF로 대체명단을 만들지 않는다. |
| 작가확정 | 이번 0건. G14 DET `PRIOR_HOLD`·ORL `ROLE_HOLD`, Chicago 정확 시즌, G16/G17 및 원고 모두 `HOLD`. |

다음은 **P0-B의 16번째 선수를 없애는 실제 후보를 선수명·급여·상대 팀·분 비용으로 비교**하고, 그보다 선행하는 8/6 Olynyk cap 경로를 날짜별 금액으로 증명하는 것이다. 7개 매크로 게이트는 1완료·1진행·5대기, 진행 중 포함 6개가 남는다.
