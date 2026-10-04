# Young 2019 서명 자금 경계 검수 — 2026-10-04

기준 main `d310ddb`; 대상 [MD](../research/CHICAGO_2019_YOUNG_SIGNING_BOUNDARY.md) / [JSON](../research/CHICAGO_2019_YOUNG_SIGNING_BOUNDARY.json). 기존 Satoransky 증명 경로의 선행 Young 직접 FA 계약을 조사했다. 정본 선택/법적 통과를 추가하지 않는다.

## 자료와 검증

NBA 공식 이적표와 cap 발표 본문, NBA2017 CBA 조항, Bulls PDF400의 날짜, NBA작성 CBA101 미러 PDF30의 0YOS 최소급여를 대조했다. SalarySwish CHI2019 이력의 CapRoom/보장/보너스 필드를 기본급과 분리했다. 보장액의 사후 표시를 서명순간 보호로 소급하지 않았다. CBA 22쪽·guide1쪽 지문 및 4개 저장소 입력지문은 JSON에 저장한다. 새 출처 재열람을 예전 기본급/AE 증거와 중복 계수하지 않는다.

- 일반 직접 FA는 TPE로 서명하지 못한다. 다른 Prior Team·신규계약·3시즌·첫해 Salary가 $9.258m을 넘는 경우 각 예외를 금액/기간/자격에 따라 배제한다.
- 비Prior Team의 3년 Summer 반례가 있으므로 당시 보호 또는 일반계약 분류 증인을 남겼다.
- roster charge 최대 한 개를 반영한 조건부 차액 $12,001,690. $100k trade 여유 적용0.
- Unlikely Bonus의 첫해 funding Room과 일반 TeamSalary caphit를 분리했다.
- Y1–Y4의 같은 순간 적법 실행 증인과 Y5의 신규TPE 없음 증인이 닫혀야 이전 TPE 대안을 제거한다. 공개 구간 또는 완전 분기로 닫을 수 있고 비공개 원계약을 필수조건으로 추가하지 않는다.

## 실제 도구 실행

| 도구 | 실제 결과 | 채택 범위 |
|---|---|---|
| Antigravity CLI | exit0, elapsed70.139초, 최종SUCCESS 응답 회수 | 지정 SalarySwish 필드 수집. 원문 도구 trace0이므로 CLI 성공을 출처인증으로 보지 않고 총괄 직접 본문과 대조 |
| NotebookLM CLI | exit0, 57.198초, 분석 회수 | 기존 2017 CBA 한 출처의 조건부 분석. 계약/수치의 외부 시험입력은 사실인증 아님 |
| 독립 Codex | 읽기 전용 `/root/independent_finish_scope` 원문·산출물 반증 회수, 결함 미발견 | 국소 논증/MD·JSON만; 전체 법적 게이트 통과 아님 |
| Claude | NOT_RUN | 앞선 실제 SESSION_USAGE_LIMIT 이후 해제 증거 없음; 통과0 |
| 전체 source-blind | NOT_RUN | 전체 설계/원고 검수로 확대하지 않음 |

[AG 회수 기록](CHI_2019_YOUNG_AG_2026_10_04.json), [NLM 회수 기록](CHI_2019_YOUNG_NLM_2026_10_04.json). 같은 출처 모델 재분석의 독립 출처 증가0. CLI와 notebook/source/conversation 식별자는 회수 JSON을 따른다.

NLM의 ‘모든 예외는 $12.9m보다 한도가 작다’는 일반화는 채택하지 않았다. DPE/기간, Bird/Prior Team, 기존계약/신규 여부, 복권/마지막 소속팀 등 서로 다른 제외 이유로 고쳤다. §5b의 Room은 I1kkk와 함께 읽어 넓은 예외 entitlement와 실제 cap gap을 구분했다. ‘cap space 사용은 모든 예외를 영구 제거’ 주장과 현재 보장의 원시점 소급도 채택하지 않았다.

독립 검수는 Summer/Y3·최대1 roster charge·bonus 경계·6m 국소범위·Y5·공개 구간/완전 분기 종료·순환금지의 일치를 확인했다. 최종 수리에서 추가한 것은 guide 지문과 이 검수 결과 표기뿐이다.

## 결과

이번 산출물의 산술·원문 지문·입력 지문·로컬 링크·S2 미완료 상태를 검문한다. 법적12HOLD/F0/5 A0/3 K0/4·R=null·최종회차0·실제Pack0·미완료6·freeze v0.30 PARTIAL·설계/원고CLOSED·원고0. 전체 검증을 대신하는 PASS는 기록하지 않는다.
