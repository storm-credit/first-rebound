# Gordon A 실행 조건과 후반 계산 경계 — O-15F6D

- 상태: `EXECUTION_CONDITIONS_SPECIFIED / FULL_CAP_AND_PICK_TERMS_HOLD`
- 선수 제안: Harris·Nnaji·보호 미래 1R → Orlando, Gordon·Clark → Denver
- 현행 권한: `DIRECTION_AUTHOR_APPROVED_H / EXACT_CHARGE_PICK_HOLD`
- 아래 F6D/D 본문의 미승인·협상 표현은 당시 이력이다. 최신 방향 승인 권위는 `canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json`이며 정확 실행 조건은 계속 미확정이다.
- 선행 보드: `ORLANDO_DENVER_2021_GORDON_BOARD.md`

## 1. 무엇이 남았는가

| 확인 항목 | 현재 | 해소 조건 |
|---|---|---|
| Denver의 신인 자산 | Bey22·Nnaji24, Hampton Dallas31 정본 | 닫힘; 새 드래프트 보드 생성 불요 |
| 두 팀 선수 수 | 2명 출발·2명 도착 | 순증 0; 각 선수의 실제 계약/가용성과는 별개 |
| Nnaji 기본급 | 24번 scale 동일120% 가정 $2,193,480 | 계약 비율·보너스 확인 전 조건부 |
| 전체 급여 | Harris·Gordon·Clark 당일 cap 급여와 조항 미확보 | 모든 수출입 급여·추가 charge·팀의 적용 예외를 같은 날짜로 확인 |
| 선행 픽 | Denver의 24번 권리 취득에 미래1R 지출 존재 | 정확 연도·보호·이연·종료 조항 확보 |
| Gordon 픽 | 2025~27 top-5 보호 보도 존재 | 선행 의무와 연결된 전달 문구·미전달 전환 자산 확보 |
| Orlando 수용 | 유망주 역할·픽 반환의 논리 있음 | Vučević 잔류/별도 매각 조건별 A/B/D 비교 후 정확 사건 선택 |

공식 2020 거래표에는 Denver의 미래1R이 Oklahoma City로 가는 비용이 있다. [NBA 공식 거래표](https://www.nba.com/news/2020-nba-draft-trade-tracker)

Gordon 픽의 2025~27 top-5 보호는 동시대 보도다. [CBS 2021-03-25](https://www.cbssports.com/nba/news/aaron-gordon-trade-grades-magic-star-dealt-to-nuggets-for-gary-harris-rj-hampton-and-a-pick-per-report/)

이번 공개 자료 검색은 정확 보호·이연 계약 원문을 확보하지 못했다. 현재 시점의 미래 픽 표는 이미 집행된 과거 의무를 생략할 수 있어 2021 장부 대용으로 쓰지 않는다. 같은 검색을 반복하며 후반 입력 작업 전체를 멈추지 않는다. 새 원문·당시 장부 확보 시 해당 셀만 재개한다.

## 2. 픽 달력 검산의 구체적 질문

아래는 **정확 계약의 복원이 아닌 보수적인 비연속 연도 조건 시험**이다. 선행 1R이 전달되는 연도를 Y라 두고, 다음 1R 후보를 Y+2 이후로 한정하는 초안의 효과를 표시한다. 선행 의무가 실제로 아래 모든 해까지 연장된다고 확인한 표가 아니다. 다른 팀의 1R 소유·스왑·별도 부담까지 포함한 NBA 적법성 인증도 아니다.

| 가정한 선행 전달 Y | 2025~27 중 초안의 비연속 조건을 만족하는 후보 | 배제되는 후보 |
|---:|---|---|
| 2023 | 2025·2026·2027 | 없음 |
| 2024 | 2026·2027 | 2025 |
| 2025 | 2027 | 2025·2026 |
| 1R 미전달·소멸/2R 전환 | 정확 종료 조항 후 판단 | 자동 2025 확정 금지 |

따라서 “2025 보호 픽 한 장”이라는 요약만으로 단일 지명권을 확정하지 않는다. 전달 가능해진 뒤에도 보호 범위면 다음 해/전환 자산을 추적해야 한다. 임의로 2028 1R을 추가하거나 새 2R을 만들어 종료 조항을 채우지 않는다. 미래 시즌의 실제 성적·실제 전달 연도는 대체 세계에서 보장되지 않는다.

## 3. 거래 선택과 조건부 계산을 분리

Chicago A 작가 승인으로 Gordon A까지 확정하지 않는다. 후반 계산은 식별된 조건부 가지를 사용할 수 있으나 그 결과에 `CONDITIONAL`을 표시하고 승인 전 합산 정본으로 승격하지 않는다.

- Vučević 잔류 + Gordon A: Carter는 Chicago에 남고 Orlando의 센터 분은 Vučević·Bamba 등을 기준으로 새로 배정한다.
- Vučević 별도 매각 + Gordon A: 실제 Chicago 대가를 재사용하지 않고 새로운 대가·수취팀이 준비된 경우에만 수치 계산한다.
- Gordon D: Denver 협상 결렬까지만 뜻한다. Gordon의 다른 행선지를 발명하지 않는다. 잔류를 시험할 때는 별도 잔류 가정이라고 쓴다.

Fournier·Teague·Wagner 후속은 별도 사건이다. 한 가지가 닫혔다고 Orlando 전체 정리를 닫지 않는다. 정확 거래 선택을 요청할 때는 남은 실행 조건과 각 선택의 직접 시즌 영향을 함께 제시한다.

## 4. 현재 29경기에 필요한 범위

후반 일정은 **19개 상대 팀, 29경기**다. Denver와의 직접 경기는 없고 Orlando는 04-14 한 경기다. Gordon 의무가 미정인 동안에도 다른 경기의 Chicago 생산성 prior와 상대 입력 수집은 진행할 수 있다. 단, 다른 상대를 자동 무변경 처리하지 않으며 Minnesota·Charlotte·Detroit·Boston 등 기존 드래프트/거래 접촉을 개별 판정한다. Denver의 리그 전체 순위 영향은 시즌 순위·2021 lottery 연결 시 회수한다.

직접 경기 목록은 `CHICAGO_2020_21_POSTDEADLINE_OPPONENT_QUEUE.csv`로 고정했다. 이 표는 작업 큐이며 상대 roster 통과 증명이 아니다. 다음 O-15F7은 각 행에 가용성·변경 선수·분 donor·생산성 입력을 붙이는 작업이다. 정확 부상/거래가 미정인 행만 조건부 분기 상태로 남긴다.

## 2026-09-11 O-15F14-D 실행 입력 구체화

상태는 `EXECUTION_INPUTS_PARTLY_RECOVERED / EXACT_CHARGE_PICK_AND_AUTHOR_CHOICE_HOLD`다. 아래는 선행 A/B/C/D 보드를 실행 가능한 입력과 재계산 범위에 연결한다. 거래 성사 판정은 아니다.

### 급여 입력: 확보값과 미확보값

| 선수·슬롯 | 이번에 사용할 수 있는 값 | 정확 matching에 넣을 값 | 상태 |
|---|---:|---|---|
| Harris | 새로 확보한 급여 근거 없음 | 거래 전 Denver outgoing / Orlando incoming charge 각각 필요 | `null / HOLD` |
| Gordon | 새로 확보한 급여 근거 없음 | 거래 전 Orlando outgoing / Denver incoming charge 각각 필요 | `null / HOLD` |
| Clark | 2020–21 명목 급여 $2,000,000 | 해당 날짜의 양쪽 charge·보너스 적용은 별도 | `REPORTED_SALARY_ONLY` |
| Nnaji 24 | 선행 120% 가정 $2,193,480 | 대체 계약 비율과 부가 charge | `CONDITIONAL_BASE_ONLY` |
| Bey 22 | 선행 120% 가정 $2,379,840 | 대체 계약 비율과 부가 charge | `CONDITIONAL_BASE_ONLY` |

Clark의 명목 급여는 이번에 본문을 읽은 [HoopsHype 급여 이력](https://hoopshype.com/player/gary-clark/salary/)에서 확인했다. 같은 페이지의 Philadelphia $18,458은 후속 계약 이력이므로 3월 25일 Denver 수취액에 합산하지 않는다. 이 페이지는 2차 급여 이력이며 당일 리그 charge 원장이 아니다.

A의 선수 총액은 Denver `Harris + Nnaji24` 발신, `Gordon + Clark` 수신이다. Orlando는 반대 방향이지만 선수의 발신·수신 charge가 항상 같다고 가정하지 않는다. B는 Nnaji24 대신 Bey22를 쓰므로 **같은 120% 기본급만 비교하면 $186,360 증가**한다. C는 Nnaji/Bey와 Clark을 모두 빼므로 A에서 선수 한 명만 제거한 거래로 계산하지 않는다. 두 팀 모두 해당 예외·팀 급여·세금·보너스 기준을 충족해야 하며, 명목 급여를 채운 것만으로 cap PASS를 선언하지 않는다. 미확보 셀은 0으로 입력하지 않는다.

### 미래 픽: 계약 원문 대신 만들지 않을 필드

| 자산 | 이미 확인된 범위 | 여전히 비어 있는 필드 | 재개 조건 |
|---|---|---|---|
| 24번 권리 취득 대가 | Denver의 선행 미래 1R 지출 존재 | 최초 전달 연도·연도별 보호·이연·종료·전환 | 해당 거래 당시의 조항/보관 장부 확보 |
| Gordon 대가 | 선행 보드의 2025~27 top-5 보호 보도 | 선행 의무와 연결된 정확 전달 문구·최종 미전달 처리 | 위 선행 의무와 한 장부로 재구성 |
| A/B/C의 픽 | 상호 배타적인 같은 제안 자산 | 실제 선택·양 팀 동의 | 세 안에 각각 별도 픽을 추가하지 않음 |

앞의 Y+2 달력은 여전히 가정 시험이다. 선행 픽이 보호로 이연될 때 후행 픽도 언제/어떻게 미뤄지는지 확인하지 않은 상태에서 2025 단일 픽으로 잠그지 않는다. 최신 미래 픽 웹페이지에 과거 의무가 없다는 사실은 과거 무부담 증거가 아니다.

### 사건 선택별 입력 폐기 범위

| 선택 | 새 40경기 중 직접 재계산해야 하는 입력 | 기존 계산에 대한 영향 | 남는 수용 문제 |
|---|---|---|---|
| A | ORL 3/28은 Vučević30·Nnaji8/12, DEN 4/21은 Bey20/24·Gordon 실제 분 조건으로 계산 완료 | CHI–ORL 4/14의 선행 A 가정과 연결 | Orlando의 빅 개발 분 경쟁·가드 유망주 부재, 양 팀 정확 거래 조건 |
| B | ORL에 Nnaji 대신 Bey, DEN에 Bey 대신 Nnaji를 남기는 새 분 배정 필요 | 4/14 Orlando 입력과 A로 묶인 전체 시즌 경로 재생성 | Denver가 새 슈팅 윙을 포기하는 비용; Orlando 선호는 공개 사실로 단정 불가 |
| C | ORL에 신인 없음·Clark 잔류, DEN에 Nnaji/Bey 유지·Clark 미합류 | A의 2대2 로스터/급여/분을 재사용할 수 없음 | Orlando가 신인 없는 반환을 받아들일 근거 부족 |
| D | DEN에서 Gordon 제거 후 대체 역할 필요; ORL은 잔류/제3행선지를 먼저 지정 | A 기반 Orlando/Denver 입력을 모두 사용 중지 | 결렬은 Gordon 잔류 확정이 아님; 다른 거래를 발명하지 않음 |

위 날짜는 **현재 계산된 40경기 안의 직접 접촉 목록**이다. 남은 리그 경기 전체에서 Orlando·Denver의 영향을 면제하는 목록이 아니다. A를 택해도 실제 역사와 같은 선수 GP·분·건강을 보장하지 않는다. 특히 ORL 3/28은 Harris에게 분을 주지 않았고, Bamba·Birch 관측 가용성을 보존했다. 4/14의 Hall 계약 가정을 3/28로 당겨 쓰지 않았다. DEN 4/21의 Rivers·McGee 등 후속 시장 경로는 별도 조건부 유지이며 Gordon 영입만으로 자동 승인되지 않는다.

### 접근 결과와 다음 조사 범위

이번 조회에서 NBA 두 구단 페이지는 iframe만 반환했다. Basketball-Reference Harris/Gordon, ProSportsTransactions Nuggets는 403, HoopsHype Harris/Gordon 및 전체 급여표는 robots 제한, Spotrac 두 선수 URL은 열기 실패였다. 실패한 페이지를 읽은 근거로 사용하지 않는다. Clark 급여 이력만 본문 확보했다. 이는 이 접근 경로의 2026-09-11 결과이며 공개 자료 전체가 없다는 주장은 아니다.

따라서 Gordon 실행보드는 **부분 구체화**다. 새로 확보된 당시 장부·조항·접근 가능한 급여 원문이 있을 때 미확보 셀부터 재개한다. 현 단계에서 승패를 맞추기 위해 A를 확정하거나, 정확 조건이 없는 승인 질문을 반복하지 않는다. 40경기 조건부 영향 작업은 완료했고, 다음 리그 입력 작업은 계속할 수 있다.


## 2026-09-11 O-15F14-F 전체시즌 연결 이후

D의40경기표는당시범위의이력이다. 현재 `CHICAGO_2020_21_FULL_SEASON_CONNECTION.md`에서남은859까지영향계산을완료했다. Gordon A를바꾸면해당거래검토단계이후DEN/ORL의전체정규시즌입력과선행Chicago–ORL을회수해야한다. 기존같은급여/동일계약조건은확인된사실로추가하지않았고,이번Harris/Gordon급여이력본문접근은제한되어새급여값을확보하지못했다. 정확charge·픽조항과작가의Gordon사건선택은여전히HOLD다. 역할전제는분검산가능성과별개이며ORL의Ross보조진행·Nnaji비상골밑및후속등록도작가패킷에포함한다.


## O-15F14-H 최신 승인 범위 — 2026-09-11

G 추천 질문에 대한 사용자의 ‘이어서’로 **A 선수/자산 방향을 채택**했다. 권위 `canon/CHICAGO_2020_21_DIRECTION_APPROVAL.json`. Harris·Nnaji·보호 미래1R 대 Gordon·Clark 방향과 Vučević 잔여시즌 ORL 잔류, Fournier 독립 Boston행을 각각 승인 범위대로 적용한다. 선행 본문의 A_NEGOTIATION_LEAN/작가 방향 미선택 표현은 이력이며 방향 재승인은 불요다.

정확 당일 charge·보너스·선행 픽 보호/이연/전환은 이번에도 미확보다. `AUTHOR_APPROVED_DIRECTION / EXACT_EXECUTION_HOLD`이며 거래 실행 PASS가 아니다. 신규 건강·후속 등록은 별도다. 최신 대조는 `CHICAGO_2020_21_EXECUTION_ADOPTION.md`와 달력 CSV를 따른다. G/F 수치 산출물은 당시 조건부 기록으로 보존한다.


## 2026-09-12 O-15F14-K 현행 실행 연결

H에서승인된Gordon A선수방향을재협상질문으로되돌리지않는다. K1은Vučević잔류세계에서도Hall/Wagner백업수요가있는조건부28경기분안을유지한다. 불필요한빅맨중복은선수별분을바꾸지않고최소화했으며4경기는중복이남는다. 근거는 `CHICAGO_2020_21_SEASON_RECOMMENDATION.md`와ORLANDO조합JSON이다.

후속선수의필요성과등록자격은분리한다. Hall5/2~5/8은기존3경기0분으로유지했다. 실제10일계약이력은2차장부로대조했지만새세계의roster slot·적용예외·charge는아직확정하지않았다. Gordon선행/후행픽및양팀charge미확보필드는그대로다. 다음L에서정확필드와창작선택을구분해결산조건을닫는다.


## O-15F14-L 현재 경계

이번 회수한 공식 출처와 날짜 대조의 권위는 `CHICAGO_2020_21_EXECUTION_CLOSEOUT.md` 및 출처 JSON이다. Hall·Wagner·Parker·McGee 관련 실제 연쇄 일부를 확인했으나 Gordon 선행/후행1R의 정확 보호·이연·종료 및 양 팀 당일 charge는 아직 미확보다. 해당 사실을 작가 선택으로 대신하지 않는다. H의 A 방향 승인·K의 조건부 분 배정은 보존하며 L 전체 실행 PASS로 승격하지 않는다.


## L 등록 인원 후속 반영

`ORLANDO_2020_21_REGISTRATION_LEDGER.md` 및 동명JSON을 후속 권위로 연결한다. 앞선 Rivers 후속 본문 미확보와 ORL 자리 수 미산출은 이력이다. 후속에서 구단본문9건 추가·계약 유형 및 기간을 회수하고 ORL 5/9 이후 일반계약16+투웨이2/추가1자리 필요5경기를 특정했다. 정확 허가·charge·거래 의무·작가 채택은 여전히 HOLD다. 날짜만 확인한 선행140행과 새 등록 인원 대조의 범위를 혼합하지 않는다.


## L 실행 조항·급여 후속 반영

`CHICAGO_2020_21_EXECUTION_TERMS.md` 및 동명JSON을 후속 권위로 연결한다. Hall 신청의4명 결장 근거·2019규약6.08, Harris/Gordon 등8명의2차 급여 항목, Denver 선행 보호기간과 Fournier 픽 연도 일부를 회수했다. 선행 미확보 표현은 해당 범위에서 이력이다. 정확charge·리그 승인·당일 팀 세금/예외·픽 연결/종료는 미완료이며 K1/L2 추천을 작가 확정으로 올리지 않는다.
