# Chicago Simon 이월·Denver 일할 범위 검수

2026-10-05 / 기준 main `92d3db4` (PR419). 추가 전체 법적 종료 0.

## 반영한 근거

[Simon JSON](../research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.json) / [설명](../research/CHICAGO_SIMON_2019_CARRY_BOUNDARY_2026_10_05.md): 당시 기자의 Exhibit10 원보도와 실제 서명 업데이트, NBA October19 원행을 연결했다. parent는 web 원문과 로컬 성공 HTML 지문, CBA PDF44/217/249/250을 직접 대조했다. 유지된 한 시즌 계약의 2020 ordinary base·당해 시즌 future stretch·실제 Exhibit10 Bonus 산입만 `[0,0]`이다. 부상/중재/후행 조정/별도 계약/전체 Chicago R까지 지우지 않는다. Windy City affiliate 분류는 NBA 계약 유형을 대신하지 않는다. 신규 계약 유형 근거는 공개 2019 방출6명 중 Simon1명에 관한 것이다.

[Denver followup](../research/DEN_GORDON_CLARK_BONUS_SCREEN_2026_10_05.json)의 VII§2(b)(4)(i)는 trade/waiver의 같은 계약 Salary를 실제 정규시즌 일수로 배분하지만 **Minimum Team Salary 목적**이다. UPC10(a)는 계약 양도의 동일 효력을 보강한다. parent는 PDF184/185/521을 직접 읽었고, 이를 XXIV의 earned 직접 정의로 승격하지 않았다. UPC3(b)의 캠프·프리시즌 주간 선지급을 earned 정의로 쓰는 경로를 기각했다. 기존 조건부 2,339,462.97과 Gamma null은 유지된다.

## 추가 2019 기간·더 짧은 비교 종료 경로

[추가 cohort JSON](../research/CHICAGO_2019_COHORT_CARRY_BOUNDARY_2026_10_05.json) / [설명](../research/CHICAGO_2019_COHORT_CARRY_BOUNDARY_2026_10_05.md): Blakeney의2018 두 시즌 이력·Deng의Chicago one-day 보도·Shittu의2019 한 시즌 첫 표를 실제 본문에서 확인해 미래ordinaryyear/currentseasonfuturestretch만 좁혔다. Simon 포함4/6 기간 경로는 전체4계약 비용 완료가 아니다. Shittu2019 caphold898310과 별도2020 계약은 삭제하지 않는다. 새 보도/데이터 이력의 권위와 기존 waive 재사용을 구분한다.

chi_salary_domain의 전체 비교 감사는 [기존 15인 차액](../research/O15F14AS_CHICAGO_PUBLIC_ROSTER_DELTA.md)−1,951,061을 새 근거로 중복 계수하지 않고 재사용했다. Young unlikely1m를 대체쪽에 전액 스트레스하면 `ALT ≤ HIST_FULL_UPPER −951,061 + OTHER_DELTA_UPPER`이다. 따라서 **동일일/동일정의의 원역사 전체 상단 + 나머지 모든 차액 상단 ≤133,578,061**이면 이 경로에서 Chicago tax 경계를 닫을 수 있다. 두 상단은 아직null이다.

이 경로가 감싸야 하는 차액은 다른 계약의 기본급 외 산입, 동일 Theis/Green의 거래 구조 차이, 공통 계약의 변경/성과 차이, 이전 의무·권리/예외 자격, 시점·급여 정의 전환의5범주다. 동일 이름이라는 이유로 전부 상쇄하지 않는다. 반대로 공개된 유한 사건·동일 법적 입력 증인으로 감싸면 되며, 비공개 장부 원본을 새로운 필수조건으로 요구하지 않는다.

원역사 거래 성립만으로 Chicago 비납세를 역추론하는 경로는 반례로 기각한다. 두 인수 거래를 하나의 Chicago 동시 인수 그룹으로 놓는 계산 반례에서는 약40.15m 송출/45.61m 수취가 납세125%+100k 허용 약50.29m 안에 들어간다. 실제 그룹 실행이 그렇게 됐다는 주장은 아니다. Denver의138,928,000 apron상단만 Chicago에 복사하면137,976,939로 세금선보다5,349,939 높아 충분하지 않다. 시즌말tax는 VII§12(f)(2), PDF286/인쇄264의 시점·실제보너스 조정에 기초하므로 거래일 TeamSalary와 정의를 자동 등치하지 않는다. **다음 핵심 근거는 March25 직후 전체 cap total과 산입 정의를 함께 제시한 당시 원분석**이다.

## 도구 실행과 판정

- Antigravity: [실행 기록](CHI_2019_CAMP_AG_2026_10_05.json). 확인한 절대 CLI 경로로 Callandret/Doyle 원문 수집을 실제 실행했다. 48.376초/exit0, terminal SUCCESS이나 response 빈 값이다. search_web2단계·run_command2단계가 DONE이어도 본문·최종 답변 회수는 false다. 신규 검증된 원문0. 같은 빈 응답의 반복 호출을 완료로 세지 않는다.
- NotebookLM: [등록](CHI_SIMON_NLM_SOURCE_2026_10_05.json) 6.545초, [분석](CHI_SIMON_NLM_2026_10_05.json) 49.565초에 새 Simon 사본의 응답을 회수했다. 명단 분류/계약 유형, 세 항목0/전체R 미확정의 경계를 확인했다. 인용3개는 모두 같은 파생 source 하나다. 독립 사실 검증·법적 승인으로 세지 않는다. 응답의 Candidate Status 표현은 미확인 비용까지 작가 후보로 승격하는 분류로 채택하지 않는다. 말미의 작업 제안은 지시가 아니다.
- Claude: [실행 기록](CHI_SIMON_CLAUDE_2026_10_05.json). 도구/MCP를 비활성화한 국소 반증을 85초 외부 예산으로 실행했으나 PROCESS_TIMEOUT, 응답 회수 false다. 앞선 세션한도 오류를 이번 결과로 재계수하지 않으며 독립 통과0이다.
- 독립 Codex: `/root/independent_finish_scope`가 실제 Simon JSON/MD/S2 변경과 로컬 CBA를 읽고 국소 범위를 수용했다. 추가3계약 JSON과 Deng 원문을 검문하고, 최종 MD·Blakeney/Shittu 성공 캐시의 기간/서로 다른 두 계약/caphold/지문도 직접 대조하여 한정 수용했다. 원수집자인 chi_salary_domain/nba_legal_next와 역할을 분리했다. 해당 reviewer는 Simon 원보도를 별도로 재회수하지 않았으므로 새 원보도 독립수집으로 세지 않는다.
- 전체 source-blind/G16: 미완료. 국소 검수와 구분한다.

## 저장소 검문

S2 검사기는 ORL_DATED_REGISTRATION·DEN_CLE_DATED_REGISTRATION만 LEGAL_BOUND_PASS, 나머지10행 HOLD다. Denver 비교 출력의 --check도 일치한다. 새 근거의 source/waive 원행과 SHA, supporting 경로를 대조하며 입력 지문은 raw repository bytes다. freeze/gate·A01 Blueprint 입력은 변경하지 않는다. 새 작가선택0·원고0.

| 큰묶음 | 현재 |
|---|---|
| 1 2020 드래프트 연쇄 | 완료 유지 |
| 2 Chicago2020–21 | 법적2완료/10HOLD·F0/5 A0/3 K0/4; 2019기간4/6의 국소 이월 범위 좁힘 |
| 3 2021–23 거래·계약 | 승인M1/G1A 유지, 정확 실행 미완료 |
| 4 장기 커리어 | 17시즌 골격, 실행/주요 결과 미완료 |
| 5 결말·전체 구조 | 14막42소막780슬롯·A01국소Blueprint3, 최종회차 기능0 |
| 6 집필 규격·Context Pack | 표본 기반 문체 규격 완료, 실제Pack0·전체 미완료 |
| 7 통합·독립·작가 승인 | 전체 미완료 |

미완료 큰묶음6. 다음은 다른 2019 계약의 기간/이월, Chicago 전체 비교 상한의 짧은 종료 경로, Denver earned·보호·기타 차액이다. 비공개 원계약이나 미공표 비용의 절대 부재를 새 조건으로 추가하지 않는다. freeze v0.30 PARTIAL·설계/원고 CLOSED 유지.
