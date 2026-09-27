# O-15G8D — Markkanen 계약연도 역할의 분 원장 대조

- 기준: `main` `8664d72`; [G8B 선수 동의 관문](O15G8B_MARKKANEN_2021_CONSENT_GATE.md), [G8C 제안 시험](../simulation/CHICAGO_2021_MARKKANEN_OFFER_STRESS.md).
- 상태: `INTERNAL_LEDGER_AUDIT / ROLE_IMPROVEMENT_UNPROVEN / G1A_CONSENT_HOLD`.
- 범위: 기존 2020–21 경기별 분과 K1의 후반 계산 입력을 읽는다. 시즌·계약·선수 의사·공격 기회·작가확정을 새로 만들지 않는다.

## 같은 계약연도의 실제 기록과 대체 후보

| 구간 | 원역사 Chicago 관측 | 대체 세계 계산 입력 | 차이와 권위 |
|---|---:|---:|---|
| 전반 43경기 중 Markkanen 출전일 | 23경기·23선발·41,429초(690:29) | 같은 23경기·23선발·41,429초 | [전반 선수 예산](../simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_BUDGET.csv)은 날짜별 Markkanen 분을 보호한다. |
| 후반 29경기 중 출전일 | 28경기·3선발·37,617초(626:57) | 최초 [용량 원장](../simulation/CHICAGO_2020_21_POSTDEADLINE_CAPACITY_BUDGET.csv)은 같은 37,617초 | 이 원장은 총분·선발의 **조건부 용량 시험**이다. |
| K1의 `PORTER_ZERO` 후반 5인 보정 | 위 37,617초 | 28경기·3선발·36,899초(614:59) | [F6B 5인 증명](../simulation/CHICAGO_2020_21_POSTDEADLINE_LINEUP_AUDIT.json)의 `minimum_change_candidate.player_seconds` 합계. 원역사보다 **718초(11:58) 감소**한다. |
| 전후반 합계 | 51경기·26선발·79,046초(1,317:26) | K1 후반 보정 연결 시 51경기·26선발·78,328초(1,305:28) | 실제 출전일·선발을 후보에 상속한 계산 결과다. 최종 대체 시즌의 건강·출전 기록이 아니다. |

후반 `PORTER_ZERO` 감소는 3/31 **116초**, 4/26 **206초**, 4/28 **396초**다. 다른 날짜의 부동소수 오차는 1초 미만이다. F6B는 최대 두 빅맨 동시 출전이라는 **분석용 전술 정책** 아래 같은 날짜 선수끼리 분을 옮겼다. 세 빅맨을 허용하면 원래 분도 수학적으로 성립하므로 718초 감소가 NBA 규칙상 필수라는 뜻은 아니다. [후반 감사](../simulation/CHICAGO_2020_21_POSTDEADLINE_EXECUTION_AUDIT.md)는 이를 확정 로테이션으로 승인하지 않았다.

K1은 `PORTER_ZERO`를 택한다. [F9 재현 코드](../tools/crosscheck_chicago_2020_21_impact.py)는 후반 `minimum_change_candidate.player_seconds`를 Chicago 영향 입력으로 읽는다. 따라서 최초 용량표의 Markkanen **0분 변화**를 K1의 최종 계산 입력으로 부르면 안 된다. 다른 `PORTER_CAPPED` 보정안은 후반 36,780초로 별도 민감도이며 K1 주경로 숫자와 섞지 않는다.

## 출전시간과 공격 기회는 다른 주장

후속 [G8E 선발 인과 감사](O15G8E_MARKKANEN_STARTER_CAUSALITY_BOARD.md)는 위 26선발 합계 중 후반 3선발이 **원역사 표기를 상속한 K1 입력**이며, Vučević 없는 세계의 코치 결정을 증명하지 않는다고 판정한다. 아래 1,305:28은 S0 입력의 분 합계이고 S1–S3 선발 후보의 실전 분·전술 결과가 아니다.

전반 모델은 LaVine·Markkanen과 센터진의 **경기별 분을 원역사와 같게** 둔다([전반 원장](../simulation/CHICAGO_2020_21_PREDEADLINE_PLAYER_GAME.md)). 후반 `PORTER_ZERO` 최초 용량도 Markkanen 분을 같게 두었고, K1이 쓰는 5인 보정에서는 오히려 11:58 줄어든다. Vučević가 없고 Carter가 남는다는 **명단 구조 변화**는 사실이지만, 현재 계산이 계약연도 Markkanen의 출전시간 확대를 보여 준다는 주장은 성립하지 않는다.

[후반 관측 priors](../simulation/CHICAGO_2020_21_POSTDEADLINE_OBSERVED_PRIORS.csv)의 Markkanen 득점·FGA는 3/24까지 원역사 표본이고, [후반 실제 박스 입력](../simulation/CHICAGO_2020_21_POSTDEADLINE_ACTUAL.csv)은 실제 Chicago 경기다. K1 보정은 **분과 영향 계수**를 계산하며 대체 세계의 Markkanen 슛 시도·터치·사용률·공격 전술·라커룸 평가를 경기별로 재배정하지 않는다. 원역사 FGA를 대체 역할의 증거로 복사하거나, 분 감소만으로 선수 불만을 확정하지 않는다.

2021–22 G1A의 정상 가용일 PF 28분, G8C M1의 PF 32분은 **다음 시즌 제안**이다. 그 제안의 역할·기간·보장이 선수에게 매력적일 수 있다는 **추론**은 가능하지만, 2020–21 계약연도에 이미 더 큰 역할을 경험했다는 근거가 되지 않는다. [Yle 직접 인터뷰](https://yle.fi/a/3-12049590)에 나타난 원역사 이적 희망도 대체 세계 의사로 자동 이식하지 않는다.

## 판정과 다음 좁은 입력

1. `M0/G1A`: 기존 잔류 추천을 유지하되 **역할 개선 근거 미입증**을 붙인다. 두 시즌 급여 비교 예산이나 28분 계획은 선수 수락·계약기간이 아니다.
2. `M1`: 32분·4년 $76.16m는 계약연도 불만을 뒤집을 수 있는 **미래 제안 후보**다. 2021–22 실전 5인 조합, 공격 권한, 2023–25 팀 비용, 경쟁 제안과 선수 선택을 추가로 대조해야 한다. `accepted=null`.
3. `M2/M3`: QO와 이탈/사인앤트레이드는 잔류 실패 때의 상호 배타적 분기다. 원역사 Cleveland 거래를 자동 실행하지 않는다.

다음에는 같은 2020–21 선수별 FGA/FTA/터치/선발 역할을 원역사 관측과 대체 **미배정**을 나란히 기록하고, 2021 제안의 공격 권한 및 경쟁팀의 조건을 별도 후보 사건으로 비교한다. 다른 실존 선수의 분·슛을 근거 없이 전용하지 않는다. D1 F1~F5·A1~A3, CP2 잠정 픽, `PROJECT_FREEZE v0.30 PARTIAL`, 설계/원고 `CLOSED`는 유지한다.

## 검증 범위

- Codex: 두 분 예산 CSV, 후반 F6B JSON과 F9 코드의 읽기 경로를 직접 재계산했다. `51 GP / 26 GS`, `79,046−78,328=718초`를 별도 읽기 전용 계산으로 확인했고 전반·후반 Node 원장 검사는 PASS였다. 저장된 F6B/F9 Python 검증은 Windows 체크아웃의 CSV `CRLF`와 저장 당시 `LF` 원문 해시가 달라 **해시 관문에서 중단**됐다. F6B 입력을 `LF`로 정규화한 SHA-256은 저장 해시와 일치했다. 이를 Python 전체 증명 PASS로 쓰지 않는다. 산술·출처 계보의 내부 검증이며 새로운 NBA 사실 출처가 아니다.
- Anti-Gravity/NotebookLM: **이번 원장 재계산에는 새 외부 자료가 없어 `NOT_RUN`**. 이전 G8B의 직접 증거 0건/NotebookLM Cleveland 원문 한정 판독을 새 검증으로 세지 않는다.
- Claude: 문서 단독 반증 CLI를 요청했으나 약 90초 동안 출력 없이 종료해 `ATTEMPTED_NO_RESPONSE`; 반증 완료로 세지 않는다. Source-blind는 `NOT_RUN`. 이 메모는 G16 독립 감리나 G17 작가 승인이 아니다.
