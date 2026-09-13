# O-15G12 자체 검토 — 날짜·가용성·정보 시점

- 기반 main: `29febb3b0bef1f83982190b15927a38a8a8148c8`, PR #178.
- 판정: `HISTORICAL_INPUT_AND_CONDITIONAL_COBY_WITNESS_PASS / NOT_INDEPENDENT`.
- 대상: [입력 검토](../simulation/CHICAGO_2021_22_INPUT_REVIEW.md), [출처](../research/CHICAGO_2021_22_INPUT_SOURCES.json), [검토 JSON](../simulation/CHICAGO_2021_22_INPUT_REVIEW.json).

| 검토 위험 | 결과 |
|---|---|
| 다른 미러 버전/중복 경기 혼입 | 기존 커밋의 세 전체 파일 SHA256 일치. 2021–22 31,321 고유 선수·경기행/1,230경기, 30팀 각82경기 |
| 원일자·변경 보도·개최일 혼동 | DET@CHI 1/10 보도와 공식 경기1/11 차이 기록. 개최 경기ID를 관측 기준으로 사용, 차이의 원인은 미확인 |
| 공식 페이지가 숫자까지 인증했다는 과장 | 네 페이지는 ID·팀·날짜만 대조. 신규 공식 숫자 박스 검증0을 명시 |
| 행 부재·감독 DNP를 부상으로 변환 | 499행 부재·82감독DNP·8명시제한·559출전·82허구를 분리. 대체 가용성/분 전부 HOLD |
| 보고서 발행일을 다음날 경기 상태에 복사 | 11/14 발행, Duarte 대상은11/15로 연결. Wieskamp 투웨이 파견과 건강 사유 구분. Chicago 다음날 미제출도 보존 |
| 초 합계가 맞도록 원문 수치를 덮어씀 | 332경기·396팀 합계의 −2~+5초 잔차 보존. 연장 추정은 실역사 진단 |
| 2021–22 미래 성적을 개막 평가에 사용 | prior는2020–21만 집계. 후속 시즌 득점을 크게 변조해도 prior가 변하지 않는 반례 검사 |
| 주인공/신인에게 가짜 NBA 표본 부여 | 주인공·Duarte·Wieskamp prior null. 정상46분에 별도 성장/환산 입력 필요, 능력0으로 해석하지 않음 |
| Coby 공백을 다른 선수의 무료 시간으로 메움 | Coby−18/Satoransky+10/Valentine+8, 5인 중복0·총240·P32 유지. 전술 성능/날짜별 적용은 미채택 |

## 검증

`test_chicago_2021_22_inputs.py` 신규8개, `test_chicago_2021_22_role_plan.py` 기존6개로 관측·정보시점·부족입력·조합 조건을 검사한다. 저장한 source snapshot/메타 해시와 파생 CSV/JSON byte 재현, 관련 로컬 링크·`git diff --check`를 대조한다. 기존 CP2 설계 샘플은 변경하지 않았고 `build_cp2_design_packets.py --check`로 그대로 유효한지 확인한다.

전체 설계 독립 검수는 미실시이며 위 결과는 같은 작업자의 자체 검토다. 실제 건강·계약·시즌/픽 채택·D1 정확 실행 및 D6 딥리드는 남아 있다. 전체1완료·6진행/남은6개, 원고0·설계/원고CLOSED 유지. 원격 CI는 실제 조회 결과로 별도 보고하며 로컬 검사와 혼합하지 않는다.
